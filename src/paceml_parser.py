import re
from paceml_tokenizer import Tokenizer
import json

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
    self.elements = []  # This will store intervals and repetitions in order
    self.calculations = []
    self.notes = []

  def add_element(self, element):
    self.elements.append(element)

  def to_dict(self):
    return {
      "metadata": {
        "title": self.metadata.title,
        "date": self.metadata.date,
        "athlete": self.metadata.athlete
      },
      "zones": [
        {
          "name": zone.name,
          "start": zone.start,
          "end": zone.end,
          "description": zone.description
        } for zone in self.zones
      ],
      "elements": [
        self._element_to_dict(element) for element in self.elements
      ],
      "calculations": [calc.calc_type for calc in self.calculations],
      "notes": self.notes
    }

  def _element_to_dict(self, element):
    if isinstance(element, Interval):
      return {
        "type": "interval",
        "title": element.title,
        "amount": element.amount,
        "zone": element.zone,
        "additional_params": element.additional_params
      }
    elif isinstance(element, Repetition):
      return {
        "type": "repetition",
        "title": element.title,
        "count": element.count,
        "intervals": [self._element_to_dict(interval) for interval in element.intervals]
      }

class Parser:
  def __init__(self, text):
    tokenizer = Tokenizer(text)
    self.tokens = tokenizer.get_tokens()
    self.current_token_index = 0
    self.workout = Workout()

  def parse(self):

    in_repetition = False
    current_repetition = None

    for self.current_token_index, (token_type, token_value) in enumerate(self.tokens):
      
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
          self.workout.add_element(interval)
          in_repetition = False
      elif token_type == 'REPS':
        current_repetition = self.parse_repetition()
        self.workout.add_element(current_repetition)
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
    if not match:
      raise PaceMLParseError(f"Invalid zone definition: {token_value}")
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

class PaceMLParseError(Exception):
  """Base exception for PaceML parsing errors."""
  pass

class InvalidZoneError(PaceMLParseError):
  """Raised when an invalid zone is encountered."""
  pass

class InvalidIntervalError(PaceMLParseError):
  """Raised when an invalid interval is encountered."""
  pass

def print_workout(workout):
  # Metadata
  print('Title:', workout.metadata.title)
  print('Date:', workout.metadata.date)
  print('Athlete:', workout.metadata.athlete)

  # Zones
  print('\nZones:')
  for zone in workout.zones:
    print(f'  {zone.name}:')
    print(f'    Start: {zone.start}')
    print(f'    End: {zone.end}')
    print(f'    Description: {zone.description}')

  # Elements (Intervals and Repetitions)
  print('\nWorkout Structure:')
  for element in workout.elements:
    if isinstance(element, Interval):
      print(f'  Interval: {element.title}')
      print(f'    Amount: {element.amount}')
      print(f'    Zone: {element.zone}')
      print(f'    Additional Params: {element.additional_params}')
    elif isinstance(element, Repetition):
      print(f'  Repetition: {element.title}')
      print(f'    Count: {element.count}')
      print('    Intervals:')
      for interval in element.intervals:
        print(f'      - {interval.title}: {interval.amount} in {interval.zone}')

  # Calculations
  print('\nCalculations:')
  for calc in workout.calculations:
    print(f'  {calc.calc_type}')

  # Notes
  print('\nNotes:')
  for note in workout.notes:
    print(f'  {note}')

def workout_to_json(workout, indent=2):
  return json.dumps(workout.to_dict(), indent=indent)