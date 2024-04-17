import os
import json
import time
from datetime import datetime


from masterpiece import Masterpiece
from librosa import note_to_midi

if __name__ == "__main__":
    dtime = datetime.now()
    ans_time = time.mktime(dtime.timetuple())
    params_file = open("song_settings.json", "r")
    params = json.load(params_file)
    params_file.close()

    # write notes into rules.json
    notes = []
    durations = []
    while True:
        print("Welcome to the note input interface!")
        note = input("Enter a note [q to end]: ")
        if note == 'q':
            break
        duration = input("Enter a duration for that note (as a float, how many beats you want that note to be) [q to end]: ")

        if duration == "q":
            break
        os.system("clear")

        notes.append(note_to_midi(f'{note}4'))
        try:
            durations.append(float(duration))
        except ValueError:
            print("Invalid input for duration. Please try again.")
            continue

    print(notes)
    if len(notes) != len(durations):
        print("The number of notes and durations do not match. Please try again.")
        exit(1)

    if len(notes) == 0:
        print("You did not enter any notes. Please try again.")
        exit(1)

    '''
    Insert model and get results here here
    '''

    with open("rules.json", "r") as f:
        rules = json.load(f)

    rules["notes"] = notes
    rules["rhythm"] = [durations]
    # rules["seq_chord"] = from model

    with open("rules.json", "w") as f:
        json.dump(rules, f)

    my_masterpiece = Masterpiece(
        rules_path="rules.json",
        length=params["length"],
        tempo=params["tempo"])
    subfolder = "output"

    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)

    my_masterpiece.create_midi_file("{folder}/midi_{suffix}.mid".format(
        folder=subfolder,
        suffix=ans_time))