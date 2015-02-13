import sqlite3
import argparse
# -*- coding: utf-8 -*-
#
# py_seqret.py
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
this script is a python implementation of sequence fetch
using a sqlit3 db -creates a database in memory

Rationale :
mostly the fasta sequence to be fetched from a local db
dosen't work properly because of the long header sequences
so the long headers are split into two
one with the pattern and the rest

example fasta :
>mm10_chr10_7625343_7625542_+ par_30_2_100
GTTTCTTTCTGCACATCTTTTATATACAAAGAAGTTATCTACAATCTAGT
CAAATAAAGGGAGCTGCTTACAAGCTTGTTTTTGTGTATGTCAGTAGAAC
.....
pattern file :
'mm10_chr10_7625343_7625542'

input :
	fatsa file
	pattern file

Important :
the fucntion 'read_fasta' can to be modified accordingly
to different set of pattern files 

"""

def read_fasta(filename):
	"""
	Return a list of tuples for all the records of fasta
	"""
	with open(filename,'r') as file:
		contents = file.read()
	entries = contents.split('>')[1:]
	partitioned_entries = [entry.partition('\n') for entry in entries]
	pairs = [(entry[0], entry[2]) for entry in partitioned_entries ]
	# use the appropriate delimitor in slipt in next line
	pairs2 = [(pair[0].split('+')[0][:-1] ,pair[0], pair[1].replace('\n','')) for pair in pairs ]
	return pairs2

def check_headers(str):
	try:
		if len(str) >=1 :
			pass
	except :
		raise


def create_db(datafilename=':memory:'):
	'''Return a db connction
	if no file name given then db is made in memory
	'''
	conn = sqlite3.connect(datafilename)
	return conn


def create_table(conn):
	'''
	Return conn
	caution : run this only once for a db
	'''
	conn.execute('''DROP TABLE IF EXISTS SeqRet;''')
	conn.execute('''
		CREATE TABLE SeqRet(
		P_Header text,
		Header text,
		Seq text 
		);
		''')
	conn.commit()
	return conn.cursor()


def polpulate_table(tup):
	try:
		conn.execute("INSERT INTO SeqRet (P_Header, Header, Seq ) VALUES(?, ?, ?)",( tup[0], tup[1], tup[2]))
		conn.commit()
	except OperationalError as e:
		print (e)
		pass


def make_fasta(hs):
	return ">" + hs[0]+ "\n" +hs[1]


def query_db(pat):
	'''
	Returns the fatsa sequences
	'''
	qres = conn.execute('SELECT Header,Seq FROM SeqRet WHERE Header LIKE ?', ('%'+pat+'%',) ).fetchall()

	to_fasta_factory=[]
	for i in qres:
		to_fasta_factory.append(i)
	for i in to_fasta_factory:
		print(make_fasta(i))


if __name__ == '__main__':

	des="""
	give two file , fasta file to search and pattern file
	"""
	parser = argparse.ArgumentParser(description=des,formatter_class=argparse.RawTextHelpFormatter )
	parser.add_argument('-f', help='fasta sequence file', action='store',dest='infasta',required=True)
	parser.add_argument('-p', help='pattern file', action='store',dest='pat_file',required=True)
	args = parser.parse_args()
	in_fasta = args.infasta
	pat_file = args.pat_file

	# datafilename = './test/lite3seq.db'
	# in_fasta = "./test/seq.fasta"
	# pat_file = "./test/pat.txt"

	# get the fasta sequences into a list - data
	data = read_fasta(in_fasta)

	# making the database in memory and popluating the table
	conn=create_db()
	create_table(conn)

	# dynamically populate the table 
	for i in  data:
		polpulate_table(i)

	for each_pat in open(pat_file, 'r').readlines():
		q = each_pat.strip()
		#print("Query is :" , q )
		query_db(q)
