param (
    [string]$commitMessage
)

if (-not $commitMessage) {
    Write-Host "Commit message is required"
    exit 1
}

# Execute Git commands
git add -A
git commit -m $commitMessage
git push