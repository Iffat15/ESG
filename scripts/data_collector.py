# import psutil
# import pandas as pd
# import time
# import os


# CPU_POWER = 35
# GPU_POWER = 20
# MEMORY_POWER = 5
# DISK_POWER = 2

# def collect_system_data(output_file='../data/energy_data.csv', duration=60, interval=1):
#     """
#     Collect system usage data and calculate energy usage.
#     """

#     output_dir = os.path.dirname(output_file)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir, exist_ok=True)

#     data = []
#     start_time = time.time()

#     while time.time() - start_time < duration:
#         cpu_usage = psutil.cpu_percent(interval=0.1)
#         memory_usage = psutil.virtual_memory().percent
#         disk_usage = psutil.disk_usage('/').percent

#         # Calculate power consumption
#         cpu_power = (cpu_usage / 100) * CPU_POWER
#         memory_power = (memory_usage / 100) * MEMORY_POWER
#         disk_power = (disk_usage / 100) * DISK_POWER
#         total_power = cpu_power + memory_power + disk_power

#         data.append({
#             "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
#             "cpu_usage": cpu_usage,
#             "memory_usage": memory_usage,
#             "disk_usage": disk_usage,
#             "total_power": total_power
#         })

#         time.sleep(interval)

#     # Save to CSV
#     df = pd.DataFrame(data)
#     df.to_csv(output_file, index=False)
#     print(f"System data collected and saved to {output_file}")

# if __name__ == "__main__":
#     collect_system_data()

# import psutil
# import pandas as pd
# import time
# import os

# # Define base power usage per component
# #MEMORY_POWER = 5  # Example, can be refined
# #DISK_POWER = 2     # Example, can be refined

# def get_dynamic_cpu_power():
#     """
#     Estimate CPU power dynamically based on frequency and core usage.
#     """
#     cpu_freq = psutil.cpu_freq()  # Get CPU frequency info
#     if cpu_freq:
#         base_freq = cpu_freq.max  # Maximum frequency in MHz
#         current_freq = cpu_freq.current  # Current frequency in MHz
#         cpu_usage = psutil.cpu_percent(interval=0.1)
        
#         # Assume power scales linearly with frequency and usage
#         estimated_cpu_power = (current_freq / base_freq) * cpu_usage * 0.5  # Adjust scaling factor as needed
#         return estimated_cpu_power
#     return 35  # Default fallback if frequency can't be retrieved

# def get_dynamic_memory_power():
#     total_memory = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
#     memory_usage = psutil.virtual_memory().percent
    
#     estimated_memory_power = total_memory * (memory_usage / 100) * 0.05
#     return estimated_memory_power

# def get_dynamic_disk_power():
#     total_disk = psutil.disk_usage('/').total / (1024 ** 3)  # Convert to GB
#     disk_usage = psutil.disk_usage('/').percent
    
#     estimated_disk_power = total_disk * (disk_usage / 100) * 0.01
#     return estimated_disk_power


# def collect_system_data(output_file='../data/energy_data.csv', duration=60, interval=1):
#     """
#     Collect system usage data and calculate energy usage dynamically.
#     """

#     output_dir = os.path.dirname(output_file)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir, exist_ok=True)

#     data = []
#     start_time = time.time()

#     while time.time() - start_time < duration:
#         cpu_usage = psutil.cpu_percent(interval=0.1)
#         memory_usage = psutil.virtual_memory().percent
#         disk_usage = psutil.disk_usage('/').percent

#         # Dynamically fetch CPU power
#         cpu_power = get_dynamic_cpu_power()
#         memory_power = get_dynamic_memory_power()
#         disk_power = get_dynamic_disk_power()
#         total_power = cpu_power + memory_power + disk_power
#         timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

#         data.append({
#             "timestamp": timestamp,
#             "cpu_usage": cpu_usage,
#             "memory_usage": memory_usage,
#             "disk_usage": disk_usage,
#             "cpu_power": cpu_power,
#             "total_power": total_power
#         })

#         # Print to console
#     #     print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} | "
#     #   f"CPU Usage: {cpu_usage:.2f}% | CPU Power: {cpu_power:.2f}W | "
#     #   f"Memory Usage: {memory_usage:.2f}% | Memory Power: {memory_power:.2f}W | "
#     #   f"Disk Usage: {disk_usage:.2f}% | Disk Power: {disk_power:.2f}W | "
#     #   f"Total Power: {total_power:.2f}W")


#         time.sleep(interval)

#     # Save to CSV
#     df = pd.DataFrame(data)
#     df.to_csv(output_file, index=False)
#     print(f"System data collected and saved to {output_file}")

# if __name__ == "__main__":
#     collect_system_data()


import psutil
import pandas as pd
import time
import os
import socket

# Function to dynamically get CPU, Memory, and Disk Power
def get_dynamic_cpu_power():
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        base_freq = cpu_freq.max  
        current_freq = cpu_freq.current  
        cpu_usage = psutil.cpu_percent(interval=0.1)
        estimated_cpu_power = (current_freq / base_freq) * cpu_usage * 0.5  
        return estimated_cpu_power
    return 35  

def get_dynamic_memory_power():
    total_memory = psutil.virtual_memory().total / (1024 ** 3)  
    memory_usage = psutil.virtual_memory().percent
    estimated_memory_power = total_memory * (memory_usage / 100) * 0.05
    return estimated_memory_power

def get_dynamic_disk_power():
    total_disk = psutil.disk_usage('/').total / (1024 ** 3)  
    disk_usage = psutil.disk_usage('/').percent
    estimated_disk_power = total_disk * (disk_usage / 100) * 0.01
    return estimated_disk_power

# Function to check all available network devices
def get_network_devices(network_path=r'\\'):
    """ Scan network folder to list available devices. """
    try:
        return [device for device in os.listdir(network_path) if os.path.isdir(os.path.join(network_path, device))]
    except FileNotFoundError:
        print("Network path not found! Make sure network discovery is enabled.")
        return []
    except PermissionError:
        print("No permission to access network devices.")
        return []

# Function to read CSV file from network device
def read_device_csv(device_name):
    """ Read CSV file from a shared network folder of a device. """
    # print(device_name);
    # print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} | "
    #   f"CPU Usage: {cpu_usage:.2f}% | CPU Power: {cpu_power:.2f}W | "
    #   f"Memory Usage: {memory_usage:.2f}% | Memory Power: {memory_power:.2f}W | "
    #   f"Disk Usage: {disk_usage:.2f}% | Disk Power: {disk_power:.2f}W | "
    #   f"Total Power: {total_power:.2f}W")
    device_path = f"//{device_name}/Shared/energy_data.csv"
    
    try:
        df = pd.read_csv(device_path)
        df["Device Name"] = device_name  # Add device name column
        return df
    except FileNotFoundError:
        print(f"File not found on {device_name}.")
    except PermissionError:
        print(f"No permission to access {device_name}. Waiting 5 sec before retrying...")
        time.sleep(5)
    except Exception as e:
        print(f"Error reading {device_name}: {e}")
    
    return None

# Function to collect and merge data from all network devices
# def collect_all_devices_data(output_file='C:/Users/Anas/Downloads/ESG - Copy/data/energy_data.csv'):
#     """ Collect and merge data from all devices into a single CSV file. """
    
#     all_data = []
    
#     # Get local machine data
#     local_device = socket.gethostname()
#     local_data = collect_system_data(device_name=local_device, return_df=True)
#     all_data.append(local_data)

#     # Check network devices
#     devices = get_network_devices()
    
#     for device in devices:
#         time.sleep(5)  # Add a 5-sec buffer before checking each device
#         df = read_device_csv(device)
#         if df is not None:
#             all_data.append(df)
#     # all_data.append("LAPTOP-V22P1IC3")
#     # Save merged data
#     if all_data:
#         final_df = pd.concat(all_data, ignore_index=True)
#         final_df.to_csv(output_file, index=False)
#         print(f"Collected data saved to {output_file}")
#     else:
#         print("No data collected.")

import os
import socket
import time
import pandas as pd
import ipaddress
from pythonping import ping

def get_active_devices(network="192.168.1.0/24"):
    """ Scan the network and return a list of active IPs """
    devices = []
    for ip in ipaddress.IPv4Network(network, strict=False):
        response = ping(str(ip), count=1, timeout=1)
        if response.success():
            try:
                hostname = socket.gethostbyaddr(str(ip))[0]
            except socket.herror:
                hostname = str(ip)
            devices.append((str(ip), hostname))
    return devices

def read_device_csv(device_ip, shared_folder="SharedData"):
    """ Try to read CSV from a shared folder on the network device """
    network_path = f"\\\\{device_ip}\\{shared_folder}\\data.csv"
    if os.path.exists(network_path):
        try:
            df = pd.read_csv(network_path)
            df["Device"] = device_ip  # Tag data with device IP
            print(f"✅ Data collected from {device_ip}")
            return df
        except Exception as e:
            print(f"❌ Could not read from {device_ip}: {e}")
    else:
        print(f"❌ No CSV found at {network_path}")
    return None

def collect_all_devices_data(output_file="C:/Users/Anas/Downloads/ESG - Copy/data/energy_data.csv"):
    """ Collect and merge data from all devices into a single CSV file. """
    
    all_data = []

    # Get local machine data
    local_device = socket.gethostname()
    local_data = read_device_csv(local_device)
    if local_data is not None:
        all_data.append(local_data)

    # Find network devices
    devices = get_active_devices()
    
    for ip, device in devices:
        time.sleep(2)  # Small delay before checking each device
        df = read_device_csv(ip)
        if df is not None:
            all_data.append(df)

    # Save merged data
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv(output_file, index=False)
        print(f"✅ Collected data saved to {output_file}")
    else:
        print("❌ No data collected.")

# Run the function
collect_all_devices_data()


# Modify collect_system_data function to return DataFrame when needed
def collect_system_data(output_file=None, duration=60, interval=1, device_name="Local", return_df=False):
    """ Collect system usage data and calculate energy usage dynamically. """

    data = []
    start_time = time.time()

    while time.time() - start_time < duration:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        cpu_power = get_dynamic_cpu_power()
        memory_power = get_dynamic_memory_power()
        disk_power = get_dynamic_disk_power()
        total_power = cpu_power + memory_power + disk_power
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        data.append({
            "timestamp": timestamp,
            "device_name": device_name,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "cpu_power": cpu_power,
            "total_power": total_power
        })

        time.sleep(interval)

    df = pd.DataFrame(data)

    if output_file:
        df.to_csv(output_file, index=False)
        print(f"System data collected and saved to {output_file}")

    if return_df:
        return df

if __name__ == "__main__":
    collect_all_devices_data()
