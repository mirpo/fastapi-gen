import os

# Point tests at a throwaway database instead of the dev app.db.
# Must happen before advanced.main is imported: the engine is created at import time.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
