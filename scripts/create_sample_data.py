"""
Script para crear datos de ejemplo en la base de datos.
Ejecutar así (con el venv activado):

python scripts/create_sample_data.py

"""
import os
import sys
from pathlib import Path
import django

# Asegurar que la carpeta raíz del proyecto está en sys.path para poder importar settings
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_example.settings')
django.setup()

from vehiclesapp.models import Vehicle

sample = [
    {'placa':'ABC123','marca':'Toyota','modelo':2020,'color':'1'},
    {'placa':'DEF456','marca':'Honda','modelo':2018,'color':'2'},
    {'placa':'GHI789','marca':'Ford','modelo':2015,'color':'3'},
]

for s in sample:
    obj, created = Vehicle.objects.get_or_create(placa=s['placa'], defaults={
        'marca': s['marca'],
        'modelo': s['modelo'],
        'color': s['color'],
    })
    if created:
        print(f"Creado: {obj}")
    else:
        print(f"Ya existe: {obj}")

print('Datos de ejemplo procesados.')
