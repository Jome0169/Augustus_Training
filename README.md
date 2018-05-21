# Augustus_Training

Augustus is a challenging software to use if you have no one to guide you
through the process. The scripts found in this repo hope to create a simpler
use case for Augustus users seeking to create a training set. 

These scripts expect a PASA ouptut protein file which will then be filtered
down in order to generate a conidate list of high quality represenatative genes
that can then be used to train agusutus and SNAP.


The standard process of these scripts goes 



complete_gene_retriever.py

(BLAST vs conserved known databases)


strict_gene_isolation.py

Blast output against itself, and feed into  pull_uniq_genes.py

Finally feed this output and Gff3 file from PASA into the script
EditGenomeGff3. This will create the final trainig set of gff3 files used to
train Augustus


