CGI_hg19="http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/cpgIslandExt.txt.gz"
CGI_hg38="http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cpgIslandExt.txt.gz"
CGI_mm10="https://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/cpgIslandExt.txt.gz"


# ---- modify here ----
ORGV='hg38'
URL=${CGI_hg38}
# ---- modiffy here -----

E=`basename ${URL} | sed 's:.txt.gz:bed:'`
OFN=${E}.${ORGV}.bed
wget -qO- ${URL}\
	   | gunzip -c \
	   | awk 'BEGIN{ OFS="\t"; }{ print $2, $3, $4, $5$6, substr($0, index($0, $7)); }' \
	   | sort-bed - >${OFN}

echo "Downloaded CpG Island bed file from ucsc"
