import json
import constants
import asyncio
import websockets.client
import lifecycle

async def main():
    try:
        stop_future = lifecycle.create_lifecycle()
        async with websockets.client.connect(f"ws://localhost:{constants.text_websocket_port}") as ws:
            while not stop_future.done():
                prompt = input("Prompt: ")
                await ws.send(json.dumps({"prompt": prompt, "stop_token": "\n"}))
                response = await ws.recv()
                print(f"Response: {response}")
    except websockets.client.ConnectionClosedError:
        print("Connection closed")

if __name__ == "__main__":
    asyncio.run(main())