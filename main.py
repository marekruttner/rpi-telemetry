import threading
import time
from utils import telemetry
from utils.app import app

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # Start telemetry data collection
    telemetry_thread = threading.Thread(target=telemetry.collect_telemetry)
    telemetry_thread.daemon = True
    telemetry_thread.start()

    # Start web server
    web_server_thread = threading.Thread(target=run_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)
