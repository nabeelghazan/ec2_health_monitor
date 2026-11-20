import time
from datetime import datetime, timezone
import psutil

LOG_FILE = "/app/logs/system_health.log"

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def collect_metrics():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime = get_uptime()
    return f"[{timestamp}] CPU: {cpu}% | Memory: {memory}% | Disk: {disk}% | Uptime: {uptime}\n"

if __name__ == "__main__":
    print("Starting system health monitor...")
    while True:
        record = collect_metrics()
        with open(LOG_FILE, "a") as f:
            f.write(record)
        print(record.strip())
        time.sleep(10)
