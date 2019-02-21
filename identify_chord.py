def identify(input=[]):
    if len(input) == 0:
        return None

    chord_position = 10000
    chord_tonic = None

    for tone in input:
        chord = set( [ ((x+12-(tone%12))%12)+1 for x in input] )
        print(chord)
        if chord in chords:
            chord_position = min(chord_position, chords.index(chord))
            chord_tonic = tone

    return chord_position, chord_tonic

#come up with a better way to 
#1. search by set (or tup)
#2. return a priority index to rule out less-likely chords
#3. also return the chord name, "C#m7"

#currently returns (position, tonic)

chords = [ {1}, {1,4}, {1,5}, {1,8}, {1,11}, {1,12}  ]
