import psutil

# free memory (MiB)
free_memory = psutil.virtual_memory().available / (1024 * 1024)

# cpu utlization (%)
total = psutil.cpu_percent()
per_cpu = psutil.cpu_percent(percpu=True)
