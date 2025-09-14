import uvicorn
from app import app

def main():
    print("Starting Slack Bot server...")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

if __name__ == "__main__":
    main()
