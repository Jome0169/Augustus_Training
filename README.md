# Augustus_Training

Augustus is a challenging software to use if you have no one to guide you
through the proper procedure when it comes to training genes. The scripts found in the pipeline hope to alleviate that, and make the process of creating a training set easier. 

These scripts expect a PASA ouptut protein file which will then be filtered
down in order to generate a conidate list of high quality represenatative genes
that can then be used to train agusutus and SNAP.


The standard process of these scripts goes as follows:

## Step 1: Isolate Complete Proteins
complete_gene_retriever.py - This outputs a fasta file of only COMPLETE
proteins as predicted by PASA. PASA reserves this mark for only genes with a
correct start and stop codon.

## Step 2: Blast Complete proteins versus known databases
These completed proteins should then be BLASTED against some known conserved
databases or closely related organisms. This will ensure proper identification
of "real" genes, and allow for better training later on. 

Combine all of your blast output using Cat, and then pass this BLAST as well as
fasta to strict_gene_isolation.py. NOTE: output format for blast MUST BE 6

## Step 3: Isolate genes with high percent identity and 80% of conserved gene length

Feed the blast and fasts into strict_gene_isolation.py - outputs genes that have at least a single good hit 80% gene length and 70% ID. 

## Step 4: Blast isolated genes versus themselves
This final FASTA list will then be BLASTED against itself. This is in order to remove duplicates genes. Duplicates could cause us to overtrain augustus, which could minimize it's capactiy to predict novel genes. Again, output format 6 for the blast

## Step 5: Pull out well the best gene set from gff3 file, and trian augustus

pull_uniq_genes.py - Takes in self vs self blast in outputfmt 6, and then
returns a good set of genes which will make up training set.

Finally feed this output and Gff3 file from PASA into the script
EditGenomeGff3.py. This will create the final trainig set of gff3 files used to
train Augustus.

And, that should be it!

