from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from drugs.models import Drug, Disease
from prescriptions.models import Prescription
from reminders.models import Reminder
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Starting data generation...')

        # Create Diseases first
        self.stdout.write('Creating diseases...')
        diseases = []
        disease_data = [
            {'name': 'Diabetes', 'is_rare': False, 'recommended_specialty': 'endocrinologist'},
            {'name': 'Hypertension', 'is_rare': False, 'recommended_specialty': 'cardiologist'},
            {'name': 'Asthma', 'is_rare': False, 'recommended_specialty': 'pulmonologist'},
            {'name': 'Arthritis', 'is_rare': False, 'recommended_specialty': 'other'},
            {'name': 'Heart Disease', 'is_rare': False, 'recommended_specialty': 'cardiologist'},
            {'name': 'Chronic Kidney Disease', 'is_rare': True, 'recommended_specialty': 'other'},
        ]
        
        for disease_info in disease_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_info['name'],
                defaults={
                    'is_rare': disease_info['is_rare'],
                    'recommended_specialty': disease_info['recommended_specialty'],
                    'description': f'Medical condition: {disease_info["name"]}'
                }
            )
            diseases.append(disease)
            if created:
                self.stdout.write(f'  ✓ Disease created: {disease.name}')

        # Create Doctors
        self.stdout.write('Creating 5 doctors...')
        doctors = []
        specialties = ['generalist', 'oncologist', 'cardiologist', 'pediatrician', 
                      'endocrinologist', 'pulmonologist', 'other']
        
        for i in range(5):
            username = f'doctor{i+1}'
            
            
            if not User.objects.filter(username=username).exists():
                doctor = User.objects.create_user(
                    username=username,
                    email=f'doctor{i+1}@medicare.com',
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    role='doctor',
                    phone=fake.phone_number()[:20],
                    specialty=random.choice(specialties)
                )
                doctors.append(doctor)
                self.stdout.write(f'  ✓ Doctor created: {doctor.username} ({doctor.specialty})')
            else:
                doctor = User.objects.get(username=username)
                doctors.append(doctor)
                self.stdout.write(f'  ℹ️  Doctor already exists: {doctor.username}')

        # Create Patients
        self.stdout.write('Creating 10 patients...')
        patients = []
        
        for i in range(10):
            username = f'patient{i+1}'
            
            
            if not User.objects.filter(username=username).exists():
                
                disease = random.choice(diseases)
                
                patient = User.objects.create_user(
                    username=username,
                    email=f'patient{i+1}@medicare.com',
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    role='patient',
                    phone=fake.phone_number()[:20],
                    condition=disease.name,
                    disease=disease,
                    assigned_doctor=random.choice(doctors)
                )
                patients.append(patient)
                self.stdout.write(f'  ✓ Patient created: {patient.username} - {patient.condition}')
            else:
                patient = User.objects.get(username=username)
                patients.append(patient)
                self.stdout.write(f'  ℹ️  Patient already exists: {patient.username}')

        # Create Drugs
        self.stdout.write('Creating 10 drugs...')
        drugs = []
        drug_data = [
            {'name': 'Metformin', 'condition': 'Diabetes', 'dosage_form': 'Tablet', 'strength': '500 mg'},
            {'name': 'Lisinopril', 'condition': 'Hypertension', 'dosage_form': 'Tablet', 'strength': '10 mg'},
            {'name': 'Albuterol', 'condition': 'Asthma', 'dosage_form': 'Inhaler', 'strength': '90 mcg'},
            {'name': 'Ibuprofen', 'condition': 'Arthritis', 'dosage_form': 'Tablet', 'strength': '200 mg'},
            {'name': 'Aspirin', 'condition': 'Heart Disease', 'dosage_form': 'Tablet', 'strength': '75 mg'},
            {'name': 'Amoxicillin', 'condition': 'Infection', 'dosage_form': 'Capsule', 'strength': '250 mg'},
            {'name': 'Omeprazole', 'condition': 'Acid Reflux', 'dosage_form': 'Capsule', 'strength': '20 mg'},
            {'name': 'Atorvastatin', 'condition': 'High Cholesterol', 'dosage_form': 'Tablet', 'strength': '10 mg'},
            {'name': 'Paracetamol', 'condition': 'Pain', 'dosage_form': 'Tablet', 'strength': '500 mg'},
            {'name': 'Salbutamol', 'condition': 'Asthma', 'dosage_form': 'Inhaler', 'strength': '100 mcg'},
        ]

        for drug_info in drug_data:
            drug, created = Drug.objects.get_or_create(
                name=drug_info['name'],
                defaults={
                    'description': f'Medication for {drug_info["condition"]}',
                    'condition': drug_info['condition'],
                    'dosage_form': drug_info['dosage_form'],
                    'strength': drug_info['strength'],
                    'is_active': True
                }
            )
            drugs.append(drug)
            if created:
                self.stdout.write(f'  ✓ Drug created: {drug.name} ({drug.strength})')

        # Create Prescriptions
        self.stdout.write('Creating 15 prescriptions...')
        prescriptions = []
        dosages = ['1 tablet', '2 tablets', '1 capsule', '2 puffs']
        frequencies = ['Once daily', 'Twice daily', '3 times daily', 'As needed']
        
        for i in range(15):
            prescription = Prescription.objects.create(
                doctor=random.choice(doctors),
                patient=random.choice(patients),
                drug=random.choice(drugs),
                dosage=random.choice(dosages),
                frequency=random.choice(frequencies),
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=random.randint(7, 90)),
                notes=fake.sentence()
            )
            prescriptions.append(prescription)
            self.stdout.write(f'  ✓ Prescription {i+1} created')

        # Create Reminders
        self.stdout.write('Creating 20 reminders...')
        reminder_times = ['08:00:00', '12:00:00', '18:00:00', '22:00:00']
        
        for i in range(20):
            prescription = random.choice(prescriptions)
            
            Reminder.objects.create(
                prescription=prescription,
                patient=prescription.patient,
                time=random.choice(reminder_times),
                is_active=True
            )
            self.stdout.write(f'  ✓ Reminder {i+1} created')

        self.stdout.write(self.style.SUCCESS('\n✅ Fake data generated successfully!'))
        self.stdout.write(f'  - {len(diseases)} Diseases')
        self.stdout.write(f'  - {len(doctors)} Doctors')
        self.stdout.write(f'  - {len(patients)} Patients')
        self.stdout.write(f'  - {len(drugs)} Drugs')
        self.stdout.write(f'  - {len(prescriptions)} Prescriptions')
        self.stdout.write(f'  - 20 Reminders')
