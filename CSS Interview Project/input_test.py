import string

def process_input(input):
    tokens = input.split(" ")
    print(tokens, end=" ")

    operation = ""
    sequence = ""
    type = ""
    direction = ""
    output = ""

    #ERROR
    if tokens[0] == "E" and len(tokens) == 2:
        if len(tokens[1]) == 2 and all(c in string.hexdigits for c in tokens[1]):   #Sequence number
            sequence = tokens[1]
            print(f"ECHO sequence: {sequence}")
    #POWER
    elif tokens[0] == "P" and len(tokens) == 3:
        if all(c in string.hexdigits for c in tokens[1]):   #Sequence number
            if tokens[2] in ['1', '0']:                     #State
                print("POWER")
    #INPUT
    elif tokens[0] == "I" and len(tokens) == 3:
        if len(tokens[1]) == 2 and all(c in string.hexdigits for c in tokens[1]):   #Sequence number
            sequence = tokens[1]
            if len(tokens[2]) == 4:
                if tokens[2][0] in ["A", "D"]:              #Type
                    if tokens[2][1] in ["I", "O"]:          #Direction
                        type = tokens[2][0]
                        direction = tokens[2][1]
                        if all(c in string.hexdigits for c in tokens[2][2:]):   #Channel
                            channel = tokens[2][2:]
                            print(f"INPUT seq: {sequence} type: {type} direction: {direction} channel: {channel}")
    #OUTPUT
    elif tokens[0] == "O" and len(tokens) == 4:
        if len(tokens[1]) == 2 and all(c in string.hexdigits for c in tokens[1]):   #Sequence number
            sequence = tokens[1]
            if len(tokens[2]) == 4:
                if tokens[2][:2] in ["AO", "DO"]:              #Type
                        type = tokens[2][:2]
                        if all(c in string.hexdigits for c in tokens[2][2:]):   #Channel
                            channel = channel = tokens[2][2:]
                            if type == "AO" and  len(tokens[3]) == 8 and all(c in string.hexdigits for c in tokens[3]):  #Analogue Output
                                output = tokens[3]
                                print(f"ANALOGUE OUTPUT seq: {sequence} type: {type} channel: {channel} output: {output}")
                            elif type == "DO" and len(tokens[3]) == 1 and tokens[3] in ["0", "1"]:                       #Digital Output
                                output = tokens[3]
                                print(f"DIGITAL OUTPUT seq: {sequence} type: {type} channel: {channel} output: {output}")

    else: print("NO MATCH")

process_input("E 15")
process_input("E ff")
process_input("E x1")
print("\n")
process_input("I 01 AI01")
process_input("I 55 AO01")
process_input("I ff DIff")  # invalid
process_input("I cc DO22")
process_input("I xx DO22")
process_input("I cc SO22")
process_input("I cc DF12")
process_input("I cc DOgg")

print("\n")
process_input("O 03 AO01 00000005")
process_input("O 06 AO02 ffffffff")
process_input("O 06 AO02 fffffff")
print("\n")
process_input("O 10 DO05 1")
process_input("O FF DOf2 0")  # invalid
print("\n")
process_input("P 04 1")
process_input("P ff 0")
process_input("P 25 5")  # invalid

print("\n")
process_input("d d d fdfsd  sdfsd ")
process_input("d fdf d")
process_input("d sdf d")  # invalid