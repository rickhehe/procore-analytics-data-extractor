# Define paths for virtual environment and requirements file
$venv_path = "./.venv"
$requirements = "./requirements.txt"

# Check if the virtual environment exists; if not, create it
if (!(Test-Path $venv_path)) {
    python -m venv $venv_path
}

# Activate the virtual environment
$activate_script = Join-Path $venv_path "Scripts/Activate.ps1"
& $activate_script

# Install dependencies if requirements.txt exists
if (Test-Path $requirements) {
    python -m pip install --upgrade pip  #| Out-Null
    python -m pip install -r $requirements  #| Out-Null
} else {
    Write-Host "requirements.txt not found. Skipping dependency installation." -ForegroundColor Yellow
}

#pprint "lint with flake8" i
#python -m flake8 src/app.py

#pprint "Lint with pylint" i
#python -m pylint src.app

# Run the Python module
python -m src.app

# Deactivate the virtual environment (if needed in PowerShell, you can just exit the session)
deactivate
