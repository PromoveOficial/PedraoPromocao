from datetime import datetime

def log(origin, msg):
    timestamp = datetime.now().strftime('[%d/%m/%Y::%H:%M:%S]')
    
    with open(f'main/logs/{origin}Logs.log', "a") as log:
        log.write(f"{timestamp} {msg}\n")

