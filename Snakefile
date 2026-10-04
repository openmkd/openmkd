rule all:
    input:
        "protein_protonated.pqr"

rule protein_alignment:
    input:
        "experimental_opm_protein.pdb",
        "alphafold_protein.pdb"
    output:
        "protein_aligned.pdb"
    shell:
        "pixi run -e protein-alignment USalign alphafold_protein.pdb experimental_opm_protein.pdb -o protein_aligned"

rule protein_protonation:
    input:
        "protein_aligned.pdb"
    output:
        "protein_protonated.pqr"
    shell:
        "pixi run -e protein-protonation pdb2pqr --ff AMBER --with-ph 7.4 protein_aligned.pdb protein_protonated.pqr"
