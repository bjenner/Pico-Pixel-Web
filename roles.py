'''
role.py - map of role functions
'''
from mylogging import safe_print

import colourwave
import fireflies
import smoothrainbow
import trail
import test_roles

def dummy_role():
    print("dummy")
    while True:
        pass

class Roles:
        
    map = {
        'primary': {
            'test': test_roles.test_primary,
            'none': dummy_role
        },
        'secondary': {
            'test': test_roles.test_secondary,
            'fireflies': fireflies.firefly_role,
            'colourwave': colourwave.colourwave_role,
            'trail': trail.trail_role,
            'rainbow': smoothrainbow.rainbow_role,
            'none': dummy_role
        }
    }
    '''        
    <input type="radio" id="{{ webmap[0]['id']" name="secondary" value="{{ webmap[0]['value']">
    <label for="secondary">{{ webmap[0]['label'] }}</label><br>
    <label for="secondary">Firefly Pixels</label><br>
    <input type="radio" id="colourwave_sec" name="secondary" value="colourwave">
    <label for="secondary">Colour Wave Pixels</label><br>
    <input type="radio" id="trail_sec" name="secondary" value="trail">
    <label for="secondary">Pixel Trail</label><br>
    <input type="radio" id="rainbow_sec" name="secondary" value="rainbow">
    <label for="secondary">Smooth Rainbow Pixels</label><br>
'''
    webmap = [
        { "label": "Test Secondary",
          "id": "secondary",
          "value": "test"} ]
    @classmethod
    def get_webmap( cls ):
        return cls.webmap
    
    @classmethod
    def default_primary(cls):
        return dummy_role
    
    @classmethod
    def default_secondary(cls):
        return dummy_role
    
    @classmethod
    def primary_map(cls):
        return( cls.map['primary'] )
    
    @classmethod
    def secondary_map(cls):
        return( cls.map['secondary'] )
    
if __name__ == "__main__":

    safe_print( "default primary" )
    safe_print( Roles.default_primary() )
    
    safe_print( "default secondmary" )
    safe_print( Roles.default_secondary() )
                
    safe_print( "primary map" )
    safe_print( Roles.primary_map() )

    safe_print( "secondary map" )
    safe_print( Roles.secondary_map() )
    
else:
    safe_print( "roles imported")


