import sys
import asyncio
import warnings

# On Windows, psycopg3 REQUIRES SelectorEventLoop for async operations.
# ProactorEventLoop (the default since Python 3.8) is NOT supported.
if sys.platform == 'win32':
    try:
        # We try to set the policy as early as possible.
        # This will affect any new event loops created.
        # We suppress the DeprecationWarning as this is currently required for psycopg3 on Windows.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            policy = asyncio.WindowsSelectorEventLoopPolicy()
            asyncio.set_event_loop_policy(policy)
        # Only print in debug/dev mode if needed, but for now we keep it to verify it runs
        # print("DEBUG: Set WindowsSelectorEventLoopPolicy for Psycopg compatibility.")
    except Exception as e:
        # If we can't set it, we at least log it.
        print(f"WARNING: Could not set WindowsSelectorEventLoopPolicy: {e}")
