import asyncio
import websockets
import json

async def subscribe():
    uri = "ws://localhost:8090"  # Change to your WebSocket server
    uri = "ws://localhost:8090/ws/v1/subscribe/websockets-example"
    async with websockets.connect(uri) as websocket:
        # Send a subscription message
        subscribe_message = {
            "type": "subscribe",
            "id": 2122,
            "payload": {
                "topic": "data"
            }
        }

        print(f"🔌 Connected to {uri}")
        print("📤 Sending subscribe message...")
        await websocket.send(json.dumps(subscribe_message))

        # Print incoming messages
        print("📥 Waiting for messages...")
        async for message in websocket:
            print(f"➡️ Received: {message}")

asyncio.run(subscribe())
