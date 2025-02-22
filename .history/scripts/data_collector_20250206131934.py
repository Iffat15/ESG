import psutil
import pandas as pd
import time
import os

# Constants for energy calculation (Wattage)
CPU_POWER = 35
GPU_POWER = 20
MEMORY_POWER = 5
DISK_POWER = 2

def collect_system_data(output_file='../data/energy_data.csv', duration=60, interval=1):
    """
    Collect system usage data and calculate energy usage.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    data = []
    start_time = time.time()

    while time.time() - start_time < duration:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Calculate power consumption
        cpu_power = (cpu_usage / 100) * CPU_POWER
        memory_power = (memory_usage / 100) * MEMORY_POWER
        disk_power = (disk_usage / 100) * DISK_POWER
        total_power = cpu_power + memory_power + disk_power

        data.append({
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "total_power": total_power
        })

        time.sleep(interval)

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"System data collected and saved to {output_file}")

if __name__ == "__main__":
    collect_system_data()
