from fastapi import WebSocket


class ConnectionManager:
    """
    WebSocket connection manager for real-time features
    TODO: Extend with:
    - Room-based connections (user groups, channels)
    - Message persistence
    - Connection authentication
    - Scaling across multiple servers with Redis pub/sub
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                dead_connections.append(connection)
        for connection in dead_connections:
            self.active_connections.remove(connection)


manager = ConnectionManager()
