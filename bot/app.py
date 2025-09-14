from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from notion_api import router as notion_api_router
from slack_api import router as slack_api_router

app = FastAPI(title="Bot", description="A FastAPI server for webhook events")
app.include_router(notion_api_router)
app.include_router(slack_api_router)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Bot is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
