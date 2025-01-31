import glob, os, re
import math

final =""

os.chdir(os.path.dirname(os.path.dirname(__file__)))
for file in glob.glob("*"):
    if not os.path.splitext(file)[1] and os.path.isfile(file):

        # Good to go on this file, set state vars
        print(file)
        lineNumber = 0
        headerLastLine = False

        with open(file, 'r', encoding='UTF-8') as curFile:
            contents = curFile.read()

            match = re.search(r"\s*(?P<name>\S.*?)\n(?P<author>\S?.*?)\n+(?P<body>[\S\s]*)$", contents)
            final += "\\beginsong{"+match.group('name').strip().rstrip('\n')+"}"
            if match.group('author') and not (match.group('author').isspace()):
                final += "[by={"+match.group('author')+"}]"
            final += "\n"

            # Now the verses and then change them to chords
            working = re.sub(r"\s*(.+?\n)\s*?(?:\n+|$)", "\\\\beginverse\\n\\1\\\\endverse\\n", match.group('body'), 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            working = re.sub(r"\\beginverse\n([\(\[]Chorus[\)\]].*?)\n\\endverse", "\\\\beginchorus\\n\\1\\n\\\\endchorus", working, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            working = re.sub(r"^\s*\(chorus\)\s*\n", "\\\\endverse\\n\\\\beginchorus(Chorus)\\\\endchorus\\n\\\\beginverse\\n", working, 0, re.MULTILINE | re.IGNORECASE)
            working = re.sub(r"\\beginverse\n\\endverse", "", working, 0, re.MULTILINE | re.IGNORECASE)


            # replace hyphens
            working = re.sub(r"-", '{\\\\textendash}', working, 0, re.MULTILINE)

            # Replace chord flat symbols, then rewrite them
            working = re.sub(r"(?<=\([A-G])(bb?)(?=(?:(?:sus|maj|min|m|aug|dim)\d?)?(?:\d)?(?:/[A-G](?:##?|bb?)?)?\))", "&", working, 0, re.MULTILINE)
            final += re.sub(r"\(([A-G](##?|bb?)?((sus|maj|min|m|aug|dim)\d?)?(\d)?(/[A-G](##?|bb?)?)?)\)[^\S\r\n]?", "\\[\\1]", working, 0, re.MULTILINE)

            final+="\\endsong\n\n"


os.chdir(os.path.dirname(__file__))
f = open("autogenerated.tex", "w", encoding='UTF-8')
f.write(final)
f.close()