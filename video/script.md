You probably know by now that large language models aren't always telling the truth.
That's where Toolformer comes in.
A technique to enable the AI to get more context, to craft better responses.

You create a markup language that the AI can easily mimic.
The AI works by generating one token at a time, growing the prompt with each token predicted.
You can show the AI the syntax for invoking the tools. Then you simply stop generating tokens once you encounter the little arrow token. At this point, you look back and check which tool the AI tried to invoke, and you get the answer for it. These tools can be anything. Searching the web, evaluating a math expression, modifying its own state, moving files on your computer.
The limit is how smart your language model is.
Is it smart enough to understand an HTML page? Can you give it access to a web browser? Can it log into your bank for you, check your balance? Cross reference your transaction history with your paystubs?

I made this slide so I could make the AI say "y'all'd've'he'hee'hoo".

The special syntax is also easy to hide in your presentation layer, but keeping the ability to peek at what the model is doing would be nice.

---

Of course, I can't use the AI voice for this whole video.
It's a freaking project about voice recognition.
The AI voice is just a way to reduce the effort of presenting this material.
Something that doesn't make mistakes in pronunciation.
I still choose the words.
I just don't care to sit here and read them out loud until I'm satisfied.
I hope you don't mind.
My main disappointment will be having used an online tool instead of running one locally.
I'm not sure if I can get the same quality of results with a local model at this stage though.