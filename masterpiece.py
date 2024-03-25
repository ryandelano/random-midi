# -*- coding: utf-8 -*-

import json

from midiutil.MidiFile import MIDIFile

from randomnote import RandomNote


class Masterpiece(object):
    def __init__(self, rules_path="rules.json", length=4, tempo=90):
        self.rules_path = rules_path
        self.length = length
        self.tempo = tempo

        rules_file = open(rules_path, "r")
        rules = json.load(rules_file)
        rules_file.close()
        self.rhythm = rules["rhythm"]
        self.velocity = rules["velocity"]
        self.rn = RandomNote(rules["notes"], rules["interval_upper"], rules["interval_lower"])

        self.MyMIDI = MIDIFile(3)
        self.current_track_number = 0

    def create_melody_sequence(self):
        seq_melody = []
        for i in range(self.length):
            for phrase in self.rhythm:
                self.rn.reset()
                for duration in phrase:
                    seq_melody.append((self.rn.random_note(), duration))
        return seq_melody

    def create_melody_track(self):
        seq_melody = self.create_melody_sequence()

        self.MyMIDI.addTrackName(
            track=self.current_track_number,
            time=0, trackName="piano")
        self.MyMIDI.addTempo(
            track=self.current_track_number,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.current_track_number,
            channel=0, time=0, program=0)

        pos = 0
        for pitch, duration in seq_melody:
            relative_pos = pos - int(pos / 4) * 4
            if 0 <= relative_pos < 1:
                vol = self.velocity["strong"]
            elif 2 <= relative_pos < 3:
                vol = self.velocity["intermediate"]
            else:
                vol = self.velocity["weak"]
            self.MyMIDI.addNote(
                track=self.current_track_number,
                channel=0, pitch=pitch, time=pos, duration=duration, volume=vol)
            if relative_pos in [0, 2]:
                self.MyMIDI.addControllerEvent(
                    track=self.current_track_number,
                    channel=0, time=pos, controller_number=64, parameter=127)
                self.MyMIDI.addControllerEvent(
                    track=self.current_track_number,
                    channel=0, time=pos + 1.96875, controller_number=64, parameter=0)
            pos += duration
        self.current_track_number += 1

        # C  D  E  F  G  A  B  | C  D  E  F  G  A  B  | C
        # 48 50 52 53 55 57 59 | 60 62 64 65 67 69 71 | 72
    def create_midi_file(self, filename, melody=True, chord=True, perc=True):
        if melody:
            self.create_melody_track()

        with open(filename, "wb") as midi_file:
            self.MyMIDI.writeFile(midi_file)
