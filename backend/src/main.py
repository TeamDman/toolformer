import lifecycle
import asyncio
import websockets.server
import websockets.client
import websockets
import json
import mic
import traceback
from dataclasses import asdict
import time
import tools.helpers
from client_types import Message
from conversation_history import track_message, get_history
from typing import *
import constants

async def respond_and_distribute(
    message: Message,
    clients: set[websockets.WebSocketServerProtocol],
    predict: Callable[[str, str], str]
):
    try:
        print(f"[RESPOND AND DISTRIBUTE] Received message from client: {message.content}")

        # send user's message to all clients
        await track_message(message)
        payload = json.dumps({"event": "message", "message": asdict(message)})
        websockets.broadcast(clients, payload)

        # send assistant's response to all clients

        chat_so_far = ""
        chat_so_far += f"User: {message.content}\n"
        # print(f"[RESPOND AND DISTRIBUTE] Sending prompt to text model: {chat_so_far}")
        response, info = await tools.helpers.predict_with_tools(chat_so_far, predict)
        wasted = len(info["bad"]) if "bad" in info else 0
        # print(f"[RESPOND AND DISTRIBUTE] Got response from text model: \"{response}\" (wasted {wasted})")
        chat_so_far += f"Assistant: {response}\n"

        message = Message(
            side="left",
            content=response,
            timestamp=time.time_ns(),
            senderName="Assistant"
        )
        await track_message(message)
        payload = json.dumps({"event": "message", "message": asdict(message)})
        websockets.broadcast(clients, payload)
    except Exception as e:
        print(f"[RESPOND AND DISTRIBUTE] Error: {e}")
        traceback.print_exc()
        return "Error: " + str(e)


async def client_handler(
    websocket: websockets.server.WebSocketServerProtocol,
    clients: set[websockets.WebSocketServerProtocol],
    predict: Callable[[str, str], str]
):
    try:
        async for message in websocket:
            print(f"[CLIENT HANDLER] Received message from client: {message}")
            try:
                received = json.loads(message)
                if received["event"] == "message":
                    message = Message(**received["message"])
                    await respond_and_distribute(message, clients, predict)

            except Exception as e:
                print(f"[CLIENT HANDLER] Error handling message: {e}")
                traceback.print_exc()
    except Exception as e:
        print(f"[CLIENT HANDLER] Error: {e}")
        traceback.print_exc()

async def voice_handler(
    voice_queue: asyncio.Queue[str],
    clients: set[websockets.WebSocketServerProtocol],
    predict: Callable[[str, str], str]
):
    try:
        async for prompt in mic.prompt_recognizer(voice_queue):
            print(f"[VOICE HANDLER] Sending message to clients: {prompt}")
            message = Message(
                side="right",
                content=prompt,
                timestamp=time.time_ns(),
                senderName="User (voice)"
            )
            await respond_and_distribute(message, clients, predict)
    except Exception as e:
        print(f"[VOICE HANDLER] Error: {e}")
        traceback.print_exc()

async def prediction_handler(
    predict_queue: asyncio.Queue[Tuple[str,str]],
    predict_reply_queue: asyncio.Queue[str],
    stop_future: asyncio.Future
):
    try:
        uri = f"ws://localhost:{constants.text_websocket_port}"
        print(f"[PREDICTION HANDLER] Connecting to text model at: {uri}")
        async with websockets.client.connect(uri) as ws:
            print("[PREDICTION HANDLER] Connected")
            while not stop_future.done():
                prompt, stop_token = await predict_queue.get()
                # print(f"[PREDICTION HANDLER] Sending prompt to text model: {prompt}")
                await ws.send(json.dumps({"prompt": prompt, "stop_token": stop_token}))
                response = await ws.recv()
                # print(f"[PREDICTION HANDLER] Got response from text model: {response}")
                predict_reply_queue.put_nowait(response)
        print("[PREDICTION HANDLER] Disconnected from text model")
    except Exception as e:
        print(f"[PREDICTION HANDLER] Error: {e}")
        traceback.print_exc()


async def main():
    # asyncio.get_event_loop().set_debug(True)
    stop_future = lifecycle.create_lifecycle()

    predict_queue: asyncio.Queue[Tuple[str,str]] = asyncio.Queue()
    predict_reply_queue: asyncio.Queue[str] = asyncio.Queue()
    async def predict(prompt: str, stop_token: str) -> str:
        nonlocal predict_queue
        nonlocal predict_reply_queue
        # print(f"[PREDICT] Sending prompt to queue: {prompt}")
        await predict_queue.put((prompt, stop_token))
        reply = await predict_reply_queue.get()
        # print(f"[PREDICT] Got reply from queue: {reply}")
        return reply
    predict_task = asyncio.create_task(prediction_handler(predict_queue, predict_reply_queue, stop_future))

    # print("[MAIN] Checking for inference server")
    # result = await predict("Hello", "\n")
    # print(f"[MAIN] got {result}")


    clients = set()

    voice_queue = await mic.start_background(stop_future)
    voice_task = asyncio.create_task(voice_handler(voice_queue, clients, predict))

    async def serve(websocket: websockets.server.WebSocketServerProtocol):
        try:
            print("[SERVE HANDLER] Client connected")
            nonlocal clients
            clients.add(websocket)
            await websocket.send(json.dumps({"event": "history", "history": [asdict(msg) for msg in await get_history()]}))
            nonlocal predict
            await client_handler(websocket, clients, predict)
        finally:
            clients.remove(websocket)
            print("[SERVE HANDLER] Client disconnected")

    print("[MAIN] Starting server")
    async with websockets.server.serve(serve, "localhost", 8765):
        await stop_future
    voice_task.cancel()
    predict_task.cancel()

if __name__ == '__main__':
    asyncio.run(main())
