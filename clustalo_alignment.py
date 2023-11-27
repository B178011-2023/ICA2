# Imports the subprocess and the os modules for running external and os dependent functionalities
import subprocess
import os
# Defines a function called run_clstalo that uses an input file and generates an output file
def run_clustalo(input_file, output_file):
    try:
        # If not checks if the input file exists via the os.path.exists command, the error trap is created which informs the user where the error originates.
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' does not exist.")
            return False

        # Runs clustalo command using the subprocess module, -I and -o define the input and output, the fasta file format is chosen despite changing it to the .txt file format later in the script for simplicity. A status update is generated for the user.
        subprocess.run(['clustalo', '-i', input_file, '-o', output_file, '--outfmt=fasta'], check=True)
        print(f"Alignment completed successfully. Output saved to '{output_file}'.")
        return True

    # This error trap handles exceptions by informing the user the the alignment has failed.
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during alignment: {e}")
        return False
# As with the previous script, this defines the main function that will be executed along with the file names and formats for the output and the input.
def main():
    input_filename = "protein_sequences.txt"
    output_filename = "clustalo_aligned.txt"

    # This clustalo command runs the alignment
    run_clustalo(input_filename, output_filename)

# Checks is the main function is being run directly and calls it to execute the script
if __name__ == "__main__":
    main()
