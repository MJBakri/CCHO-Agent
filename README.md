# CCHO-Agent API Documentation

## Starting the Server

In order to start the server, activate your virtual environment and make sure to install the dependencies by executing the command `pip install -r .\requirements.txt` then CD to src\app and run command: `uvicorn main:app`.

## Architecture Overview

The application is a FastAPI-based web service that implements WebSocket communication for real-time interactions with an LLM (Language Learning Model) service using Groq.

### Core Components

1. **Main Application** (main.py)

   - Initializes the FastAPI application
   - Configures middleware
   - Sets up WebSocket handlers
   - Mounts API routes

2. **WebSocket Implementation** (websockets.py)

   - Manages real-time bidirectional communication
   - Handles client connections and disconnections
   - Processes messages through an LLM Provider

3. **Middleware** (middleware.py)

   - CORS (Cross-Origin Resource Sharing) configuration
   - Trusted Host validation

## Flow of Operation

### 1. Application Startup

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
```

- Initializes FastAPI with project configuration
- Sets up API documentation endpoints

### 2. WebSocket Connection Flow

1. **Client Connection**

   ```python
   @app.websocket("/ws/{client_id}")
   async def websocket_endpoint(websocket: WebSocket, client_id: str)
   ```

   - Accepts connections at `/ws/{client_id}`
   - Maintains active connections in `WebSocketManager`

2. **Message Processing**

   ```python
   async def broadcast(self, payload: dict, client_id: str):
       # Creates LLM client
       llm_client = LLMServiceFactory.create_service("groq")

       # Streams responses from Groq
       stream = await llm_client.chat.completions.create(...)
   ```

   - Receives messages from clients
   - Processes through Groq LLM
   - Streams responses back to clients

### 3. Security and Middleware

```python
def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
```

- Implements CORS protection
- Validates trusted hosts
- Handles cross-origin requests

## API Routes

### Health Check

- Endpoint: `GET /api/v1/health`
- Returns API health status and timestamp

## WebSocket Usage

1. Connect to websocket endpoint:

   ```
   ws://your-domain/ws/{client_id}
   ```

2. Send message format:

   ```json
   {
     "message": "Your message here"
   }
   ```

3. Receive streamed responses:

   ```json
   {
     "reply": "LLM response chunk"
   }
   ```

## Error Handling

- WebSocket disconnections are handled gracefully
- Connections are cleaned up when clients disconnect
- Invalid hosts are rejected with 400 status code

The application provides a robust foundation for real-time AI interactions with proper security measures and error handling in place.
