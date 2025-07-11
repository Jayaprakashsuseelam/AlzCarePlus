# Generated manually for caretakers app

from django.db import migrations, models
import django.db.models.deletion
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caretaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer-not-to-say', 'Prefer not to say')], max_length=20, null=True)),
                ('professional_title', models.CharField(blank=True, max_length=100, null=True)),
                ('license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('years_of_experience', models.IntegerField(blank=True, null=True)),
                ('specialization', models.CharField(blank=True, max_length=200, null=True)),
                ('employment_status', models.CharField(choices=[('full-time', 'Full Time'), ('part-time', 'Part Time'), ('contract', 'Contract'), ('volunteer', 'Volunteer'), ('private', 'Private Practice')], default='full-time', max_length=20)),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('verification_token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('background_check_verified', models.BooleanField(default=False)),
                ('background_check_date', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CaretakerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='caretaker_profiles/')),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(default='United States', max_length=100)),
                ('bio', models.TextField(blank=True, null=True)),
                ('certifications', models.TextField(blank=True, null=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('languages_spoken', models.CharField(blank=True, max_length=200, null=True)),
                ('availability_schedule', models.JSONField(blank=True, default=dict)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('caretaker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='caretakers.caretaker')),
            ],
        ),
        migrations.CreateModel(
            name='CaretakerPatientAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('assignment_type', models.CharField(choices=[('primary', 'Primary Caretaker'), ('secondary', 'Secondary Caretaker'), ('temporary', 'Temporary Caretaker'), ('specialist', 'Specialist Caretaker')], default='primary', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('caretaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_assignments', to='caretakers.caretaker')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caretaker_assignments', to='patients.patient')),
            ],
            options={
                'ordering': ['-assignment_date'],
                'unique_together': {('caretaker', 'patient', 'is_active')},
            },
        ),
        migrations.CreateModel(
            name='CaretakerSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('schedule_type', models.CharField(choices=[('regular', 'Regular Shift'), ('overtime', 'Overtime'), ('on-call', 'On Call'), ('emergency', 'Emergency'), ('vacation', 'Vacation'), ('sick', 'Sick Leave')], default='regular', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('caretaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='caretakers.caretaker')),
            ],
            options={
                'ordering': ['date', 'start_time'],
                'unique_together': {('caretaker', 'date', 'start_time')},
            },
        ),
        migrations.CreateModel(
            name='CaretakerTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('task_type', models.CharField(choices=[('medication', 'Medication'), ('hygiene', 'Hygiene'), ('feeding', 'Feeding'), ('exercise', 'Exercise'), ('monitoring', 'Monitoring'), ('appointment', 'Appointment'), ('emergency', 'Emergency'), ('other', 'Other')], default='other', max_length=20)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium', max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('scheduled_date', models.DateField()),
                ('scheduled_time', models.TimeField(blank=True, null=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('caretaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='caretakers.caretaker')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caretaker_tasks', to='patients.patient')),
            ],
            options={
                'ordering': ['-scheduled_date', '-scheduled_time'],
            },
        ),
    ] 