# from typing import *
from transformers import GPTNeoXForCausalLM, AutoTokenizer
# from accelerate import init_empty_weights
import torch

model: GPTNeoXForCausalLM | None = None
tokenizer: AutoTokenizer | None = None

async def preheat(model_repo: str, model_name: str, model_revision: str) -> None:
    global model
    global tokenizer
    print("Loading model and tokenizer...")

    model = GPTNeoXForCausalLM.from_pretrained(
        f"{model_repo}/{model_name}",
        revision=model_revision,
        cache_dir=f"../{model_name}/{model_revision}",
        device_map="auto",
        torch_dtype=torch.float16
    )
    print("Model loaded!")

    tokenizer = AutoTokenizer.from_pretrained(
        f"{model_repo}/{model_name}",
        revision=model_revision,
        cache_dir=f"../{model_name}/{model_revision}",
        device_map="auto",
        torch_dtype=torch.float16
    )
    print("Tokenizer loaded!")

    print("Adding special tokens...")
    num_added_tokens = tokenizer.add_tokens(
        ["[", "]", "->"], special_tokens=True)
    model.resize_token_embeddings(len(tokenizer))
    print(f"Added {num_added_tokens} special tokens!")


def predict(prompt: str, eos: str) -> str:
    assert model is not None
    assert tokenizer is not None
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        # do_sample=True,
        temperature=0.9,
        max_new_tokens=100,
        eos_token_id=tokenizer.encode(eos)[0],
        pad_token_id=tokenizer.encode(eos)[0],
    )
    response = tokenizer.decode(outputs[:, inputs["input_ids"].shape[1]:][0])
    return response
