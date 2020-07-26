#!/usr/bin/env python3
from math import log2

# Based on AudioLazy module (https://pythonhosted.org/audiolazy/index.html)
MIDI_A4 = 69                      # MIDI Pitch number
FREQ_A4 = 440.                    # Hz
SEMITONE_RATIO = 2. ** (1. / 12.) # Ascending

# From https://en.wikibooks.org/wiki/X86_Assembly/Programmable_Interval_Timer
PIT_FREQ = 0x1234de

# Bytes taken from card dump
bytes_from_badge = [0x20bd,0x3bfa,0x20bd,0x2345,0x2772,0x2409,0x21c9,0x20bd]


# Based on AudioLazy module (https://pythonhosted.org/audiolazy/index.html)
def midi2str(midi_number):
    num = midi_number - (4 * 12 - 9)
    note = (num + .5) % 12 - .5
    rnote = int(round(note))
    error = note - rnote
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    names = names[rnote]
    # Modified from error < 1e-4 to reduce the "sensitivity" (this is the 
    # reason why I can't use Audiolazy module directly)
    if abs(error) < 1e-2:
        return names
    else:
        # This is not a "pure" note
        return "KK"

# Based on AudioLazy module (https://pythonhosted.org/audiolazy/index.html)
def freq2note(freq):
    return midi2str(12 * (log2(freq) - log2(FREQ_A4)))


if __name__ == "__main__":
    # We only care about printable chars range (0x20-0x7e)
    #
    # As we already have the bytes sent to PIT's channel 2 (bytes from the badge
    # xored with the unknown key ), we must calculate the frequencies associated
    # with them. According to the formula:
    #
    #   counter = (PIT frequency )/( frequency you want)
    #
    # then frequency = (PIT frequency) / (xored bytes from badge)
    # (http://heim.ifi.uio.no/~inf3150/grupper/1/pcspeaker.html)
    for i in range (0x2000,0x7eff):
        notes = ""
        for bytes in bytes_from_badge:
            try:
                notes += freq2note(PIT_FREQ / (bytes ^ i))
            except:
                pass

        # Print only frequencies that resulted in "pure" notes
        if (notes.find('KK') == -1):
            print ("Using key %s (%c%c): %s" %  (
             hex(i), chr(int(hex(i)[2:4], 16)), chr(int(hex(i)[4:6], 16)), notes
            ))
