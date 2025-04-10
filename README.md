# Load-Balanced URL Shortener

A containerized URL shortener service built with Python, Flask, Docker, and Kubernetes that allows users to submit long URLs and get shortened versions. The system is scalable, with a load balancer distributing requests across multiple instances. URL mappings are stored in Redis, a key-value store running in a separate container.

## Features

- Shorten long URLs to easily shareable short URLs
- Containerized application using Docker
- Redis for URL storage
- Horizontally scalable with Kubernetes
- Auto-scaling based on CPU usage
- Load balancing across multiple instances
- Stress testing tools included

## Project Structure

```
├── Project1.pdf                  # PDF of Project Statement
├── app.py                        # Flask application code
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
├── redis-deployment.yaml         # Redis Kubernetes deployment
├── url-shortener-config.yaml     # ConfigMap and Secret
├── url-shortener-deployment.yaml # URL shortener deployment
├── url-shortener-hpa.yaml        # Horizontal Pod Autoscaler
├── url-shortener-ingress.yaml    # Ingress configuration
└── stress-test.ps1               # PowerShell stress testing script
├── stress-test.sh                # Bash stress testing script
```

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Docker Desktop, minikube, or cloud provider)
- kubectl command-line tool

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

### Deploying to Kubernetes

1. Make sure your Kubernetes cluster is running:
   - Docker Desktop: Enable Kubernetes in settings
   - minikube: `minikube start`

2. Build and push the Docker image (if not using an existing image):
   ```bash
   docker build -t your-dockerhub-username/url-shortener:v1 .
   docker push your-dockerhub-username/url-shortener:v1
   ```

3. Update the image name in `url-shortener-deployment.yaml` to use your Docker Hub username:
   ```yaml
   # Change this line in url-shortener-deployment.yaml
   image: your-dockerhub-username/url-shortener:v1
   ```

4. Apply Kubernetes configurations:
   ```bash
   # Apply ConfigMap and Secret
   kubectl apply -f url-shortener-config.yaml

   # Deploy Redis
   kubectl apply -f redis-deployment.yaml

   # Deploy URL shortener
   kubectl apply -f url-shortener-deployment.yaml

   # Apply HPA for auto-scaling
   kubectl apply -f url-shortener-hpa.yaml

   # Apply Ingress (if needed)
   kubectl apply -f url-shortener-ingress.yaml
   ```

5. For Ingress to work locally, add this entry to your `/etc/hosts` file:
   ```
   127.0.0.1  url-shortener.local
   ```

6. Run in a separate terminal:
   ```
   minikube tunnel
   ```

7. Access the application:
   - With LoadBalancer: http://localhost
   - With Ingress: http://url-shortener.local

### Sending API Requests

Send API request via terminal:

   ```bash
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"url":"https://amazon.in"}' \
    http://url-shortener.local/shorten
   ```

### Stopping the application

1. If using docker:
   ```bash
    docker-compose down -v
   ```

2. If using kubernetes:
   ```bash
   kubectl delete -f url-shortener-ingress.yaml -f url-shortener-hpa.yaml -f url-shortener-deployment.yaml -f redis-deployment.yaml -f url-shortener-config.yaml
   ```

## Running Stress Tests

### Using Bash (Unix/Linux/Mac)

```bash
chmod +x stress-test.sh
./stress-test.sh
```

### Using PowerShell (Windows/Mac with PowerShell installed)

```powershell
pwsh -File stress-test.ps1
```

## Monitoring

Monitor your deployment with standard Kubernetes commands:

```bash
# Check if pods are running
kubectl get pods

# View pod details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Monitor HPA
kubectl get hpa
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
- Kubernetes - Orchestration
