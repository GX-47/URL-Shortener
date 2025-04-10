import os
import sys
import pytest
import json

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app import app as flask_app

@pytest.fixture
def app():
    # Set up test environment variables
    os.environ['REDIS_HOST'] = 'localhost'
    os.environ['REDIS_PORT'] = '6379'
    
    # Return Flask app for testing
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Test that the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'URL Shortener' in response.data

def test_shorten_url_form(client):
    """Test URL shortening with form data"""
    response = client.post(
        '/shorten',
        data={'url': 'https://example.com'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Original URL: https://example.com' in response.data
    assert b'Shortened URL' in response.data

def test_shorten_url_json(client):
    """Test URL shortening with JSON data"""
    response = client.post(
        '/shorten',
        data=json.dumps({'url': 'https://example.com'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert 'short_url' in json_data
    assert json_data['long_url'] == 'https://example.com'

def test_redirect(client):
    """Test URL redirection"""
    # First create a shortened URL
    response = client.post(
        '/shorten',
        data=json.dumps({'url': 'https://example.com'}),
        content_type='application/json'
    )
    json_data = json.loads(response.data)
    short_url = json_data['short_url']
    
    # Extract the short code from the URL
    short_code = short_url.split('/')[-1]
    
    # Test redirection
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'https://example.com'
