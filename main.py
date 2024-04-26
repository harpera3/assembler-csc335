#############################################################################
# An assembler that converts hack language to binary
# For PR06 in CSC335
# Author: Alyssa Harper
#############################################################################

def stripfluff(line):
    # this takes all the symbols out of the line so symbol save doesn't get confused
    line = line.strip()
    line = line.split("//")[0]
    line = line.replace("/n", "")
    return line


def convertainstruction(x, SymbolLib, r):
    """
    Converts hack language A instructions
    :param x: the line in given file
    :param SymbolLib: A library of symbols that mimics how memory is set up
    :return: a binary number
    """

    x = x.replace("@", "")
    if x in SymbolLib:
        x = SymbolLib.get(x)
        x = int(x)
    else:
        x = int(x)

    binary = format(x, '016b')
    r.write(binary)
    r.write("\n")

    return binary


def convertcinstruction(x, destdict, compdict0, jumpdict, compdict1, r):
    """
    converts hack language to c instruction
    :param x: the line in given file
    :param destdict: a dictionary that saves hack destination binary
    :param compdict0: computation dictionary for hack (depends on a)
    :param jumpdict: a dictionary that saves hack jump language binary
    :param compdict1: computation dictionary for hack (depends on a)
    :return: a binary number
    """
    if "=" in x:  # for arithmatic instructions
        words = x.split("=")
        dest = destdict.get(words[0])
        JMP = "000"
        if "M" in words[1]:
            a = "1"
            comp = compdict1.get(words[1])
        else:
            a = "0"
            comp = compdict0.get(words[1])


    else:  # for jump instructions
        words = x.split(";")
        JMP = jumpdict.get(words[1])
        dest = "000"
        if "M" in words[0]:
            a = "1"
            comp = compdict1.get(words[0])
        else:
            a = "0"
            comp = compdict0.get(words[0])

    cbinary = "111" + a + comp + dest + JMP
    r.write(cbinary)
    r.write("\n")
    return cbinary


def symbolsave(f, SymbolLib, linenumber, value):
    for line in f:
        x = stripfluff(line)

        if x != "" and x.startswith("(") != True:
            linenumber = linenumber + 1

        if x.startswith("("):
            x = x.replace("(", "")
            x = x.replace(")", "")
            if x not in SymbolLib:
                SymbolLib[x] = linenumber
    f.seek(0,0)
    for line in f:
        x = stripfluff(line)
        if x.startswith("@"):
            x = x.replace("@", "")
            if x not in SymbolLib and x.isnumeric() is False:
                SymbolLib[x] = value
                value = value + 1

    return SymbolLib




def main():
    filename = input("please enter a filename")
    f = open(filename, "r")
    SymbolLib = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }  # symbol library from the text that mirrors how storage space is set up
    lineNumber = 0
    value = 16

    SymbolLib = symbolsave(f, SymbolLib, lineNumber,value)
    print(SymbolLib)

    compdict0 = {"0": "101010",
                 "1": "111111",
                 "-1": "111010",
                 "D": "001100",
                 "A": "110000",
                 "!D": "001101",
                 "!A": "110001",
                 "-D": "001111",
                 "-A": "110011",
                 "D+1": "011111",
                 "A+1": "110111",
                 "D-1": "001110",
                 "A-1": "110010",
                 "D+A": "000010",
                 "D-A": "010011",
                 "A-D": "000111",
                 "D&A": "000000",
                 "D|A": "010101"
                 }
    destdict = {"M": "001",
                "D": "010",
                "MD": "011",
                "A": "100",
                "AM": "101",
                "AD": "110",
                "AMD": "111"
                }
    jumpdict = {"JGT": "001",
                "JEQ": "010",
                "JGE": "011",
                "JLT": "100",
                "JNE": "101",
                "JLE": "110",
                "JMP": "111"}
    compdict1 = {"M": "110000",
                 "!M": "110001",
                 "-M": "110011",
                 "M+1": "110111",
                 "M-1": "110010",
                 "D+M": "000010",
                 "D-M": "010011",
                 "M-D": "000111",
                 "D&M": "000000",
                 "D|M": "010101"
                 }
    r = open("C:\\Users\\harpera3\\PycharmProjects\\assembler-csc335\\venv\\Scripts\\Prog.hack", "a")
    f = open(filename, "r")
    for line in f:
        x = stripfluff(line)

        if x.startswith("@"):
            convertainstruction(x, SymbolLib, r)
        elif x.startswith("(") or x == "":
            pass
        else:
            convertcinstruction(x, destdict, compdict0, jumpdict, compdict1, r)


main()
