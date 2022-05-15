from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)
from datetime import datetime as dt

global_data = []


#/dump route: Returns global data (used for testing purposes)
@app.route('/dump')
def Dump():
    return jsonify(global_data)

#/add route: 
@app.route('/add')
def Add():
    r = request.args
    payload = r.to_dict()
    payload["points"] = int(payload["points"])
    global_data.append(payload)
    return jsonify(global_data)

@app.route('/spend')
def Spend():
    points = request.args.get('points')
    numPoints = int(points)
    sorted_data = sorted(global_data, key = lambda i: i['timestamp'])
    spend_data = []
    for pay in sorted_data:
        if numPoints <= 0:
            break
        pointInt = int(pay["points"])
        numPoints -= pointInt
        if pointInt > numPoints:
            balance = (numPoints + pointInt) * -1
        else:
            balance = pointInt * -1  
        entry = {"payer": pay["payer"], "points": balance}
        listofbool = [True for elem in spend_data if pay["payer"] in elem.values()]
        if any(listofbool):
            for elem in spend_data:
                if elem["payer"] == entry["payer"]:
                    elem["points"] += entry["points"]
        else:
            spend_data.append(entry)
    time_dict = {'timestamp' :  dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")}
    [global_data.append(i|time_dict) for i in spend_data]
    return jsonify(spend_data) 


@app.route('/balance')
def returnBalance():
    updatedBalance={}
    for data in global_data:
        if data["payer"] in updatedBalance:
            newBalance = updatedBalance[data["payer"]] + data["points"]
            updatedBalance[data["payer"]] = newBalance
        else:
            updatedBalance[data["payer"]] = data["points"]
    return updatedBalance

if __name__ == "__main__":
    app.run(debug=True)