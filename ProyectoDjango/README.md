# Plataforma Voluntariado

Proyecto Django minimal para gestión de voluntariado con registro, actividades, inscripciones, asistencia y generación de certificados.

Estructura principal:

```
proyecto django/
├── manage.py
├── voluntariado/
├── app/
├── templates/
└── static/
```

Instalación y ejecución (Windows PowerShell):

1. Crear y activar entorno virtual (opcional pero recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Migraciones y superusuario:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Ejecutar servidor:

```powershell
python manage.py runserver
```

Accede a `http://127.0.0.1:8000/` para ver la aplicación. El panel de administración está en `/admin/`.

## Generar certificados en PDF (opcional)

Si quieres que la aplicación genere un PDF del certificado (archivo descargable), instala `WeasyPrint` en el entorno:

```powershell
pip install weasyprint
```

Luego, desde la vista de certificado (por ejemplo `http://127.0.0.1:8000/certificado/1/`) puedes añadir `?pdf=1` al final de la URL para descargar el PDF:

```
http://127.0.0.1:8000/certificado/1/?pdf=1
```

Si `WeasyPrint` no está instalado, la aplicación mostrará el certificado como HTML y un aviso.
