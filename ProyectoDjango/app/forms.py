from django import forms
from django.contrib.auth.hashers import make_password
from .models import Voluntario, Actividad


class RegistroVoluntarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirmar = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Voluntario
        fields = ['nombre', 'cedula', 'correo', 'telefono', 'ciudad', 'habilidades', 'contrasena']

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get('contrasena')
        c = cleaned.get('confirmar')
        if p and c and p != c:
            self.add_error('confirmar', 'Las contraseñas no coinciden')
        return cleaned

    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            inst.save()
        return inst


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'fecha', 'hora', 'cupos']

    def clean_cupos(self):
        v = self.cleaned_data.get('cupos')
        if v is None or v < 0:
            raise forms.ValidationError('Cupos inválidos')
        return v
