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
            --pattern "main_text.py;constants.py;lifecycle.py" `
            --recursive `
            --signal SIGTERM ..\venv\Scripts\python.exe main_text.py
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
