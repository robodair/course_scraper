import argparse
import fileinput
from pathlib import Path
import json

def check_sets(sets, units, filter_text, debug):
    for s in sets:
        if filter_text and filter_text.lower() not in s["title"].lower():
            continue
        entitled = True
        met_requirements = []
        unmet_requirements = []
        if debug:
            print("-- Checking", s['title'])
        for r in s['requirements']:
            code = r.split('-')[0].strip()
            if not units.get(code, None):
                if debug:
                    print("--- Missing unit", r)
                # Failure - requirements not met
                entitled = False
                unmet_requirements += [r]
            else:
                if debug:
                    print("--- Found unit", r)
                met_requirements += [r]

        if entitled:
            # wow, entitled to a unit set!
            if not s['requirements']:
                print("* Found Unit Set:", s["title"], "Caveat: This unit set's requirements were empty, it is likely restricted")
            elif 'restricted' in s["title"].lower():
                print("* Found Unit Set:", s["title"], "Caveat: This unit set looks to be restricted")
            else:
                print("Found Unit Set:", s["title"])
            print('==================')
        elif len(unmet_requirements) < 3:
            print("CLOSE:", s["title"], "\n >> unmet requirements:\n ", "\n  ".join(unmet_requirements))
            print('==================')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("units_file", type=Path,
                        help="file with each unit on a new line, unit code needs to be the first part of each line, seperated from a comment to describe the unit by any amount of whitespace")
    parser.add_argument("set_json", type=Path, nargs="+",
                        help="scraped json files of unit sets")
    parser.add_argument("-f", "--filter", default=None)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    units = {}
    for line in args.units_file.read_text().splitlines():
        units[line.split()[0]] = line

    all_sets = [json.loads(pth.read_text()) for pth in args.set_json]
    print()
    for sets in all_sets:
        check_sets(sets, units, args.filter, args.debug)

if __name__ == "__main__":
    main()