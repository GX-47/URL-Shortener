# Load-Balanced URL Shortener

A containerized URL shortener service built with Python, Flask, Docker, and Kubernetes that allows users to submit long URLs and get shortened versions. The system is scalable, with a load balancer distributing requests across multiple instances. URL mappings are stored in MongoDB, a key-value store running in a separate container.

## Features

- Shorten long URLs to easily shareable short URLs
- Containerized application using Docker
- MongoDB for URL storage
- Horizontally scalable with Kubernetes
- Auto-scaling based on CPU usage
- Load balancing across multiple instances
- Stress testing tools included

## Project Structure

```
/
├── app/                            # Application code
│   ├── app.py                      # Flask application
│   └── requirements.txt            # Python dependencies
│
├── docker/                         # Docker configurations
│   ├── Dockerfile                  # Main Dockerfile
│   └── docker-compose.yml          # Docker Compose config
│
├── kubernetes/                     # Kubernetes manifests
│   ├── config/                     # Configuration files
│   │   └── url-shortener-config.yaml  # ConfigMaps and Secrets
│   │
│   ├── deployments/                # Deployment manifests
│   │   ├── mongodb-deployment.yaml # MongoDB deployment
│   │   ├── redis-deployment.yaml   # Redis deployment
│   │   └── url-shortener-deployment.yaml # URL shortener deployment
│   │
│   ├── storage/                    # Storage configurations
│   │   └── mongodb-pvc.yaml        # MongoDB persistent volume claim
│   │
│   ├── networking/                 # Network configurations
│   │   └── url-shortener-ingress.yaml # Ingress configuration
│   │
│   └── scaling/                    # Scaling configurations
│       └── url-shortener-hpa.yaml  # Horizontal Pod Autoscaler
│
├── tests/                          # Testing scripts
│   ├── stress-test.sh              # Bash stress test
│   └── stress-test.ps1             # PowerShell stress test
│
├── .gitignore                      # Git ignore file
├── GITHUB_ACTIONS_SETUP.md         # CI/CD Setup documentation
└── README.md                       # Project documentation
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
   cd docker
   docker-compose up --build
   ```

3. Access the application at http://localhost:5000

### Running in Redis-only Mode

The application can be configured to use only Redis for storage, without MongoDB:

1. For Docker Compose:
   ```bash
   cd docker
   # Edit the docker-compose.yml file to remove the MongoDB service
   # And update the environment variables for the web service:
   # - Remove MONGO_URI
   # - Add REDIS_HOST=redis

   docker-compose up --build
   ```

2. For Kubernetes:
   ```bash
   # Edit kubernetes/config/url-shortener-config.yaml
   # In the Secret section, remove the MONGO_URI and ensure REDIS_HOST is set:
   #
   # stringData:
   #   REDIS_HOST: "redis"
   #   # Remove or comment out MONGO_URI
   
   # Apply only the Redis-related manifests
   kubectl apply -f kubernetes/config/url-shortener-config.yaml
   kubectl apply -f kubernetes/deployments/redis-deployment.yaml
   kubectl apply -f kubernetes/deployments/url-shortener-deployment.yaml
   kubectl apply -f kubernetes/scaling/url-shortener-hpa.yaml
   kubectl apply -f kubernetes/networking/url-shortener-ingress.yaml
   ```

### Deploying to Kubernetes

1. Make sure your Kubernetes cluster is running:
   - Docker Desktop: Enable Kubernetes in settings
   - minikube: `minikube start`

2. Build and push the Docker image (if not using an existing image):
   ```bash
   cd docker
   docker build -t your-dockerhub-username/url-shortener:v1 -f Dockerfile ..
   docker push your-dockerhub-username/url-shortener:v1
   ```

3. Update the image name in `kubernetes/deployments/url-shortener-deployment.yaml` to use your Docker Hub username:
   ```yaml
   # Change this line in url-shortener-deployment.yaml
   image: your-dockerhub-username/url-shortener:v1
   ```

4. Apply Kubernetes configurations:
   ```bash
   cd ..
   # Apply MongoDB PVC
   kubectl apply -f kubernetes/storage/mongodb-pvc.yaml

   # Apply MongoDB deployment
   kubectl apply -f kubernetes/deployments/mongodb-deployment.yaml

   # Apply updated ConfigMap and Secret
   kubectl apply -f kubernetes/config/url-shortener-config.yaml

   # Deploy Redis
   kubectl apply -f kubernetes/deployments/redis-deployment.yaml

   # Deploy URL shortener
   kubectl apply -f kubernetes/deployments/url-shortener-deployment.yaml

   # Apply HPA for auto-scaling
   kubectl apply -f kubernetes/scaling/url-shortener-hpa.yaml

   # Apply Ingress (if needed)
   kubectl apply -f kubernetes/networking/url-shortener-ingress.yaml
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

### Checking the Database

#### MongoDB

1. Open mongosh:
   - Docker: `docker exec -it $(docker ps -q -f name=mongodb) mongosh`
   - Kubernetes: `kubectl exec -it $(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}') -- mongosh`

2. Run
   ```bash
   use url_shortener
   db.urls.find().pretty()
   ```

#### Redis

1. Access the Redis CLI:
   - Docker: `docker exec -it $(docker ps -q -f name=redis) redis-cli`
   - Kubernetes: `kubectl exec -it $(kubectl get pods -l app=redis -o jsonpath='{.items[0].metadata.name}') -- redis-cli`

2. List all keys:
   ```bash
   KEYS *
   ```

3. Get a specific URL by its short code:
   ```bash
   GET <short_code>
   ```

4. Count the number of URLs stored:
   ```bash
   DBSIZE
   ```

5. Monitor Redis operations in real-time:
   ```bash
   MONITOR
   ```

### Stopping the application

1. If using docker:
   ```bash
    cd docker
    docker-compose down -v
   ```

2. If using kubernetes:
   ```bash
   kubectl delete -f kubernetes/networking/url-shortener-ingress.yaml \
                  -f kubernetes/scaling/url-shortener-hpa.yaml \
                  -f kubernetes/deployments/url-shortener-deployment.yaml \
                  -f kubernetes/deployments/redis-deployment.yaml \
                  -f kubernetes/deployments/mongodb-deployment.yaml \
                  -f kubernetes/storage/mongodb-pvc.yaml \
                  -f kubernetes/config/url-shortener-config.yaml
   ```

## Running Stress Tests

### Using Bash (Unix/Linux/Mac)

```bash
cd tests
chmod +x stress-test.sh
./stress-test.sh
```

### Using PowerShell (Windows/Mac with PowerShell installed)

```powershell
cd tests
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
- MongoDB - Document database
- Docker - Containerization
- Gunicorn - WSGI HTTP Server
- Kubernetes - Orchestration

## Continuous Integration/Continuous Deployment

For setting up automated builds and deployments using GitHub Actions, see the [GitHub Actions Setup Guide](GITHUB_ACTIONS_SETUP.md).
