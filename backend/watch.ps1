try
{
    # $env:PATH = ".\venv\Scripts;$env:PATH" # Update path to your virtual environment
    # $env:PYTHONPATH = ".\venv\Lib\site-packages;$env:PYTHONPATH" # Update path to your virtual environment
    # Activate.ps1 # Activate the virtual environment
    Push-Location src
    watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM ..\venv\Scripts\python.exe main.py
}
finally
{
    Pop-Location
}