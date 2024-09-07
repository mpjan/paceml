from flask import Flask, render_template
from paceml_parser import Parser, workout_to_json
import os

app = Flask(__name__)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the examples directory
examples_dir = os.path.join(os.path.dirname(current_dir), 'examples')
# Construct the full path to the PaceML file
paceml_file = os.path.join(examples_dir, 'hill_repeats.paceml')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/workout')
def get_workout():
  try:
    with open(paceml_file, 'r') as file:
      text = file.read()
    
    parser = Parser(text)
    workout = parser.parse()
    return workout_to_json(workout)
  except FileNotFoundError:
    return {"error": f"PaceML file not found: {paceml_file}"}, 404
  except Exception as e:
    return {"error": str(e)}, 500

if __name__ == '__main__':
  app.run(debug=True)