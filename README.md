# ollama-ai-video-transcribe
Using Ollama to convert the audio from a video into a transcript

# Quick Notes About Transcribing Audio Files
- Please note that Open WebUI can already transcribe an audio file for you. Just upload the audio file with a chat model and ask for some good formatting.
- There is a script here in this repository to convert a video to an audio file but I usually download my audio using an android application that lets me choose video or audio, what format, and what size. FFMPEG is still needed but, if using the video-to-audio.py you will need to install moviepy.
- One can also use ffmpeg -i input.mp4 -vn -c:a copy output.m4a

### Note: For this application, ffmpeg and pytorch are required.

## Running on Windows using PowerShell with Administrative permissions
  Install ffmpeg from ffmpeg.org
  ```bash
  pip3 install py
  ```
  What python versions are installed?
  ```bash
    py -0p
  ```
  Create the virtual environment. The name of the virtual environment directory here is venv and python3 is used
  ```bash
    python3 -m venv venv
    .\venv\Scripts\Activate.ps1
  ```
  Verify pytorch is installed
  ```bash
    python3 .\torch_check.py
  ```
  If that failed, try installing pytorch
  ```bash
    py -3.12 .\venv\Scripts\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```
  Install the dependencies
  ```bash
    py -3.12 .\venv\Scripts\pip install -r requirements.txt
  ```
  To run the transcription powershell script (in an admin powershell terminal):
  ```bash
    .\transcribe.ps1 .\sample\test.m4a'
  ```
  When done, deactivate the virtual environment
  ```bash
    deactivate
  ```
  To remove the virtual environment when you want to
  ```bash
    .\venv\Scripts\pip uninstall -f requirements.txt
    deactivate
    rmdir /s /q .\venv
  ```

## Running on Linux
  If you need to install python...
    Get things up to date of course
  ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip python3-venv -y
  ```
  If you need to install ffmpeg...
  ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install ffmpeg
  ```
  What versions of python are installed?
  ```bash
    ls -ls /usr/bin/python*
  ```
    Note: Do not uninstall the default python installed with the operating system or things break
  Is pytorch installed?
  ```bash
    chmod +x ./torch_check.py
    ./torch_check.py
  ```
    If that failed, try installing pytorch
  ```bash
    pip3 install torch torchvision torchaudio
  ```
  Create an environment for this application
  ```bash
    python3 -m venv venv
  ```
  Activate the environment
  ```bash
    source ./venv/bin/activate
  ```
  Install the requirements
  ```bash
    pip3 install -r requirements.txt
  ```
  To run the transcription bash script:
  ```bash
    chmod +x ./transcribe.sh
    .\transcribe.sh ./sample/test.m4a
  ```
  When done, deactivate the virtual environment
  ```bash
    deactivate
  ```
  To remove the virtual environment when you want to
  ```bash
    pip3 uninstall -f requirements.txt
    deactivate
    rm -rf ./venv
  ```

## Converting Video To Audio
There is a python script to convert an mp4 video file into an m4a audio file:
- Install MoviePy
  ```bash
  pip3 install moviepy
  ```
- Make video-to-audio.py executable
  ```bash
    chmod +x ./video-to-audio.py
  ```
- Run video-to-audio.py
   ```bash
   ./video-to-audio.py ./sample/MyTest.mp4 ./test.m4a
   ```
