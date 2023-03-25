import switchcase
from mylogging import safe_print

def test_switchcase():
    test_cases = [
        ("red", "red"),
        ("green", "green"),
        ("blue", "blue"),
        ("yellow", "yellow")
    ]

    for input_color, expected_output in test_cases:
        output = switchcase_test(input_color)
        assert output == expected_output, f"Expected {expected_output}, but got {output}"
        safe_print(f"Test passed for input '{input_color}' with expected output '{expected_output}'")

def switchcase_test(colour):
    result = None
    while switchcase.switch(colour):
        if switchcase.case("red"):
            result = "red"
            break

        if switchcase.case("green"):
            result = "green"
            break

        if switchcase.case("blue"):
            result = "blue"
            break

        if switchcase.case("yellow"):
            result = "yellow"
            break
    return result

if __name__ == "__main__":
    safe_print("switchcase testing...")
    test_switchcase()
