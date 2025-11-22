from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro_voluntario, name='registro'),
    path('actividades/', views.actividades_disponibles, name='actividades'),
    path('inscribir/<int:actividad_id>/', views.inscribir, name='inscribir'),
    path('coordinador/', views.coord_panel, name='coord_panel'),
    path('coordinador/actividad/nueva/', views.nueva_actividad, name='nueva_actividad'),
    path('coordinador/actividad/editar/<int:pk>/', views.editar_actividad, name='editar_actividad'),
    path('coordinador/actividad/eliminar/<int:pk>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('coordinador/asistencia/<int:actividad_id>/', views.registrar_asistencia, name='registrar_asistencia'),
    path('coordinador/certificados/', views.certificados_panel, name='certificados_panel'),
    path('coordinador/certificado/generar/', views.generar_certificados, name='generar_certificados'),
    path('certificado/<int:cert_id>/', views.ver_certificado, name='ver_certificado'),
    path('certificados/', views.mis_certificados, name='mis_certificados'),
    path('certificados/public/', views.lista_certificados, name='lista_certificados'),
]
