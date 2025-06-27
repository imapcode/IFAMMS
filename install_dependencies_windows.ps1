# # Activate virtual environment if exists
# $activateScriptPath = ".\Scripts\activate.ps1"
# if (Test-Path -Path $activateScriptPath) {
#     Write-Host "Activating virtual environment..."
#     Invoke-Expression -Command ". $activateScriptPath"
# }
# else {
#     Write-Host "Virtual environment not found. Creating a new one..."
#     python -m venv .venv
#     Invoke-Expression -Command ". $activateScriptPath"
# }


# Check if Python 3 is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python 3 is not installed. Installing..."
    Invoke-WebRequest "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe" -OutFile "$env:TEMP\python3installer.exe" -UseBasicParsing
    Start-Process -Wait -FilePath "$env:TEMP\python3installer.exe" -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1"
    Remove-Item -Path "$env:TEMP\python3installer.exe"
    Write-Host "Python 3 installed successfully."
}

# Check if pip is installed
if (!(Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "pip is not installed. Installing..."
    Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "$env:TEMP\get-pip.py" -UseBasicParsing
    Start-Process -Wait -FilePath "python" -ArgumentList "$env:TEMP\get-pip.py"
    Remove-Item -Path "$env:TEMP\get-pip.py"
    Write-Host "pip installed successfully."
}

# Install packages from requirements.txt
$requirementsFile = "requirements.txt"
if (Test-Path -Path $requirementsFile) {
    Write-Host "Installing packages from requirements.txt..."
    pip3 install -r $requirementsFile
    Write-Host "Packages installed successfully."
}
else {
    Write-Host "requirements.txt file not found."
}

# Install and execute pipwin commands
Write-Host "Installing pipwin..."
pip3 install pipwin

Write-Host "Installing cairocffi with pipwin..."
pipwin install cairocffi

