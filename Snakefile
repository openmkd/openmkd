rule all:
    input:
        "protein_aligned.pdb"

rule protein_alignment:
    input:
        "experimental_opm_protein.pdb",
        "alphafold_protein.pdb"
    output:
        "protein_aligned.pdb"
    shell:
        "pixi run -e protein-alignment USalign alphafold_protein.pdb experimental_opm_protein.pdb -o protein_aligned"
