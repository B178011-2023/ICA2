# Imports the subprocess and the os modules for running external and os dependent functionalities
import subprocess
import os

# Defines the function which runs the patmatmotifs tool from the EMBOSS suite of tools 
def run_patmatmotifs(input_file, output_file):
    with open(output_file, 'w') as outfile:
        subprocess.run(['patmatmotifs', input_file, output_file], stdout=outfile)

# Defines the function which runs the profit tool from the EMBOSS suite of tools 
def run_profit(input_file, motif, output_file):
    with open(output_file, 'w') as outfile:
        subprocess.run(['profit', '-sequence', input_file, '-motif', motif], stdout=outfile)

# Defines the ‘main’ function that contains the filenames and formats for the input and output files
def main():
    input_filename = "protein_sequences.txt"
    prosite_output_filename = "PROSITE_results.txt"
    profit_output_filename = "profit_results.txt"

    # Runs patmatmotifs tool using the input file, informs the user about the status of the function
    run_patmatmotifs(input_filename, prosite_output_filename)
    print(f"PROSITE analysis results saved to {prosite_output_filename}")

    # Asks user if they want to run profit, with a simple Y/N response allowing flexibility to reference against a particular motif, runs and >
    user_response = input("Do you want to run profit for a specific motif? (Y/N): ")
    if user_response.upper() == 'Y':
        motif = input("Enter the motif for profit analysis: ")
        run_profit(input_filename, motif, profit_output_filename)
        print(f"PROFIT analysis results saved to {profit_output_filename}")

# Checks if the main function is being run directly and calls it to execute the script
if __name__ == "__main__":
    main()
