# -*- coding: utf-8 -*-
#
# insert_rDNA.py
#
# Copyright 2018 roshan padmanabhan <rosaak@gmail.com>
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
Aim : Insert the rDNA sequence in chr13, by replacing the N's from the initial unsequenced region
Reference : Integrative genomic analysis of human ribosomal DNA, NAR, 2011, Vol. 39, No. 12, 4949-4960
Inputs	: require rDNA fasta file (U13369.1)  and hg19 chr13 file
"""

import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

Ns =  re.compile( 'N+' )

hg19_chr13 = "chr13.fa"
insert= "U13369.1.fasta"

insertx = list(  SeqIO.parse( insert, format="fasta"))[0]
chr13x =  list( SeqIO.parse( hg19_chr13, format="fasta"))[0]

first_N = list( Ns.finditer( str( chr13x.seq) ))[0]
fn = str( chr13x.seq)[ first_N.span()[0]  :  first_N.span()[1] ]
fn2 = str(chr13x.seq)[ first_N.span()[1] : ]
fn_remainder = fn[ len( str( insertx.seq)) : ]
fn3  =  str( insertx.seq )[::-1] +  fn_remainder
final = fn3[::-1] + fn2

# Sanity check
print( "Chr name :{}, length :{}".format( chr13x.name , len( str(chr13x.seq)) ))
print( "Length of Initial N's : {}".format( first_N.span()[1] - first_N.span()[0]))
print( len( final))

# save the new rdna chr13 fatsa file
with open( "chr13.fasta", "w") as ofh:
  SeqIO.write( SeqRecord( Seq(final),"chr13_with_rdna" ), ofh, "fasta")
  
  
  
