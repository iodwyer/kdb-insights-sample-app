import asyncio
import websockets
import json
import random
import time

connected_clients = set()

async def handler(websocket, path):
    print(f"🟢 New connection from {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📨 Received: {message}")
            try:
                data = json.loads(message)
                if data.get("type") == "subscribe":
                    topic = data.get("payload", {}).get("topic", "default")
                    print(f"🔔 Subscribed to topic: {topic}")
                    # Start sending data every second
                    while True:
                        if websocket.closed:
                            break
                        payload = {
                            "value": round(random.uniform(20, 40), 2),
                            "topic": topic,
                            "timestamp": time.time()
                        }
                        await websocket.send(json.dumps(payload))
                        await asyncio.sleep(1)
                else:
                    print("⚠️ Unknown message type")
            except json.JSONDecodeError:
                print("❌ Invalid JSON received")
    except websockets.exceptions.ConnectionClosed:
        print(f"🔴 Connection closed: {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(handler, "localhost", 8090)

print("🚀 Starting WebSocket server on ws://localhost:8090/ws/v1/subscribe/websockets-example")

# Start server loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
