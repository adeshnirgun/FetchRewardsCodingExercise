from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)
from datetime import datetime as dt

#global_txn_data contains all transaction records
global_txn_data = []

#/add: Adds a new transaction to global_txn_data, returns the payload
@app.route('/add')
def Add():
    r = request.args
    payload = r.to_dict()
    payload["points"] = int(payload["points"])
    global_txn_data.append(payload)
    return payload

#/spend: Deducts points from each payer in chronological order of transactions, returns a list of points deducted from payers  
@app.route('/spend')
def Spend():
    points = request.args.get('points')
    numPoints = int(points)
    #Sorts global_txn_data by timestamp
    sorted_data = sorted(global_txn_data, key = lambda i: i['timestamp'])
    spend_data = []
    #Iterates through sorted_data and deducts each txn's points from numPoints till numPoints <=0
    #The deducted balance from each txn is assigned in balance
    for txn in sorted_data:
        if numPoints <= 0:
            break
        pointInt = int(txn["points"])
        numPoints -= pointInt
        if pointInt > numPoints:
            balance = (numPoints + pointInt) * -1
        else:
            balance = pointInt * -1  
        entry = {"payer": txn["payer"], "points": balance}
        #returns a list of booleans where a duplicate payer is found
        listofbool = [True for elem in spend_data if txn["payer"] in elem.values()]
        #if there is a duplicate, update the deducted points instead of creating a new entry in spend_data
        if any(listofbool):
            for elem in spend_data:
                if elem["payer"] == entry["payer"]:
                    elem["points"] += entry["points"]
        else:
            spend_data.append(entry)
    #create a current timestamp for each deduction and append it to global_txn_data 
    time_dict = {'timestamp' :  dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")}
    [global_txn_data.append(i|time_dict) for i in spend_data]
    return jsonify(spend_data) 

#/balance: returns each payers' total number of points
@app.route('/balance')
def returnBalance():
    updatedBalance={}
    for data in global_txn_data:
        if data["payer"] in updatedBalance:
            newBalance = updatedBalance[data["payer"]] + data["points"]
            updatedBalance[data["payer"]] = newBalance
        else:
            updatedBalance[data["payer"]] = data["points"]
    return updatedBalance

if __name__ == "__main__":
    app.run(debug=True)
