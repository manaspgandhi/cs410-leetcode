param (
    [string]$commitMessage
)

if (-not $commitMessage) {
    Write-Host "Error: Commit message is required."
    Write-Host "Usage: ./git_script.ps1 'your commit message'"
    exit 1
}

# Execute Git commands
git add -A
git commit -m $commitMessage
git push