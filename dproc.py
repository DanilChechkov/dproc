import os, subprocess, psutil, pickle
from datetime import datetime

#Директория будет местом для хранения данных
workDir = os.path.dirname((os.path.abspath(__file__)))
file = str(input('Process to start: '))         #Пользователь указывает путь к процессу
tinterval = int(input('How often (seconds): ')) #Пользователь указывает интервал
#'/home/danil/Загрузки/Telegram/Telegram'
proc = subprocess.Popen([file], stdout=subprocess.PIPE) #Запускаем процесс
data = {}
while proc.poll() is None:  #Пока процесс запущен собираем статистику с помощью psutil
    try:
        #CPU_USAGE - определяет интервал повторения цикла, выбранный пользователем
        cpu_usage = psutil.Process(proc.pid).cpu_percent(interval=tinterval)/psutil.cpu_count()
        rss_usage = psutil.Process(proc.pid).memory_percent(memtype="rss")
        vms_usage = psutil.Process(proc.pid).memory_percent(memtype="vms")
        fds_num = psutil.Process(proc.pid).num_fds()
        data[datetime.now().isoformat()] = {cpu_usage,rss_usage,vms_usage,fds_num}
        print('[%s]:\tCPU:%.2f\tRSS:%.2f\tVMS:%.2f\tFDS:%d'%(datetime.now(),cpu_usage, rss_usage,vms_usage,fds_num))
    except:
        print('NO ACCESS')
#Сохраняем статистику в удобном формате, для автоматизированного построения графиков потребления ресурсов
f = open(workDir+'/data.pkl','wb')
pickle.dump(data,f)
f.close()
print('bye')