# Generated manually for clinics app

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
        ('caretakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
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
                ('clinic_name', models.CharField(max_length=200)),
                ('clinic_type', models.CharField(choices=[('general', 'General Practice'), ('specialist', 'Specialist Clinic'), ('geriatric', 'Geriatric Care'), ('neurology', 'Neurology'), ('cardiology', 'Cardiology'), ('oncology', 'Oncology'), ('rehabilitation', 'Rehabilitation'), ('mental_health', 'Mental Health'), ('dental', 'Dental'), ('other', 'Other')], default='general', max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('country', models.CharField(default='United States', max_length=100)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('tax_id', models.CharField(blank=True, max_length=50, null=True)),
                ('npi_number', models.CharField(blank=True, max_length=20, null=True)),
                ('operating_hours', models.JSONField(default=dict)),
                ('is_verified', models.BooleanField(default=False)),
                ('verification_date', models.DateTimeField(blank=True, null=True)),
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
            name='ClinicProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='clinic_logos/')),
                ('banner_image', models.ImageField(blank=True, null=True, upload_to='clinic_banners/')),
                ('description', models.TextField(blank=True, null=True)),
                ('specialties', models.TextField(blank=True, null=True)),
                ('services_offered', models.JSONField(default=list)),
                ('insurance_accepted', models.JSONField(default=list)),
                ('facility_type', models.CharField(choices=[('outpatient', 'Outpatient Clinic'), ('inpatient', 'Inpatient Facility'), ('ambulatory', 'Ambulatory Care'), ('urgent_care', 'Urgent Care'), ('specialty_center', 'Specialty Center'), ('rehabilitation_center', 'Rehabilitation Center'), ('diagnostic_center', 'Diagnostic Center')], default='outpatient', max_length=50)),
                ('total_beds', models.IntegerField(default=0)),
                ('total_rooms', models.IntegerField(default=0)),
                ('parking_spaces', models.IntegerField(default=0)),
                ('wheelchair_accessible', models.BooleanField(default=True)),
                ('accreditations', models.JSONField(default=list)),
                ('certifications', models.JSONField(default=list)),
                ('emergency_contact', models.CharField(blank=True, max_length=20, null=True)),
                ('after_hours_contact', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='clinics.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='ClinicStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_type', models.CharField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse'), ('receptionist', 'Receptionist'), ('administrator', 'Administrator'), ('technician', 'Technician'), ('therapist', 'Therapist'), ('pharmacist', 'Pharmacist'), ('other', 'Other')], max_length=50)),
                ('employee_id', models.CharField(max_length=50, unique=True)),
                ('hire_date', models.DateField()),
                ('termination_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('specialization', models.CharField(blank=True, max_length=200, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('work_schedule', models.JSONField(default=dict)),
                ('can_view_patients', models.BooleanField(default=False)),
                ('can_edit_patients', models.BooleanField(default=False)),
                ('can_view_records', models.BooleanField(default=False)),
                ('can_edit_records', models.BooleanField(default=False)),
                ('can_manage_appointments', models.BooleanField(default=False)),
                ('can_manage_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='clinics.clinic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinic_employments', to='auth.user')),
            ],
            options={
                'ordering': ['-hire_date'],
                'unique_together': {('clinic', 'user', 'is_active')},
            },
        ),
        migrations.CreateModel(
            name='ClinicPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('patient_number', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('insurance_provider', models.CharField(blank=True, max_length=100, null=True)),
                ('insurance_number', models.CharField(blank=True, max_length=50, null=True)),
                ('insurance_group', models.CharField(blank=True, max_length=50, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_contact_relationship', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_care_physician', models.CharField(blank=True, max_length=100, null=True)),
                ('referring_physician', models.CharField(blank=True, max_length=100, null=True)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('current_medications', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='clinics.clinic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinics', to='patients.patient')),
            ],
            options={
                'ordering': ['-registration_date'],
                'unique_together': {('clinic', 'patient', 'is_active')},
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_number', models.CharField(max_length=50, unique=True)),
                ('appointment_type', models.CharField(choices=[('consultation', 'Consultation'), ('follow_up', 'Follow-up'), ('emergency', 'Emergency'), ('routine_checkup', 'Routine Checkup'), ('procedure', 'Procedure'), ('therapy', 'Therapy'), ('diagnostic', 'Diagnostic Test'), ('vaccination', 'Vaccination'), ('other', 'Other')], max_length=50)),
                ('scheduled_date', models.DateField()),
                ('scheduled_time', models.TimeField()),
                ('duration', models.IntegerField(default=30)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('no_show', 'No Show'), ('rescheduled', 'Rescheduled')], default='scheduled', max_length=20)),
                ('room_number', models.CharField(blank=True, max_length=20, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('treatment_plan', models.TextField(blank=True, null=True)),
                ('check_in_time', models.DateTimeField(blank=True, null=True)),
                ('check_out_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinics.clinic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinics.clinicpatient')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinics.clinicstaff')),
            ],
            options={
                'ordering': ['-scheduled_date', '-scheduled_time'],
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(choices=[('vital_signs', 'Vital Signs'), ('physical_exam', 'Physical Examination'), ('lab_results', 'Laboratory Results'), ('imaging', 'Imaging Results'), ('medication', 'Medication Record'), ('procedure', 'Procedure Record'), ('progress_note', 'Progress Note'), ('discharge_summary', 'Discharge Summary'), ('allergy_record', 'Allergy Record'), ('immunization', 'Immunization Record'), ('other', 'Other')], max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('findings', models.TextField(blank=True, null=True)),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('treatment', models.TextField(blank=True, null=True)),
                ('prescriptions', models.JSONField(default=list)),
                ('blood_pressure', models.CharField(blank=True, max_length=20, null=True)),
                ('heart_rate', models.IntegerField(blank=True, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('oxygen_saturation', models.IntegerField(blank=True, null=True)),
                ('attachments', models.JSONField(default=list)),
                ('is_private', models.BooleanField(default=False)),
                ('access_level', models.CharField(choices=[('public', 'Public'), ('staff', 'Staff Only'), ('doctor', 'Doctors Only'), ('private', 'Private')], default='staff', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='clinics.appointment')),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='clinics.clinic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='clinics.clinicpatient')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='clinics.clinicstaff')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ClinicSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('schedule_type', models.CharField(choices=[('regular', 'Regular Hours'), ('overtime', 'Overtime'), ('on_call', 'On Call'), ('emergency', 'Emergency'), ('vacation', 'Vacation'), ('sick', 'Sick Leave'), ('holiday', 'Holiday'), ('training', 'Training'), ('meeting', 'Meeting')], default='regular', max_length=20)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('room_number', models.CharField(blank=True, max_length=20, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='clinics.clinic')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinic_schedules', to='clinics.clinicstaff')),
            ],
            options={
                'ordering': ['date', 'start_time'],
                'unique_together': {('clinic', 'staff', 'date', 'start_time')},
            },
        ),
    ] 