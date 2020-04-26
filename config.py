from shutil import copy
from urllib.parse import quote
from yaml import load, dump

MAX_ENTRY_LENGTH = 20

class PlayerConfig:
  def create_player_from_template(templatefile, outfile):
    ''' Load template for a new player.
    Neither of these are validated. It's up to the caller to do so.'''
    copy(templatefile, outfile)
    
  def update_player_setting(playerfile, path, value):
    ''' Update a setting in a given YAML file.'''
    player_dict = load(playerfile)
    elem = player_dict
    while '/' in path:
      next, path = path.split('/', 1)
      elem = elem[next]
    elem[path] = self.validate_input(value)
    open(playerfile, 'w').write(dump(player_dict))
  
  def validate_input(input):
    ''' Generic validator for YAML input.'''
    return quote(input)[:MAX_ENTRY_LENGTH]
