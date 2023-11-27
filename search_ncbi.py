import requests

# Defines the function written to search for protein sequences chosen by the user
def search_ncbi_proteins(protein_family, taxonomic_group):
    # Constructs a query string for the NCBI ESearch API, using the URL for for the API. Params sets up the parameter for this search
    query = f"{protein_family}[ProtName] AND {taxonomic_group}[Organism]"
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "protein",
        "term": query,
        "retmode": "json"
    }

    # Sends a get request based on the defined parameters 
    search_response = requests.get(url, params=params)
    search_results = search_response.json()

    # Finds and extracts sequence IDs from the search result 
    id_list = search_results['esearchresult']['idlist']

    # Followed by fetch there is a loop that covers all the sequence IDs
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    sequences = []
    for id in id_list:
        fetch_params = {
            "db": "protein",
            "id": id,
            "rettype": "fasta",
            "retmode": "text"
        }
        fetch_response = requests.get(fetch_url, params=fetch_params)
        # Adds sequence to the growing list, return sends the ids back to the caller (NCBI)
        sequences.append(fetch_response.text)

    return sequences

# Function to save and print the sequences
def save_and_print_sequences(sequences, filename):
    with open(filename, 'w') as file:
        for sequence in sequences:
            print(sequence)
            file.write(sequence + "\n")

# User input for protein family and taxonomic group
protein_family = input("Enter the protein family: ")
taxonomic_group = input("Enter the taxonomic group: ")

# Fetches the protein sequences
sequences = search_ncbi_proteins(protein_family, taxonomic_group)

# Names and defines the format of the output file 
output_filename = "protein_sequences.txt"

# Saves the above defined file and prints the retrieved sequences
save_and_print_sequences(sequences, output_filename)

print(f"Protein sequences have been saved to {output_filename}")
