# Parse the TkLayout cabling map file, to convert it to the format
# expected by this unpacker code.

def process_file(input_filename, output_filename):
    rows = []
    
    # Read the input file and collect the rows
    with open(input_filename, 'r') as infile:
        # Skip first 2 lines of documentation
        next(infile)
        next(infile)
      
        for line in infile:
            # Split the line by commas to get the three integers
            numbers = line.strip().split(',')
            first_integer = int(numbers[0])
            second_integer = int(numbers[1])
            third_integer = int(numbers[2])
            
            # Append a tuple of the three integers to the rows list
            rows.append((first_integer, second_integer, third_integer))
    
    # Sort the rows based on the third integer, then by the second integer if third integers are identical
    rows.sort(key=lambda x: (x[2], x[1]))
    
    # Write the sorted rows to the output file
    with open(output_filename, 'w') as outfile:
        for first_integer, second_integer, third_integer in rows:
            
            # Write the result to the output file
            outfile.write(f'{first_integer}  {third_integer}  {second_integer}\n')

#----- Main -----
input_filename = 'tkLayoutCablingRaw.txt'  # Replace with the name of your input file
output_filename = 'tkLayoutCabling.txt'  # Replace with the name of your desired output file
process_file(input_filename, output_filename)
