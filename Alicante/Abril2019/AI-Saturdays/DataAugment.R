###############################################################################################
### CARGAR LIBRERÍAS
###############################################################################################

library(fitdistrplus)
library(logspline)
library(boot)
library(ssdtools)

###############################################################################################
### CARGAR DATOS
###############################################################################################

# Carecemos de permiso para incluir los datos en el repositorio

datos <- read.table(file='datos.txt', sep=';', quote='', dec='.', header=TRUE)

###############################################################################################
### SELECCIÓN DE DATOS CUANTITATIVOS
### Y CREACIÓN DE MATRICES VACÍAS PARA LOS PARÁMETROS
###############################################################################################

datos.fit <- datos[, -c(1, 10, 11, 17)]

param.mean = matrix(ncol=13, nrow=5)
param.sd = matrix(ncol=13, nrow=5)

###############################################################################################
### AJUSTE DE DISTRIBUCIONES PARA CADA PARÁMETRO (1 - 13)
### Y CADA GRUPO (1 - 5)
### ASUMIENDO NORMALIDAD
###############################################################################################

myRows = 1:5
myCols = 1:13

for (i in myRows) {
  
  for (j in myCols) {
    
    param <- fitdist(datos.fit[(10 * (i -1) + (1:10)), j], 'norm')
    param.mean[i, j] <- param$estimate['mean']
    param.sd[i, j] <- param$estimate['sd']
    
  }
  
}

rm(i, j, myCols, myRows, param)

###############################################################################################
### CREACION DE 90 DATOS SINTÉTICOS PARA CADA GRUPO
### A PARTIR DE LAS DISTRIBUCIONES CALCULADAS
###############################################################################################

myN = 90

datos.new <- as.data.frame(matrix(rep(-1000, 13*5*myN), ncol=13, nrow=5*myN))
colnames(datos.new) <- colnames(datos.fit)

myRows = 1:5
myCols = 1:13

for (i in myRows) {
  
  for (j in myCols) {
    
    datos.new[(((i - 1) * myN + 1) : (i * myN)), j] <- rnorm(n=myN, 
                                                             mean=param.mean[i, j], 
                                                             sd=param.sd[i, j])

  }
  
}

rm(i, j, myCols, myRows)

###############################################################################################
### CREACION DE DATOS FICTICIOS
### PARA LAS VARIABLES BINOMIALES
### SEXO Y OJO (AUNQUE ESTA ÚLTIMA NO SE USE POSTERIORMENTE EN LOS MODELOS)
### HACIENDO QUE SE RESPETEN LAS PROPORCIONES INICIALES
###############################################################################################

datos.new$Sexo <- -1
cutoff <- prop.table(table(datos$Sexo))[1]

for (i in 1:nrow(datos.new)) {
  
  if (runif(1) < cutoff) {
    datos.new$Sexo[i] <- 1
  } else {
    datos.new$Sexo[i] <- 2
  }
  
}

datos.new$Ojo <- -1
cutoff <- prop.table(table(datos$Ojo))[1]

for (i in 1:nrow(datos.new)) {
  
  if (runif(1) < cutoff) {
    datos.new$Ojo[i] <- 1
  } else {
    datos.new$Ojo[i] <- 2
  }
  
}   
    
datos.new$Grado <- c(rep(0, myN), rep(1, myN), rep(2, myN), rep(3, myN), rep(4, myN))
datos.new$IdOjo <- paste('OjoGrado', datos.new$Grado, sep='')

rm(i, cutoff, myN)

datos.new$Sexo <- factor(datos.new$Sexo, labels = c('hombre', 'mujer'))
datos.new$Ojo <- factor(datos.new$Ojo, labels = c('OD', 'OI'))

prop.table(table(datos.new$Sexo))
prop.table(table(datos.new$Ojo))

###############################################################################################
### COMBINACIÓN DE DATOS ANTÍGUOS Y NUEVOS
### Y GUARDADO DE ARCHIVO
###############################################################################################

datos.augmented <- rbind(datos, datos.new)

write.table(datos.augmented, file='datosAug.txt', sep=';', quote=FALSE, dec='.',
            col.names=TRUE, row.names=FALSE)
