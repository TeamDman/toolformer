import json
import constants
import asyncio
import websockets.client
import lifecycle

async def main():
    stop_future = lifecycle.create_lifecycle()
    while not stop_future.done():
        try:
            prompt = input("Prompt: ")
            async with websockets.client.connect(f"ws://localhost:{constants.text_websocket_port}") as ws:
                await ws.send(prompt)
                response = await ws.recv()
                print(f"Response: {response}")
        except Exception as e:
            print(f"Error connecting to websocket: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
