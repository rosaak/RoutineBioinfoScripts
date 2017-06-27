RoutineBioinfoScripts
====================

## getFastaHeader.py
#### usgae

    usage: getFastaHeader.py [-h] -i BLAST_OUT -d {nuc,pro} -o OUTFILE_BASENAME
    Given the blastoutput file in tab format and the database name ( protein [pro] or nucelotide [nuc] )
    It search NCBI for the gi ids and get the header and taxonomic id

    Creates two csv files
      -> _hypothetical.csv contains gene description containing hypothetical genes/ proteins
      -> _other.csv contains rest of the results  
    
    optional arguments:
     -h, --help           show this help message and exit
     -i BLAST_OUT         blastoutput file
     -d {nuc,pro}         database to search
     -o OUTFILE_BASENAME  outfile base name
  
## py_seqret.py
#### usage

	usage: py_seqret.py [-h] -f INFASTA -p PAT_FILE

	this script is a python implementation of sequence fetch
	more like emboss seqret
	inputs are : fasta file to search and pattern file
	
    optional arguments:
    -h, --help   show this help message and exit
    -f INFASTA   fasta sequence file
    -p PAT_FILE  pattern file

## micca_modify_tsv_fasta_v01.py 
#### usage

	usage: micca_modify_tsv_fasta_v01.py [-h] -i OTU_ID -t OTU_TABLE -f OTU_FASTA
					     -x NEW_OTUID -y NEW_TABLE -z NEW_FASTA

		This script modifies otus.fasta , otutable.txt made from the output of micca otu command

	optional arguments:
	  -h, --help    show this help message and exit
	  -i OTU_ID     micca_otu_id_file
	  -t OTU_TABLE  micca_otu_table
	  -f OTU_FASTA  micca_otu_fasta
	  -x NEW_OTUID  micca_otu_ids_out_fp
	  -y NEW_TABLE  micca_otu_table_out_fp
	  -z NEW_FASTA  micca_otu_fasta_out_fp

