# Computational Modeling Pipeline for the Na⁺/Cl⁻ Cotransporter (NCC)

## Abstract

Computational protein modeling is a cornerstone of modern biomedical engineering, providing atomic-level structural insights that can accelerate drug discovery. We present a project-based pipeline that guides researchers through:

1. Sequence retrieval  
2. Structure prediction using four methods:
   - **AlphaFold v3**  
   - **RoseTTAFold** via the Robetta server  
   - **SWISS-MODEL**  
   - **MODELLER**  
3. Model refinement with **RosettaRelax**  
4. Validation with **MolProbity** and **UCSF ChimeraX**  

This workflow was applied to the thiazide-sensitive Na⁺/Cl⁻ cotransporter (NCC), a membrane protein critical for renal sodium homeostasis and blood pressure regulation—and the target of thiazide diuretic drugs. We generated high-quality models of both human and eel NCC. Models show strong convergence: monomer backbone RMSDs < 2 Å and dimer RMSDs < 3 Å across methods. All methods captured the central ion-binding (thiazide) pocket; method-specific features emerged (e.g. an extra peripheral pocket predicted by RoseTTAFold and a secondary inter-subunit cavity seen in SWISS-MODEL’s dimer). CavityPlus analysis consistently identified three main cavities: a central orthosteric site, an alternative pocket near Ala542, and a dimer-interface cavity. AlphaFold v3 achieved >98% residues in favored Ramachandran regions after refinement and faithfully reproduced the drug-binding pocket. This integrated approach highlights each tool’s strengths and differences and provides a robust foundation for future NCC studies and rational inhibitor design. **All model data** (simulation files, top-ranked PDBs, ChimeraX sessions, cavity analyses) are available via Google Drive in this repository.

---

## AlphaFold v3 (DeepMind)

**AlphaFold v3** (Multimer) is an AI-driven predictor from DeepMind, achieving top performance in CASP. It uses deep neural networks to predict 3D structures from sequence alone.

- **Usage**  
  - Requires significant GPU/TPU compute.  
  - Install the open-source package or use cloud services.  
  - To model a homodimer, place two FASTA entries (one per chain) in a single file.  
- **Outputs**  
  - PDB coordinates  
  - Per-residue **pLDDT** confidence scores  
  - **PAE** matrix for domain uncertainty  
- **Pros**  
  - Unprecedented accuracy without templates  
  - Handles large, complex proteins  
- **Cons**  
  - Does not model bound ligands/cofactors  
  - High computational cost  

All AlphaFold models were refined with RosettaRelax and passed MolProbity validation (≥98% favored residues).

---

## SWISS-MODEL (Homology Modeling)

**SWISS-MODEL** creates models by aligning your sequence to PDB template structures.

- **Usage**  
  - Submit FASTA on the SWISS-MODEL web server.  
  - Optionally select specific templates or use the automatic “Project Mode.”  
- **Outputs**  
  - One PDB per template  
  - **GMQE** and **QMEAN** quality scores  
- **Pros**  
  - Easy, no install required  
  - Integrates with UniProt for sequence lookup  
- **Cons**  
  - Accuracy depends on template identity  
  - Limited if no close homolog exists  

We retrieved 5 monomer and 5 dimer models per species, refined with RosettaRelax, and validated with MolProbity.

---

## Robetta Server (RoseTTAFold)

**RoseTTAFold** (Baker lab) uses a three-track neural network to predict structures.

- **Usage**  
  - Submit the FASTA sequence on the Robetta server  
  - Select RoseTTAFold mode  
- **Outputs**  
  - One PDB per job  
- **Pros**  
  - Accurate without templates  
  - No local install needed  
- **Cons**  
  - Currently supports monomers only  
  - No built-in pLDDT/PAE scores  

We generated 5 monomer models for each NCC variant, refined them, and validated externally.

---

## MODELLER (Comparative Modeling)

**MODELLER** builds models by satisfying spatial restraints from target-template alignments.

- **Usage**  
  - Install MODELLER (academic license)  
  - Prepare a Python script with your PIR/FASTA alignment to templates  
  - Run “automodel” to generate multiple PDBs  
- **Pros**  
  - Customizable templates and restraints  
  - Good for loop modeling and mutations  
- **Cons**  
  - Requires scripting skill  
  - Limited atomic-level refinement (hence RosettaRelax follow-up)  

We produced 5 monomer and 5 dimer models per species using the same templates as SWISS-MODEL, then refined and validated them.

---

## Pipeline Overview

1. **Retrieve Sequence**  
   - Human NCC (UniProt P55017), Eel NCC (Q2PDH2) in FASTA  
2. **Model Generation**  
   - **Template-based**: SWISS-MODEL, MODELLER  
   - **AI-based**: AlphaFold v3 (multimer), RoseTTAFold (monomer)  
   - Generate ≥5 models per method per condition  
3. **Initial Validation**  
   - Upload to **MolProbity**  
   - Record Ramachandran favored %, clashscore, rotamer outliers  
   - Visual inspection in ChimeraX/PyMOL  
4. **Refinement (RosettaRelax)**  
   - Run Relax (local or via ROSIE)  
   - Re-validate in MolProbity  
5. **Cavity Detection (CavityPlus)**  
   - Submit refined PDBs to CavityPlus  
   - Extract cavity volumes, SASA, DrugScore  
   - Identify central, alternative (Ala542), and interface cavities  
6. **Comparative Analysis**  
   - Align models in ChimeraX (MatchMaker)  
   - Compute backbone RMSD heatmaps (<2 Å monomers; <3 Å dimers)  
   - Compare conserved vs. unique features  
   - Rank models by combined quality metrics  
7. **Conclusions & Next Steps**  
   - Consensus pockets guide docking or mutagenesis studies  
   - Share scripts and data for reproducibility  

---
