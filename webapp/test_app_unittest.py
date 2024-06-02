import unittest
from unittest.mock import patch
import json
import os
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

        self.test_project = "test_project"
        self.context_file_path = f"/output/{self.test_project}/context.json"
        os.makedirs(os.path.dirname(self.context_file_path), exist_ok=True)

        self.initial_context = {
            "key1": "value1",
            "key2": "value2"
        }
        with open(self.context_file_path, 'w') as f:
            json.dump(self.initial_context, f)

        self.test_project_to_delete = "test_project_to_delete"
        self.context_file_path_delete = f"/output/{self.test_project_to_delete}/context.json"
        os.makedirs(os.path.dirname(self.context_file_path_delete), exist_ok=True)

        self.initial_context_delete = {
            "release_dir": "value1",
        }
        with open(self.context_file_path_delete, "w") as f:
            json.dump(self.initial_context_delete, f)

        self.constant_project = "constant_project"
        self.constant_context_path = f"/output/{self.constant_project}/context.json"
        os.makedirs(os.path.dirname(self.constant_context_path), exist_ok=True)
        self.constant_context = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "model": "Test_Model",
            "duration": "12 hour(s)",
            "start_time": "2024-06-02T12:00:00Z"
        }
        with open(self.constant_context_path, 'w') as f:
            json.dump(self.constant_context, f)

        self.test_project_1 = "test_project_1"
        self.context_file_path_1 = f"/output/{self.test_project_1}/context.json"
        os.makedirs(os.path.dirname(self.context_file_path_1), exist_ok=True)
        self.context_data_1 = {
            "name": "Project 1",
            "created_time": "2024-06-01T10:00:00Z"
        }
        with open(self.context_file_path_1, 'w') as f:
            json.dump(self.context_data_1, f)

        self.test_project_2 = "test_project_2"
        self.context_file_path_2 = f"/output/{self.test_project_2}/context.json"
        os.makedirs(os.path.dirname(self.context_file_path_2), exist_ok=True)
        self.context_data_2 = {
            "name": "Project 2",
            "created_time": "2024-06-02T12:00:00Z"
        }
        with open(self.context_file_path_2, 'w') as f:
            json.dump(self.context_data_2, f)

    def tearDown(self):
        os.remove(self.context_file_path)
        os.rmdir(os.path.dirname(self.context_file_path))

        os.remove(self.context_file_path_delete)
        os.rmdir(os.path.dirname(self.context_file_path_delete))

        os.remove(self.context_file_path_1)
        os.rmdir(os.path.dirname(self.context_file_path_1))

        os.remove(self.context_file_path_2)
        os.rmdir(os.path.dirname(self.context_file_path_2))

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

    def test_api_project_new_with_existing_model(self):
        existing_model = "MSI_leeway"
        response = self.client.get(f"/project/new?model={existing_model}")
        self.assertEqual(response.status_code, 200)

    def test_api_project_new_with_nonexisting_model(self):
        non_existing_model = "non-existing-model"
        response = self.client.get(f"/project/new?model={non_existing_model}")
        # If model does not exist user should be redirector to "/" and code should be 302.
        self.assertEqual(response.status_code, 302)

    def test_api_project_new_with_model_not_provided(self):
        response = self.client.get("/project/new")
        # If model is not provided user is redirected to "/" and code should be 302.
        self.assertEqual(response.status_code, 302)

    def test_update_existing_key(self):
        response = self.client.post(f'/project/{self.test_project}/update', data={
            'name': 'ctx_key1',
            'value': 'new_value1'
        })
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(response.status_code, 200)

        # Verify the context file was updated
        with open(self.context_file_path) as f:
            updated_context = json.load(f)
        self.assertEqual(updated_context['key1'], 'new_value1')

    def test_update_non_existing_key(self):
        response = self.client.post(f'/project/{self.test_project}/update', data={
            'name': 'ctx_non_existing_key',
            'value': 'new_value'
        })
        self.assertEqual(response.data.decode(), 'OK')

        # Verify the context file was not updated
        with open(self.context_file_path) as f:
            updated_context = json.load(f)
        self.assertNotIn('non_existing_key', updated_context)

    def test_update_without_ctx_prefix(self):
        response = self.client.post(f'/project/{self.test_project}/update', data={
            'name': 'key2',
            'value': 'new_value2'
        })
        self.assertEqual(response.data.decode(), 'OK')

        # Verify the context file was updated
        with open(self.context_file_path) as f:
            updated_context = json.load(f)
        self.assertEqual(updated_context['key2'], 'new_value2')

    def test_delete_project_success(self):
        response = self.client.delete(f'/project/{self.test_project_to_delete}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')

    def test_delete_project_not_found(self):
        non_existing_project = 'non_existing_project'
        try:
            response = self.client.delete(f'/project/{non_existing_project}/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), 'OK')
        except FileNotFoundError:
            # If FileNotFoundError is caught, the test passes
            pass
        else:
            # If no exception is thrown, the test fails
            self.fail("Expected FileNotFoundError but no exception was raised")

    def test_show_output_success(self):
        response = self.client.get(f'/project/{self.constant_project}/project')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'40.7128', response.data)
        self.assertIn(b'-74.006', response.data)

    def test_show_output_missing_file(self):
        # Test when context.json file does not exist
        try:
            response = self.client.get('/project/non_existing_project/project')
            self.assertEqual(response.status_code, 404)
        except FileNotFoundError:
            # If FileNotFoundError is caught, the test passes
            pass
        else:
            # If no exception is thrown, the test fails
            self.fail("Expected FileNotFoundError but no exception was raised")