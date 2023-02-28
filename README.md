# Toolformer

![demo](./demo.mp4)

Using toolformer prompting to create a copilot for your operating system.

Currently only supports moving windows around.
Example: 

```
User: 
move notepad, main monitor, top right
Assistant: Okay, moving spotify... [SNAP(notepad, main monitor top right) ->moved notepad to  main monitor top right] done!
```

Runs locally using [pythia-2.8B-deduped](https://huggingface.co/EleutherAI/pythia-2.8b-deduped). This would work a lot better if I just used the ChatGPT api, but I have a nice graphics card for testing, and I think it's important that we try and develop these tools to run locally instead of only relying on third party inference.

[Original paper](https://arxiv.org/abs/2302.04761)

Check out [main.ipynb](main.ipynb) for a demo.
Windows only for now.


Credit to [minosvasilias](https://github.com/minosvasilias/toolformer-zero) for their prompt