import lifecycle
import json
import traceback
import signal
import constants
from transformers import GPTNeoXForCausalLM, AutoTokenizer
import torch
import asyncio
import websockets.server

async def main():
    assert torch.cuda.is_available()

    model_repo, model_name, model_revision = "EleutherAI", "pythia-6.9B-deduped", "step143000"
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

    stop_future = lifecycle.create_lifecycle()
    async def serve(websocket: websockets.server.WebSocketServerProtocol):
        nonlocal model
        nonlocal tokenizer
        async for message in websocket:
            print(f"[MAIN] Received {message}")
            try:
                received = json.loads(message)
                prompt = received["prompt"]
                stop_token = received["stop_token"]
                
                inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
                outputs = model.generate(
                    **inputs,
                    # do_sample=True,
                    temperature=0.9,
                    max_new_tokens=100,
                    eos_token_id=tokenizer.encode(stop_token)[0],
                    pad_token_id=tokenizer.encode(stop_token)[0],
                )
                # print(f"[MAIN] Generated {outputs}")
                response = tokenizer.decode(outputs[:, inputs["input_ids"].shape[1]:][0])
                print(f"[MAIN] Sending {response}")
                await websocket.send(response)
            except Exception as e:
                print(f"[MAIN] Error handling message: {e}")
                traceback.print_exc()
    async with websockets.server.serve(serve, "localhost", constants.text_websocket_port):
        await stop_future
if __name__ == "__main__":
    asyncio.run(main())