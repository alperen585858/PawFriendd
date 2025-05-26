import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Pet
from django.core.files.base import ContentFile
from io import BytesIO
import random

# Replicate API ayarları
REPLICATE_API_TOKEN = getattr(settings, 'REPLICATE_API_TOKEN', None)
REPLICATE_MODEL = "stability-ai/sdxl"
REPLICATE_VERSION = "7762fd07"  # SDXL modelinin güncel ve erişilebilir version ID'si
REPLICATE_URL = f"https://api.replicate.com/v1/predictions"

# Hayvan türleri ve örnekler
SAMPLE_PETS = [
    {"name": "Oscar", "species": "dog", "breed": "Pug", "age": 2, "gender": "male"},
    {"name": "Mia", "species": "cat", "breed": "Bengal", "age": 1, "gender": "female"},
    {"name": "Sunny", "species": "bird", "breed": "Canary", "age": 1, "gender": "female"},
    {"name": "Bunny", "species": "other", "breed": "Rabbit", "age": 1, "gender": "male"},
    {"name": "Simba", "species": "dog", "breed": "Labrador", "age": 3, "gender": "male"},
    {"name": "Lily", "species": "cat", "breed": "Ragdoll", "age": 2, "gender": "female"},
    # Yeni eklenenler
    {"name": "Pepper", "species": "dog", "breed": "Cocker Spaniel", "age": 4, "gender": "female"},
    {"name": "Shadow", "species": "cat", "breed": "Sphynx", "age": 3, "gender": "male"},
    {"name": "Kiwi", "species": "bird", "breed": "Budgerigar", "age": 2, "gender": "male"},
    {"name": "Nibbles", "species": "other", "breed": "Guinea Pig", "age": 1, "gender": "female"},
    {"name": "Daisy", "species": "dog", "breed": "Shih Tzu", "age": 5, "gender": "female"},
]

def generate_prompt(pet):
    return f"A high quality photo of a {pet['age']}-year-old {pet['breed']} {pet['species']} ({pet['gender']}) in natural light, looking cute."

def generate_image(prompt):
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "version": REPLICATE_VERSION,
        "input": {"prompt": prompt}
    }
    response = requests.post(REPLICATE_URL, json=data, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Replicate API error: {response.text}")
    prediction = response.json()
    # Prediction is async, poll until completed
    prediction_url = prediction["urls"]["get"]
    while True:
        poll = requests.get(prediction_url, headers=headers)
        poll_json = poll.json()
        if poll_json["status"] == "succeeded":
            return poll_json["output"][0]
        elif poll_json["status"] == "failed":
            raise Exception(f"Image generation failed: {poll_json}")
        import time; time.sleep(2)

def download_image(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return ContentFile(resp.content)

class Command(BaseCommand):
    help = 'Tüm hayvanlara otomatik fotoğraf ekler ve yeni hayvanlar oluşturur.'

    def handle(self, *args, **options):
        if not REPLICATE_API_TOKEN:
            self.stdout.write(self.style.ERROR('REPLICATE_API_TOKEN ayarlanmalı!'))
            return

        # 1. Mevcut hayvanlara fotoğraf ekle
        pets = Pet.objects.all()
        for pet in pets:
            if not pet.photo:
                prompt = generate_prompt({
                    "age": pet.age,
                    "breed": pet.breed,
                    "species": pet.species,
                    "gender": pet.gender
                })
                self.stdout.write(f"{pet.name} için fotoğraf üretiliyor...")
                try:
                    image_url = generate_image(prompt)
                    image_file = download_image(image_url)
                    filename = f"{pet.name.lower()}_{pet.id}.jpg"
                    pet.photo.save(filename, image_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f"{pet.name} için fotoğraf kaydedildi."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"{pet.name} için hata: {e}"))

        # 2. Yeni hayvanlar ekle
        for pet_data in SAMPLE_PETS:
            # Her seferinde benzersiz isim oluştur
            unique_name = f"{pet_data['name']}_{random.randint(1000, 9999)}"
            prompt = generate_prompt({**pet_data, "name": unique_name})
            self.stdout.write(f"Yeni hayvan {unique_name} için fotoğraf üretiliyor...")
            try:
                image_url = generate_image(prompt)
                image_file = download_image(image_url)
                pet = Pet.objects.create(
                    name=unique_name,
                    species=pet_data["species"],
                    breed=pet_data["breed"],
                    age=pet_data["age"],
                    gender=pet_data["gender"],
                    description=f"{unique_name} is a lovely {pet_data['breed']} {pet_data['species']}.",
                    health_status="Healthy",
                    is_vaccinated=random.choice([True, False]),
                    is_neutered=random.choice([True, False]),
                    status="available"
                )
                filename = f"{unique_name.lower()}_{pet.id}.jpg"
                pet.photo.save(filename, image_file, save=True)
                self.stdout.write(self.style.SUCCESS(f"Yeni hayvan {unique_name} eklendi ve fotoğrafı kaydedildi."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Yeni hayvan {unique_name} için hata: {e}"))

        self.stdout.write(self.style.SUCCESS('Tüm hayvanlarda fotoğraf mevcut ve yeni hayvanlar eklendi!'))

        # Tüm hayvanların status'unu 'available' yap
        Pet.objects.all().update(status='available')
        self.stdout.write(self.style.SUCCESS('Tüm hayvanların status alanı available olarak güncellendi!'))

        # Veritabanındaki hayvan sayısını ve mevcut olanların sayısını kontrol et
        self.stdout.write(f"Tüm hayvanların sayısı: {Pet.objects.all().count()}")
        self.stdout.write(f"Mevcut hayvanların sayısı: {Pet.objects.filter(status='available').count()}")
        self.stdout.write("Son eklenen 10 hayvanın bilgileri:")
        for pet in Pet.objects.order_by('-id').values('name', 'status')[:10]:
            self.stdout.write(f"{pet['name']} - {pet['status']}")

        # Yeni eklenen hayvanların status'unu kontrol et
        self.stdout.write("Yeni eklenen hayvanların statusları:")
        for pet in Pet.objects.filter(name__in=["Pepper", "Shadow", "Kiwi", "Nibbles", "Daisy"]).values("name", "status"):
            self.stdout.write(f"{pet['name']} - {pet['status']}")

        # Yeni eklenen hayvanların status'unu kontrol et
        self.stdout.write("Yeni eklenen hayvanların statusları:")
        for pet in Pet.objects.filter(name__in=["Pepper", "Shadow", "Kiwi", "Nibbles", "Daisy"]).values("name", "status"):
            self.stdout.write(f"{pet['name']} - {pet['status']}") 