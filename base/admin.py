from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Cultura, Fazenda


class CulturaInline(admin.TabularInline):
    model = Cultura

    fields = [
        "tipo_cultura",
        "area",
    ]
    extra = 0
    verbose_name = "Cultura"
    verbose_name_plural = "Culturas"


@admin.register(Fazenda)
class FazendaAdmin(ModelAdmin):
    list_display = ["nome_fazenda", "nome_produtor", "cidade", "uf"]

    inlines = [CulturaInline]
