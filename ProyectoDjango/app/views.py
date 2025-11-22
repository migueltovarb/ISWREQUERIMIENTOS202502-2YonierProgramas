from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import F
from django.utils import timezone

from .models import Voluntario, Actividad, Inscripcion, Asistencia, Certificado
from .forms import RegistroVoluntarioForm, ActividadForm


def index(request):
    q = request.GET.get('q', '')
    if q:
        actividades = Actividad.objects.filter(titulo__icontains=q).order_by('fecha')
    else:
        actividades = Actividad.objects.all().order_by('fecha')
    return render(request, 'app/actividades_list.html', {'actividades': actividades, 'q': q})


def registro_voluntario(request):
    if request.method == 'POST':
        form = RegistroVoluntarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso')
            return redirect('app:index')
        else:
            messages.error(request, 'Corrija los errores del formulario')
    else:
        form = RegistroVoluntarioForm()
    return render(request, 'app/registro.html', {'form': form})


def actividades_disponibles(request):
    actividades = Actividad.objects.all().order_by('fecha')
    return render(request, 'app/actividades_list.html', {'actividades': actividades})


def inscribir(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        correo = request.POST.get('correo')
        try:
            voluntario = Voluntario.objects.get(cedula=cedula, correo=correo)
        except Voluntario.DoesNotExist:
            messages.error(request, 'Voluntario no encontrado. Regístrese primero.')
            return redirect('app:registro')

        inscritos = Inscripcion.objects.filter(actividad=actividad).count()
        if inscritos >= actividad.cupos:
            messages.error(request, 'No hay cupos disponibles')
            return redirect('app:actividades')

        ins, created = Inscripcion.objects.get_or_create(voluntario=voluntario, actividad=actividad)
        if created:
            messages.success(request, 'Inscripción registrada')
        else:
            messages.info(request, 'Ya estás inscrito a esta actividad')
        return redirect('app:actividades')

    return render(request, 'app/inscribir.html', {'actividad': actividad})


def coord_panel(request):
    actividades = Actividad.objects.all().order_by('fecha')

    # Para cada actividad obtenemos los inscritos y la suma de horas registradas
    actividades_rows = []
    for a in actividades:
        inscritos = Inscripcion.objects.filter(actividad=a).select_related('voluntario')
        participantes = [ins.voluntario.nombre for ins in inscritos]
        # sumar horas de Asistencia asociadas a estas inscripciones
        total_horas = 0.0
        any_horas = False
        for ins in inscritos:
            asist = Asistencia.objects.filter(inscripcion=ins).first()
            if asist and asist.horas:
                try:
                    total_horas += float(asist.horas)
                    any_horas = True
                except Exception:
                    pass
        actividades_rows.append({'actividad': a, 'participantes': participantes, 'total_horas': (total_horas if any_horas else None)})

    return render(request, 'app/coord_panel.html', {'actividades_rows': actividades_rows})


def nueva_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad creada')
            return redirect('app:coord_panel')
        else:
            messages.error(request, 'Corrija los errores')
    else:
        form = ActividadForm()
    return render(request, 'app/nueva_actividad.html', {'form': form})


def editar_actividad(request, pk):
    act = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=act)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad actualizada')
            return redirect('app:coord_panel')
        else:
            messages.error(request, 'Corrija los errores')
    else:
        form = ActividadForm(instance=act)
    return render(request, 'app/editar_actividad.html', {'form': form, 'actividad': act})


def eliminar_actividad(request, pk):
    act = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        act.delete()
        messages.success(request, 'Actividad eliminada')
        return redirect('app:coord_panel')
    return render(request, 'app/eliminar_actividad.html', {'actividad': act})


def registrar_asistencia(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    inscripciones = Inscripcion.objects.filter(actividad=actividad).select_related('voluntario')
    if request.method == 'POST':
        generados = []
        for ins in inscripciones:
            key = f'asistio_{ins.id}'
            asistio = request.POST.get(key) == 'on'
            horas_val = request.POST.get(f'horas_{ins.id}')
            horas = None
            try:
                horas = float(horas_val) if horas_val else None
            except Exception:
                horas = None

            a, created = Asistencia.objects.get_or_create(inscripcion=ins)
            a.asistio = asistio
            a.horas = horas
            a.save()

            # Generar certificado inmediatamente si asistió y no existe aún
            if a.asistio:
                cert, c_created = Certificado.objects.get_or_create(voluntario=ins.voluntario, actividad=actividad)
                if c_created:
                    generados.append(cert)

        msg = 'Asistencia guardada.'
        if generados:
            msg = f"Asistencia guardada. Generados {len(generados)} certificados."
        messages.success(request, msg)
        return redirect('app:coord_panel')

    rows = []
    for ins in inscripciones:
        try:
            a = Asistencia.objects.get(inscripcion=ins)
        except Asistencia.DoesNotExist:
            a = None
        rows.append({'inscripcion': ins, 'asistencia': a})

    return render(request, 'app/registro_asistencia.html', {'actividad': actividad, 'rows': rows})


def certificados_panel(request):
    actividades = Actividad.objects.all().order_by('-fecha')
    return render(request, 'app/certificados_panel.html', {'actividades': actividades})


def generar_certificados(request):
    if request.method == 'POST':
        actividad_id = request.POST.get('actividad')
        actividad = get_object_or_404(Actividad, pk=actividad_id)
        inscritos = Inscripcion.objects.filter(actividad=actividad).select_related('voluntario')
        selected = request.POST.getlist('vol')
        generados = []
        for ins in inscritos:
            try:
                asist = Asistencia.objects.get(inscripcion=ins)
            except Asistencia.DoesNotExist:
                continue
            if not asist.asistio:
                continue
            if str(ins.voluntario.id) in selected:
                cert = Certificado.objects.create(voluntario=ins.voluntario, actividad=actividad)
                generados.append(cert)
        if generados:
            messages.success(request, f'Generados {len(generados)} certificados')
            return redirect('app:ver_certificado', cert_id=generados[0].id)
        else:
            messages.info(request, 'No se generaron certificados')
            return redirect('app:certificados_panel')

    return redirect('app:certificados_panel')


def ver_certificado(request, cert_id):
    cert = get_object_or_404(Certificado, pk=cert_id)

    # intentar obtener las horas desde Asistencia (vía Inscripcion)
    horas = None
    try:
        ins = Inscripcion.objects.get(voluntario=cert.voluntario, actividad=cert.actividad)
        asist = Asistencia.objects.filter(inscripcion=ins).first()
        if asist and asist.horas:
            horas = asist.horas
    except Inscripcion.DoesNotExist:
        horas = None

    # Si el querystring contiene pdf=1 intentamos generar PDF (WeasyPrint)
    if request.GET.get('pdf') in ['1', 'true', 'yes']:
        try:
            from django.template.loader import render_to_string
            from weasyprint import HTML
            html_string = render_to_string('app/certificate.html', {'cert': cert, 'horas': horas, 'pdf_mode': True})
            html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
            pdf = html.write_pdf()
            from django.http import HttpResponse
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"certificado_{cert.voluntario.nombre.replace(' ','_')}_{cert.actividad.titulo.replace(' ','_')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception:
            # si falla la generación PDF, seguimos y mostramos HTML con aviso
            messages.warning(request, 'Generación de PDF no disponible (no está instalada la dependencia). Mostrando HTML.')

    return render(request, 'app/certificate.html', {'cert': cert, 'horas': horas})


def lista_certificados(request):
    """Página pública donde se pueden ver y descargar certificados ya generados.
    Permite filtrar por actividad mediante un select."""
    actividades = Actividad.objects.all().order_by('-fecha')
    actividad_id = request.GET.get('actividad')
    certificados = Certificado.objects.select_related('voluntario', 'actividad').order_by('-fecha_emision')
    if actividad_id:
        try:
            certificados = certificados.filter(actividad__id=int(actividad_id))
        except Exception:
            pass

    # adjuntar horas si existen
    cert_rows = []
    for c in certificados:
        horas = None
        try:
            ins = Inscripcion.objects.get(voluntario=c.voluntario, actividad=c.actividad)
            a = Asistencia.objects.filter(inscripcion=ins).first()
            if a and a.horas:
                horas = a.horas
        except Inscripcion.DoesNotExist:
            horas = None
        cert_rows.append({'cert': c, 'horas': horas})

    return render(request, 'app/certificados_public.html', {'actividades': actividades, 'cert_rows': cert_rows, 'selected': actividad_id})


def mis_certificados(request):
    """Permite a un voluntario ver y descargar sus certificados.
    Se solicita `cedula` y `correo` para validar identidad.
    """
    cert_rows = []
    voluntario = None
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        correo = request.POST.get('correo')
        try:
            voluntario = Voluntario.objects.get(cedula=cedula, correo=correo)
        except Voluntario.DoesNotExist:
            messages.error(request, 'Voluntario no encontrado. Verifica cédula y correo.')
            voluntario = None

        if voluntario:
            certificados = Certificado.objects.filter(voluntario=voluntario).select_related('actividad').order_by('-fecha_emision')
            for c in certificados:
                horas = None
                try:
                    ins = Inscripcion.objects.get(voluntario=c.voluntario, actividad=c.actividad)
                    a = Asistencia.objects.filter(inscripcion=ins).first()
                    if a and a.horas:
                        horas = a.horas
                except Inscripcion.DoesNotExist:
                    horas = None
                cert_rows.append({'cert': c, 'horas': horas})

    return render(request, 'app/mis_certificados.html', {'voluntario': voluntario, 'cert_rows': cert_rows})
