from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize
from dimorphite_dl import protonate_smiles

tautomer_enumerator = rdMolStandardize.TautomerEnumerator()
molecule_microstates = []

with open("ligand.smi", "r") as f:
    ligand_smiles = f.read()

molecule = Chem.MolFromSmiles(ligand_smiles)

# a canonical tautomer is a single tautomer that all tautomers will become following canonicalization
canonical_molecule = tautomer_enumerator.Canonicalize(molecule)
molecule_tautomers = tautomer_enumerator.Enumerate(canonical_molecule)

for tautomer_index, tautomer in enumerate(molecule_tautomers):
    tautomer_microstates = protonate_smiles(
        Chem.MolToSmiles(tautomer), ph_min=7.4, ph_max=7.4
    )

    for microstate_index, tautomer_microstate in enumerate(tautomer_microstates):
        molecule_microstates.append({"id": f"t{tautomer_index}p{microstate_index}", "smiles": tautomer_microstate})

with Chem.SDWriter("ligands.sdf") as writer:
    for molecule_microstate in molecule_microstates:
        rdkit_microstate = Chem.MolFromSmiles(molecule_microstate["smiles"])
        rdkit_microstate = Chem.AddHs(rdkit_microstate)
        AllChem.EmbedMolecule(rdkit_microstate)
        AllChem.MMFFOptimizeMolecule(rdkit_microstate)
        writer.write(rdkit_microstate)        
