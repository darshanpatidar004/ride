import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.websocket.connection_manager import manager
from app.api import deps
from app.models.driver import Driver
from app.models.user import User

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # In a real app, you would validate the token sent during handshake 
    # or as the first message.
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # Example Payload from Driver: 
            # {"type": "location_update", "lat": 12.9716, "lng": 77.5946, "booking_id": 1, "customer_id": 2}
            
            event_type = payload.get("type")
            
            if event_type == "location_update":
                customer_id = payload.get("customer_id")
                
                # In production, here we would:
                # 1. Update the driver's current location in DB or Redis
                # 2. Calculate new ETA
                # 3. Forward the update to the customer
                
                if customer_id:
                    update_msg = {
                        "type": "driver_location",
                        "lat": payload.get("lat"),
                        "lng": payload.get("lng"),
                        "eta": "5 mins" # Dummy ETA logic
                    }
                    await manager.send_personal_message(update_msg, customer_id)
                    
            elif event_type == "ping":
                await manager.send_personal_message({"type": "pong"}, user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
