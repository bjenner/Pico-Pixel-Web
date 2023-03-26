'''
test_role.py - just a couple of sample threads
'''
from time import sleep

from controls import Flag
from mylogging import safe_print

# Thread zero runs the primary role
def test_primary():
    
    safe_print( "Starting the primary role" )
    
    while True:
        safe_print( "Primary sleeping..." )
        sleep( 5 )
        
        safe_print( "Signal secondary" )
        Flag.set_run_flag()
        
        safe_print( "Primary waiting..." )
        sleep( 5 )
        
        safe_print( "Primary stopping secondary" )
        Flag.clear_run_flag()
    
# thread one runs the secondary role
def test_secondary():
    
    safe_print( "Starting the secondary role" )
    
    while True:
        
        # wait for primary role to signal
        safe_print( "Secondary role waiting..." )
        while not Flag.get_run_flag():
            pass
        
        safe_print( "Secondary role running..." )
        sleep( 1 )
            
        if not Flag.get_run_flag():
            safe_print( "Secondary role sleeping..." )

if __name__ == "__main__":

    import _thread
    import machine

    thread_one = _thread.start_new_thread(test_secondary, ())
    test_primary()

else:
    safe_print( "test_roles imported")


