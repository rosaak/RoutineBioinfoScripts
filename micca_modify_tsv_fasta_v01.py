# -*- coding: utf-8 -*-
#
# micca_modify_tsv_fasta_v01.py
#
# Copyright 2017 roshan padmanabhan <rosaak@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# See the GNU General Public License for more details.
# WITHOUT ANY WARRANTY
#

__version__ = 0.1
__author__ = 'roshan padmanabhan'

from collections import OrderedDict
from Bio import SeqIO
import argparse

des = """
This script modifies otus.fasta , otutable.txt made from the output of micca otu command
"""
parser = argparse.ArgumentParser(description=des,formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument( '-i', help='micca_otu_id_file', action='store',dest='otu_id',required=True)
parser.add_argument( '-t', help='micca_otu_table', action='store',dest='otu_table',required=True)
parser.add_argument( '-f', help='micca_otu_fasta', action='store',dest='otu_fasta',required=True)
parser.add_argument( '-x', help='micca_otu_ids_out_fp', action='store',dest='new_otuid',required=True)
parser.add_argument( '-y', help='micca_otu_table_out_fp', action='store',dest='new_table',required=True)
parser.add_argument( '-z', help='micca_otu_fasta_out_fp', action='store',dest='new_fasta',required=True)
# files
args = parser.parse_args()
otu_id = args.otu_id
otu_table = args.otu_table
otu_fas = args.otu_fasta
new_id = args.new_id
new_table = args.new_table
new_fasta = args.new_fasta
# OTU ids to dictionary
with open(otu_id ,'r') as nf:
    otuids = nf.readlines()
    otuids = [ i.replace('\n','').split('\t')  for i in otuids ]
otuids_dict = OrderedDict()
for i in otuids:
    if i[0].startswith('REF') :
        otuids_dict[i[0]] = i[1]
    else :
        otuids_dict[i[0]] = i[0]
# Write the new OTU ids
with open( new_id ,'w') as oids:
    for i in otuids_dict.items(): 
        x = i[0]+"\t"+i[1]
        oids.writeline(x)
# Modify the otutable and save them
# Not modifying the DENOVO lines in the otu_table
with open(otu_table, 'r') as tsvh:
    tsvd = tsvh.readlines()
    with open( new_table, 'w')  as otable :
        for i in tsvd[:]:
            i_list = i .split('\t')
            if i_list[0].startswith("REF"):
                ggid = otuids_dict.get( i_list[0] )
                if ggid !=None :
                    i_list[0] = ggid
                    x = '\t'.join(i_list)
                    otable.writelines( x )
            else :
                otable.writelines( i )
# Modify fasta file
# change the header where REF replace with ggid
# rest of the lines are printed as such
with open( new_fasta, 'w')  as ofasta :
    for record in SeqIO.parse(otu_fas ,format="fasta") :
        if record.description.startswith("REF"):
            ggid = otuids_dict.get( record.description )
            if ggid !=None :
                newseq = ">"+ggid+'\n'+str(record.seq)+"\n"
                #print(newseq)
                ofasta.writelines( newseq )
        else :
            newseq = ">"+record.description+'\n'+str(record.seq)+"\n"
            #print(newseq)
            ofasta.writelines( newseq )
