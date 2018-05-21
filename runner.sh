set -euxo pipefail

python CompleteGeneRetriever.py ${1}

for i in `cat $2` ; do 
    makeblastdb -in ${i} -dbtype prot ; 
done


for i in `cat $2` ; do 
    basename=${i%.fa*};
    
    blastp -db ${i} -query CanidateGene.fasta \
    -num_threads 10 \
    -outfmt "6 qseqid sseqid qlen slen length pident evalue bitscore" \
    -out ${basename}_vs_canidate_complete.blast &

done 

#Wait for the last one in the loop to finisih before moving on
wait $!

cat *_vs_canidate_complete.blast > total_canidate_complete.blast ;

python StrictGeneIsolation.py total_canidate_complete.blast CanidateGene.fasta;



makeblastdb -in StrictPossibleConsvdSeq.fasta -dbtype prot ;

blastp -db StrictPossibleConsvdSeq.fasta -query StrictPossibleConsvdSeq.fasta \
-num_threads 20 \
-outfmt "6 qseqid sseqid qlen slen length pident qcovs" -out self_vs_self.blast 

python PullUniqGenes.py self_vs_self.blast StrictPossibleConsvdSeq.fasta
