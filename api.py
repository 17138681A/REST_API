import flask
import json
import threading
import glob
import os
import time
from flask import flash
from flask import jsonify
from flask import request
from flask import render_template
from flask import make_response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# test data
def extract_time(json):

    try:
    
        return int(json['id'])
        
    except KeyError:
    
        return 0

def updateBuffer():

    global buffer
    
    
    while 1:
        
        for filename in glob.glob('*.json'):
        
            try:
            
                with open(os.path.join(os.getcwd(), filename), 'r') as f: 
                    
                    data = json.load(f)
                    
                    if 'cities' in data:        
                        cities = data['cities']
                        buffer.extend(x for x in cities if x not in buffer)
                    
            except Exception as e:
                #print("update error")
                print(e)
                continue    
                
        buffer.sort(key=extract_time)    
        



@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask!</h1>"


@app.route('/getData', methods=['GET'])

def getData():
    
    return jsonify(buffer)

@app.route('/uploadData', methods=['GET', 'POST'])
def uploadData():
    
    if request.method == 'POST':
  
        '''
        data = {
            "cities": [
                {
                    "id": 483,
                    "city_name": "Taipei",
                    "country_name": "Taiwan",
                    "is_capital": True,
                    "location": {
                        "longitude": 121.569649,
                        "latitude": 25.036786
                    }
                },
                
                {
                    "id": 481,
                    "city_name": "New York",
                    "country_name": "United States",
                    "is_capital": False,
                    "location": {
                        "longitude": -74.004364,
                        "latitude": 40.710405
                    }
                },
                
                {
                    "city_name": "London", 
                    "country_name": "United Kingdom", 
                    "id": 489, 
                    "is_capital": True, 
                    "location": {
                      "latitude": 51.507497, 
                      "longitude": -0.114089
                    }
                }
            ]
        }
        '''
        
        timestr = time.strftime("%Y%m%d_%H%M%S")
        fileName = timestr + '.json'
        
        try:
            data = {"cities": []}
            
            temp = request.get_json()
            
            if "cities" in temp:         
                data = temp
            else:   
                data['cities'].append(temp)
                
            #cities = data['cities']
            #data = jsonify(data)
            
            with open(fileName, 'w') as f:
                json.dump(data, f)
                
            #print(data)    
            
            return make_response(data,200)
            
        except Exception as e:
            print(e)
            return make_response(e,404)
        
        #return redirect(request.args.get("new") or url_for("new"))
        #return render_template('submit_article.html', title='upload')
        
    #return render_template('submit_article.html', title='upload')

buffer = []

rt = threading.Thread(target = updateBuffer)
rt.daemon = True
rt.start()

#readerQ = Queue.Queue(maxsize = 0)
app.secret_key = 'many random bytes'
app.run(host = '192.168.12.112')