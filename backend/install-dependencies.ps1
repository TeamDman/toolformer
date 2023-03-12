python -m pip install --upgrade pip
pip install ipykernel
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
pip install websockets SpeechRecognition openai-whisper pipwin pyaudio accelerate transformers sympy fuzzywuzzy screeninfo pip install lovely-tensors datasets selenium==4.8.2

# pip install -r https://github.com/coqui-ai/TTS/raw/dev/requirements.txt
# pip install TTS
pip install git+https://github.com/coqui-ai/TTS
pip install pyinstaller
pip install numba==0.56.4
pip install numpy==1.23.5

# follow selenium install instructions
# https://github.com/SeleniumHQ/selenium
# https://www.selenium.dev/selenium/docs/api/py/
## Write-Host "run 'choco install bazelisk' from an admin prompt :P"