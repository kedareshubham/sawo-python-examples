from flask import Flask,render_template,request
from sawo import createTemplate,verifyToken
import json

app = Flask(__name__)
createTemplate("templates/partials",flask=True) #using flask = True genrates flask template

load = ''
loaded = 0


def setPayload(payload):
    global load
    load = payload

def setLoaded(reset=False):
    global loaded
    if reset:
        loaded=0
    else:
        loaded+=1


@app.route("/")
def index():
    setLoaded()
    setPayload(load if loaded<2 else '')
    sawo = {
        "auth_key":"088c25d0-82ba-48fa-949f-c9c5c87cdd2b",
        "to":"login",
        "identifier":"phone_number_sms"
    }
    return render_template("index.html",sawo=sawo,load=load)

@app.route("/login",methods=["POST","GET"])
def login():
    payload = json.loads(request.data)["payload"]
    setLoaded(True)
    setPayload(payload)
    status = 200 if(verifyToken(payload)) else 404
    return {"status" : status}

if __name__ =='__main__':
    app.run()