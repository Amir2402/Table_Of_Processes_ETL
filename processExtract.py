import psutil 
import time 
import sys 

def get_processes_list() : 
    processes = [] 
    
    for proc in psutil.process_iter(['pid' , 'name' , 'username' ,'cpu_percent']) : 
        processes.append(proc.info)
        
    processes = sorted(processes , key = lambda d : d['cpu_percent'] , reverse = True )
    processes = processes[:20]
    return(processes)

if __name__ == '__main__' :   
      
    while True :
        try : 
            print(get_processes_list())
            print(psutil.cpu_percent())
            time.sleep(3)
        except KeyboardInterrupt : 
            print('stoped')
            sys.exit()