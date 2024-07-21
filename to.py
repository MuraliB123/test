import json

# Function to parse the text file
def parse_diff_output(file_path):
    data = {
        "Reference Database": "",
        "Comparison Database": "",
        "Compared Schemas": "",
        "Product Name": "",
        "Product Version": "",
        "Missing Catalog(s)": [],
        "Unexpected Catalog(s)": [],
        "Changed Catalog(s)": {},
        "Missing Check Constraint(s)": [],
        "Unexpected Check Constraint(s)": [],
        "Changed Check Constraint(s)": [],
        "Missing Column(s)": [],
        "Unexpected Column(s)": [],
        "Changed Column(s)": [],
        "Missing Database Package(s)": [],
        "Unexpected Database Package(s)": [],
        "Changed Database Package(s)": [],
        "Missing Database Package Body(s)": [],
        "Unexpected Database Package Body(s)": [],
        "Changed Database Package Body(s)": [],
        "Missing Foreign Key(s)": [],
        "Unexpected Foreign Key(s)": [],
        "Changed Foreign Key(s)": [],
        "Missing Function(s)": [],
        "Unexpected Function(s)": [],
        "Changed Function(s)": [],
        "Missing Index(s)": [],
        "Unexpected Index(s)": [],
        "Changed Index(s)": [],
        "Missing Primary Key(s)": [],
        "Unexpected Primary Key(s)": [],
        "Changed Primary Key(s)": [],
        "Missing Schema(s)": [],
        "Unexpected Schema(s)": [],
        "Changed Schema(s)": [],
        "Missing Sequence(s)": [],
        "Unexpected Sequence(s)": [],
        "Changed Sequence(s)": [],
        "Missing Stored Procedure(s)": [],
        "Unexpected Stored Procedure(s)": [],
        "Changed Stored Procedure(s)": [],
        "Missing Synonym(s)": [],
        "Unexpected Synonym(s)": [],
        "Changed Synonym(s)": [],
        "Missing Table(s)": [],
        "Unexpected Table(s)": [],
        "Changed Table(s)": [],
        "Missing Trigger(s)": [],
        "Unexpected Trigger(s)": [],
        "Changed Trigger(s)": [],
        "Missing Unique Constraint(s)": [],
        "Unexpected Unique Constraint(s)": [],
        "Changed Unique Constraint(s)": [],
        "Missing View(s)": [],
        "Unexpected View(s)": [],
        "Changed View(s)": []
    }
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_section = None
    change_name = None
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("Reference Database:"):
            data["Reference Database"] = line.split(": ", 1)[1]
        elif line.startswith("Comparison Database:"):
            data["Comparison Database"] = line.split(": ", 1)[1]
        elif line.startswith("Compared Schemas:"):
            data["Compared Schemas"] = line.split(": ", 1)[1]
        elif line.startswith("Product Name:"):
            data["Product Name"] = line.split(": ", 1)[1]
        elif line.startswith("Product Version:"):
            data["Product Version"] = line.split(": ", 1)[1]
        elif line.endswith(": NONE"):
            current_section = line[:-6]
            data[current_section] = "NONE"
        elif line.endswith(":"):
            current_section = line[:-1]
            change_name = None
        elif current_section and line:
            if current_section in ["Changed Catalog(s)", "Changed Check Constraint(s)", "Changed Column(s)", "Changed Database Package(s)", "Changed Database Package Body(s)", "Changed Foreign Key(s)", "Changed Function(s)", "Changed Index(s)", "Changed Primary Key(s)", "Changed Schema(s)", "Changed Sequence(s)", "Changed Stored Procedure(s)", "Changed Synonym(s)", "Changed Table(s)", "Changed Trigger(s)", "Changed Unique Constraint(s)", "Changed View(s)"]:
                if "changed from" in line:
                    key, value = line.split(" changed from '", 1)
                    value = value[:-1]  # Remove the trailing quote
                    if change_name:
                        data[current_section][change_name] = {key: value}
                    else:
                        data[current_section][key] = value
                else:
                    change_name = line
                    data[current_section][change_name] = {}
            else:
                print(current_section,line)
                data[current_section].append(line)
    
    return data

# Convert to JSON
def convert_to_json(file_path, output_path):
    data = parse_diff_output(file_path)
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
input_file = 'output.txt'
output_file = 'output.json'
convert_to_json(input_file, output_file)
