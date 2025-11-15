Proyecto CRUD básico en Django - Vehículos

Archivos creados:

- `manage.py`
- `crud_example/` (settings, urls, wsgi)
- `vehiclesapp/` (models, forms, views, urls, templates)

Instrucciones rápidas (PowerShell):

1. Crear y activar entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Crear migraciones y migrar:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Ejecutar servidor:

```powershell
python manage.py runserver
```

Puntos finales:

- Lista: http://127.0.0.1:8000/
- Crear: http://127.0.0.1:8000/create/
- Editar: http://127.0.0.1:8000/update/<id>/
- Borrar: http://127.0.0.1:8000/delete/<id>/

Si quieres, puedo crear un `superuser` y añadir instrucciones para deploy.
