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
buzzer_line = chip.get_line(BUZZER_LINE_OFFSET)

# Request the line as an output
buzzer_line.request(consumer="bitbeep", type=gpiod.LINE_REQ_DIR_OUT)

try:
    print(f"Speaking on GPIO {BUZZER_LINE_OFFSET} (Ctrl+C to stop)")
    while True:
        buzzer_line.set_value(1)
        time.sleep(BUZZER_DELAY_SEC)
        buzzer_line.set_value(0)
        time.sleep(BUZZER_DELAY_SEC)

except KeyboardInterrupt:
    print("\nScript stopped by user.")

finally:
    # Cleanup: release the line and close the chip
    buzzer_line.release()
    chip.close()

