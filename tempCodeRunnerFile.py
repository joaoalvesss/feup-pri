    rows = ""
    for rank in range(max_rows):
        row = [str(rank + 1)]  # Add the rank
        for system in systems:
            # Handle cases where a system has fewer results
            if rank < len(top_results[system]):
                doc_id = top_results[system][rank]
                relevance = "R" if doc_id in qrels[system] else "N"
            else:
                relevance = "-"  # Placeholder for missing results
            row.append(relevance)
        rows += " & ".join(row) + r" \\ \hline" + "\n"

    return table_header + rows + table_footer