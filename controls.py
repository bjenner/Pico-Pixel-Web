'''
controls.py - a nice class to control the secondary thread

'''
from mylogging import safe_print

class Flag:
    run_second_core = False
    
    @classmethod
    def set_run_flag(cls):
        cls.run_second_core = True
 
    @classmethod
    def clear_run_flag(cls):
        cls.run_second_core = False
 
    @classmethod
    def get_run_flag(cls):
        return cls.run_second_core

if __name__ == "__main__":
    safe_print("controls testing...")

    safe_print("Initial value")
    safe_print("run flag {}".format(Flag.get_run_flag()))   

    safe_print("set flag")
    Flag.set_run_flag()
    safe_print("run flag {}".format(Flag.get_run_flag()))   

    safe_print("clear flag")
    Flag.clear_run_flag()
    safe_print("run flag {}".format(Flag.get_run_flag()))   

else:
    safe_print("controls imported")
