# This script takes the OTU biom (json format) file and converts it into a tsv file
# Use it when biom convert fails
# Also removes the rows where rowSums is zero

source("/home/roshan/Scripts/rosh.lib/da.R")
library( biom )

write_biom = function(df, fileout ){
	firstLine="# Constructed from biom file"
	write(file = fileout, x = firstLine, append=TRUE)
	write.table( file=fileout, x=df, row.names=F, quote=F, sep="\t" , append=TRUE)
}

filein = "otu_table.json"
fileout = "otu_table.tsv"

x = read_biom( filein ) 
mat.d = as.matrix(biom::biom_data(x) )
mat.md = as.matrix(biom::observation_metadata(x) )
biom.df =  as.data.frame(merge( mat.d, mat.md , by = 0 ) )

# dim( mat.d)
# dim( mat.md)

# Remove NAs and write the tsv file

if ( any(rowSums( mat.d ) == 0 ) ){
# Remove the rows with only zeros
	mat.d2 = mat.d[rowSums( mat.d ) >=1,]
	biom.df2 = merge( mat.d2, mat.md , by=0) 
	biom.df2 = biom.df2 %>% rename( '#OTU ID' = Row.names )
	write_biom( biom.df2 , fileout )
} else {
	biom.df = biom.df %>% rename( '#OTU ID' = Row.names );
	write_biom( biom.df , fileout )
}

