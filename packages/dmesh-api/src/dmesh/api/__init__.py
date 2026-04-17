import sys
import asyncio

# On Windows, psycopg3 REQUIRES SelectorEventLoop for async operations.
# ProactorEventLoop (the default since Python 3.8) is NOT supported.
if sys.platform == 'win32':
    try:
        # We try to set the policy as early as possible.
        # This will affect any new event loops created.
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        print("DEBUG: Set WindowsSelectorEventLoopPolicy for Psycopg compatibility.")
    except Exception as e:
        # If we can't set it, we at least log it.
        print(f"WARNING: Could not set WindowsSelectorEventLoopPolicy: {e}")
