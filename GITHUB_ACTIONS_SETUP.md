# GitHub Actions Setup

## Prerequisites
- Docker installed on your system
- GitHub account
- Personal Access Token (PAT) with proper permissions

## Configure GitHub Container Registry Access

Make sure your Kubernetes cluster has access to pull images from GitHub Container Registry:

1. Create a Personal Access Token (PAT) in GitHub with `read:packages` permission
2. Create a Kubernetes secret for Docker registry authentication:

```bash
kubectl create secret docker-registry github-container-registry \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_PAT_TOKEN \
  --docker-email=YOUR_GITHUB_EMAIL
```

3. Update your deployment to use this secret by adding this section under spec.template.spec:

```yaml
imagePullSecrets:
- name: github-container-registry
```

## Pull and Run the Image

Open your terminal and run:

```bash
echo YOUR_PAT_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

Replace:
- `YOUR_PAT_TOKEN` with the token you created
- `YOUR_GITHUB_USERNAME` with your GitHub username

## Step 3: Pull the Docker Image

```bash
docker pull ghcr.io/gx-47/url-shortener:sha-a53c646
```

## Step 4: Run the Container

```bash
docker run -d -p 8080:8080 --name url-shortener ghcr.io/gx-47/url-shortener:sha-a53c646
```
