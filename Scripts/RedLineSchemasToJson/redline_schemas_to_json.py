import os
from os import path
import xmlschema
import json


CURR_SCRIPT_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.abspath(CURR_SCRIPT_DIR + r"\..\..")
REDLINE_SCHEMAS_DIR = path.join(ROOT_DIR, "RedLine Schemas", "Schemas")
OUTPUT_JSON = path.join(ROOT_DIR, "schemas_map.json")


def main():
    schemas_dict = {}
    for schem_dirname, schem_filename, schem_filepath in schemas_iter(REDLINE_SCHEMAS_DIR):
        if schem_dirname not in schemas_dict:
            schemas_dict[schem_dirname] = {}
            schemas_dict[schem_dirname]["fields"] = {}
        else:
            raise Exception(f"Duplicate schema dir name: {schem_dirname}")

        elements_list = get_xml_schema_data(schem_filepath)
        for element in elements_list:
            name = element['@name']
            schemas_dict[schem_dirname]["fields"][name] = {}
            schemas_dict[schem_dirname]["fields"][name]['maxOccurs'] = element.get('@maxOccurs')
            schemas_dict[schem_dirname]["fields"][name]['minOccurs'] = element.get('@minOccurs')
            schemas_dict[schem_dirname]["fields"][name]['nillable'] = element.get('@nillable')
            schemas_dict[schem_dirname]["fields"][name]['type'] = element.get('@type')

            schemas_dict[schem_dirname]["fields"][name]['description'] = ""
            schemas_dict[schem_dirname]["fields"][name]['ECS_name'] = "?"

    with open(OUTPUT_JSON, "w") as write_file:
        json.dump(schemas_dict, write_file, indent=4)


def get_xml_schema_data(schem_filepath):
    schem_xml_root = xmlschema.XMLSchema(schem_filepath)
    schem_dict = schem_xml_root.to_dict(schem_filepath)
    elements_list = schem_dict['xs:complexType'][0]['xs:complexContent'][
        'xs:extension']['xs:sequence']['xs:element']
    return elements_list


def schemas_iter(schemas_dir):
    for subdir, dirs, files in os.walk(REDLINE_SCHEMAS_DIR):
        for dir in dirs:
            files_in_dir = os.listdir(path.join(subdir, dir))
            if files_in_dir and files_in_dir[0].endswith(".xsd"):
                yield (
                    dir, # dir name
                    files_in_dir[0], # .xsd file name
                    path.abspath(path.join(subdir, dir, files_in_dir[0]))) # .xsd file path


if __name__== "__main__":
    main()