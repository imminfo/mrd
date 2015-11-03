# Code for paper "???"

Scripts used for analysis MRD TCR clones in the paper [link](link will be here).

### Files with MRD TCR clones
- mrd_tcr_clones.txt
- mrd_tcr_table.txt

### Make a file with paths to repertoire files

    `build_links.py <file with input files>`

Example of file is `input_files.txt`. It consists of blocks with files for each individual:
    <path to the folder with individuals 1 and 2>
    #Individual_1
    file_1_1 pattern
    file_1_2 pattern
    #Individual_2
    file_2_1 pattern
    file_2_2 pattern
    }
    <path to the folder with individuals 3, etc.>
    ...

Resulting file will be `input_files.links.txt`.

### Search files (exact / fuzzy)

    `search_clones.py <file with links> <file with MRD clones> <optional postfix for the output file>`
    `fuzzy_search_clones.py <file with links> <file with MRD clones> <number of max errors (mism / indels)> <optional postfix for the output file>`

Output is a number of files with various information about the search results.

### Divide the search result to groups by hamming distance

    `extract_seq_vseg.py <search result with "lines" in the name from the previous function>`

Output is a number of files each corresponding to the specific hamming distance between one of the MRD clonal sequences and found sequence in the data.

### Perform Monte-Carlo based sampling to find the number of shared clonotypes

    `montecarlo.py <file with links> <output file name>`

From each file take a number of clones equal to the number of MRD clones and find in how many people they are occurred. Output is a tab-delimited files with number of occurrences for each try.

### Generate neighbor sequences and process their generation probabilities after computing
    
    `make_neighbors.py <file with MRD clones>`
    `process_neis_prob.py <resulting file from the previous script>`
