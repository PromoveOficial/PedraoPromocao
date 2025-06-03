from datetime import datetime
import requests
from pathlib import Path

def log(origin, msg):
    timestamp = datetime.now().strftime('[%d/%m/%Y::%H:%M:%S]')
    
    with open(f'main/logs/{origin}Logs.log', "a") as log:
        log.write(f"{timestamp} {msg}\n")


def downloadImage(url, id):
    try:
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Create the directory if it doesn't exist
        Path("pictures").mkdir(parents=True, exist_ok=True)
        
        # Save the image
        with open(f"pictures/{id}.jpg", "wb") as file:
            file.write(response.content)
        
        return True
    except Exception as e:
        log("PICTURES", f"[FAILED: DOWNLOAD IMAGE] {url} - {e}")
        return False
