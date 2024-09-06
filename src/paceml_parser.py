import re
from paceml_tokenizer import Tokenizer

class Metadata:
  def __init__(self, title=None, date=None, athlete=None):
    self.title = title
    self.date = date
    self.athlete = athlete

class Zone:
  def __init__(self, name, start, end, description=None):
    self.name = name
    self.start = start
    self.end = end
    self.description = description

class Interval:
  def __init__(self, amount, zone, title=None, additional_params=None):
    self.title = title
    self.amount = amount
    self.zone = zone
    self.additional_params = additional_params

class Repetition:
  def __init__(self, count, intervals, title=None):
    self.title = title
    self.count = count
    self.intervals = intervals

class Calculation:
  def __init__(self, calc_type):
    self.calc_type = calc_type

class Workout:
  def __init__(self):
    self.metadata = Metadata()
    self.zones = []
    self.standalone_intervals = []  # For intervals not in repetitions
    self.repetitions = []
    self.calculations = []
    self.notes = []

class Parser:
  def __init__(self, text):
    tokenizer = Tokenizer(text)
    self.tokens = tokenizer.get_tokens()
    self.current_token_index = 0
    self.workout = Workout()

  def parse(self):
    print(f'TOKENS\n=====')
    for token in self.tokens:
      print(f"- Token: {token}")
    
    print(f'\n\nPARSING\n======')

    in_repetition = False
    current_repetition = None

    for self.current_token_index, (token_type, token_value) in enumerate(self.tokens):
      print(f"Current token index: {self.current_token_index}")
      print(f"Parsing token_type: {token_type} with token_value: {token_value}")
      
      if token_type == 'TITLE':
        self.workout.metadata.title = self.extract_value(token_value)
      elif token_type == 'DATE':
        self.workout.metadata.date = self.extract_value(token_value)
      elif token_type == 'ATHLETE':
        self.workout.metadata.athlete = self.extract_value(token_value)
      elif token_type == 'ZONE':
        self.workout.zones.append(self.parse_zone(token_value))
      elif token_type == 'INTERVAL':
        interval = self.parse_interval(token_value)
        if in_repetition and token_value.startswith('  '):  # Check for indentation
          current_repetition.intervals.append(interval)
        else:
          self.workout.standalone_intervals.append(interval)
          in_repetition = False
      elif token_type == 'REPS':
        current_repetition = self.parse_repetition()
        self.workout.repetitions.append(current_repetition)
        in_repetition = True
      elif token_type == 'CALCULATION':
        calc_type = self.extract_value(token_value)
        self.workout.calculations.append(Calculation(calc_type))
      elif token_type == 'NOTE':
        self.workout.notes.append(token_value)
      
    return self.workout
  
  def extract_value(self, token_value):
    # First, try to extract value from curly braces
    match = re.search(r'\{(.*?)\}', token_value)
    if match:
      return match.group(1)
    # If no curly braces, return the whole token value
    return token_value.split('@')[-1]  # Remove the '@' prefix if present

  def parse_zone(self, token_value):
    match = re.match(r'@define_zone\[(.*?)\]\{(.*?)\}\{(.*?)\}\{(.*?)\}', token_value)
    return Zone(match.group(1), match.group(2), match.group(3), match.group(4))

  def parse_interval(self, token_value):
    match = re.match(r"\s*@interval(?:\[(.*?)\])?\{([^{}]+)\}\{([^{}]+)\}(?:\{([^{}]*)\})?", token_value)
    additional_params = {}
    if match.group(4):
      params = match.group(4).split(',')
      for param in params:
        key, value = param.split('=')
        additional_params[key.strip()] = value.strip()
    return Interval(match.group(2), match.group(3), match.group(1), additional_params)

  def parse_repetition(self):
    token_type, token_value = self.tokens[self.current_token_index]
    match = re.match(r'@reps(?:\[(.*?)\])?\{([^{}]+)\}', token_value)
    title = match.group(1)
    count = int(match.group(2))
    return Repetition(count, [], title)  # Initialize with empty intervals list