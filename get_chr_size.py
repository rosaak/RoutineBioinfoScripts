import pybedtools
import pandas as pd

def get_chr_size( genome_build="hg19" , cannonical=False):
    """
    Returns a data frame of chr sizes
    """
    X = pybedtools.chromsizes(genome=genome_build)
    if cannonical :
        df = pd.DataFrame( [[ i, X.get(i)[1]] for i in X ], columns=["Chr","Size"])
    else :
        df = pd.DataFrame( [[ i, X.get(i)[1]] for i in X if '_' not in i ], columns=["Chr","Size"])
    if not df.empty :
    return(df)
