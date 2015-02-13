
__author__ = 'Roshan'
__version__ = 0.1
__lisense__ = 'BSD'

# python 2.7 or 3.4

'''

given the blast output file in tab format
it Return the fasta header of all the subject 
NCBI Entrez eutility features

Requirement : biopython

'''

import argparse
import os
import sys
from Bio import Entrez
# EDIT here
Entrez.email = '' #pls add


def main():
    des="""
    Given the blastoutput file in tab format and the database name ( protein [pro] or nucelotide [nuc] )
    It search NCBI for the gi ids and get the header and taxonomic id

    Creates two csv files
      -> _hypothetical.csv contains gene description containing hypothetical genes/ proteins
      -> _other.csv contains rest of the results  
    """
    parser = argparse.ArgumentParser(description=des,formatter_class=argparse.RawTextHelpFormatter )
    parser.add_argument('-i', help='blastoutput file', action='store',dest='blast_out',required=True)
    parser.add_argument('-d', help='database to search', action='store',dest='database' ,required=True,choices=['nuc', 'pro'])
    parser.add_argument('-o', help='outfile base name', action='store',dest='outfile_basename',required=True)

    args = parser.parse_args()
    infile = args.blast_out
    dbname = args.database
    outfile = args.outfile_basename
    o_hypo  = outfile + '_hypothetical.csv'
    o_other = outfile + '_other.csv'
    
    try :
        os.remove(o_other)
        os.remove(o_hypo)    
    except:
        pass

    
    with open(o_hypo, "a") as text_file:
        text_file.write("Gi,Description,Organism,TaxID\n")

    with open(o_other, "a") as text_file:
        text_file.write("Gi,Description,Organism,TaxID\n")

    with open(infile,'r') as fh:
        blastout = fh.readlines()
    gi = []
    for e in blastout[:]:
        gi.append(e.split('|')[5])

    print('...........Begining NCBI requetst...........')

    print ("Total number of Gis in the file : {} ".format(len(gi)))

    if 'pro' in dbname.lower() :
        dbname = 'protein'
    if 'nuc' in dbname.lower() :
        dbname = 'nuccore'
    
    for i in gi[:]:
        i = i.rstrip()
        try:
            handle = Entrez.efetch(db=dbname,rettype='fasta',retmode='xml',id=i)
            record = Entrez.read(handle)
            tofile = record[0]['TSeq_gi'] + ',' + record[0]['TSeq_defline'] + ',' + record[0]['TSeq_orgname'] +','+ record[0]['TSeq_taxid'] + '\n'
            if 'hypothetical protein' not in record[0]['TSeq_defline'] :
                with open(o_other, "a") as text_file:
                    text_file.write(tofile)
            else:
                with open(o_hypo, "a") as text_file:
                    text_file.write(tofile)
            handle.close()
        except :
            print ('\nERROR: BAD request, check gi id : ' + i )
            pass

    print('\ncheck the files {} and {} '.format(o_hypo, o_other))

    print('\n...........Finished...........')



if __name__=='__main__':
    main()

#
# To Do
# Check the blast file
# 
