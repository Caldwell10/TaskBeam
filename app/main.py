import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def read_root() -> dict:
    return {"message": "Welcome to Taskbeam"}

# run app via uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)



