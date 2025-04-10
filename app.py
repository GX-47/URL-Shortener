from flask import Flask, request, redirect, jsonify
import string
import random
import os
import redis
from pymongo import MongoClient

app = Flask(__name__)

# Connect to Redis or MongoDB based on environment variables
if os.environ.get('MONGO_URI'):
    mongo_client = MongoClient(os.environ.get('MONGO_URI'))
    db = mongo_client.get_database('url_shortener')
    urls_collection = db.urls
    
    # Use MongoDB for storage
    def save_url(short_url, long_url):
        urls_collection.update_one(
            {'short_code': short_url}, 
            {'$set': {'long_url': long_url}},
            upsert=True
        )
    
    def get_url(short_url):
        result = urls_collection.find_one({'short_code': short_url})
        if result:
            return result['long_url']
        return None
        
elif os.environ.get('REDIS_HOST'):
    r = redis.Redis(
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        db=0,
        decode_responses=True
    )
    # Use Redis for storage
    def save_url(short_url, long_url):
        r.set(short_url, long_url)
    
    def get_url(short_url):
        return r.get(short_url)
else:
    # Use in-memory dictionary for storage
    url_mapping = {}
    
    def save_url(short_url, long_url):
        url_mapping[short_url] = long_url
    
    def get_url(short_url):
        return url_mapping.get(short_url)

def generate_short_code(length=6):
    """Generate a random string of fixed length"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head><title>URL Shortener</title></head>
        <body>
            <h1>URL Shortener</h1>
            <form action="/shorten" method="post">
                <input type="url" name="url" placeholder="Enter URL to shorten" required>
                <button type="submit">Shorten</button>
            </form>
        </body>
    </html>
    """

@app.route('/shorten', methods=['POST'])
def shorten_url():
    # Get the URL from form data or JSON
    if request.is_json:
        long_url = request.json.get('url')
    else:
        long_url = request.form.get('url')
    
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    
    # Generate a short code
    short_code = generate_short_code()
    
    # Store the mapping
    save_url(short_code, long_url)
    
    # Build the shortened URL
    host = request.host
    short_url = f"http://{host}/{short_code}"
    
    # Return as JSON if the request was JSON, otherwise as HTML
    if request.is_json:
        return jsonify({"short_url": short_url, "long_url": long_url})
    else:
        return f"""
        <html>
            <head><title>URL Shortened</title></head>
            <body>
                <h1>URL Shortened</h1>
                <p>Original URL: {long_url}</p>
                <p>Shortened URL: <a href="{short_url}">{short_url}</a></p>
                <a href="/">Shorten another URL</a>
            </body>
        </html>
        """

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    long_url = get_url(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))