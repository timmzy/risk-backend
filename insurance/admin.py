from django.contrib import admin
from .models import RiskField, Risk, EnumChoice
from .model_utils import SchemaBuilder
from .forms import RiskFieldForm
from django.apps import apps


class RiskFieldLine(admin.TabularInline):
    model = RiskField
    form = RiskFieldForm
    extra = 1


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    inlines = (RiskFieldLine,)
    list_display = ['name']

    def save_related(self, request, form, formsets, change):
        # This allows database table to be created at once with all data needed
        super().save_related(request, form, formsets, change)
        if not change:
            risk = form.instance
            model = risk.get_django_model()
            builder = SchemaBuilder(model)
            builder.create_db_table()

    def delete_model(self, request, obj):
        # Remove table from database when delete from admin change view
        model = obj.get_django_model()
        del apps.all_models[obj._meta.app_label][obj.get_model_name]
        builder = SchemaBuilder(model)
        builder.delete_model()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Remove table from database when delete from admin list view
        for obj in queryset:
            model = obj.get_django_model()
            del apps.all_models[obj._meta.app_label][obj.get_model_name]
            builder = SchemaBuilder(model)
            builder.delete_model()
        super().delete_model(request, queryset)


@admin.register(EnumChoice)
class EnumChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice', 'value']
