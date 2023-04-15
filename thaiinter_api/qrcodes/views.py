from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import MetalSheetRoof
from .forms import MetalSheetRoofForm, RoofColorForm, RoofTypeForm, RoofSizeForm

import base64
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

@login_required
def index(request):
    roofs = MetalSheetRoof.objects.order_by('-created_date')[:10]
    return render(request, 'qrcodes/index.html', {'roofs': roofs})

@login_required
def add_roof(request):
    if request.method == 'POST':
        form = MetalSheetRoofForm(request.POST)
        if form.is_valid():
            new_roof = form.save(commit=False)

            # Set the created_by field to the current user
            new_roof.created_by = request.user

            new_roof.save()
            download_url = reverse('qrcodes:download_and_redirect', args=[new_roof.qr_code_id])
            return redirect(download_url)
    else:
        form = MetalSheetRoofForm()
    return render(request, 'qrcodes/add_roof.html', {'form': form})

@login_required
def add_roof_type(request):
    if request.method == 'POST':
        form = RoofTypeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('qrcodes:add_roof')
            except IntegrityError:
                form.add_error('name', 'A roof type with that name already exists.')
    else:
        form = RoofTypeForm()
    return render(request, 'qrcodes/add_roof_type.html', {'form': form})

@login_required
def add_roof_size(request):
    if request.method == 'POST':
        form = RoofSizeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('qrcodes:add_roof')
            except IntegrityError:
                form.add_error('name', 'A roof size with that name already exists.')
    else:
        form = RoofSizeForm()
    return render(request, 'qrcodes/add_roof_size.html', {'form': form})

@login_required
def add_roof_color(request):
    if request.method == 'POST':
        form = RoofColorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('qrcodes:add_roof')
            except IntegrityError:
                form.add_error('name', 'A roof color with that name already exists.')
    else:
        form = RoofColorForm()
    return render(request, 'qrcodes/add_roof_color.html', {'form': form})

@login_required
def roof_detail(request, roof_id):
    roof = get_object_or_404(MetalSheetRoof, id=roof_id)
    qr_code_url = reverse('qrcodes:qr_code_detail', args=[roof.qr_code_id])
    return render(request, 'qrcodes/roof_detail.html', {'roof': roof, 'qr_code_url': qr_code_url})

@login_required
def qr_code_detail(request, qr_code_id):
    roof = get_object_or_404(MetalSheetRoof, qr_code_id=qr_code_id)
    return render(request, 'qrcodes/qr_code_detail.html', {'roof': roof})

@login_required
def print_qr_code(request, qr_code_id):
    try:
        roof = MetalSheetRoof.objects.get(qr_code_id=qr_code_id)
    except MetalSheetRoof.DoesNotExist:
        return HttpResponseNotFound()

    # Generate the QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,  # set the box size to 1 to get a smaller QR code image
        border=4,
    )
    qr.add_data(f'{settings.SITE_URL}/tracking/{qr_code_id}/')
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    qr_code_data = img.tobytes()

    # Generate the PDF
    qr_size = 100  # set the size of the QR code image in mm
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{roof.id}.pdf"'
    can = canvas.Canvas(response, pagesize=portrait((qr_size*mm, qr_size*mm)))

    # Create the QR code image and draw it on the canvas
    img = Image.frombytes('1', img.size, qr_code_data)
    img = img.resize((qr_size, qr_size))
    can.drawImage(ImageReader(img), x=0, y=0, width=qr_size*mm, height=qr_size*mm)
    can.showPage()
    can.save()

    return response, roof.id

@login_required
def download_and_redirect(request, qr_code_id):
    pdf_response, roof_id = print_qr_code(request, qr_code_id)
    pdf_base64 = base64.b64encode(pdf_response.content).decode('utf-8')
    return render(request, 'qrcodes/download_and_redirect.html', {'pdf_base64': pdf_base64, 'filename': f'{roof_id}.pdf'})