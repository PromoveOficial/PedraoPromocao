import os
from dotenv import load_dotenv

load_dotenv()

DM = os.getenv("DEBUG_MODE")
print(f"DEBUG_MODE: {DM}")