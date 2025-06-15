import subprocess
import time
import logging
from prometheus_client import Gauge, start_http_server

log_file = "pipeline.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Disk I/O metrics
io_read_rate = Gauge('io_read_rate', 'Disk read rate', ['device'])
io_write_rate = Gauge('io_write_rate', 'Disk write rate', ['device'])
io_tps = Gauge('io_tps', 'Disk I/O operations per second', ['device'])
io_read_bytes = Gauge('io_read_bytes', 'Disk read bytes', ['device'])
io_write_bytes = Gauge('io_write_bytes', 'Disk written bytes', ['device'])

# CPU usage metrics
cpu_avg_percent = Gauge('cpu_avg_percent', 'CPU usage in percentage', ['mode'])


# Memory information metrics
meminfo_stats = {} # key-> metric name; value-> Memory value



def disk_io():
    result = subprocess.run('iostat', capture_output=True, text=True)
    if result.returncode!=0:
        logging.info("iostat command failed!")
    
    lines = result.stdout.splitlines()
    logging.info("Reading Cpu Metrics")
    
    cpu_mode = lines[2].split()[1:]
    cpu_avg = lines[3].split()
    
    for i in range(len(cpu_mode)):
        if cpu_mode[i].startswith("%"):
            cpu_mode[i] = cpu_mode[i][1:]
    
    for i in range(len(cpu_mode)):
        cpu_avg_percent.labels(mode=cpu_mode[i]).set(cpu_avg[i])
    #print(cpu_avg_percent)
    #print(cpu_avg)
    logging.info("Cpu metrics read without errors")
    
    lines = lines[5:]
    logging.info("Reading I/O metrics")
    for line in lines:
        
        if line.startswith("Device"):
            continue
        
        fields = line.split()
        
        if len(fields)!=0:
            device = fields[0]   
            read_rate = float(fields[2])  # kB_r/s
            write_rate = float(fields[3])  # kB_w/s
            tps = float(fields[1])  # tps
            read_bytes = float(fields[5])  # kB_r/s
            write_bytes = float(fields[6])  # kB_w/s
            
            io_read_rate.labels(device=device).set(read_rate)
            io_write_rate.labels(device=device).set(write_rate)
            io_tps.labels(device=device).set(tps)
            io_read_bytes.labels(device=device).set(read_bytes)
            io_write_bytes.labels(device=device).set(write_bytes)
    logging.info("Read I/O metrics without any errors")


def memInfo():
    result = subprocess.run(['cat', '/proc/meminfo'], capture_output=True, text=True)
    if result.returncode!=0:
        logging.info("cat /proc/meminfo command failed!")
    
    logging.info("cat /proc/meminfo command executed!")
    lines = result.stdout.splitlines()
    
    for line in lines:
        fields = line.split(":")
        key = fields[0].strip()
        value = int(fields[1].strip().split()[0])*1024
        #print((key, value))
        
        metric = f"meminfo_{key.replace('(', '_').replace(')', '')}_bytes"
        logging.info(f"Processing: {key} = {value} bytes")
        #print(metric)
        if metric not in meminfo_stats:
            meminfo_stats[metric] = Gauge(metric, f"{key} in bytes")
            logging.info(f"Created new metric: {metric}")
            
        meminfo_stats[metric].set(value)
        logging.info(f"Set value for {metric}: {value} bytes")
    
    logging.info("Finished processing /proc/meminfo.")  
    #print(meminfo_stats.values)
    #print(meminfo_stats.keys)
    

def main():
    start_http_server(18000)
    logging.info("Device Metrics server started on port 18000.")
    while True:
        disk_io()
        
        memInfo()
        
        time.sleep(1)
    

    
if __name__ == "__main__":
    main()
