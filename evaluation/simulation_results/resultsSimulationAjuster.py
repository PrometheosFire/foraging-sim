import csv
import sys

def increment_simulation(input_file, output_file, increment):
    with open(input_file, mode='r', newline='') as infile, \
         open(output_file, mode='w', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        if 'Simulation' not in fieldnames:
            raise ValueError("Missing 'Simulation' column in CSV.")

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                row['Simulation'] = str(int(row['Simulation']) + increment)
            except ValueError:
                print(f"Warning: Skipping invalid Simulation value: {row['Simulation']}")
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input.csv output.csv increment")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    try:
        increment_value = int(sys.argv[3])
    except ValueError:
        print("Increment value must be an integer.")
        sys.exit(1)

    increment_simulation(input_csv, output_csv, increment_value)
