#!/usr/bin/env python3

import gpiod
import time
import sys

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
    "S": 0.0, # Silence
    "C3": 130.81, # Do
    "C3#": 138.59, # Do#
    "D3": 146.83, # Re
    "D3#": 155.56, # Re#
    "E3": 164.81, # Mi
    "F3": 174.61, # Fa
    "F3#": 185.00, # Fa#
    "G3": 196.00, # Sol
    "G3#": 207.65, # Sol#
    "A3": 220.00, # La
    "A3#": 233.08, # La#
    "B3": 246.94, # Si
    "C4": 261.63, # Do
    "C4#": 277.18, # Do#
    "D4": 293.66, # Re
    "D4#": 311.13, # Re#
    "E4": 329.63, # Mi
    "F4": 349.23, # Fa
    "F4#": 370.00, # Fa#
    "G4": 392.00, # Sol
    "G4#": 415.30, # Sol#
    "A4": 440.00, # Standard tuning pitch (La)
    "A4#": 466.16, # La#
    "B4": 493.88, # Si
    "C5": 523.25, # Do
    "C5#": 554.37, # Do#
    "D5": 587.33, # Re
    "D5#": 622.25, # Re#
    "E5": 659.25, # Mi
    "F5": 698.46, # Fa
    "F5#": 739.99, # Fa#
    "G5": 783.99, # Sol
    "G5#": 830.61, # Sol#
    "A5": 880.00, # La
    "A5#": 932.33, # La#
    "B5": 987.77  # Si
}

def load_song(file_path: str) -> list:
    song = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                note, duration = line.strip().split(' ')
                song.append((note, float(duration)))
    except Exception as e:
        print(f"Error loading song in {file_path}: {e}")
    return song

def play_song(list_notes: list):
    try:
        for note, duration in list_notes:
            frequency = NOTE_FREQUENCIES.get(note)
            if frequency:
                play_frequency(frequency, duration)
                time.sleep(0.01) # Small delay between notes to distinguish them
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

# load notes
if len(sys.argv) < 2:
    print("Usage: python3 bitbeep.py <song_file>")
    sys.exit(1)
song_notes = load_song(sys.argv[1])

# play
try:
    print(f"Speaking on GPIO {BUZZER_LINE_OFFSET} (Ctrl+C to stop)")
    play_song(song_notes)

except KeyboardInterrupt:
    print("\nScript stopped by user.")

finally:
    # Cleanup: release the line and close the chip
    buzzer_line.release()
    chip.close()

