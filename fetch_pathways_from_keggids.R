# author : roshan
# date  : 29 Jan 2016

# Given a file from kegg id list [ one id per line ]
# for each kegg id it search KEGG db and get back a data frame 
# of kegg ids, pathway ids and defenition
# requirement KEGGREST 

r.get_col = function(col, delimiter, recol ){
        # return a specific col from a list after splitting a column using delimiter 
        sapply( strsplit( as.character(col), delimiter),'[', recol)
        }

keggid_to_pathwayids_df_v1 = function( keggids ){
        suppressMessages(require('KEGGREST'))
        # give a character vector of kegg ids 
        # it gives back a data frame of keggids and corresponding pathway ids, pathway defenition and the defenition of keggid
        cnames = c("KO", "Pwy.IDs", "Pwy.Def", "Def")
        temp.mat = matrix( ncol=4, nrow=1)
        colnames( temp.mat) = cnames
        ko.df = as.data.frame( temp.mat )
        # col full of NAs
        temp.mat2 = matrix( ncol=4, nrow=1)
        colnames( temp.mat2) = cnames
        ko.err = as.data.frame( temp.mat2 )

        for ( i in seq_along( keggids ) )
        {
                k.id = keggids[i]
                print( paste0("Processing : ", k.id ) )
                
                #k.data = keggGet(k.id)
                k.data.r = try( keggGet(k.id), silent=T)
                if(  class(k.data.r) != 'try-error' ){
                        k.data = k.data.r
                        # Initializing the Matrix
                        if( length(k.data[[1]]$PATHWAY) >=1  ){
                                k.pway = k.data[[1]]$PATHWAY
                                k.out =  matrix( nrow=length( names(k.pway)) , ncol=4 )
                                colnames(k.out) = cnames
                                k.out[,'Pwy.IDs'] = names(k.pway)
                                k.out[,'Pwy.Def'] = k.pway
                        }
                        else{
                                k.out =  matrix( nrow=1 , ncol=4 )
                                colnames(k.out) = cnames
                        }
                        if ( length(k.data[[1]]$ENTRY) ==1 ){
                                k.entry = k.data[[1]]$ENTRY
                                k.out[,'KO'] = as.character( k.entry) 
                        }
                        else{
                                k.entry = k.id
                                k.out[,'KO'] = k.id
                        }
                        if ( !is.null( k.data[[1]]$DEFINITION ) ){
                                k.def  = k.data[[1]]$DEFINITION
                                k.out[,'Def'] = as.character( k.def)
                        }
                        else{
                                k.def = 'NA'
                                k.out[,'Def'] = 'NA'
                        }
                        k.out = as.data.frame(k.out)
                        #print(k.out)
                        ko.df = rbind( ko.df, k.out )
                }
                else{
                        k.err = as.character( c( k.id,'not in kegg','not in kegg','not in kegg','not in kegg')  )
                        ko.df = rbind( ko.df, k.err)
                }
        }
        ko.df = ko.df[-1,]
        return( ko.df )
}


x = read.table("kegg.ids")
keggids = r.get_col( as.character(x[,1]), '[:] ', 1)
# remove duplicated
keggids = unique(keggids)

df_k = keggid_to_pathwayids_df_v1( keggids )
write.table(df_k, "out_kegg_df2.tsv",sep="\t", row.names=F, quote=F)

print("Done\n")
