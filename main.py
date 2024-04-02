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
