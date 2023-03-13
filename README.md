# Toolformer

https://user-images.githubusercontent.com/9356891/221771638-95936503-db50-4b50-9cc8-bef088cb9d72.mp4

![[I made a longer video too](https://youtu.be/DmiczzgEfMw)](https://img.youtube.com/vi/DmiczzgEfMw/maxresdefault.jpg)

Using toolformer prompting to create a copilot for your operating system.

Currently only supports moving windows around.
Example: 

```
User: 
move notepad, main monitor, top right
Assistant: Okay, moving spotify... [SNAP(notepad, main monitor top right) ->moved notepad to  main monitor top right] done!
```

Runs locally using [pythia-2.8B-deduped](https://huggingface.co/EleutherAI/pythia-2.8b-deduped). This would work a lot better if I just used the ChatGPT api, but I have a nice graphics card for testing, and I think it's important that we try and develop these tools to run locally instead of only relying on third party inference.

Because the local models are less smart, I do some dumb things to make it work.  
I tried using the language model to pick the process name that best matched the user input, but it wasn't very good at it. Better prompts would probably help, but I just used a fuzzy string matcher instead.
Same with converting from natural language to window coordinates.

The important thing is that it shows the agent invoking the tool, and that the parameters for the tool are passed as natural language.

[Original paper](https://arxiv.org/abs/2302.04761)

Check out [main.ipynb](main.ipynb) for a demo.
Windows only for now.


Credit to [minosvasilias](https://github.com/minosvasilias/toolformer-zero) for their prompt

Credit to [tatellos](https://github.com/mallorbc/whisper_mic) for their whisper mic stuff

Credit to [coqui-ai](https://github.com/coqui-ai/TTS) for their TTS stuff

## Notes to self

checkout langchain