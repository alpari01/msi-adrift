import unittest
import json
from app import create_app


class FlaskTestCase(unittest.TestCase):

    longMessage = True  # display assertion custom messages

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_load_index_page_response_is_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_models_endpoint_response_is_200(self):
        response = self.client.get('/api/models')
        self.assertEqual(response.status_code, 200)

    def test_each_model_has_correct_variables_naming_convention(self):
        # Each model has to have correct variables naming to work with MSI opendap and wind data.
        response = self.client.get('/api/models')
        data = json.loads(response.data.decode('utf-8'))

        for model_data in data:
            self.assertIn("variables", model_data, "'variables' field is missing from model config")

            self.assertIn("latitude", model_data["variables"],
                          "'latitude' variable is missing from model config")

            self.assertIn("longitude", model_data["variables"],
                          "'longitude' variable is missing from model config")

            self.assertIn("time", model_data["variables"],
                          "'time' variable is missing from model config")

            self.assertEqual("lat", model_data["variables"]["latitude"], "Incorrect latitude naming")
            self.assertEqual("lon", model_data["variables"]["longitude"], "Incorrect longitude naming")
            self.assertEqual("time", model_data["variables"]["time"], "Incorrect time naming")

    def test_each_model_has_correct_type(self):
        response = self.client.get('/api/models')
        data = json.loads(response.data.decode('utf-8'))

        model_types = [model_data["id"].split("_")[-1].lower() for model_data in data]
        expected_types = ['leeway', 'openoil']
        for name in expected_types:
            self.assertIn(name, model_types)

    def test_each_model_has_correct_data_urls(self):
        response = self.client.get('/api/models')
        data = json.loads(response.data.decode('utf-8'))

        for model_data in data:
            self.assertIn("opendap_url", model_data, "'opendap_url' variable is missing from model config")
            self.assertIn("wind_url", model_data, "'wind_url' variable is missing from model config")

    def test_each_model_data_url_is_not_empty(self):
        response = self.client.get('/api/models')
        data = json.loads(response.data.decode('utf-8'))

        for model_data in data:
            self.assertNotEqual(model_data["opendap_url"], "", "'opendap_url' cannot be empty string")
            self.assertNotEqual(model_data["wind_url"], "", "'wind_url' cannot be empty string")

    def test_msi_leeway_model_exists(self):
        model_name = 'MSI_leeway'
        response = self.client.get(f'/api/model/{model_name}/info')
        self.assertEqual(response.status_code, 200)

    def test_msi_openoil_model_exists(self):
        model_name = 'MSI_openoil'
        response = self.client.get(f'/api/model/{model_name}/info')
        self.assertEqual(response.status_code, 200)
    def test_msi_leeway_model_contains_correct_attributes(self):
        model_name = 'MSI_leeway'
        response = self.client.get(f'/api/model/{model_name}/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('time_min', data)
        self.assertIn('time_max', data)
        self.assertIn('lat_min', data)
        self.assertIn('lat_max', data)
        self.assertIn('lon_min', data)
        self.assertIn('lon_max', data)
        self.assertIn('polygon', data)
        self.assertIn('drifters', data)

    def test_msi_openoil_model_contains_correct_attributes(self):
        model_name = 'MSI_openoil'
        response = self.client.get(f'/api/model/{model_name}/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('time_min', data)
        self.assertIn('time_max', data)
        self.assertIn('lat_min', data)
        self.assertIn('lat_max', data)
        self.assertIn('lon_min', data)
        self.assertIn('lon_max', data)
        self.assertIn('polygon', data)
        self.assertIn('drifters', data)