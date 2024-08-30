import re

class Tokenizer:
  def __init__(self, text):
    self.text = text
    self.tokens = []
    self.tokenize()

  def tokenize(self):
    # Define regex patterns for different token types
    patterns = {
      'COMMENT': r'#.*',
      'TITLE': r'@title\{.*?\}',
      'DATE': r'@date\{.*?\}',
      'ATHLETE': r'@athlete\{.*?\}',
      'ZONE': r'@define_zone\[\w+\]\{.*?\}\{.*?\}\{.*?\}',
      'INTERVAL': r"\s*@interval(?:\[(.*?)\])?\{([^{}]+)\}\{([^{}]+)\}(?:\{([^{}]*)\})?",
      'REPS': r'@reps(?:\[(.*?)\])?\{([^{}]+)\}',
      'CALCULATION': r'@total_(distance|time)',
      'NOTE': r'.+'
    }

    # Combine patterns into a single regex
    combined_pattern = '|'.join(f'(?P<{key}>{pattern})' for key, pattern in patterns.items())
    regex = re.compile(combined_pattern)

    # Tokenize the text
    for match in regex.finditer(self.text):
      token_type = match.lastgroup
      token_value = match.group(token_type)
      self.tokens.append((token_type, token_value))

  def get_tokens(self):
    return self.tokens