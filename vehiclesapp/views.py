from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehicle
from .forms import VehicleForm


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def vehicle_create(request):
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')
    return render(request, 'vehicle_form.html', {'form': form})


def vehicle_update(request, pk):
    obj = get_object_or_404(Vehicle, pk=pk)
    form = VehicleForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')
    return render(request, 'vehicle_form.html', {'form': form, 'object': obj})


def vehicle_delete(request, pk):
    obj = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicle_confirm_delete.html', {'object': obj})
