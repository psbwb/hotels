import uvicorn
import sys
from pathlib import Path
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))
from src.api.hotels import router as router_hotels

app = FastAPI()
app.include_router(router_hotels)


@app.get("/")
def func():
    return "I WANNA BUY THIS GOD DAMN RACING CAR"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
