# Pico-Pixel-Web

This project controls Pixel Bullets using a Raspberry PI Pico. 

## External code

This project is only possible because of code from other projects. 

### Phew - install this library, used for website and logging
https://github.com/pimoroni/phew

### Phew Access Point - a more complete example
https://www.kevsrobots.com/blog/phew-access-point.html

### Ideas for multi-threading
https://bytesnbits.co.uk/multi-thread-coding-on-the-raspberry-pi-pico-in-micropython/

### Ideas for checking files in micropython
https://forum.micropython.org/viewtopic.php?t=8112

### Ideas for switchcase
https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python

### Ideas for cryptography
https://docs.micropython.org/en/latest/library/cryptolib.html

### GPT-4
All of the unit tests for this project were created by GPT-4 with very simple queries, for example

Me: please write unit tests for this micropython module without using unittest.mock.
<insert module text here>

GPT-4: To write Micropython unit tests for the colourwave module, you will need to create a separate test file, say test_colourwave.py, and use the unittest library available in Micropython. Since Micropython does not support the unittest.mock library, you can manually create mock functions for testing.
Here is an example of the test file for the colourwave module:
<text of unit test here> 

In this test file, we create a TestColourWave class that inherits from unittest.TestCase. We then use the setUp and tearDown methods to mock the time.sleep and Neopixel classes to avoid waiting and interacting with the hardware during the test. In the test_colourwave_role method, we test the colourwave_role function to ensure it does not raise any exceptions when executed.
To run the tests, you can import the test module and call unittest.run() in the Micropython REPL:

import test_colourwave
unittest.run(test_colourwave.TestColourWave)

Keep in mind that the test case here is quite limited as we are only checking if the function does not raise any exceptions. Due to the nature of the module, it's challenging to test the actual behavior of the hardware without proper mocking and integration tests.
