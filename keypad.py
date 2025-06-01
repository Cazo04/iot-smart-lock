import RPi.GPIO as GPIO
import time
import subprocess

ROW_PINS = [0, 5, 6, 13]
COL_PINS = [25, 8, 7, 1]

KEY_MAP = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

DEBOUNCE_MS = 50
PIN_OUT = 2
EXTERNAL_SCRIPT_CMD = ["python3", "app.py"]

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in ROW_PINS:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
    for pin in COL_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def pulse_pin():
    GPIO.setup(PIN_OUT, GPIO.OUT)
    GPIO.output(PIN_OUT, GPIO.LOW)
    time.sleep(1.5)
    GPIO.setup(PIN_OUT, GPIO.IN)

def validate_pin(pin_str):
    # Change this to your actual PIN validation logic
    return "ok" if pin_str == "123456" else "fail"

def run_external_script():
    try:
        completed = subprocess.run(
            EXTERNAL_SCRIPT_CMD, capture_output=True, text=True, timeout=30
        )
        return completed.stdout.strip().lower()
    except Exception as e:
        print(f"Error running external script: {e}")
        return "error"

def handle_result(result):
    if result == "ok":
        print("Unlock")
        pulse_pin()
    else:
        print("Result:", result)
    print("Press A to enter PIN or B to run script")

def scan_keypad():
    for r_idx, r_pin in enumerate(ROW_PINS):
        GPIO.output(r_pin, GPIO.LOW)
        time.sleep(0.0005)
        for c_idx, c_pin in enumerate(COL_PINS):
            if GPIO.input(c_pin) == GPIO.LOW:
                time.sleep(DEBOUNCE_MS / 1000)
                while GPIO.input(c_pin) == GPIO.LOW:
                    pass
                GPIO.output(r_pin, GPIO.HIGH)
                return KEY_MAP[r_idx][c_idx]
        GPIO.output(r_pin, GPIO.HIGH)
    return None

def main():
    setup_gpio()
    mode = "idle"
    pin_buffer = []
    print("Press A to enter PIN or B to run script")
    try:
        while True:
            key = scan_keypad()
            if not key:
                time.sleep(0.01)
                continue

            if mode == "idle":
                if key == 'A':
                    mode = "pin"
                    pin_buffer = []
                    print("Enter 6-digit PIN")
                elif key == 'B':
                    result = run_external_script()
                    handle_result(result)
            elif mode == "pin":
                if key.isdigit():
                    pin_buffer.append(key)
                    print("*", end="", flush=True)
                    # Check if we have 6 digits
                    if len(pin_buffer) == 6:
                        print()
                        result = validate_pin("".join(pin_buffer))
                        handle_result(result)
                        mode = "idle"
                elif key == 'C':
                    pin_buffer = []
                    print("\nPIN cleared")
                elif key == 'D':
                    print("\nOperation cancelled")
                    print("Press A to enter PIN or B to run script")
                    mode = "idle"
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nExiting")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
