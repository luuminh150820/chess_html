from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any

app = FastAPI()

# Cho phép trình duyệt truy cập từ mọi nguồn (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lưu trữ trạng thái bàn cờ trong bộ nhớ (RAM)
class GameState(BaseModel):
    boardState: List[Any]
    capturedPieces: Any
    turn: str
    history: List[Any]
    historyLogs: List[str]
    status: str
    lastMove: Optional[Any] = None
    isCapture: bool = False
    checkPos: Optional[Any] = None
    isMate: bool = False
    version: int = 0 # Dùng để nhận biết có nước đi mới

# Khởi tạo bàn cờ mặc định
current_game = {
    "boardState": [], # Sẽ được client gửi lên lần đầu
    "version": 0
}

@app.get("/get_game")
async def get_game():
    return current_game

@app.post("/update_game")
async def update_game(state: GameState):
    global current_game
    current_game = state.dict()
    current_game["version"] += 1
    return {"status": "ok", "version": current_game["version"]}

if __name__ == "__main__":
    import uvicorn
    import socket
    
    # Tự động lấy IP máy bạn để bạn của bạn kết nối
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"--- SERVER CỜ VUA ĐANG CHẠY ---")
    print(f"Gửi địa chỉ này cho bạn của bạn: http://{local_ip}:5000")
    print(f"-------------------------------")
    
    uvicorn.run(app, host="0.0.0.0", port=5000)