import psutil
import pandas as pd


CPU_COUNT = psutil.cpu_count()


df = pd.DataFrame()


for i in range(CPU_COUNT):
    df[f'cpu{i+1}'] = [0.0] * 300
df['ram'] = [0.0] * 300
df['swap'] = [0.0] * 300
df['disk_usage'] = [0.0] * 300
df['disk_write'] = [0.0] * 300
df['disk_read'] = [0.0] * 300
df['network_sent'] = [0.0] * 300
df['network_received'] = [0.0] * 300
df['temperature'] = [0.0] * 300
df['cpu_avg'] = [0.0] * 300 
df['connections'] = [0] * 300 

conections = {}


def update_df():
    
    df.iloc[:-1, :] = df.iloc[1:, :]

    
    df.iloc[-1, :CPU_COUNT] = psutil.cpu_percent(percpu=True)
    df.iloc[-1, CPU_COUNT] = psutil.virtual_memory().percent
    df.iloc[-1, CPU_COUNT+1] = psutil.swap_memory().percent
    df.iloc[-1, CPU_COUNT+2] = psutil.disk_usage('/').percent
    df.iloc[-1, CPU_COUNT+3] = psutil.disk_io_counters().write_bytes
    df.iloc[-1, CPU_COUNT+4] = psutil.disk_io_counters().read_bytes
    df.iloc[-1, CPU_COUNT+5] = psutil.net_io_counters().bytes_sent
    df.iloc[-1, CPU_COUNT+6] = psutil.net_io_counters().bytes_recv
    df.iloc[-1, CPU_COUNT+7] = psutil.cpu_percent()  

    conections["test"] = "127.0.0.1"