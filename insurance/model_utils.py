from django.db import models
from django.db import connection
from django.db.utils import ProgrammingError
from django.contrib import admin


class SchemaBuilder:
    def __init__(self, model):
        self.model = model

    def create_db_table(self):
        try:
            with connection.schema_editor() as editor:
                editor.create_model(self.model)
        except ProgrammingError as err:
            # TODO: I couldn't figure out why sometimes despite the
            # fact that the model exists, the initial_model is None and
            # therefore this method will be called which leads to this
            # error
            pass

    def remove_field(self, field):
        try:
            with connection.schema_editor() as editor:
                editor.remove_field(self.model, field)
        except ProgrammingError as err:
            # TODO: I couldn't figure out why sometimes despite the
            # fact that the model exists, the initial_model is None and
            # therefore this method will be called which leads to this
            # error
            pass

    def alter_table(self, old_name, new_name):
        try:
            with connection.schema_editor() as editor:
                editor.alter_db_table(self.model, old_name, new_name)
        except ProgrammingError as err:
            pass

    def delete_model(self):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(self.model)
        except ProgrammingError as err:
            pass

    def add_field(self, old_field, new_field):
        if old_field is None:
            try:
                with connection.schema_editor() as editor:
                    editor.add_field(self.model, new_field)
            except ProgrammingError as err:
                pass
        else:
            try:
                with connection.schema_editor() as editor:
                    editor.alter_field(self.model, old_field, new_field)
            except ProgrammingError as err:
                pass

    def alter_field(self, old_field, new_field):
        try:
            with connection.schema_editor() as editor:
                editor.alter_field(self.model, old_field, new_field)
        except ProgrammingError as err:
            pass


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """

    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass

        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model
