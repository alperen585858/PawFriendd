from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Pet
import os
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Adds sample photos to pets'

    def handle(self, *args, **kwargs):
        # Dictionary mapping species to photo URLs
        photo_urls = {
            'dog': [
                'https://images.unsplash.com/photo-1543466835-00a7907e9de1',
                'https://images.unsplash.com/photo-1587300003388-59208cc962cb',
                'https://images.unsplash.com/photo-1517849845537-4d257902454a',
            ],
            'cat': [
                'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba',
                'https://images.unsplash.com/photo-1573865526739-10659fec78a5',
                'https://images.unsplash.com/photo-1495360010541-f48722b34f7d',
            ],
            'bird': [
                'https://images.unsplash.com/photo-1552728089-57bdde30beb3',
                'https://images.unsplash.com/photo-1544923408-75c5cef46f14',
                'https://images.unsplash.com/photo-1522858547137-f1dcec554f55',
            ],
            'other': [
                'https://images.unsplash.com/photo-1425082661705-1834bfd09dca',
                'https://images.unsplash.com/photo-1559253664-ca249d4608c6',
                'https://images.unsplash.com/photo-1583301286816-f4f05e1e8b25',
            ],
        }

        # Get all pets without photos
        pets = Pet.objects.all()
        
        for pet in pets:
            if not pet.photo:
                # Get random photo URL for the pet's species
                import random
                urls = photo_urls.get(pet.species, photo_urls['other'])
                photo_url = random.choice(urls)
                
                try:
                    # Download the image
                    response = requests.get(f"{photo_url}?w=800&q=80")
                    if response.status_code == 200:
                        # Create a file-like object from the image data
                        image_io = BytesIO(response.content)
                        
                        # Generate a filename
                        filename = f"{pet.species}_{pet.name.lower().replace(' ', '_')}.jpg"
                        
                        # Save the image to the pet
                        pet.photo.save(filename, File(image_io), save=True)
                        
                        self.stdout.write(self.style.SUCCESS(f'Successfully added photo for {pet.name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Failed to download photo for {pet.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding photo for {pet.name}: {str(e)}'))
            else:
                self.stdout.write(self.style.NOTICE(f'{pet.name} already has a photo')) 