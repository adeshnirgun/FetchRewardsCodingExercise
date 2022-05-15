from datetime import datetime as dt
global_data = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }, {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
, { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
, { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
, { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]

def helper(entry, elem):
    elem["points"] += entry["points"]
    return -1

numPoints = 5000
sorted_data = sorted(global_data, key = lambda i: i['timestamp'])
spend_data = []
for txn in sorted_data:
    if numPoints <= 0:
        break
    numPoints -= txn["points"]
    if txn["points"] > numPoints:
        balance = (numPoints + txn["points"]) * -1
    else:
        balance = txn["points"] * -1  
    entry = {"payer": txn["payer"], "points": balance}
    listofbool = [True for elem in spend_data if txn["payer"] in elem.values()]
    if any(listofbool):
        for elem in spend_data:
            if elem["payer"] == entry["payer"]:
                elem["points"] += entry["points"]
    else:
        spend_data.append(entry)

time_dict = {'timestamp' :  dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")}
spend_txn_list = [i|time_dict for i in spend_data]
global_data.append(spend_txn_list)
print(global_data)