import csv
import os

##########################################################
#
#   Post Processing Script for Simulation Data
#
##########################################################

def process_csv(input_file):
    # Generate the output filename
    base_name, extension = os.path.splitext(input_file)
    output_file = base_name + "_processed" + extension

    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Process and write header
        header = next(reader)
        writer.writerow(header)

        for row in reader:
            # Process each non-header row
            processed_row = []
            for idx, cell in enumerate(row):
                if idx == 0 or cell.strip()[0].isalpha():  # For the first column do not remove letters or percent signs
                    processed_row.append(cell.strip())
                else:
                    processed_row.append(''.join(char for char in cell if char.isdigit() or char == '.'))

            writer.writerow(processed_row)

    print(f"File '{input_file}' processed and saved as '{output_file}'")

if __name__ == '__main__':   
    batch_size = 16
    i = 0
    while i < batch_size:
        process_csv("hpc_metrics_" + str(i) + ".csv")
        i += 1

