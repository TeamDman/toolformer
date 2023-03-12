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
import tools
from client_types import Message
from typing import *
import constants
from state import State, Mode

async def respond_and_distribute(
    state: State,
    message: Message,
):
    try:
        print(f"[RESPOND AND DISTRIBUTE] Received message from client: {message.content}")

        # send user's message to all clients
        state.message_history.append(message)
        payload = json.dumps({"event": "message", "message": asdict(message)})
        websockets.broadcast(state.connected_clients, payload)

        # send assistant's response to all clients

        chat_so_far = ""
        chat_so_far += f"User: {message.content}\n"
        # print(f"[RESPOND AND DISTRIBUTE] Sending prompt to text model: {chat_so_far}")
        response, info = await tools.predict_with_tools(state, chat_so_far, state.predict)
        wasted = len(info["bad"]) if "bad" in info else 0
        # print(f"[RESPOND AND DISTRIBUTE] Got response from text model: \"{response}\" (wasted {wasted})")
        chat_so_far += f"Assistant: {response}\n"

        message = Message(
            side="left",
            content=response,
            timestamp=time.time_ns(),
            senderName="Assistant"
        )
        state.message_history.append(message)
        payload = json.dumps({"event": "message", "message": asdict(message)})
        websockets.broadcast(state.connected_clients, payload)
    except Exception as e:
        print(f"[RESPOND AND DISTRIBUTE] Error: {e}")
        traceback.print_exc()
        return "Error: " + str(e)


async def connect_client(
    state: State,
    websocket: websockets.server.WebSocketServerProtocol,
):
    try:
        async for message in websocket:
            print(f"[CLIENT HANDLER] Received message from client: {message}")
            try:
                received = json.loads(message)
                if received["event"] == "message":
                    message = Message(**received["message"])
                    await respond_and_distribute(state, message)

            except Exception as e:
                print(f"[CLIENT HANDLER] Error handling message: {e}")
                traceback.print_exc()
    except Exception as e:
        print(f"[CLIENT HANDLER] Error: {e}")
        traceback.print_exc()

async def connect_voice(state: State):
    try:
        activation_keywords = ["computer", "pewter", "pewder", "cuter", "puter"]
        while True:
            prompt = await state.voice_queue.get()
            print(f"[VOICE HANDLER] heard '{prompt}'")
            activated = False
            if state.mode == Mode.ALWAYS_ON:
                activated = True
            elif state.mode == Mode.ACTIVATION_KEYWORD:
                for keyword in activation_keywords:
                    if prompt.lower().startswith(keyword):
                        activated = True
                        prompt = prompt[len(keyword):].strip().lstrip(",").lstrip(".").strip()
                        break
                if not activated:
                    print(f"[VOICE HANDLER] not activated")
            if activated and len(prompt) > 0:
                print(f"[VOICE HANDLER] activated with '{prompt}'")
                message = Message(
                    side="right",
                    content=prompt,
                    timestamp=time.time_ns(),
                    senderName="User (voice)"
                )
                await respond_and_distribute(state, message)

    except Exception as e:
        print(f"[VOICE HANDLER] Error: {e}")
        traceback.print_exc()

async def connect_predictions(state: State):
    try:
        uri = f"ws://localhost:{constants.text_websocket_port}"
        print(f"[PREDICTION HANDLER] Connecting to text model at: {uri}")
        async with websockets.client.connect(uri) as ws:
            print("[PREDICTION HANDLER] Connected")
            while not state.stop_future.done():
                prompt, stop_token = await state.predict_queue.get()
                # print(f"[PREDICTION HANDLER] Sending prompt to text model: {prompt}")
                await ws.send(json.dumps({"prompt": prompt, "stop_token": stop_token}))
                response = await ws.recv()
                # print(f"[PREDICTION HANDLER] Got response from text model: {response}")
                state.predict_reply_queue.put_nowait(response)
        print("[PREDICTION HANDLER] Disconnected from text model")
    except Exception as e:
        print(f"[PREDICTION HANDLER] Error: {e}")
        traceback.print_exc()


async def main():
    state = State(
        message_history=[
            Message(
                side= "left",
                content= "Suh dude",
                timestamp= "2023-03-06T04:11:00.902Z",
                senderName= "Assistant",
            ),
        ],
    )
    state.voice_queue=await mic.start_background(state.stop_future)
    asyncio.create_task(connect_predictions(state))
    asyncio.create_task(connect_voice(state))

    async def handleWebSocket(websocket: websockets.server.WebSocketServerProtocol):
        try:
            print("[SERVE HANDLER] Client connected")
            nonlocal state
            state.connected_clients.add(websocket)
            await websocket.send(json.dumps({
                "event": "history",
                "history": [asdict(msg) for msg in state.message_history]
            }))
            await connect_client(state, websocket)
        finally:
            state.connected_clients.remove(websocket)
            print("[SERVE HANDLER] Client disconnected")

    print("[MAIN] Starting server")
    async with websockets.server.serve(handleWebSocket, "localhost", 8765):
        await state.stop_future 

if __name__ == '__main__':
    asyncio.run(main())
