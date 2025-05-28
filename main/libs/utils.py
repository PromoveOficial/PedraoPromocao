from datetime import datetime, date

def write_log(origin, msg):
    timestamp = datetime.now().strftime('[%d/%m/%Y::%H:%M:%S]')
    
    with open(f'logs/{origin}Logs.log', "a") as log:
        log.write(f"{timestamp} {msg}\n")

