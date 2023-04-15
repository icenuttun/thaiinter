from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .forms import RoofTrackingForm, ProcessNameForm
from qrcodes.models import MetalSheetRoof
from .models import RoofTracking, ProcessName

@login_required
def index(request):
    # Retrieve the last 10 items from RoofTracking
    last_10_trackings = RoofTracking.objects.order_by('-date_added')[:10]
    # Extract the qr_code_id values from the last 10 trackings
    qr_code_ids = [tracking.qr_code_id for tracking in last_10_trackings]
    # Retrieve the corresponding MetalSheetRoof records, ordered by date_added in descending order
    roofs = MetalSheetRoof.objects.filter(qr_code_id__in=qr_code_ids).order_by('-created_date')

    # Create a dictionary mapping qr_code_id to roof object
    roof_dict = {roof.qr_code_id: roof for roof in roofs}

    # Assign the roof object to each tracking object
    for tracking in last_10_trackings:
        tracking.roof = roof_dict.get(tracking.qr_code_id)

    context = {'last_10_trackings': last_10_trackings}
    return render(request, 'tracking/index.html', context)

@login_required
def track_roof(request, qr_code_id):
    try:
        roof = MetalSheetRoof.objects.get(qr_code_id=qr_code_id)
    except MetalSheetRoof.DoesNotExist:
        return HttpResponseNotFound()

    try:
        roof_tracking = RoofTracking.objects.filter(qr_code_id=qr_code_id).latest('date_added')
        if not roof_tracking.is_active:
            return HttpResponse('This roof has already been finished.')
    except RoofTracking.DoesNotExist:
        roof_tracking = None
    
    processes = ProcessName.objects.all() 
    if request.method == 'POST':
        form = RoofTrackingForm(request.POST)
        if form.is_valid():
            new_tracking = form.save(commit=False)
            new_tracking.qr_code_id = qr_code_id
            new_tracking.updated_by = request.user
            new_tracking.is_active = not form.cleaned_data['last_process']
            new_tracking.save()
            return redirect('tracking:index')
    else:
        initial_data = {}
        if roof_tracking:
            initial_data = {
                'process_name': roof_tracking.process_name,
                'note': roof_tracking.note,
                'last_process': not roof_tracking.is_active,
            }
        form = RoofTrackingForm(initial=initial_data)

    context = {
        'form': form,
        'roof': roof,
        'roof_id': roof.id,
        'roof_type': roof.roof_type,
        'roof_size': roof.size,
        'roof_color': roof.color,
        'roof_quantity': roof.quantity,
        'roof_created_date': roof.created_date,
        'processes': processes, 
    }
    return render(request, 'tracking/track_roof.html', context)

@login_required
def add_process_name(request, qr_code_id):
    if request.method == 'POST':
        form = ProcessNameForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('tracking:track_roof', qr_code_id=qr_code_id)
            except IntegrityError:
                form.add_error('name', 'A process name with that name already exists.')
    else:
        form = ProcessNameForm()
    return render(request, 'tracking/add_process_name.html', {'form': form})
