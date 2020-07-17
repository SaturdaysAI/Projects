# Proyecto COVID-19 y Twitter
# Limpieza de datos
# ---------------------------

# Carga de librerias
library(tidyverse) # Manejo y carga de datos en formato tidy
library(tidytext) # Manejo de texto en formato tidy
library(tm) # Procesamiento de texto
library(readxl) # Lectura de archivos excel
library(udpipe) # Modelos diseñados para lematización
library(ggplot2)


# Carga de los datos recolectados
# -------------------------------
covid_data <- read_excel("data/covid_guayaquil.xlsx", 
                   col_types = c("date", "text", "text", 
                                  "text", "numeric", "numeric"))
str(covid_data)

covid_data <- as.data.frame(covid_data)
str(covid_data)

covid_data_l <- covid_data


#crear la columna id_tw para la lematizacion
id_tw <- str_c("doc", row.names(covid_data_l))
covid_data_l <- cbind(covid_data_l, id_tw) 

View(covid_data_l)


# Limpieza de la data
# -------------------

# quitar los saltos de linea y tabulaciones
covid_data_l$tweet_full_text <- gsub("[[:cntrl:]]", " ", covid_data_l$tweet_full_text)

# convertir todo a minusculas
covid_data_l$tweet_full_text <- tolower(covid_data_l$tweet_full_text)

# quitar los signos de puntuacion
covid_data_l$tweet_full_text <- removePunctuation(covid_data_l$tweet_full_text)

# quitar los numeros
covid_data_l$tweet_full_text <- removeNumbers(covid_data_l$tweet_full_text)

# eliminar los espacios vacios excesivos
covid_data_l$tweet_full_text <- stripWhitespace(covid_data_l$tweet_full_text)

str(covid_data_l)


# Eliminacion de stopwords
# ------------------------
stopwords_es_2 = tibble(Palabra=tm::stopwords(kind = "es"), Fuente="tm")
stopwords_es_3 = tibble(Palabra=stopwords::stopwords(language = "es", source = "stopwords-iso")
                        , Fuente="stopwords-iso")
stopwords_es_4 = tibble(Palabra=stopwords::stopwords(language = "es", source = "snowball")
                        , Fuente="snowball")
stopwords_es = rbind(stopwords_es_2, stopwords_es_3, stopwords_es_4)
stopwords_es = stopwords_es[!duplicated(stopwords_es$Palabra),]
remove(stopwords_es_2, stopwords_es_3, stopwords_es_4)

stopwords_es[sample(nrow(stopwords_es),size = 10, replace = F),]

covid_data_l$tweet_full_text <- removeWords(covid_data_l$tweet_full_text, words = stopwords_es$Palabra)
covid_data_l$tweet_full_text = str_squish(covid_data_l$tweet_full_text)

str(covid_data_l)



# Analisis del corpus
# -------------------
nov_corpus <- Corpus(VectorSource(covid_data_l$tweet_full_text))
nov_corpus

# Term Document Matrix
nov_tdm <- TermDocumentMatrix(nov_corpus)
nov_tdm

# Frecuencia de palabras
nov_mat <- as.matrix(nov_tdm)
dim(nov_mat)

nov_mat <- nov_mat %>% rowSums() %>% sort(decreasing = TRUE)
nov_mat <- data.frame(palabra = names(nov_mat), frec = nov_mat)
nov_mat[1:100, ]

# Graficas de las palabras
nov_mat[1:50, ] %>%
  ggplot(aes(palabra, frec)) +
  geom_bar(stat = "identity", color = "black", fill = "#87CEFA") +
  geom_text(aes(hjust = 1.3, label = frec)) + 
  coord_flip() + 
  labs(title = "Palabras más frecuentes",  x = "Palabras", y = "Número de usos")

nov_mat %>%
  mutate(perc = (frec/sum(frec))*100) %>%
  .[1:50, ] %>%
  ggplot(aes(palabra, perc)) +
  geom_bar(stat = "identity", color = "black", fill = "#87CEFA") +
  geom_text(aes(hjust = 1.3, label = round(perc, 2))) + 
  coord_flip() +
  labs(title = "Diez palabras más frecuentes", x = "Palabras", y = "Porcentaje de uso")


# Lematizacion
# ------------
dl <- udpipe_download_model(language = "spanish")
str(dl)

model <- udpipe_load_model(file = "spanish-gsd-ud-2.4-190531.udpipe")
udpipe_lema <- udpipe_annotate(model, x = covid_data_l$tweet_full_text)
udpipe_lema <- as_tibble(udpipe_lema)

udpipe_lema %>%
  unnest_tokens(output = Palabra, input = token) %>% 
  anti_join(stopwords_es) -> udpipe_lema

udpipe_lema[udpipe_lema$Palabra=="pacientes",c("Palabra","lemma")]

View(covid_data_l)



# Tokenizacion
# ------------

# Tokenización por palabras
tidy_covid_data <- covid_data_l %>%
  unnest_tokens(output = Palabra,input = tweet_full_text)

# La función se encarga de descartar puntuación y caracteres especiales, todo en minúsculas
head(tidy_covid_data$Palabra, n = 50)


# Tokenización por n-gramas
tidy_covid_data_ngram3 <- covid_data_l %>%
  unnest_tokens(output = Palabra,input = tweet_full_text, token = "ngrams", n = 3)

head(tidy_covid_data_ngram3$Palabra, n = 20)



# Tokenización final a partir del DF lematizado
# ---------------------------------------------
tidy_covid_data = udpipe_lema %>% 
  filter(!is.na(lemma)) %>% 
  unnest_tokens(output = Palabra, input = Palabra)

names(tidy_covid_data)[which(names(tidy_covid_data)=="doc_id")] = "id_tw"

head(tidy_covid_data$lemma, n = 20)

View (tidy_covid_data)


# Stemming
# --------
tidy_covid_data$Stem = stemDocument(tidy_covid_data$Palabra, language="spanish")
tidy_covid_data[tidy_covid_data$Palabra=="tiempos",c("Palabra","lemma","Stem")]

tidy_covid_data[tidy_covid_data$Palabra=="ecuatoriano",c("Palabra","lemma","Stem")]

View(tidy_covid_data)



# Grabar el resultado de la limpieza
# ----------------------------------
View(covid_data_l)

tidy_covid_data1 <- tidy_covid_data

tidy_covid_data %>% 
  inner_join(covid_data_l[c("id_tw","tweet.created_at","tweet.user.screen_name","tweet.user.location","Depresivo","Cadena depres")], 
             by="id_tw") -> tidy_covid_data

View(tidy_covid_data)

write.csv(covid_data_l, file="covid_data_limpio.csv", row.names = F)
write.csv(tidy_covid_data, file="lema_covid_data.csv", row.names = F)

# Se obtiene 2 archivos
# covid_data_limpio.csv: es el archivo original en el cual se agrego una columna id_tw que es el identificador del tweet,
#                        el texto esta limpio y listo para lematizacion
# lema_covid_data.csv: es el archivo con el resultado de la lematizacion, tokenizacion y steeming.
#                      se encuentra la descripcion de cada palabra, la columna id_tw indica el tweet que corresponde. 
#                      a traves del id_tw se puede hacer un join con el primer archivo.




