#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# rdp2_gg.py
#
# Copyright 2015 roshan padmanabhan <rosaak@gmail.com>
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


"""
This script parse the massive rdp file into a fasta file and taxonomy file
which could be used instead of gg13.5
Need to cross verify with the gg13.5  file
"""

from Bio import SeqIO

def rdp_to_ggline(l):
    return_line = []
    c =  record_dict[l].description.split('\t')[::-1][0].split(';')[::-1]
    ID = l.strip() + "\t"
    return_line.append(ID)
    return_line.append('s__')
    for e, i in enumerate(c) :
        if i in 'genus' and len(i) == 5:
            G = "g__" + c[c.index('genus')+1].replace('\"','') + "; "
            return_line.append(G)
        elif i in 'unclassified':
            pass
        elif i in 'family':
            F = "f__" + c[c.index('family')+1].replace('\"','') + "; "
            return_line.append(F)
        elif i in 'order':
            O =  "o__" + c[c.index('order')+1].replace('\"','') + "; "
            return_line.append(O)
        elif i in 'class':
            C = "c__" + c[c.index('class')+1].replace('\"','') + "; "
            return_line.append(C)
        elif i in 'phylum':
            P =  "p__" + c[c.index('phylum')+1].replace('\"','') + "; "
            return_line.append(P)
        elif i in 'domain':
            K =  "k__" + c[c.index('domain')+1].replace('\"','') + "; "
            return_line.append(K)
    return return_line[0] +  ''.join(return_line[1:][::-1]) + "\n"


if __name__=='__main__':
    #f1 = "../test/rdp.fasta"
    #f2 = "/anas/bank/bugs/rdp/rdp.bacteria16s.aligned.fasta"
    handle = open(f1 , 'rU')
    # CAUTION : using to_dict fucntion
    # Dictionaries don't keep the same input order
    # if seq order is imp then use the SeqIO.parse method or
    record_dict = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
    of = "rdp.taxa.txt"
    offasta = "rdp.otus.fasta"
    # writing the sequences and taxonomy files
    with open(of, 'a') as ofh :
        with open(offasta , 'w+a') as ofhf:
            for l in record_dict:
                # print l
                ofh.writelines( rdp_to_ggline(l))
                seq =  ">"+record_dict[l].id + "\n" + record_dict[l].seq + "\n"
                ofhf.writelines(seq)


