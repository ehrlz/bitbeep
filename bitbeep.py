#!/usr/bin/env python3

import gpiod
import time

# Configuration for Physical Pin PC5
# GPIO Line calcs
# Port | ID
#  A   | 0
#  B   | 1
#  C   | 2
#  D   | 3

# gpiochip0 is port A
# gpiochip1 is port B, C & D
# (run gpiodetect in terminal)

CHIP = 'gpiochip1'  # The GPIO chip name
BUZZER_LINE_OFFSET = 69  # PC5 GPIO number = (port_id * 32) + pin_number

# Musical notes to frequency
NOTE_FREQUENCIES = {
    "C4": 261.63, # Do
    "D4": 293.66, # Re
    "E4": 329.63, # Mi
    "F4": 349.23, # Fa
    "G4": 392.00, # Sol
    "A4": 440.00, # Standard tuning pitch (La)
    "B4": 493.88, # Si
    "C5": 523.25, # Do
    "D5": 587.33, # Re
    "E5": 659.25, # Mi
    "F5": 698.46, # Fa
    "G5": 783.99, # Sol
    "A5": 880.00, # La
    "B5": 987.77  # Si

}

# Himno de la alegría
SONG_OF_JOY = [
    ("B4", 0.5), ("B4", 0.5), ("C5", 0.5), ("D5", 0.5), ("D5", 0.5), ("C5", 0.5), ("B4", 0.5), ("A4", 0.5),
    ("G4", 0.5), ("G4", 0.5), ("A4", 0.5), ("B4", 0.5), ("B4", 0.75), ("A4", 0.5), ("A4", 1.0)
]

def play_song(list_notes: list):
    try:
        for note, duration in list_notes:
            frequency = NOTE_FREQUENCIES.get(note)
            if frequency:
                play_frequency(frequency, duration)
                time.sleep(0.04) # Small delay between notes to distinguish them
    except KeyboardInterrupt:
        print("\nSong playback stopped by user.")

def play_frequency(frequency: float, duration: float):
    period = 1.0 / frequency
    half_period = period / 2

    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        buzzer_line.set_value(1)
        time.sleep(half_period)
        buzzer_line.set_value(0)
        time.sleep(half_period)

# Get the GPIO chip and line
chip = gpiod.Chip(CHIP)
buzzer_line = chip.get_line(BUZZER_LINE_OFFSET)

# Request the line as an output
buzzer_line.request(consumer="bitbeep", type=gpiod.LINE_REQ_DIR_OUT)

try:
    print(f"Speaking on GPIO {BUZZER_LINE_OFFSET} (Ctrl+C to stop)")
    play_song(SONG_OF_JOY)

except KeyboardInterrupt:
    print("\nScript stopped by user.")

finally:
    # Cleanup: release the line and close the chip
    buzzer_line.release()
    chip.close()

