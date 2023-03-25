import trail
from mylogging import safe_print

def test_trail_step():
    try:
        strip = trail.get_strip()
        initial_pixels = strip.get_pixels()  # Get the initial state of the strip

        for i in range(10):  # Execute trail_step() 10 times
            trail.trail_step()

        final_pixels = strip.get_pixels()  # Get the final state of the strip

        # Check if the strip has been updated
        assert initial_pixels != final_pixels, "Strip not updated"

        safe_print("Test passed for trail_step()")
    except Exception as e:
        safe_print(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_trail_step()
