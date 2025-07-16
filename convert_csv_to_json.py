#!/usr/bin/env python3
import csv
import json
import sys
from collections import defaultdict
"""
This script converts csv formatted ticket titles to Limina CLI compliant json, allowing you to upload titles in bulk. 

Limina bulk CLI command: limina bulk-request-titles --ticket-titles-file titles.json
CSV input format: 
Category/Type/Item, Title
Category/Type/Item, Title
Category/Type/Item, Title
"""

def process_csv(input_file):

    # Use defaultdict to collect titles for each unique type/item combination
    cti_groups = defaultdict(list)
    
    with open(input_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        
        for row in reader:
            # Split the first column to get components
            column_parts = row[0].split(',')
            path_parts = column_parts[0].split('/')
            
            if len(path_parts) >= 2:
                # Extract type and item from path
                type_name = path_parts[1]
                item_name = path_parts[2] if len(path_parts) > 2 else "Other"
                cti_key = (type_name, item_name)
                
                # Add the alert text to this CTI's list
                if len(column_parts) > 1:
                    cti_groups[cti_key].append(column_parts[1])

    # Convert the grouped data to final JSON format
    json_data = []
    for (type_name, item_name), titles in cti_groups.items():
        entry = {
            "titles": titles,  # All titles for this CTI
            "category": "Network Reliability Engineering (NRE)",
            "type": type_name,
            "item": item_name,
            "justification": "Initial title additions"
        }
        json_data.append(entry)

    return json_data

def main():
    if len(sys.argv) != 2:
        print("Usage: ./script.py input.csv output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    json_data = process_csv(input_file)

    # Write the output JSON file with proper formatting
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=4)

    print(f"Processed {len(json_data)} unique type/item combinations")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
