import os
import sys
import asyncio

# On Windows, psycopg3 requires SelectorEventLoop for async operations.
# This must be set BEFORE uvicorn starts the event loop.
if sys.platform == 'win32':
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import uvicorn

def main():
    from dmesh.api.main import app
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting DMesh API on {host}:{port}...")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
