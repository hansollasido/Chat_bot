from django.contrib import admin
from .models import *

from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin


class PostAdmin(ImportExportMixin,SummernoteModelAdmin,admin.ModelAdmin):
    list_display = ('d_q','d_a')
    summernote_field = ('content',)

admin.site.register(data_save,PostAdmin)
# Register your models here.
