# WORK IN PROGRESS

__author__="Roshan Padmanabhan"
__ver__=0.1

import os
from pathlib import Path
import argparse
import pandas as pd

"""
this script downloads the cpgIsland data from ucsc 
schema="http://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=regulation&hgta_track=cpgIslandExt&hgta_table=cpgIslandExt&hgta_doSchema=describe%20table%20schema"
"""

def create_url(org_ver):
    url1="http://hgdownload.cse.ucsc.edu/goldenpath/"
    url2="/database/cpgIslandExt.txt.gz"
    url = url1+org_ver+url2
    return url

def get_data(url):
    header=["bin", "chrom", "chromStart", "chromEnd", "name", "length", "cpgNum", "gcNum", "perCpg", "perGc", "obsExp"]
    try :
        df = pd.read_csv(url, sep="\t", header=0)
        df.columns = header
        df.name = df.name.str.replace(" ","")
        df2 = df[["chrom", "chromStart", "chromEnd", "name", "bin", "length", "cpgNum", "gcNum", "perCpg", "perGc", "obsExp"]]
        return df2
    except :
        print("Check url or org version")

def make_bed3format(df):
    dfn = df[["chrom", "chromStart", "chromEnd"]]
    return dfn

def save_data(df, ofn, saveheader=False):
    df.to_csv(ofn, sep="\t", index=False, header=saveheader)

def parse_cmd( ):
    des="""This script downloads cpgIsland files from ucsc
    """
    parser = argparse.ArgumentParser(description=des,formatter_class=argparse.RawTextHelpFormatter )
    parser.add_argument('-i', help='org version ex: hg19', action='store',dest='org_ver',required=True)
    parser.add_argument('-d', help='outfile dir', action='store',dest='out_dir',required=True) 
    parser.add_argument('--bed3', dest='download_in_bed3_format', action='store_true')
    parser.add_argument('--no-bed3', dest='download_in_bed3_format', action='store_false')
    parser.set_defaults(feature=True)
    
    args = parser.parse_args()
    return ([args.org_ver, args.download_in_bed3_format, args.out_dir])

def main(org_ver, bed3=False, outfilepath=False, save=False):
    url = create_url(org_ver)
    df = get_data(url)
    if bed3 :
        df = make_bed3format(df)
    if save and outfilepath:
        outfilename = os.path.join(str(Path(outfilepath).resolve()), org_ver) + ".cpgIslandExt.bed"
        print(f"Saving the file {outfilename}")
        if bed3:
            save_data(df, ofn=outfilename, saveheader=False)
        else :
            save_data(df, ofn=outfilename, saveheader=True)

if __name__ == '__main__':
    org, bed3, outfilepath = parse_cmd()
    if outfilepath:
        main(org_ver=org, bed3=bool(bed3), outfilepath=outfilepath, save=True)
    else:
        main(org_ver=org, bed3=bed3, outfilepath=outfilepath, save=False)
