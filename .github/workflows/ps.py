
import psutil
import matplotlib.pyplot as plt
import time
# CPU-Informationen
# print("CPU-Informationen:")
# print("CPU-Auslastung (pro Kern):", psutil.cpu_percent(interval=1, percpu=True))
# print("CPU-Zeiten:", psutil.cpu_times())
# print("Anzahl der logischen CPUs:", psutil.cpu_count())
# print("Anzahl der physischen CPUs:", psutil.cpu_count(logical=False))
# print("\n")

# Speicherinformationen
# print("Speicherinformationen:")
# mem_info = psutil.virtual_memory()
# print("Gesamter Speicher:", mem_info.total)
# print("Verfügbarer Speicher:", mem_info.available)
# print("Prozentsatz des verwendeten Speichers:", mem_info.percent)
# print("Verwendeter Speicher:", mem_info.used)
# print("Freier Speicher:", mem_info.free)
# print("\n")

# Festplatteninformationen
# print("Festplatteninformationen:")
# print("Festplattennutzung:", psutil.disk_usage('/'))
# print("Festplatten-IO-Statistiken:", psutil.disk_io_counters())
# print("\n")

# Netzwerkinformationen
# print("Netzwerkinformationen:")
# print("Netzwerk-IO-Statistiken:", psutil.net_io_counters())
# print("Aktive Netzwerkverbindungen:", psutil.net_connections())
# print("\n")

# Prozessinformationen
# print("Prozessinformationen:")
# for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
#     print(proc.info)



# Sammeln Sie CPU-Auslastungsdaten über einen Zeitraum von 10 Sekunden
cpu_percentages = []
for i in range(10):
    cpu_percentages.append(psutil.cpu_percent(interval=1))
    time.sleep(1)

# Erstellen Sie ein Diagramm der CPU-Auslastung
plt.plot(cpu_percentages)
plt.title('CPU-Auslastung im Laufe der Zeit')
plt.xlabel('Zeit (Sekunden)')
plt.ylabel('CPU-Auslastung (%)')
plt.show()