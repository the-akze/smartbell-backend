import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from time import time
import firebase_admin
from firebase_admin import credentials, db
from pytz import timezone, utc
import datetime

app = Flask(__name__)
CORS(app)

print("initializing firebase...")
c = json.loads(os.environ['firebase_admin_certificate'])
cred = credentials.Certificate(c)
firebase_admin.initialize_app(
    cred,
    {'databaseURL': 'https://smartbell-7861e-default-rtdb.firebaseio.com'})
print("initialized firebase!")

print(db.reference("/").get())


@app.route("/")
def index():
    return "<h1>Hello! this is the backend server's url of the project</h1>"


@app.route("/rep")
def rep():
    try:
        data = request.args.get("data", None)
        if (data == None):
            return jsonify(
                {
                    "status": 400,
                    "message": "data not provided in query string parameters"
                }, 400)
        date_format = '%Y-%m-%d'
        date = datetime.datetime.now(tz=utc)
        date = date.astimezone(timezone('US/Pacific'))
        pstDateTime = date.strftime(date_format)
        set_index = 8
        ref = db.reference("/workouts/users/qwertyuiop/" + pstDateTime +
                           "/set/" + str(set_index))
        set = ref.get()
        nr = 1
        if (set != None):
            print("set exists!")
            if ("reps" in set.keys()):
                print("reps exist!")
                print("THE SET", set)
                rep_count = len(set["reps"].values())
                print("rep_count", rep_count)
                nr = rep_count + 1
                print("nr", nr)
            else:
                print("reps don't exist! creating")
        else:
            print("set doesn't exist! creating")
        set_ref = db.reference("/workouts/users/qwertyuiop/" + pstDateTime +
                               "/set/" + str(set_index) + "/reps/r" + str(nr))
        set_ref.set({"time": float(data)})
        return jsonify({"status": 200, "message": "ok"})
    except Exception as e:
        print("ERROR!!1", e)
        return jsonify({"status": 500, "message": "error"})


if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8080, debug=False)
