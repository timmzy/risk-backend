from django import forms
from django.core.exceptions import ValidationError
from .models import RiskField, EnumChoice
from datetime import datetime


class RiskFieldForm(forms.ModelForm):
    max_length = forms.IntegerField(required=False, min_value=1)
    null = forms.BooleanField(required=False)
    default = forms.CharField(max_length=20, required=False)
    kwargs = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'readonly': 'readonly'}),
                             label='KWARGS - (not editable)', required=False)

    class Meta:
        model = RiskField
        fields = ['name', 'field_type', 'max_length', 'null', 'default', 'choices', 'kwargs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('name'):
            kwargs = self.initial['kwargs']
            update_kwargs = dict(kwargs)
            if kwargs.get('choices'):
                self.initial.update({'field_type': 'EnumField'})
                update_kwargs.pop('choices')
            self.initial.update(update_kwargs)

    def clean_name(self):
        value = self.cleaned_data.get('name')
        return str(value).lower()

    def clean_default(self):
        value = self.cleaned_data.get('default')
        null_value = self.cleaned_data.get('null')
        field_type = self.cleaned_data.get('field_type')
        risk_id = self.fields['risk'].initial
        risk_field_instance = self.instance
        if field_type == 'IntegerField':
            if "." in value:
                raise ValidationError("Integer number allowed only!")
        if field_type == 'DateField':
            if value:
                try:
                    datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError('Default date must be in "YYYY-MM-DD" format')
        if risk_id and risk_field_instance.id is None:
            if value == "" and null_value == False:
                raise ValidationError("Null can not be false while default is empty")
        return value

    def clean_max_length(self):
        value = self.cleaned_data.get('max_length')
        field_type = self.cleaned_data.get('field_type')
        if field_type == 'CharField' and value is None:
            raise ValidationError("Text field type must have a max_length value")
        return value

    def clean_choices(self):
        value = self.cleaned_data.get('choices')
        field_type = self.cleaned_data.get('field_type')
        if field_type == 'EnumField' and value.count() == 0:
            raise ValidationError('This field is required for Enum field')
        return value

    def save(self, commit=True):
        form = super().save(commit=False)
        data = self.cleaned_data
        kwargs_data = dict()
        default_val = data.get('default')
        field_type = data.get('field_type')
        if field_type == 'CharField':
            kwargs_data.update({'max_length': data.get('max_length')})
        else:
            if default_val:
                kwargs_data.update({'default': default_val})
        if field_type == 'EnumField':
            form.field_type = 'CharField'
            kwargs_data.update({'choices': True, 'max_length': 20})
        else:
            data.update({'choices': []})
        kwargs_data.update({'null': data.get('null')})
        form.kwargs = kwargs_data
        if commit:
            form.save()
            if len(list(data.get('choices'))) > 0:
                form.choices.set([item.id for item in data.get('choices')])
            else:
                form.choices.set([])
        return form
