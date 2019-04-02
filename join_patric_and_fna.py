"""
Merge gff and fna file in each dir
The merge file should look like
    content of gff file
    ##FASTA
    content of fasta file
"""

author ='roshan padmanabhan'
date= '1April2019'
version = 1

from pathlib import Path
import logging
import time

def _make_logger( namex ):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    ct = time.ctime()
    log_t=':'.join(ct.split(' ')[0:2]) + '-' +'-'.join(ct.split(' ')[3:5])
    handler = logging.FileHandler(namex+'.'+log_t+'.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return( logger )


loc ="." # change the location of dir here
locx=Path(loc)
fna=sorted(list(locx.glob("*/*.fna")))
gff=sorted(list(locx.glob("*/*.PATRIC.gff")))

log = _make_logger( 'MERGE_GFF_FNA' )
log.info("Merge PATRIC GFF and FNA files...")
log.info("Number of FNA files :{}".format( len(fna)))
log.info("Number of GFF files :{}".format( len(gff)))

if len(fna) == len(gff) :
    log.info("Merging Loop Starts...\n\n")
    for fn in zip(gff, fna):
        eg = fn[0]
        ef = fn[1]
        if len(fn)==2:
            if eg.exists() and ef.exists() and eg.stat()[6] >0 and ef.stat()[6] >0:
                with open( str(eg), 'r') as ifh :
                    gff_data = ifh.readlines()
                with open( str(ef).replace('.PATRIC.gff', '.fna')) as fnah :
                    fna_data = fnah.readlines()
                merged_fp = str(eg).replace('.PATRIC.gff','_merged.gff')
                log.info("GFF:{}\tFNA:{}\tMERGED_FP:{}".format(eg.name, ef.name, merged_fp))
                with open(merged_fp , 'w') as ofh :
                    for i in gff_data :
                        ofh.writelines(i)
                    ofh.writelines("##FASTA\n")
                    for i in fna_data :
                        ofh.writelines(i)

else :
    log.info("Problem : Numbers don't match\n")
log.info("Done")


