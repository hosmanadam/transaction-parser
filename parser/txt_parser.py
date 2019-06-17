from parser.regexes import *


def parse_txt(txt):
    regex = re.compile(RE_ENTRY)
    entries = [match.groupdict() for match in regex.finditer(txt)]
    return entries
