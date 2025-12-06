
import unittest
import sys
import os
import io

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestErrorCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_unsupported_file_extension(self):
        # Create a text file in memory
        data = {
            'file': (io.BytesIO(b"some text"), 'test.txt')
        }
        response = self.app.post('/predict', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported file type', response.data.decode('utf-8'))

    def test_empty_paste(self):
        response = self.app.post('/predict', data={'code_text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please provide some code', response.data.decode('utf-8'))

    def test_short_paste(self):
        response = self.app.post('/predict', data={'code_text': 'print'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('too short', response.data.decode('utf-8'))

    def test_valid_paste(self):
        response = self.app.post('/predict', data={'code_text': 'print("hello world")'})
        self.assertEqual(response.status_code, 200)

    def test_garbage_text(self):
        # Text that is long enough (>10 chars) but is not code (0 LOC)
        # This one has spaces and no logic
        response = self.app.post('/predict', data={'code_text': 'just some random sentence that is definitely longer than ten chars but has no code logic'})
        self.assertEqual(response.status_code, 400)
    
    def test_trivial_identifier(self):
        # Single long word (technically a variable name, but garbage for us)
        response = self.app.post('/predict', data={'code_text': 'ksfhkujfhczldjcnskfsrfseudfsiduhvd'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No valid code structure', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
