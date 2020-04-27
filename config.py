from shutil import copy
from urllib.parse import quote
from yaml import load, dump, SafeLoader

MAX_ENTRY_LENGTH = 20

class PlayerConfig:
    def create_player_from_template(self, templatefile, outfile):
        ''' Load template for a new player.
        Neither of these are validated. It's up to the caller to do so.'''
        copy(templatefile, outfile)

    def get_player_setting(self, playerfile, path):
        ''' Extract and return a player setting.'''
        player_dict = load(open(playerfile, 'r').read())
        elem = player_dict
        while '/' in path:
            next, path = path.split('/', 1)
            elem = elem[next]
        return elem[path]

    def update_player_setting(self, playerfile, path, value):
        ''' Update a setting in a given YAML file.'''
        player_dict = load(open(playerfile, 'r').read(), Loader=SafeLoader)
        elem = player_dict
        while '/' in path:
            next, path = path.split('/', 1)
            elem = elem[next]
        elem[path] = self.validate_input(value)
        open(playerfile, 'w').write(dump(player_dict))
        return 'Updated successfully!'

    def validate_input(self, value):
        ''' Generic numeric validator for YAML input.'''
        return int(value)
