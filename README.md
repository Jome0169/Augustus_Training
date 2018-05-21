# Augustus_Training

Augustus is a challenging software to use if you have no one to guide you
through the process. The scripts found in this repo hope to create a simpler
use case for Augustus users seeking to create a training set. 

These scripts expect a PASA ouptut protein file which will then be filtered
down in order to generate a conidate list of high quality represenatative genes
that can then be used to train agusutus and SNAP.


The standard process of these scripts goes 

complete_gene_retriever.py - This outputs a fasta file of only COMPLETE
proteins as predicted by PASA. Accurate start and stop codongs.


These completed proteins in should then be BLASTED against some known conserved
databases or closely related organisms. Cat all of the outputs, which need to
be in blast output fmt 6, and then feed this information to the next script.

strict_gene_isolation.py - outputs genes that have at least a single good hit
80% gene length and 70% ID. This final FASTA list will then be BLASTED against
itself. This is in order to remove duplicates.

pull_uniq_genes.py - Takes in self vs self blast in outputfmt 6, and then
returns a good set of genes which will make up training set.

Finally feed this output and Gff3 file from PASA into the script
EditGenomeGff3. This will create the final trainig set of gff3 files used to
train Augustus.

And, that should be it!

