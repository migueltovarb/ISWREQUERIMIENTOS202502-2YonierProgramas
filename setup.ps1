# setup.ps1 - Automatiza creación de venv, instalación, migraciones y arranque
# Ejecuta desde PowerShell en la carpeta del proyecto (donde está manage.py)

Write-Host "Creando entorno virtual..."
python -m venv venv

Write-Host "Activando entorno virtual..."
.\venv\Scripts\Activate

Write-Host "Instalando dependencias..."
pip install -r requirements.txt

Write-Host "Creando y aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

Write-Host "(Opcional) Crear superusuario interactivo ahora..."
python manage.py createsuperuser

Write-Host "Arrancando servidor de desarrollo..."
python manage.py runserver
