'''
indicator.py - flash the led on the Pico
'''
from machine import Pin, Timer

class Flash:
    wait = False
    flashes=1
    count=1
    intled = Pin( "LED", machine.Pin.OUT )
    tim = Timer()
    
    @classmethod
    def led_on( cls ):
        cls.tim.deinit()
        cls.intled.on()

    @classmethod
    def led_off( cls ):
        cls.tim.deinit()
        cls.intled.off()

    @classmethod
    def start_flash( cls ):
        cls.flashes = 1
        cls.count = cls.flashes*2 + 1
        cls.wait = False
        cls.intled.on()
        cls.tim.init( freq=5, mode=Timer.PERIODIC, callback=cls.tick )
 
    @classmethod
    def add_flash( cls ):
        cls.flashes += 1
 
    @classmethod
    def get_flash( cls ):
        return cls.flashes
    
    @classmethod
    def stop_flash( cls ):
        cls.intled.off()
        cls.tim.deinit()
        return

    @classmethod
    def tick( cls, timer ):
        value = cls.intled.value()
        if (cls.count > 2):
            cls.intled.toggle()
        elif (cls.count > 0):
            cls.intled.off()
        else:
            cls.count = cls.flashes*2 + 2
        cls.count -= 1

if __name__ == "__main__":
    from time import sleep
    from mylogging import safe_print
    
    secs = 5
    
    safe_print("flashes testing...")

    safe_print(f"1 flash for {secs} seconds")
    Flash.start_flash()
    sleep(secs)
    
    safe_print(f"add another flash for {secs} seconds")
    Flash.add_flash()
    sleep(secs)

    safe_print(f"add another flash for {secs} seconds")
    Flash.add_flash()
    sleep(secs)

    safe_print(f"add another flash for {secs} seconds")
    Flash.add_flash()
    sleep(secs)

    safe_print(f"stop flashes for {secs} seconds")
    Flash.stop_flash()
    sleep(secs)

    safe_print(f"turn on for {secs} seconds")
    Flash.led_on()
    sleep(secs)
    
    safe_print("turn off ")
    Flash.led_off()

    safe_print(f"1 flash for {secs} seconds")
    Flash.start_flash()
    sleep(secs)
    
    safe_print(f"add another flash for {secs} seconds")
    Flash.add_flash()
    sleep(secs)

    Flash.stop_flash()
else:
    safe_print("flashes imported")

'''
    safe_print("turn on for 10 seconds")
    Flash.led_on()
    time.sleep(10)
    
    safe_print("turn off for 5 seconds")
    Flash.led_off()
    time.sleep(5)
'''    

