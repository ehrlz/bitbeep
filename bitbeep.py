#!/usr/bin/env python3

import gpiod
import time

# Configuration for Physical Pin PC5
CHIP = 'gpiochip1'  # The GPIO chip name
BUZZER_LINE_OFFSET = 69  # The Linux GPIO number for physical pin PC5

# Frequency settings
BUZZER_DELAY_SEC = 0.001  # Time in seconds between toggles

# Get the GPIO chip and line
chip = gpiod.Chip(CHIP)
led_line = chip.get_line(LED_LINE_OFFSET)

# Request the line as an output
led_line.request(consumer="bitbeep", type=gpiod.LINE_REQ_DIR_OUT)

try:
    print(f"Speaking on GPIO {LED_LINE_OFFSET} (Ctrl+C to stop)")
    while True:
        led_line.set_value(1)
        time.sleep(BLINK_DELAY_SEC)
        led_line.set_value(0)
        time.sleep(BLINK_DELAY_SEC)

except KeyboardInterrupt:
    print("\nScript stopped by user.")

finally:
    # Cleanup: release the line and close the chip
    led_line.release()
    chip.close()

