from django.core.management.base import BaseCommand
from core.models import Pet

class Command(BaseCommand):
    help = 'Adds sample pets to the database'

    def handle(self, *args, **kwargs):
        # Sample pets data
        pets_data = [
            {
                'name': 'Luna',
                'species': 'dog',
                'breed': 'Golden Retriever',
                'age': 2,
                'gender': 'female',
                'description': 'Luna is a friendly and energetic Golden Retriever who loves to play fetch and go for long walks.',
                'health_status': 'Excellent health, up to date on all vaccinations',
                'is_vaccinated': True,
                'is_neutered': True,
                'status': 'available'
            },
            {
                'name': 'Max',
                'species': 'dog',
                'breed': 'German Shepherd',
                'age': 3,
                'gender': 'male',
                'description': 'Max is a loyal and intelligent German Shepherd. He is great with kids and makes an excellent guard dog.',
                'health_status': 'Good health, regular check-ups',
                'is_vaccinated': True,
                'is_neutered': True,
                'status': 'available'
            },
            {
                'name': 'Bella',
                'species': 'cat',
                'breed': 'Siamese',
                'age': 1,
                'gender': 'female',
                'description': 'Bella is a playful Siamese cat who loves attention and cuddles.',
                'health_status': 'Excellent health, recently checked by vet',
                'is_vaccinated': True,
                'is_neutered': True,
                'status': 'available'
            },
            {
                'name': 'Charlie',
                'species': 'cat',
                'breed': 'Persian',
                'age': 4,
                'gender': 'male',
                'description': 'Charlie is a calm and gentle Persian cat who enjoys lounging in sunny spots.',
                'health_status': 'Good health, regular grooming required',
                'is_vaccinated': True,
                'is_neutered': True,
                'status': 'available'
            },
            {
                'name': 'Rocky',
                'species': 'dog',
                'breed': 'Bulldog',
                'age': 2,
                'gender': 'male',
                'description': 'Rocky is a friendly bulldog who loves to play and snuggle.',
                'health_status': 'Good health, regular exercise needed',
                'is_vaccinated': True,
                'is_neutered': False,
                'status': 'available'
            }
        ]

        # Create pets
        for pet_data in pets_data:
            Pet.objects.create(**pet_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully added pet "{pet_data["name"]}"')) 