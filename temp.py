# load chord_to_chords.json
import json
import pickle
from pprint import pprint

# load chord_to_chords.json
rules_file = open("chord_to_chords.json")
rules = json.load(rules_file)
rules_file.close()

print(type(rules))

# find all chords that have the same midi_notes list


chord_to_chords = {}
for chord, midi_notes in rules.items():
    midi_notes_str = json.dumps(midi_notes, sort_keys=True)
    if midi_notes_str in chord_to_chords:
        chord_to_chords[midi_notes_str].append(chord)
    else:
        chord_to_chords[midi_notes_str] = [chord]

matching_tuples = []
for midi_notes_str, chords in chord_to_chords.items():
    if len(chords) > 1:
        matching_tuples.append([chord for chord in chords])
print(matching_tuples)

with open("chords_to_map.pkl", "rb") as f:
    chord_to_map = pickle.load(f)

# match the matching tuples to the chord_to_map
matching_chords = []
for matching_tuple in matching_tuples:
    matching_chords.append([chord_to_map[chord] for chord in matching_tuple])

# dump the matching chords into a pickle file
with open("matching_chords.pkl", "wb") as f:
    pickle.dump(matching_chords, f)
    

