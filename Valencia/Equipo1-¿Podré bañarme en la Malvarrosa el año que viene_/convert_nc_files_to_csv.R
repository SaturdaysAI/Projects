#install.packages('raster')
#library('raster')
library('ncdf4')

#library(chron)
#library(RColorBrewer)
#library(lattice)
library(stringr)
library(DataCombine)
library(tibble)

setwd('C:/Users/luism/Desktop/Saturdays_AI/Project/data/')
list_of_files <- setdiff(list.files('C:/Users/luism/Desktop/Saturdays_AI/Project/data/'), 
                                    list.dirs(recursive = FALSE, full.names = FALSE))

for (element in list_of_files){
  print(element)
  nc.file <- ncdf4::nc_open(element)
  variables <- c(names(nc.file$var))
  df_final <- data.frame(matrix(data = NA, nrow = length(ncvar_get(nc.file, variables[1])), 
                    ncol = length(variables)))
  colnames(df_final) <- variables
  index <- 1
  for (variable in variables){
    print(variable)
    
    ## if rows > 1 --> append columns to the right. _1,_2,_3... 
    if (length(dim(ncvar_get(nc.file, variable))) == 2){
      nrows <- dim(ncvar_get(nc.file, variable))[1] # Get the number of rows, e.g. 3.
      
      #Small dataframe transposing the variable subset.
      values_df <- as.data.frame(t(ncvar_get(nc.file, variable))) 
      colnames(values_df) <- paste(variable, 1:nrows, sep = '_')
        
      if (index == length(df_final)){
        df_final <- cbind(df_final, values_df)
      } 
      else{
        df_final <- cbind(df_final[1:index-1], values_df,
                            df_final[(index+1):length(df_final)])
      }
      index <- index + nrows
    }
    else{
      
      if (dim(df_final)[1] == 1){
        count <- 1
        new.row <- rep(NA, length(df_final))
        max <- length(ncvar_get(nc.file, variable))
        while (count < max){
          df_final <- rbind(df_final, new.row)
          count <- count + 1
        }
      }
      df_final[index] <- ncvar_get(nc.file, variable)
      index <- index + 1 
    }
  }
  write.csv(df_final, paste0("./csv_files/", substr(element, 1, nchar(element) - 2), 'csv'))
}
