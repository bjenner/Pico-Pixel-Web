from mylogging import safe_print

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

if __name__ == "__main__":
    
    safe_print("switchcase testing...")
    for colour in ('red', 'green', 'blue'):
        while switch( colour ):
            if case( 'red' ):
                safe_print( "red" )
                break
            
            if case( 'green' ):
                safe_print( "green" )
                break

            if case( 'blue' ):
                safe_print( "blue" )
                break
            
            if case( 'yellow' ):
                safe_print( "yellow" )
                break

else:
    safe_print( __name__ + " imported")


