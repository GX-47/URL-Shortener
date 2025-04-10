# PowerShell stress test script for URL shortener
$url = "http://url-shortener.local/shorten"
$payload = Get-Content -Path ".payload.json" -Raw
$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "Starting stress test - Press Ctrl+C to stop"

# Run 100 requests in parallel using jobs
1..100 | ForEach-Object -Parallel {
    try {
        Invoke-WebRequest -Uri $using:url -Method Post -Body $using:payload -Headers $using:headers
        Write-Host "Request $_ completed"
    } catch {
        Write-Host "Request $_ failed: $($_.Exception.Message)"
    }
} -ThrottleLimit 20

Write-Host "Stress test completed"