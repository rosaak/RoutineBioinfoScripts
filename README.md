RoutineBioinfoScripts
====================

##getFastaHeader.py 
####usgae



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
  
