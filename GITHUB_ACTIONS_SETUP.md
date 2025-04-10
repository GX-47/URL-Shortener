# GitHub Actions Setup

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
