
# URL_Shortener
Implementation of final project for the course Cloud Computing (UE22CS351A)
=======
# Load-Balanced URL Shortener

A containerized URL shortener service built with Python, Flask and Docker that allows users to submit long URLs and get shortened versions. URL mappings are stored in Redis.

## Features

- Shorten long URLs to easily shareable short URLs
- Containerized application using Docker
- Redis for URL storage

## Project Structure

```
├── Project1.pdf                  # PDF of Project Statement
├── app.py                        # Flask application code
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
└── requirements.txt              # Python dependencies
```

## Setup and Installation

### Prerequisites

- Docker

### Running with Docker (Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/GX-47/URL-Shortener.git
   cd URL-Shortener
   ```

2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

3. Access the application at http://localhost:5000

### Sending API Requests

Send API request via terminal:

   ```bash
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"url":"https://amazon.in"}' \
    http://localhost:5000/shorten
   ```

### Stopping the application

If using docker:
```bash
   docker-compose down -v
```


## API Endpoints

- `GET /` - Home page with URL submission form
- `POST /shorten` - Shorten a URL (accepts form data or JSON)
- `GET /<short_code>` - Redirect to the original URL


## Technologies Used

- Python/Flask - Web application
- Redis - Key-value store
- Docker - Containerization
- Gunicorn - WSGI HTTP Server

