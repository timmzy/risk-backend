from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Risk, RiskField
from .api.serializers import RiskAndFieldsSerializer, RiskOnlySerializer
from django.contrib.auth.models import User
from django.apps import apps

# initialize the APIClient app
client = APIClient()


class GetRiskTest(APITestCase):
    def setUp(self):
        """
        Initialize data into the model
        """
        car_risk_obj = Risk.objects.create(name='Car Risk', description='car risk model')
        RiskField.objects.bulk_create([
            RiskField(name='name', field_type='CharField', risk=car_risk_obj, kwargs={'max_length': 25, 'null': True}),
            RiskField(name='no_seats', field_type='IntegerField', risk=car_risk_obj, kwargs={'null': True}),
            RiskField(name='date_bought', field_type='DateField', risk=car_risk_obj, kwargs={'null': True}),
        ])

    def test_risk_fields_api(self):
        """
        Test the rest api for all risk and fields
        """
        response = self.client.get('/api/v1/risks-fields/', content_type={'Content-Type': 'application/json'})
        serializer = RiskAndFieldsSerializer(Risk.objects.all(), many=True)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_single_risk_api(self):
        """
        Test the rest api for single risk
        """
        risk_obj = Risk.objects.first()
        serializer = RiskOnlySerializer(risk_obj)
        response = self.client.get(f'/api/v1/risks/{risk_obj.id}/', content_type={'Content-Type': 'application/json'})
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, 200)


class ModelTest(TestCase):
    def setUp(self):
        """
        Initialize certain process/actions
        """
        self.client.force_login(User.objects.create_superuser('admin_test', '123'))
        self.post_data = {'name': ['Car'], 'description': ['This is for an insurance'], 'fields-TOTAL_FORMS': ['2'],
                          'fields-INITIAL_FORMS': ['0'], 'fields-MIN_NUM_FORMS': ['0'],
                          'fields-MAX_NUM_FORMS': ['1000'], 'fields-0-id': [''], 'fields-0-risk': [''],
                          'fields-0-name': ['name'], 'fields-0-field_type': ['CharField'],
                          'fields-0-max_length': ['20'], 'fields-0-default': [''], 'fields-0-kwargs': [''],
                          'fields-1-id': [''], 'fields-1-risk': [''], 'fields-1-name': ['age'],
                          'fields-1-field_type': ['IntegerField'], 'fields-1-max_length': [''],
                          'fields-1-default': [''], 'fields-1-kwargs': [''], 'fields-__prefix__-id': [''],
                          'fields-__prefix__-risk': [''], 'fields-__prefix__-name': [''],
                          'fields-__prefix__-field_type': [''], 'fields-__prefix__-max_length': [''],
                          'fields-__prefix__-default': [''], 'fields-__prefix__-kwargs': [''], '_save': ['Save']}
        self.client.post('/admin/insurance/risk/add/', data=self.post_data)

    def test_post_admin(self):
        """
        Post data with admin
        Create a dynamic model using admin
        """
        risk_obj = Risk.objects.first()
        model = risk_obj.get_django_model()
        # Exclude id because it is created by default and not created in the RiskField model
        fields_excluding_id = model._meta.fields[1:]
        car_dict = {'name': 'Toyota', 'age': 3}
        car_obj = model.objects.create(**car_dict)
        car_obj_dict = car_obj.__dict__
        # Test each fields created
        self.assertEqual('id', model._meta.get_field('id').name)
        self.assertEqual('name', model._meta.get_field('name').name)
        self.assertEqual('age', model._meta.get_field('age').name)
        # Test database records created
        self.assertEqual(risk_obj.fields.count(), len(fields_excluding_id))
        self.assertEqual(car_dict['name'], car_obj_dict['name'])
        self.assertEqual(car_dict['age'], car_obj_dict['age'])

    def test_model_delete(self):
        risk = Risk.objects.first()
        model = risk.get_django_model()
        self.assertEqual(model._meta.model_name in apps.all_models[model._meta.app_label], True)
        risk.delete()
        self.assertEqual(model._meta.model_name in apps.all_models[model._meta.app_label], False)

    def test_model_alter_field(self):
        """
        Test for fields change in model field name
        """
        risk = Risk.objects.first()
        first_field = risk.fields.first()
        model = risk.get_django_model()
        self.assertEqual(first_field.name, model._meta.get_field(first_field.name).name)
        first_field.name = 'car_name'
        first_field.save()
        latest_model = risk.get_django_model()
        self.assertEqual(first_field.name, latest_model._meta.get_field(first_field.name).name)

    def test_remove_field(self):
        """
        Test for fields removed from the dynamic model
        """
        risk = Risk.objects.first()
        first_field = risk.fields.first()
        model = risk.get_django_model()
        model_fields = [field.name for field in model._meta.fields]
        self.assertEqual((first_field.name in model_fields), True)
        first_field_name = first_field.name
        first_field.delete()
        latest_model = risk.get_django_model()
        latest_model_fields = [field.name for field in latest_model._meta.fields]
        self.assertEqual((first_field_name in latest_model_fields), False)

    def test_rename_model(self):
        """
        Test for rename of database table name create dynamically
        """
        risk = Risk.objects.first()
        model = risk.get_django_model()
        self.assertEqual(risk.get_model_name, model._meta.model_name)
        risk.name = 'Animal'
        risk.save()
        latest_model = risk.get_django_model()
        self.assertEqual(risk.get_model_name, latest_model._meta.model_name)
