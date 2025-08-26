Param(
    [parameter(mandatory=$true)][string]$file
)

$ep = Get-ExecutionPolicy
if (!($ep -eq "RemoteSigned")) {
    Write-host "Execution Policy does not allow this script to run properly"
    Write-host "If you have the proper permissions, please close powershell"
    Write-host "Then right click the powershell icon and run as administrator"
    Write-host "Once in the powershell environment, execute the following:"
    Write-host "Set-ExecutionPolicy RemoteSigned -Force"
    exit 1
}

$VenvDir = "venv"
$PythonScript = "main.py"

if (!(Test-Path $VenvDir -PathType Container)) {
    Write-Host "Virtual environment not found."
    Write-Host  "Please create it using 'python -m venv venv'"
    Write-Host  "Install dependencies using 'venv\Scripts\pip install -r requirements.txt"
    exit 1
}

& "$PSScriptRoot\$VenvDir\Scripts\Activate.ps1"

$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL_NAME = "llama3.2:latest"
$env:OLLAMA_TIMEOUT_SECONDS = "1800"

py -3.12 $PythonScript $file

deactivate