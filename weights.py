
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
