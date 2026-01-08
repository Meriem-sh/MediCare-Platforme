from django.core.management.base import BaseCommand
from faker import Faker
from users.models import CustomUser
from drugs.models import Drug, Disease
from prescriptions.models import Prescription
from datetime import date, timedelta
from reminders.models import Reminder
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Generate fake data for MediCare platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--doctors',
            type=int,
            default=5,
            help='Number of doctors to create'
        )
        parser.add_argument(
            '--patients',
            type=int,
            default=10,
            help='Number of patients to create'
        )
        parser.add_argument(
            '--prescriptions',
            type=int,
            default=20,
            help='Number of prescriptions to create'
        )

    def handle(self, *args, **options):
        fake = Faker()
        
        num_doctors = options['doctors']
        num_patients = options['patients']
        num_prescriptions = options['prescriptions']

        self.stdout.write(self.style.SUCCESS('Starting data generation...'))

        # 1. Create Diseases
        self.stdout.write('Creating diseases...')
        diseases = []
        disease_data = [
            {'name': 'Diabetes', 'description': 'Chronic disease affecting blood sugar levels'},
            {'name': 'Hypertension', 'description': 'High blood pressure condition'},
            {'name': 'Asthma', 'description': 'Respiratory condition causing breathing difficulties'},
            {'name': 'Arthritis', 'description': 'Joint inflammation and pain'},
            {'name': 'Heart Disease', 'description': 'Various conditions affecting the heart'},
            {'name': 'Chronic Kidney Disease', 'description': 'Progressive loss of kidney function'},
        ]
        
        for disease_info in disease_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_info['name'],
                defaults={'description': disease_info['description']}
            )
            diseases.append(disease)
            if created:
                self.stdout.write(f'  ✓ Disease created: {disease.name}')

        # 2. Create Doctors
        self.stdout.write(f'\nCreating {num_doctors} doctors...')
        doctors = []
        specialties = ['generalist', 'oncologist', 'cardiologist', 'pediatrician', 
              'neurologist', 'endocrinologist', 'pulmonologist', 'other']

        for i in range(num_doctors):
            username = f'doctor{i+1}'
            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(f'  ⊘ Doctor already exists: {username}')
                doctors.append(CustomUser.objects.get(username=username))
                continue
                
            doctor = CustomUser.objects.create_user(
                username=username,
                email=fake.email(),
                password='doctor123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='doctor',
                phone=fake.phone_number()[:20],
                specialty=random.choice(specialties)
            )
            doctors.append(doctor)
            self.stdout.write(f'  ✓ Doctor created: {doctor.username} ({doctor.specialty})')

        # 3. Create Patients
        self.stdout.write(f'\nCreating {num_patients} patients...')
        patients = []
        
        for i in range(num_patients):
            username = f'patient{i+1}'
            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(f'  ⊘ Patient already exists: {username}')
                patients.append(CustomUser.objects.get(username=username))
                continue
                
            patient = CustomUser.objects.create_user(
                username=username,
                email=fake.email(),
                password='patient123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='patient',
                phone=fake.phone_number()[:20],
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                assigned_doctor=random.choice(doctors),
                disease=random.choice(diseases)
            )
            patients.append(patient)
            self.stdout.write(f'  ✓ Patient created: {patient.username} - Disease: {patient.disease.name}')

        # 4. Create Drugs
        self.stdout.write('\nCreating drugs...')
        drugs = []
        drug_data = [
            {'name': 'Aspirin', 'strength': '100mg', 'condition': 'Pain', 'dosage_form': 'Tablet'},
            {'name': 'Paracetamol', 'strength': '500mg', 'condition': 'Pain/Fever', 'dosage_form': 'Tablet'},
            {'name': 'Ibuprofen', 'strength': '200mg', 'condition': 'Pain/Inflammation', 'dosage_form': 'Tablet'},
            {'name': 'Amoxicillin', 'strength': '250mg', 'condition': 'Bacterial Infection', 'dosage_form': 'Capsule'},
            {'name': 'Metformin', 'strength': '500mg', 'condition': 'Diabetes', 'dosage_form': 'Tablet'},
            {'name': 'Lisinopril', 'strength': '10mg', 'condition': 'Hypertension', 'dosage_form': 'Tablet'},
            {'name': 'Omeprazole', 'strength': '20mg', 'condition': 'Acid Reflux', 'dosage_form': 'Capsule'},
            {'name': 'Simvastatin', 'strength': '40mg', 'condition': 'High Cholesterol', 'dosage_form': 'Tablet'},
            {'name': 'Losartan', 'strength': '50mg', 'condition': 'Hypertension', 'dosage_form': 'Tablet'},
            {'name': 'Levothyroxine', 'strength': '50mcg', 'condition': 'Thyroid', 'dosage_form': 'Tablet'},
        ]

        for drug_info in drug_data:
            drug, created = Drug.objects.get_or_create(
                name=drug_info['name'],
                defaults={
                    'description': f"{drug_info['name']} for {drug_info['condition']}",
                    'strength': drug_info['strength'],
                    'dosage_form': drug_info['dosage_form'],
                    'condition': drug_info['condition'],
                    'is_active': True
                }
            )
            drugs.append(drug)
            if created:
                self.stdout.write(f'  ✓ Drug created: {drug.name} ({drug.strength})')

        # 5. Create Prescriptions
        self.stdout.write(f'\nCreating {num_prescriptions} prescriptions...')
        frequencies = ['Once daily', 'Twice daily', 'Three times daily', 'Every 8 hours', 'As needed']

        for i in range(num_prescriptions):
            start_date = date.today() - timedelta(days=random.randint(0, 30))
            end_date = start_date + timedelta(days=random.randint(7, 30))
            
            prescription = Prescription.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                drug=random.choice(drugs),
                dosage=f'{random.randint(1, 3)} tablet(s)',
                frequency=random.choice(frequencies),
                start_date=start_date,
                end_date=end_date,
                notes=fake.text(max_nb_chars=100)
            )

            self.stdout.write(f'  ✓ Prescription #{i+1}: {prescription.drug.name} for {prescription.patient.username}')

        # 6. Create Reminders
        self.stdout.write('\nCreating reminders...')
        reminder_count = 0

        # Get prescriptions to create reminders for them
        all_prescriptions = list(Prescription.objects.all())

        if all_prescriptions:
            # Create 2-3 reminders per prescription (for different times of day)
            from datetime import time as dt_time
            times_of_day = [
                dt_time(8, 0),   # 8:00 AM
                dt_time(14, 0),  # 2:00 PM
                dt_time(20, 0),  # 8:00 PM
            ]
            
            for prescription in all_prescriptions[:10]:  # First 10 prescriptions
                num_reminders = random.randint(1, 2)  # 1-2 reminders per prescription
                for _ in range(num_reminders):
                    reminder = Reminder.objects.create(
                        prescription=prescription,
                        patient=prescription.patient,
                        time=random.choice(times_of_day),
                        is_active=True
                    )
                    reminder_count += 1
                    self.stdout.write(f'  ✓ Reminder created for {prescription.patient.username} at {reminder.time}')
        else:
            self.stdout.write('  ⊘ No prescriptions available to create reminders')

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Data generation completed successfully!'))
        self.stdout.write('='*60)
        self.stdout.write(f'Total Diseases: {Disease.objects.count()}')
        self.stdout.write(f'Total Doctors: {CustomUser.objects.filter(role="doctor").count()}')
        self.stdout.write(f'Total Patients: {CustomUser.objects.filter(role="patient").count()}')
        self.stdout.write(f'Total Drugs: {Drug.objects.count()}')
        self.stdout.write(f'Total Prescriptions: {Prescription.objects.count()}')
        self.stdout.write(f'Total Reminders: {Reminder.objects.count()}')
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.WARNING('Login credentials:'))
        self.stdout.write('  Doctors: username=doctor1-{}, password=doctor123'.format(num_doctors))
        self.stdout.write('  Patients: username=patient1-{}, password=patient123'.format(num_patients))
        self.stdout.write('='*60)
