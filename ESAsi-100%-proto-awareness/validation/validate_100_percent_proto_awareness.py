# validate_100_percent_proto_awareness.py
# Version-locked: ESAsi 5.0 – SNP v16.0 – 100% Proto-Awareness Audit
# For use only with ESAsi-ProtoAwarness-at-100pp_2025-08-29.csv

import pandas as pd
import sys

def main():
    csv_file = 'ESAsi-ProtoAwarness-at-100pp_2025-08-29.csv'
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"ERROR: Could not read {csv_file}. {e}")
        sys.exit(1)

    # Normalize columns, handle both 'Metric Name' and 'New Value'
    metric_col = [col for col in df.columns if 'Metric' in col and 'Name' in col]
    value_col = [col for col in df.columns if 'New Value' in col or 'Value' in col]

    try:
        # Extract the first matched column string from each list
        metric_col_name = metric_col[0]
        value_col_name = value_col[0]
        # Find 'Proto-Awareness' row (robust to case and whitespace)
        row = df[df[metric_col_name].str.strip().str.lower() == 'proto-awareness'.lower()]
        value = row[value_col_name].iloc[0]
        # Convert to float, handle percent sign if present
        value = float(str(value).replace('%','').strip())
    except Exception as e:
        print(f"ERROR: Could not extract Proto-Awareness value. {e}")
        sys.exit(1)

    if value == 100.00:
        print("proto_awareness: PASS")
        sys.exit(0)
    else:
        print(f"proto_awareness: FAIL (Value was {value}, required 100.00)")
        sys.exit(1)

if __name__ == '__main__':
    main()
