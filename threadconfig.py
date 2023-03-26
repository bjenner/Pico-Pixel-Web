'''
threadconfig - Thread Configuration
'''
from roles import Roles

class ThreadConf:
    primary_role = None
    secondary_role = None

    @classmethod
    def set_primary(cls, role):
        cls.primary_role = role

    @classmethod
    def set_secondary(cls, role):
        cls.secondary_role = role

    @classmethod
    def start_primary(cls):
        role_map = Roles.primary_map()
        role_map[cls.primary_role]()

    @classmethod
    def start_secondary(cls):
        role_map = Roles.secondary_map()
        role_map[cls.secondary_role]()

    @classmethod
    def get_roles(cls):
        return {"Primary Role": cls.primary_role,
                "Secondary Role": cls.secondary_role}

    @classmethod
    def save_roles(cls, roles):
        ThreadConf.set_primary(roles["Primary Role"])
        ThreadConf.set_secondary(roles["Secondary Role"])

    @classmethod
    def get_role_defaults(cls):
        return {"Primary Role": "test",
                "Secondary Role": 'none'}
