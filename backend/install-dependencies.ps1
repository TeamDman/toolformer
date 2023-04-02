python -m pip install --upgrade pip
pip install ipykernel
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
pip install websockets SpeechRecognition openai-whisper pipwin pyaudio accelerate sympy fuzzywuzzy screeninfo pip install lovely-tensors datasets selenium==4.8.2

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

# pip uninstall transformers
# https://github.com/oobabooga/text-generation-webui/issues/223
# pip install git+https://github.com/zphang/transformers@llama_push
#  https://colab.research.google.com/drive/1eWAmesrW99p7e1nah5bipn0zikMb8XYC#scrollTo=X_pz8MuY84Qh


pip install bitsandbytes
# needs patching
# https://github.com/oobabooga/text-generation-webui/issues/20#issuecomment-1411650652


pip install -q pip install -q datasets loralib sentencepiece
pip install -q git+https://github.com/zphang/transformers@c3dc391
pip install -q git+https://github.com/huggingface/peft.git


# https://github.com/ggerganov/llama.cpp
# for converting pths to other format
pip install sentencepiece

pip install pyautogui mss pytesseract
pip install opencv-python