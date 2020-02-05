from os import path
from io import StringIO
import csv
import json


CURR_SCRIPT_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.abspath(CURR_SCRIPT_DIR + r"\..\..")
MAP_JSON = path.join(ROOT_DIR, "schemas_map.json")
INPUT_CSV = path.join(ROOT_DIR, "schemas_map.csv")

FIELDS_TYPES = {
    'schema_name': str,
    'field_name': str,
    'ECS_name': str,
    'type': str,
    'maxOccurs': int,
    'minOccurs': int,
    'nillable': bool,
    'description': str,
}

def main():
    # TODO: Raise warning if last change in json is newer than last csv change

    json_map_data = read_json(MAP_JSON)
    csv_dicts_list = read_csv_to_dicts_list(INPUT_CSV)
    is_updated = False

    for row_dict in csv_dicts_list:
        schema_name = row_dict['schema_name']
        if not schema_name:
            continue
        if schema_name not in json_map_data:
            print(f"* WARNING: schema name: {schema_name} not in json. skipped.")
            continue

        field_name = row_dict['field_name']
        if field_name not in json_map_data[schema_name]['fields']:
            print(f"* WARNING: field name: {field_name} not in the schema {schema_name} in json. skipped.")
            continue
        
        for property_name, property_val in row_dict.items():
            if property_name == 'schema_name' or property_name == 'field_name':
                continue

            if property_name not in json_map_data[schema_name]['fields'][field_name]:
                print(f"* WARNING: property name: {schema_name}.{field_name}.{property_name} not in json . skipped.")
                continue

            if not are_csv_and_json_values_equal(
                csv_val=property_val,
                json_val=json_map_data[schema_name]['fields'][field_name][property_name]
                ):
                print(f"Update value of {schema_name}.{field_name}.{property_name} to: {property_val}")
                json_map_data[schema_name]['fields'][field_name][property_name] = (
                    convert_csv_value_to_json_value(property_val, property_name))
                is_updated = True

    if is_updated:
        with open(MAP_JSON, "w", encoding='utf-8') as write_file:
            json.dump(json_map_data, write_file, indent=4, ensure_ascii=False)


def read_json(json_path):
    with open(json_path, encoding='utf-8') as json_file:
        json_map_data = json.load(json_file)
        return json_map_data


def read_csv_to_dicts_list(csv_path):
    with open(csv_path, encoding='utf-8') as f:
        csv_dicts_list = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
        return csv_dicts_list

def are_csv_and_json_values_equal(csv_val, json_val):
    if csv_val == json_val:
        return True

    if not csv_val and not json_val:
        return True

    json_val_as_csv_str = convert_value_to_csv_string_value(json_val)
    csv_val_as_str = f"{csv_val}"

    if json_val_as_csv_str == csv_val_as_str:
        return True
    if json_val_as_csv_str.lower() == csv_val_as_str.lower():
        if json_val_as_csv_str.lower() in ("true", "false"):
            return True
    return False

def convert_csv_value_to_json_value(csv_value, csv_property_name):
    if csv_property_name not in FIELDS_TYPES:
        return csv_value
    csv_property_type = FIELDS_TYPES[csv_property_name]
    if csv_property_type == int:
        try:
            return int(csv_value)
        except ValueError: # Probably the value: "unbounded"
            return csv_value
    elif csv_property_type == bool:
        if f"{csv_value}".lower() == "false":
            return False
        elif f"{csv_value}".lower() == "true":
            return True
    return csv_value

def convert_value_to_csv_string_value(value):
    output = StringIO()
    writer = csv.writer(output, lineterminator="")
    writer.writerow([value])
    return output.getvalue()



if __name__== "__main__":
    main()