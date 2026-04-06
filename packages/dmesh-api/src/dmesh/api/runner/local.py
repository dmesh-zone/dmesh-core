import uvicorn
from dmesh.api.main import app

def main():
    """Run the API locally using uvicorn."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
