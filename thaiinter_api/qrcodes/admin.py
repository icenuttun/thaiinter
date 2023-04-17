from django.contrib import admin
from .models import MetalSheetRoof, RoofType, RoofColor, RoofSize

# Register your models here.
admin.site.register(MetalSheetRoof)
admin.site.register(RoofType)
admin.site.register(RoofColor)
admin.site.register(RoofSize)