# Basketball scores(Balldontlie.io) and details Flask web application

## Objective : 
Statistics are displayed in a flask web application. Basketball details player stats are fetched from  https://www.balldontlie.io/#introduction  API. 


## Step 1 - Fetching data from API 
This code fetches data from the API on Basketball players' weights and create a chart for the distribution of the weights. 

```python
import httpx
from fastapi import FastAPI, Request
import json
import uvicorn 
import os
import matplotlib

# Set the backend for matplotlib to 'agg' to avoid GUI errors
matplotlib.use('agg')
import matplotlib.pyplot as plt


# Define the BallDontLie API endpoint and API key
app = FastAPI()
BALDONTLIE_ENDPOINT = "https://api.balldontlie.io/v1/players"
API_KEY = "4848b742-b4f4-4673-a96b-c473415c9b84"
headers = {"Authorization": f"{API_KEY}"}

# Define the route to get weight data
@app.get("/")
def get_weight():
  response = httpx.get(BALDONTLIE_ENDPOINT, headers=headers)
  response.raise_for_status()  # Raise an exception for non-200 status codes
  data = response.json()
   # Extract player weights from the API
  weights = []
  for player in data["data"]:
      if player["weight"].isdigit():
          weights.append(int(player["weight"]))
        
   # Calculate the average player weight
  average_weight = sum(weights) / len(weights) if weights else 0
  # Print the average weight (for debugging purposes)
  print(average_weight)

  # Create a histogram of player weights
  plt.figure(figsize=(12, 6))
  plt.hist(weights, 
           bins=20, 
           color='skyblue',
           edgecolor='black')
  plt.title('Distribution of Player Weights')
  plt.xlabel('Weight (lbs)')
  plt.ylabel('Number of Players')
  plt.grid(axis='y', alpha=0.75)
  plt.tight_layout()
  weight_plot_path = 'static/player_weights_histogram.png'
  plt.savefig(weight_plot_path)
  plt.close()

  # Return the average weight and the path to the weight plot
  return average_weight, weight_plot_path
  # return {"average_weight":average_weight, "weight_plot_path": weight_plot_path}
# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```


**Distribution of Basketball player's weight**

![player_weights_histogram](https://github.com/anosharangalla/basketball_scores/assets/156144296/8d269e90-f8ae-42b3-b3a0-1ec31d19936f)


## Step 2 - Flask application to visualize the chart

```python
from flask import Flask, render_template, request
from weights import get_weight

# Create a Flask application
#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


# Define a route
@app.route('/', methods=['GET'])
def index(): 
   #Call the get_weight function 
  average_weight, weight_plot_path= get_weight()
  # for debugging purpose
  print(f"Average Weight: {average_weight}")
  # Render the index.html template, passing the average weight and the weight plot path 
  return render_template('index.html',average_weight = average_weight,
                         weight_plot_path=weight_plot_path)

app.run(host='0.0.0.0', port=8080)
````
## Step 3 -  HTML page 

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Player Weights Histogram</title>
</head>
<body>
  <!-- Page heading -->
    <h1>Analysis of the Weights of Basketball Players</h1>
  <br>
   <!-- Display the average weight of a player -->
    <p>The average weight of a player is: {{ average_weight }} lbs</p>
  <br>
  <!-- Display the histogram of player weights -->
  <h3>Histogram of the Weights of Basketball Players</h3>
  <br>
    <img src="static/player_weights_histogram.png" alt="Player Weights Histogram">



  <br>

</body>
</html>
```

original work in [Replit](https://replit.com/@a00284480/A00284480-Assignment-4-Basketball#main.py)


