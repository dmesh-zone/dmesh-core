import sys
import os

# Add src to sys.path to ensure we test the local source, not the installed package
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)
