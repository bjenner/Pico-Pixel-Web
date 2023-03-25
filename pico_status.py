'''
pico_status.py = status of the device 
'''
from machine import ADC
import gc
from mylogging import safe_print
        
class PicoStatus:
    adc = ADC(4) 
    
    @classmethod
    def temperature(cls):
        ADC_voltage = cls.adc.read_u16() * (3.3 / (65535))
        temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
        temp_fahrenheit=32+(1.8*temperature_celcius)
        
        return temperature_celcius

    @classmethod
    def memory(cls):
        return round(gc.mem_free() / 1024)

if __name__ == "__main__":
    
    safe_print( f"Temp: { PicoStatus.temperature()  }" )
    safe_print( f"Mem: { PicoStatus.memory()  }" )
    

else:
    safe_print( __name__ + " imported")


