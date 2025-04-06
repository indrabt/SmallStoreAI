# Utility functions for tests
import os
import logging
import json
import tempfile
from contextlib import contextmanager

@contextmanager
def temp_file_with_content(content, suffix='.json'):
    """Create a temporary file with the given content."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        yield path
    finally:
        os.unlink(path)

def create_test_json_file(data):
    """Create a temporary JSON file with the given data."""
    with temp_file_with_content(json.dumps(data)) as path:
        return path

class MockResponse:
    """Mock response object for API testing."""
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code
        self.text = json.dumps(json_data)
    
    def json(self):
        return self.json_data
