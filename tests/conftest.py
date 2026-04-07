import asyncio
import sys
import os

# This must be done at the module level to ensure it happens before any event loop is created
if sys.platform == 'win32':
    # On Windows, psycopg3 (and some other libs) require the SelectorEventLoop
    # instead of the default ProactorEventLoop to run async operations correctly.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Also disable Ryuk on Windows by default as it often fails with port mapping errors
    if "TESTCONTAINERS_RYUK_DISABLED" not in os.environ:
        os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"
