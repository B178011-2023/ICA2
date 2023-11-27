# Imports the modules for running external commands and os dependent functionalities
import subprocess
import os

# Defines a function called run_plotcon to run plotcon for conservation analysis
def run_plotcon(input_file, output_file, plot_file_base, winsize):
    try:
        # Checks if the input file exists using the os.path.exists
        if not os.path.exists(input_file):
            # Error trap to print an error message if the input file does not exist
            print(f"Error: Input file '{input_file}' does not exist.")
            return False

        # Constructs the filename for the PostScript (.ps) output of the plotcon tool
        plot_file_ps = f"{plot_file_base}.ps"

        # Executes the plotcon command with the specified parameters using subprocess, '-sequences' represents the input file, '-winsize' for the window size with a string to inser the window size selected by the user,'-graph' 'postscript' defines the output format, finally '-goutfile' for the output file.'capture_output=True' registers the command output, 'text=True' interprets the output as text, 'check=True' flags an error signal if the command fails.
        result = subprocess.run(['plotcon', '-sequences', input_file, '-winsize', str(winsize), '-graph', 'postscript', '-goutfile', plot_file_base], capture_output=True, text=True, check=True)

        # Opens the output file for writing
        with open(output_file, 'w') as file:
            # Writees and prints the results
            file.write(result.stdout)
        print(result.stdout)

        # Tries to open the .ps file with Evince for graphical viewing, evince was used because it is installed on the server that the client will use. However, often evince generates its own error message before this error trap can be implemented. Essentially, asking the user to use an environment that evince can utilise, like a GUI.
        try:
            subprocess.run(['evince', plot_file_ps])
        except Exception:
            # Command to print an error message if evince fails to open the file
            print("Unable to open the plot file with Evince. This may be due to the absence of a graphical environment. Use -X to enable X11 forwarding if running pipeline on a remote server.")

        # Informs the user of the status/success of their command and the name of the outputted .ps file 
        print(f"Conservation analysis completed. Plot saved as '{plot_file_ps}'.")
        return True

    # Except is used to catch the situation which prompts the error message under the print command. This is achieved via subprocess.
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during running plotcon: {e}")
        return False

# Defines the main function and the names and formats of the input and output files.
def main():
    input_filename = "clustalo_aligned.txt"
    output_filename = "conservation_analysis.txt"
    plot_file_base = "conservation_plot"

    # Here a while loop is used allow to repeatedly prompt for a valid window size
    while True:
        try:
            winsize = int(input("Enter the window size for conservation analysis (The positive integer here will represent the conservation score being calculated after the inputted number of residues. This affects the sensitivity and specificity of the conservation analysis while impacting the runtime of this script. Suggestion: use smaller value for proteins with shorter sequence and bigger values for longer protein sequences.): "))
               
            # Checks if the entered winsize is positive, while printing an error if not.
            if winsize <= 0:
                print("Please enter a positive integer.")
            else:
                # Breaks the loop if valid input is entered to continue with the rest of the script.
                break
        # Catches error via ValueError if the input is not a positive integer
        except ValueError:
            # Prints an error message for invalid input
            print("Invalid input. Please enter a positive integer.")

    # Calls the run_plotcon function, validates if it was successful and prints a status message of success to the user.
    if not run_plotcon(input_filename, output_filename, plot_file_base, winsize):
        print("Plotcon analysis failed.")

# Ensures that the main script is being run directly as with previous scripts.
if __name__ == "__main__":
    main()
