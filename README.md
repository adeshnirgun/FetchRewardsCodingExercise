# Fetch Rewards Coding Exercise - Backend Software Engineering
## How To Run
1. Install packages from requirements.txt in your Python environment with the following command:\
`pip install -r requirements.txt`

2. Start the Flask server with the following command:\
`python fetch.py`

3. You can access the API with the following URL:\
`http://127.0.0.1:5000`

## API Endpoints
**/add**: \
This endpoint adds a new transaction to the in-memory data. The request payload should contain payer, points, and timestamp. \
 `/add?payer=Dannon&points=1000&timestamp=2020-11-02T14:00:00Z`\
The endpoint will return back the transaction that was added.\
  `{
    "payer": "Dannon", 
    "points": 1000, 
    "timestamp": "2020-11-02T14:00:00Z"
  }`

**/spend**: \
This endpoint deducts a given number of points from the list of transactions. The request argument should contain the number of points to deduct.\
`/spend?points=1000` \
The deductions are based on the following rules:\
    - Points are deducted from the oldest transactions first\
    - Each payer's balance must not go negative\
The endpoint returns a payload with the total deducted points from each payer.\
    `[
        {
          "payer": "Dannon", 
          "points": -300
        }
      ]`  
      
**/balance**: \
This endpoint calculates the total balance of points for each payer and returns the list as a payload\
      `{
        "Dannon": 700
      }`
