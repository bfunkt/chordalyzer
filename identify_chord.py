
"""
base_quality sets
    -{5}
        major (no tag necessary)
   
    if-{4,7}
        if [10] dim
        elif [11] m7b5
        if [12] dim(maj7)
    elif-{4}
        minor
     -{9}
        if [8] - this is a b13
        else - aug/+/#5
    -{6}
        

    -{}
    -{}
    -{}
    -{}

semitone interval
    -[8]  major 3rd, always
    -1
        tonic
    -2
        b9, always
        if [3] in chord, [2] should read "add b9" in the upper extensions
    -3
        9, always
    -4
        if [5] in chord, [4] is "#9"
        elif [7] in chord && neither [8](perfect 5th) nor [11](dom7), base_quality is "dim"
        elif [7] in chord && [11] in chord, base_quality is "half-dim"(m7b5)
        else, base_quality is "m"
    -5
    -6
    -7
    -9
    -10
    -11
    -12

base_quality
    -[_]   (Major, no marked quality)  (optionally, "M"?)
        single note only,
        perfect 5th [8], 
        can contain Major 3rd [5]
        notate as "M", rather than [_] under the following conditions:
            -
            -
    -m
        must contain [4]
        must NOT contain [5] (else it is a b9)
    -dim
        must contain [7]
        can contain [4] (likely)
        must NOT contain [8] (else it is a #11)
        must NOT contain [11] (else base_quality is 'half-dim')
    -half-dim (m7b5)  # possibly use UTF-16 char(248) to indicate half-dim
    -aug 
    -sus

extensions
    -9th
        9
        #9
        b9
    -11th
        11
        #11
    -13th
        6
        b6
        13
        b13



"""


def check_9(chord, extensions):
    # b9
    if 4 in chord:
        extensions.append("#9")
        #add b9
        if 2 in chord:
            extensions.append("b9")
    # 9
    elif 3 in chord:
        extensions.append("9")
    # b9
    elif 2 in chord:
        extensions.append("b9")

    return(extensions)



def run_rules(chord):
    base_quality = ""
    extensions = []

    # dominant7 or maj7 
    if 11 in chord:
        extensions.append("7")
    elif 12 in chord:
        extensions.append("maj7")

    # 9th
    extensions = check_9(chord, extensions)




def identify(raw_list):
    if len(raw_list) == 0:
        return None

    #remove duplicate tones
    tones = list(set(raw_list))

    #store the chord notes and root value totals for each inversion
    #tone_test_data = { 19:[{1,5,8,9),10] }
    tone_test_data = {}
    #once the root tone has been determined, chord_tonic will be assigned (tone[root] % 12)
    chord_data = { "root_tone":0,
                    "root_weight":0,
                    "base_quality":"",
                    "extensions":[]     }

    for tone in tones:
        #create the chord in 1 octave, with potential root=1
        chord = set( [ ((x+12-(tone%12))%12)+1 for x in tones] )

        #get the root_weight
        rw = sum([root_weight_points[x] for x in chord])

        #store data on each tone
        tone_test_data[tone] = [chord, rw, "root weight={0}".format(rw)] 

        #set chord_data if root_weight is highest
        if rw > chord_data["root_weight"]:
            #store the new root tone (1-12), used to identify the tonic key to be attached to the chord (e.g.   2 = "Bb")
            chord_data["root_tone"] = tone % 12
            chord_data["root_weight"] = rw

    print("The chord tonic is {0}, with a root_weight of {1}.".format(note_names[chord_data["root_tone"]], chord_data["root_weight"]))
    print("\n")
    for t in tone_test_data.items():
        print(t)

#paired as {scale semitone:value}  where the highest total semitone values per chord should indicate root tone
root_weight_points = {  1:0,
                        8:5, 
                        4:3, 
                        5:3, 
                        11:3,
                        12:2,
                        3:1,
                        6:1,
                        10:1,
                        2:0,
                        7:0,
                        9:0    }


note_names = {  0:"Ab",
                1:"A",
                2:"Bb",
                3:"B",
                4:"C",
                5:"C#",
                6:"D",
                7:"Eb",
                8:"E",
                9:"F",
                10:"F#",
                11:"G",
                12:"Ab"   }
