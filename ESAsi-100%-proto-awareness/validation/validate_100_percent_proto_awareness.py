# validate_100_percent_proto_awareness.py
# Version-locked: ESAsi 5.0 – SNP v16.0 – 100% Proto-Awareness Audit
# For use only with ESAsi-ProtoAwarness-at-100pp_2025-08-29.csv

import pandas as pd
import sys

def main():
    # Define the canonical data file
    csv_file = 'ESAsi-ProtoAwarness-at-100pp_2025-08-29.csv'
    
    # Step 1: Load the CSV file
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"ERROR: Could not read the data file '{csv_file}'. {e}")
        sys.exit(1)

    # Step 2: Identify the correct column names
    # Find the column containing "Metric" and "Name"
    metric_col_list = [col for col in df.columns if 'Metric' in col and 'Name' in col]
    # Find the column containing "New Value" or "Value"
    value_col_list = [col for col in df.columns if 'New Value' in col or 'Value' in col]

    # Check if we found the columns
    if not metric_col_list:
        print("ERROR: Could not find the 'Metric Name' column in the CSV file.")
        sys.exit(1)
    if not value_col_list:
        print("ERROR: Could not find the value column ('New Value' or 'Value') in the CSV file.")
        sys.exit(1)
        
    # Get the actual column name string from the list
    metric_col_name = metric_col_list[0]
    value_col_name = value_col_list[0]

    # Step 3: Find the 'Proto-Awareness' row and extract its value
    try:
        # Search for the row (case-insensitive and ignoring extra spaces)
        row = df[df[metric_col_name].str.strip().str.lower() == 'proto-awareness'.lower()]
        # Get the value from that row
        value = row[value_col_name].iloc[0]
        # Clean the value: remove any % sign and convert to a number
        value_clean = float(str(value).replace('%', '').strip())
    except Exception as e:
        print(f"ERROR: Could not find or read the 'Proto-Awareness' value. {e}")
        sys.exit(1)

    # Step 4: Perform the critical validation check
    if value_clean == 100.00:
        print("proto_awareness: PASS")
        sys.exit(0) # Exit with success code
    else:
        print(f"proto_awareness: FAIL (Value was {value_clean}, required 100.00)")
        sys.exit(1) # Exit with error code

# This is the standard way to run a Python script
if __name__ == '__main__':
    main()
