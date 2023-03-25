'''
mylogging.py
'''
import _thread
from phew import logging

sLock = _thread.allocate_lock()

# it would seem that the phew logging function is not thread safe
def safe_print( message ):

    sLock.acquire()
    logging.debug( message )
    sLock.release()

if __name__ == "__main__":
    safe_print("logging test...")

else:
    logging.debug( "logging imported")


