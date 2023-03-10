[CmdletBinding()]
param(
    [switch]$watch=$false
)

try
{
    Push-Location src
    if ($watch) 
    {
        watchmedo auto-restart `
            --pattern "*.py" `
            --recursive `
            --signal SIGTERM ..\venv\Scripts\python.exe main.py
    }
    else
    {
        python main_text.py
    }
}
finally
{
    Pop-Location
}
