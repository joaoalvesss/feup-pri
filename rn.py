import os

# Define the base path
config_path = "config"

systems = ["simple", "improved", "advanced", "semantic"]
result_files = [f"results_sys{i}_trec.txt" for i in range(1, 6)]
queries = [f"qrels{i}.txt" for i in range(1, 6)]

# Function to read qrels file
def read_qrels(file_path):
    print(f"Attempting to read qrels file: {file_path}")  # Debugging log
    with open(file_path, "r") as f:
        return {line.strip() for line in f}

# Function to read results file and get all results
def read_results(file_path):
    print(f"Attempting to read results file: {file_path}")  # Debugging log
    with open(file_path, "r") as f:
        lines = f.readlines()
    return [line.split()[2] for line in lines]  # Return all document IDs

# Function to generate the LaTeX table for one query
def generate_table(query_index, top_results, qrels):
    table_header = r"""
\begin{table}[H]
    \centering
    \begin{tabular}{|c|c|}
    \hline
    \rowcolor[gray]{0.9} Rank & Relevance \\ \hline
    """
    table_footer = r"""
    \end{tabular}
    \caption{Relevance for all results for query """ + f"{query_index}" + r"""}
    \label{tab:query""" + f"{query_index}_results" + r"""}
\end{table}
    """

    # Find the maximum number of results for the system
    max_rows = len(top_results)

    rows = ""
    for rank in range(max_rows):
        row = [str(rank + 1)]  # Add the rank
        doc_id = top_results[rank]
        relevance = "R" if doc_id in qrels else "N"
        row.append(relevance)
        rows += " & ".join(row) + r" \\ \hline" + "\n"

    return table_header + rows + table_footer

# Main logic to process each query and corresponding system
tables = []
for query_index in range(1, 6):
    system = systems[query_index - 1]  # Match the system to the query index
    result_file = result_files[query_index - 1]

    system_path = os.path.join(config_path, system)

    # Qrels for the specific query
    qrels_file = os.path.join(system_path, "qrels", f"qrels{query_index}.txt")  # Updated path to include "qrels" subdirectory
    print(f"Checking qrels file: {os.path.abspath(qrels_file)}")  # Debugging log
    if not os.path.exists(qrels_file):
        print(f"Error: File not found - {qrels_file}")
        continue  # Skip if file doesn't exist
    qrels = read_qrels(qrels_file)

    # Results for the corresponding system
    result_file_path = os.path.join(system_path, "results", result_file)  # Updated path to include system subdirectory
    print(f"Checking results file: {os.path.abspath(result_file_path)}")  # Debugging log
    if not os.path.exists(result_file_path):
        print(f"Error: File not found - {result_file_path}")
        continue  # Skip if file doesn't exist
    top_results = read_results(result_file_path)

    # Generate LaTeX table for the query
    table = generate_table(query_index, top_results, qrels)
    tables.append(table)

# Write LaTeX tables to file
output_file = "latex_tables.tex"
with open(output_file, "w") as f:
    for table in tables:
        f.write(table + "\n\n")

print(f"LaTeX tables generated and saved to {output_file}")
