import lifecycle
import asyncio
import websockets.server
import json
import mic
import traceback
from dataclasses import asdict
import time
import tools.helpers
from client_types import Message
from conversation_history import track_message, get_history

INFERENCE_ENABLED = False

async def respond_and_distribute(message: Message, clients: set[websockets.WebSocketServerProtocol]):
    print(f"[MAIN] Received message from client: {message.content}")

    # send user's message to all clients
    await track_message(message)
    payload = json.dumps({"event": "message", "message": asdict(message)})
    websockets.broadcast(clients, payload)

    # send assistant's response to all clients
    if INFERENCE_ENABLED:
        chat_so_far = ""
        chat_so_far += f"User: {message.content}\n"
        print(f"[MAIN] Sending prompt to text model: {chat_so_far}")
        response, info = tools.helpers.predict_with_tools(chat_so_far)
        wasted = len(info["bad"]) if "bad" in info else 0
        print(f"[MAIN] Got response from text model: \"{response}\" (wasted {wasted})")
        chat_so_far += f"Assistant: {response}\n"
    else:
        response = "inference is not enabled."
    message = Message(
        side="left",
        content=response,
        timestamp=time.time_ns(),
        senderName="Assistant"
    )
    await track_message(message)
    payload = json.dumps({"event": "message", "message": asdict(message)})
    websockets.broadcast(clients, payload)


async def client_handler(websocket, clients):
    async for message in websocket:
        print(f"[MAIN] Received message from client: {message}")
        try:
            received = json.loads(message)
            if received["event"] == "message":
                message = Message(**received["message"])
                await respond_and_distribute(message, clients)
                
        except Exception as e:
            print(f"[MAIN] Error handling message: {e}")
            traceback.print_exc()

                             
async def voice_handler(voice_queue, clients):
    async for prompt in mic.prompt_recognizer(voice_queue):
        print(f"[MAIN] Sending prompt to clients: {prompt}")
        message = Message(
            side="right",
            content=prompt,
            timestamp=time.time_ns(),
            senderName="User (voice)"
        )
        await respond_and_distribute(message, clients)


async def main():
    voice_queue, stop_event, record_task, transcribe_task = await mic.start_background()
    clients = set()
    try:
        if INFERENCE_ENABLED:
            await text.preheat("EleutherAI", "pythia-6.9B-deduped", "step143000")
    except:
        print("[MAIN] Error loading text model")
        traceback.print_exc()
        raise SystemExit(1)

    send_prompt_task = asyncio.create_task(voice_handler(voice_queue, clients))

    stop = asyncio.get_running_loop().create_future()
    def shutdown():
        stop_event.set()
        record_task.cancel()
        transcribe_task.cancel()
    stop = lifecycle.create_lifecycle(shutdown)

    async def serve(websocket: websockets.server.WebSocketServerProtocol):
        try:
            print("[MAIN] Client connected")
            nonlocal clients
            clients.add(websocket)
            await websocket.send(json.dumps({"event": "history", "history": [asdict(msg) for msg in await get_history()]}))
            await client_handler(websocket, clients)
        finally:
            clients.remove(websocket)
            print("[MAIN] Client disconnected")

    print("[MAIN] Starting server")
    async with websockets.server.serve(serve, "localhost", 8765):
        await stop
    send_prompt_task.cancel()

if __name__ == '__main__':
    asyncio.run(main())
