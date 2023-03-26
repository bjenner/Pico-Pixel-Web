"""
role.py - map of role functions
"""

from mylogging import safe_print
import colourwave
import fireflies
import smoothrainbow
import trail
import testroles


def dummy_role():
    print("dummy")
    while True:
        pass


class Roles:
    map = {
        'primary': {
            'test': testroles.test_primary,
            'web': dummy_role,
            'none': dummy_role
        },
        'secondary': {
            'test': testroles.test_secondary,
            'fireflies': fireflies.firefly_role,
            'colourwave': colourwave.colourwave_role,
            'trail': trail.trail_role,
            'rainbow': smoothrainbow.rainbow_role,
            'none': dummy_role
        }
    }

    @classmethod
    def set_role(cls, thread, name, role):
        safe_print(f"Setting {thread} role to {name} with fn {role}")
        cls.map[thread][name] = role

    webmap = {
        "primary":
            [
                {"label": "Test Primary",
                 "id": "test_prim",
                 "value": "test",
                 "checked": ""},
                {"label": "Web Server",
                 "id": "web_prim",
                 "value": "web",
                 "checked": ""},
                {"label": "Dummy Primary",
                 "id": "dumb_prim",
                 "value": "none",
                 "checked": ""},
            ],
        "secondary":
            [
                {"label": "Test Secondary",
                 "id": "test_sec",
                 "value": "test",
                 "checked": ""},
                {"label": "Fireflies",
                 "id": "firefly_sec",
                 "value": "fireflies",
                 "checked": ""},
                {"label": "Colour Wave",
                 "id": "colour_sec",
                 "value": "colourwave",
                 "checked": ""},
                {"label": "Pixel Trail",
                 "id": "trail_sec",
                 "value": "trail",
                 "checked": ""},
                {"label": "Smooth Rainbow Pixels",
                 "id": "smooth_sec",
                 "value": "rainbow",
                 "checked": ""},
                {"label": "Dummy Secondary",
                 "id": "dumb_sec",
                 "value": "none",
                 "checked": ""},
            ]
    }

    @classmethod
    def set_checked(cls, primary, secondary):
        def update_checked(thread, current):
            safe_print("thread " + thread)
            safe_print("current " + current)
            for item in cls.webmap[thread]:
                if item['value'] == current:
                    item['checked'] = "checked"
                else:
                    item['checked'] = ""
                safe_print(item)

        update_checked('primary', primary)
        update_checked('secondary', secondary)

        safe_print("done")

    @classmethod
    def get_webmap(cls):
        return cls.webmap

    @classmethod
    def default_primary(cls):
        return dummy_role

    @classmethod
    def default_secondary(cls):
        return dummy_role

    @classmethod
    def primary_map(cls):
        return cls.map['primary']

    @classmethod
    def secondary_map(cls):
        return cls.map['secondary']

    @classmethod
    def check_role(cls, thread, role, fn):
        current = cls.map[thread][role]
        if current == fn:
            safe_print("match")
        else:
            safe_print("no match")

    
if __name__ == "__main__":

    safe_print( "default primary" )
    safe_print( Roles.default_primary() )
    
    safe_print( "default secondmary" )
    safe_print( Roles.default_secondary() )
                
    safe_print( "primary map" )
    safe_print( Roles.primary_map() )

    safe_print( "secondary map" )
    safe_print( Roles.secondary_map() )
    
    Roles.set_checked( "test", "rainbow" )
    
    def foo():
        pass
    
    Roles.set_role( "primary", "web", foo )
    Roles.check_role( "primary", "web", foo )
    
else:
    safe_print( "roles imported")


