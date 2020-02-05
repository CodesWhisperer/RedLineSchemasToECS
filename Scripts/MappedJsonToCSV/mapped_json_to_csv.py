from os import path
from collections import OrderedDict
import csv
import json


CURR_SCRIPT_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.abspath(CURR_SCRIPT_DIR + r"\..\..")
INPUT_JSON = path.join(ROOT_DIR, "schemas_map.json")
OUTPUT_CSV = path.join(ROOT_DIR, "schemas_map3.csv")

def main():
    # TODO: Raise warning if last change in csv is newer than last json change

    with open(INPUT_JSON) as input_json_file, open(OUTPUT_CSV, 'w') as write_csv_file:
        json_map_data = json.load(input_json_file)

        flat_map_list = []
        for schem_dirname, schem_values in json_map_data.items():
            for fname, fproperties in schem_values["fields"].items():
                flat_map_list.append(OrderedDict([
                    ('schema_name', schem_dirname),
                    ('field_name', fname),
                    ('ECS_name', fproperties['ECS_name']),
                    ('type', fproperties['type']),
                    ('maxOccurs', fproperties['maxOccurs']),
                    ('minOccurs', fproperties['minOccurs']),
                    ('nillable', fproperties['nillable']),
                    ('description', fproperties['description']),
                ]))

        # Write to csv
        keys = flat_map_list[0].keys()
        writer = csv.DictWriter(write_csv_file, keys)
        writer.writeheader()
        writer.writerows(flat_map_list)


if __name__== "__main__":
    main()