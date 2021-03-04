from django.db import models
from django.core.exceptions import FieldDoesNotExist
from .model_utils import create_model, SchemaBuilder
from django.apps import apps


# Create your models here.
class Risk(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        # Get old value to check variations
        super().__init__(*args, **kwargs)
        self.__initial_model = self.get_django_model()
        self.__old_name = self.name

    def get_django_model(self):
        "Returns a functional Django model based on current data"
        # Get all associated fields into a list ready for dict()
        fields = [(f.name, f.get_django_field()) for f in self.fields.all()]
        # Use the create_model function defined above
        model_name = self.parse_model_name(self.name.lower())
        if self.is_registered:
            del apps.all_models[self._meta.app_label][self.get_model_name]
        return create_model(model_name, dict(fields), self._meta.app_label, f"{self._meta.app_label}.models")

    def get_django_model_app(self):
        return apps.get_model(self._meta.app_label, self.get_model_name)

    @classmethod
    def parse_model_name(cls, name):
        return name.title().replace(" ", "_")

    @property
    def is_registered(self):
        return self.parse_model_name(self.name).lower() in apps.all_models[self._meta.app_label]

    @property
    def get_model_name(self):
        return self.parse_model_name(self.name).lower()

    def save(self, *args, **kwargs):
        # Alter table if there a change in the name column of the record. For update only
        if self.id is not None:
            old_db_name = self.__initial_model._meta.db_table
            new_db_name = self.get_django_model()._meta.db_table
            if old_db_name != new_db_name:
                builder = SchemaBuilder(self.get_django_model())
                builder.alter_table(old_db_name, new_db_name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        model = self.get_django_model()
        del apps.all_models[self._meta.app_label][self.get_model_name]
        builder = SchemaBuilder(model)
        builder.delete_model()
        super().delete(*args, **kwargs)


class RiskField(models.Model):
    class RiskTypeField(models.TextChoices):
        TEXT = 'CharField', 'Text'
        NUMBER = 'IntegerField', 'Number'
        DATE = 'DateField', 'Date'

    name = models.CharField(max_length=50)
    field_type = models.CharField(max_length=12, choices=RiskTypeField.choices, default=RiskTypeField.TEXT)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='fields')
    kwargs = models.JSONField()

    class Meta:
        unique_together = (('name', 'risk'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_name = self.name
        self.__field_type = self.field_type
        self.__old_kwargs = self.kwargs

    def get_django_field(self):
        "Returns the correct field type, instantiated with applicable settings"
        # Get all associated settings into a list ready for dict()
        settings = self.kwargs

        # Instantiate the field with the settings as **kwargs
        return getattr(models, self.field_type)(**dict(settings))

    def delete(self, **kwargs):
        # When a column/field is removed from the model, it removes from the table
        model = self.risk.get_django_model()
        field = model._meta.get_field(self.name)
        builder = SchemaBuilder(model)
        builder.remove_field(field)
        super().delete(**kwargs)

    def get_old_field(self):
        # Return old field record
        model = self.risk.get_django_model()
        try:
            field = model._meta.get_field(self.__old_name)
            return field
        except FieldDoesNotExist:
            return None

    def get_latest_field(self):
        # Return new field record
        model = self.risk.get_django_model()
        try:
            field = model._meta.get_field(self.name)
            return field
        except FieldDoesNotExist:
            return None

    def save(self, *args, **kwargs):
        # Get old field and new.
        # This works for both created and updated
        old_field = self.get_old_field()
        super().save(*args, **kwargs)
        model = self.risk.get_django_model()
        builder = SchemaBuilder(model)
        builder.add_field(old_field, self.get_latest_field())
