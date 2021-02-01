#################################################################################################
### CARGAR LIBRERÍAS
#################################################################################################

library(tidyr)
library(dlookr)
library(car)
library(corrplot)
library(MASS)
library(dplyr)
library(Epi)
library(pROC)
library(ROCR)
library(yarrr)
library(nnet)

#################################################################################################
### CARGAR DATOS
#################################################################################################

datos <- read.table(file='datosAug.txt', quote='', sep=';', dec='.', header=TRUE)

#################################################################################################
### CREACIÓN DE VARIABLES AUXILIARES GRADO1 Y GRADO2
### Y ANÁLISIS EXPLORATORIO BÁSICO
#################################################################################################

datos$Grado1 <- c(rep(0,10), rep(1,10), rep(NA,30))

datos$Grado1 <- NA
datos$Grado1[datos$Grado == 0] <- 0
datos$Grado1[datos$Grado == 1] <- 1

datos$Grado2 <- datos$Grado > 0
datos$IdOjo <- as.character(datos$IdOjo)

summary(datos)

#################################################################################################
### TABLA DE DESCRIPTIVOS
#################################################################################################

tabla <- datos %>%
  dplyr::select(IdOjo:Grado) %>%
  group_by(Grado) %>%
  describe(-Grado) %>%
  dplyr::select(variable, Grado, n, na, mean, sd, se_mean, p50, p00, p100) %>%
  gather(parametro, estadistico, -variable, -Grado) %>%
  dplyr::select(Grado, variable, parametro, estadistico) %>%
  arrange(Grado, variable, parametro) %>%
  spread(key=variable, value=estadistico)

#################################################################################################
### SCATTERPLOT Y BARPLOTS
#################################################################################################

scatterplotMatrix(~Volumen + AreaCaraAnterior + AreaCaraPosterior +
                  AreaTotal + CentroMasasX + CentroMasasY + CentroMasasZ +
                  Edad + Esfera + Cilindro + Eje + EquivEsf + AVCC | Grado,
                  data=datos, smooth=FALSE, regLine=FALSE, pch=rep(20,5))

boxplot(datos$Volumen~datos$Grado, main='Volumen', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$AreaCaraAnterior~datos$Grado, main='AreaCaraAnterior', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$AreaCaraPosterior~datos$Grado, main='AreaCaraPosterior', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$AreaTotal~datos$Grado, main='AreaTotal', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$CentroMasasX~datos$Grado, main='CentroMasasX', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$CentroMasasY~datos$Grado, main='CentroMasasY', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$CentroMasasZ~datos$Grado, main='CentroMasasZ', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$Edad~datos$Grado, main='Edad', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$Esfera~datos$Grado, main='Esfera', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$Cilindro~datos$Grado, main='Cilindro', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$Eje~datos$Grado, main='Eje', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$EquivEsf~datos$Grado, main='EquivEsf', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))
boxplot(datos$AVCC~datos$Grado, main='AVCC', 
        names=c('Ctrl', 'I', 'II', 'III', 'IV'))

#################################################################################################
### CREAR DATA FRAME PARA REGRESIÓN LOGÍSTICA
#################################################################################################

datos.reglog = data.frame(datos[datos$Grado==0 |
                                  datos$Grado==1, -c(1, 11, 17, 18)])

datos.reglog$Grado2 = factor(datos.reglog$Grado2)
colnames(datos.reglog)[15] = 'SUBCLINICO'

#################################################################################################
### CORRELACIÓN ENTRE VARIABLES
#################################################################################################

correlaciones <- cor(datos.reglog[,-c(9,15,16)])

corrplot(correlaciones, method='circle', tl.cex=0.6)

correlaciones <- data.frame(correlaciones)
correlaciones <- data.frame(correlaciones > 0.9) + 0

#################################################################################################
### MODELOS DE REGRESIÓN LOGÍSTICA
### 1.- CON TODAS LAS VARIABLES
### 2.- SUPRIMIENDO LAS VARIABLES MENOS IMPORTANTES (MÉTODO AIC)
### 3.- IGUAL QUE 2, PERO AÑADIENDO LA EDAD POR INTERÉS DEMOGRÁFICO
#################################################################################################

mod_fit_one <- glm(SUBCLINICO ~ 
                     Edad +
                     Sexo +
                     Volumen + 
                     AreaCaraAnterior + 
                     AreaCaraPosterior + 
                     AreaTotal + 
                     CentroMasasX + 
                     CentroMasasY + 
                     CentroMasasZ + 
                     Esfera + 
                     Cilindro + 
                     Eje + 
                     EquivEsf + 
                     AVCC, 
                   data=datos.reglog, family = binomial(link = "logit"))

summary(mod_fit_one)

mod_fit_two_ORG <- mod_fit_one %>% stepAIC(direction='backward', trace=TRUE)

# Redefinimos el mod_fit_two a mano añadiendo EDAD por interés demográfico
mod_fit_two <- glm(SUBCLINICO ~
                     Sexo + 
                     Edad +
                     AreaCaraPosterior + 
                     CentroMasasZ +
                     AreaTotal + 
                     Volumen + 
                     AreaCaraAnterior + 
                     Cilindro + 
                     Eje,
                   data=datos.reglog, family = binomial(link = "logit"))

summary(mod_fit_two)

#################################################################################################
### CURVAS ROC
#################################################################################################

datos.reglog$prob1 = predict(mod_fit_one, type=c("response"))

curva1a <- ROC(form = datos.reglog$SUBCLINICO ~ datos.reglog$prob1,
               plot="ROC", PV=TRUE, MX=TRUE, MI=TRUE, AUC=TRUE,
               main='TODAS LAS VARIABLES')

curva1b <- roc(datos.reglog$SUBCLINICO, datos.reglog$prob1,
                        ci=TRUE, print.auc=TRUE, show.thres=TRUE)

curva1b

datos.reglog$prob2 = predict(mod_fit_two, type=c("response"))

curva2a <- ROC(form = datos.reglog$SUBCLINICO ~ datos.reglog$prob2,
               plot="ROC", PV=TRUE, MX=TRUE, MI=TRUE, AUC=TRUE,
               main='MODELO SELECCIONADO')

curva2b <- roc(datos.reglog$SUBCLINICO, datos.reglog$prob2,
               ci=TRUE, print.auc=TRUE, show.thres=TRUE)

curva2b

par(mar=c(4.5, 4.5, 1, 1))
plot(x=(1-curva2a$res$spec), y=curva2a$res$sens, type='l', lwd=2,
     xlab='1 - Specificity', ylab='Sensibility', main=NA)
lines(x=c(-0.2, 1.2), y=c(-0.2, 1.2), lty=2)
lines(x=c(-0.2, 1.2), y=c(0.727, 2.127), lty=2)
points(x=(1-0.97), y=0.96, pch=1, lwd=3, cex=2, col='red')
text(x=0.55, y=0.35, labels=paste('Bootstrap    (mean ', intToUtf8(177), ' SD)'), adj=0)
text(x=0.55, y=0.2, labels='AUC:\nSensitivity:\nSpecificity:', adj=0)
text(x=0.75, y=0.2, labels=paste('0.965 ', intToUtf8(177), ' 0.036\n', 
                                '0.934 ', intToUtf8(177), ' 0.042\n', 
                                '0.950 ', intToUtf8(177), ' 0.039' , sep=''), adj=0)

#################################################################################################
### BOOTSTRAP AUC, SENS Y SPEC
#################################################################################################

R = 100
n = nrow(datos.reglog)

# Creación de matriz vacía para almacenar resultados
B = matrix(nrow = R, ncol = 3,
           dimnames = list(paste('Sample',1:R),
                           c("AUC", "Sensitivity", "Specificity")))

set.seed(1234)

for(i in 1:R){
  
  # Obtención de muestra aleatoria
  obs.boot <- sample(x = 1:n, size = n, replace = T)
  data.boot <- datos.reglog[obs.boot, ]
  data.noboot <- datos.reglog[-obs.boot, ]
  
  # Ajustar el modelo con la muestra bootstrapped
  logit.boot <- glm(mod_fit_two$formula , 
                    data = data.boot,
                    family = binomial(link = "logit"))
  
  # Aplicar modelo sobre los datos non bootstrapped
  prob = predict(logit.boot, type='response', data.noboot)
  pred = prediction(prob, data.noboot$SUBCLINICO)
  
  auc = performance(pred,"auc")@y.values[[1]][1]
  
  resultados = data.frame(performance(pred,"sens")@y.values,
                          performance(pred,"spec")@y.values)
  colnames(resultados) <- c("sens", "spec")
  resultados$suma = resultados$sens + resultados$spec 
  
  sens = resultados[resultados$suma == max(resultados$suma),][1]
  spec = resultados[resultados$suma == max(resultados$suma),][2]
  
  B[i, 1] = auc
  B[i, 2] = sens[1,1]
  B[i, 3] = spec[1,1]
  
}

resultados = data.frame(c("AUC", "Sens", "Spec"),
                        c(mean(B[,1]), mean(B[,2]), mean(B[,3])),
                        c(sd(B[,1]), sd(B[,2]), sd(B[,3])))

colnames(resultados)=c("Param", "Mean", "SD")
resultados

#################################################################################################
### COMPARACIÓN DE PREDICCIONES Y DIAGNÓSTICOS REALES
#################################################################################################

par(mar=c(2.5, 4.5, 1, 1))
pirateplot(formula = datos.reglog$prob2 ~ factor(datos.reglog$SUBCLINICO, 
                                                 levels=c(FALSE, TRUE), 
                                                 labels=c('Control', 'Grado I')),
           data=datos.reglog, point.cex=0.5, theme=1, 
           bean.lwd=1, inf.lwd=1, avg.line.lwd=1, bar.lwd=1,
           width.max=0.2, gl=NA, inf.disp='bean', point.o=0.5,
           bw=1, adjust=0.08, inf.method='iqr', avg.line.fun=median,
           ylab='Score', xlab=NA)

lines(x=c(0.08, 4), y=c(0.615, 0.615), lwd=4, lty=5, col='gray40')
text(x=1.5, y=0.70, labels='Cut-off value = 0.615')

#################################################################################################
### SUMMARIES
#################################################################################################

datos.reglog$pred1[datos.reglog$prob1 > 0.348] = 1
datos.reglog$pred1[datos.reglog$prob1 <= 0.348] = 0

datos.reglog$pred2[datos.reglog$prob2 > 0.615] = 1
datos.reglog$pred2[datos.reglog$prob2 <= 0.615] = 0

table(datos.reglog$pred1, datos.reglog$SUBCLINICO)
table(datos.reglog$pred2, datos.reglog$SUBCLINICO)

summary(mod_fit_one)
summary(mod_fit_two)

#################################################################################################
### PREPARACIÓN DE DATOS 
### PARA REGRESIÓN LOGÍSTICA ORDINAL
### ELIMINANDO OJO PORQUE CARECE DE INTERÉS MÉDICO
#################################################################################################

datos.ordinal <- datos[, -c(18, 19)]
datos.ordinal$Grado <- as.factor(datos.ordinal$Grado)

#################################################################################################
### REGRESIÓN LOGÍSTICA ORDINAL
### SELECCIONANDO LAS VARIABLES MÁS IMPORTANTES
### USANDO EL MÉTODO AIC BACKWARDS
#################################################################################################

mod.reglog.ord <- polr(Grado ~ 
                         Edad +
                         Sexo +
                         Volumen + 
                         AreaCaraAnterior + 
                         AreaCaraPosterior + 
                         AreaTotal + 
                         CentroMasasX + 
                         CentroMasasY + 
                         CentroMasasZ + 
                         Esfera + 
                         Cilindro + 
                         Eje + 
                         EquivEsf + 
                         AVCC, 
                       data = datos.ordinal, Hess=TRUE) %>%
  stepAIC(direction='backward', trace=TRUE)

summary(mod.reglog.ord)

# Modelo igual al anterior, pero metiendo edad y sexo por motivos demográficos
mod.reglog.ord <- polr(Grado ~ 
                         Edad +
                         Sexo +
                         Volumen + 
                         AreaCaraAnterior + 
                         AreaCaraPosterior + 
                         AreaTotal + 
                         CentroMasasY + 
                         CentroMasasZ + 
                         Esfera + 
                         Cilindro + 
                         Eje + 
                         EquivEsf + 
                         AVCC, 
                       data = datos.ordinal, Hess=TRUE)

summary(mod.reglog.ord)

# Significaciones de los coeficientes
ctable <- coef(summary(mod.reglog.ord))
p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2
ctable <- cbind(ctable, "p value" = p)

# Intervalos de confianza
ci <- confint.default(mod.reglog.ord)

# Odds ratios
exp(coef(mod.reglog.ord))
exp(cbind(OR = coef(mod.reglog.ord), ci))

#################################################################################################
### EVALUACIÓN DEL GRADO DE ACUERDO 
### ENTRE PREDICCIONES DEL MODELO Y EL DIAGNÓSTICO VERDADERO
### TABLA DE CONFUSIÓN Y GRÁFICOS DE PUNTUACIONES
#################################################################################################

datos.ordinal$pred = predict(mod.reglog.ord, type='class')
datos.ordinal <- cbind(datos.ordinal, predict(mod.reglog.ord, type='prob'))

table(datos.ordinal$Grado, datos.ordinal$pred)

datos.ordinal.graf <- datos.ordinal %>%
  select(Grado, '0', '1', '2', '3', '4') %>%
  gather(GradoPred, Pred, '0':'4')

datos.ordinal.graf$GradoPred[datos.ordinal.graf$GradoPred == '0'] <- 'Ctrl'
datos.ordinal.graf$GradoPred[datos.ordinal.graf$GradoPred == '1'] <- 'I'
datos.ordinal.graf$GradoPred[datos.ordinal.graf$GradoPred == '2'] <- 'II'
datos.ordinal.graf$GradoPred[datos.ordinal.graf$GradoPred == '3'] <- 'III'
datos.ordinal.graf$GradoPred[datos.ordinal.graf$GradoPred == '4'] <- 'IV'

datos.ordinal.graf$GradoPred <- factor(datos.ordinal.graf$GradoPred)

pirateplot(formula = Pred ~ GradoPred,
           data = datos.ordinal.graf[datos.ordinal.graf$Grado == 0,],           
           theme = 2, cex.axis = 0.7,
           inf.method = 'iqr', avg.line.fun = median,
           bean.b.o = 0, bean.f.o = 0, ylim = c(0, 1), 
           width.max = 0.2, xlab = NA, ylab = 'Control', gl = NA, xaxt = NA)

myData <- datos.ordinal.graf %>% 
  filter(Grado == 0) %>% 
  select(GradoPred, Pred) %>% 
  group_by(GradoPred) %>% 
  summarize(Median = median(Pred)) %>% 
  select(Median)

lines(x=c(1,2,3,4,5), y=myData$Median, type='b', lwd=4, col='red')

pirateplot(formula = Pred ~ GradoPred,
           data = datos.ordinal.graf[datos.ordinal.graf$Grado == 1,],           
           theme = 2, cex.axis = 0.7,
           inf.method = 'iqr', avg.line.fun = median,  
           bean.b.o = 0, bean.f.o = 0, ylim = c(0, 1), 
           width.max = 0.2, xlab = NA, ylab = 'Grado I', gl = NA, xaxt = NA)

myData <- datos.ordinal.graf %>% 
  filter(Grado == 1) %>% 
  select(GradoPred, Pred) %>% 
  group_by(GradoPred) %>% 
  summarize(Median = median(Pred)) %>% 
  select(Median)

lines(x=c(1,2,3,4,5), y=myData$Median, type='b', lwd=4, col='red')

pirateplot(formula = Pred ~ GradoPred,
           data = datos.ordinal.graf[datos.ordinal.graf$Grado == 2,],           
           theme = 2, cex.axis = 0.7,
           inf.method = 'iqr', avg.line.fun = median,  
           bean.b.o = 0, bean.f.o = 0, ylim = c(0, 1), 
           width.max = 0.2, xlab = NA, ylab = 'Grado II', gl = NA, xaxt = NA)

myData <- datos.ordinal.graf %>% 
  filter(Grado == 2) %>% 
  select(GradoPred, Pred) %>% 
  group_by(GradoPred) %>% 
  summarize(Median = median(Pred)) %>% 
  select(Median)

lines(x=c(1,2,3,4,5), y=myData$Median, type='b', lwd=4, col='red')

pirateplot(formula = Pred ~ GradoPred,
           data = datos.ordinal.graf[datos.ordinal.graf$Grado == 3,],           
           theme = 2, cex.axis = 0.7,
           inf.method = 'iqr', avg.line.fun = median,  
           bean.b.o = 0, bean.f.o = 0, ylim = c(0, 1), 
           width.max = 0.2, xlab = NA, ylab = 'Grado III', gl = NA, xaxt = NA)

myData <- datos.ordinal.graf %>% 
  filter(Grado == 3) %>% 
  select(GradoPred, Pred) %>% 
  group_by(GradoPred) %>% 
  summarize(Median = median(Pred)) %>% 
  select(Median)

lines(x=c(1,2,3,4,5), y=myData$Median, type='b', lwd=4, col='red')

pirateplot(formula = Pred ~ GradoPred,
           data = datos.ordinal.graf[datos.ordinal.graf$Grado == 4,],           
           theme = 2, cex.axis = 0.7,
           inf.method = 'iqr', avg.line.fun = median,  
           bean.b.o = 0, bean.f.o = 0, ylim = c(0, 1), 
           width.max = 0.2, xlab = NA, ylab = 'Grado IV', gl = NA)

myData <- datos.ordinal.graf %>% 
  filter(Grado == 4) %>% 
  select(GradoPred, Pred) %>% 
  group_by(GradoPred) %>% 
  summarize(Median = median(Pred)) %>% 
  select(Median)

lines(x=c(1,2,3,4,5), y=myData$Median, type='b', lwd=4, col='red')

#################################################################################################
### GUARDAR MODELOS PARA APLICACIÓN WEB
#################################################################################################

summary(mod_fit_two)
summary(mod.reglog.ord)

save(file='modRegLog', mod_fit_two)
save(file='modRegLogOrd', mod.reglog.ord)
