library(readxl)
library(dplyr)
library(tidyr)
library(ggplot2)
library(Amelia)
library(stringr)

# Getting data ----
# Reading and checking the Excel file
tef <- read_excel("Downloads/BD CE FUNDACION TELEFONICA 29_04_2020.xlsx", 
                  col_types = c("numeric", "text", "date", 
                  "date", "text", "numeric", "text", 
                  "text", "text", "text", "text", "text", 
                  "text", "text", "text", "text", "text"))

glimpse(tef)
summary(tef)
colnames(tef)

# setting features names
tef_colnames <- c("ID", "Curso", "Fecha_inicio", "Fecha_fin", "Estado", "Puntuacion",
                  "Sexo", "Fecha_registro", "Ultimo_login", "Fecha_nacimiento",
                  "Ciudad", "Pais", "Desempleado", "Nivel_estudios", "Tiempo_exp_laboral",
                  "Tiempo_reg_serv_emp", "Tiempo_desemp")

colnames(tef) <- tef_colnames
colnames(tef)

# Change <chr> to factor 
tef[, c(2, 5, 7, 11, 13:17)] <- data.frame(sapply(tef[, c(2, 5, 7, 11, 13:17)], as.factor))

# Change char dates to dates type
tef$Fecha_inicio <- as.Date(tef$Fecha_inicio)
tef$Fecha_fin <- as.Date(tef$Fecha_fin)
tef$Fecha_registro <- as.Date(tef$Fecha_registro)
tef$Ultimo_login <- as.Date(tef$Ultimo_login)
tef$Fecha_nacimiento <- as.Date(tef$Fecha_nacimiento)

# Adding Age column
tef$Edad <- as.numeric(round((Sys.Date() - tef$Fecha_nacimiento) / 365, 2))
summary(tef$Edad)

# Adding 'Tiempo_curso'
tef$Tiempo_curso <- as.numeric(tef$Fecha_fin - tef$Fecha_inicio) + 1
summary(tef$Tiempo_curso)

sum(stringr::str_detect(tef$Curso, ".Oro."))
#[1] 1925 There are only 1925 rows in El Oro

# 'Curso' column - check the freq and reducing the number of factors
table(tef$Curso)

tef$Curso <- str_replace(tef$Curso, "(.*Analí.*)", "Analitica_web")
tef$Curso <- str_replace(tef$Curso, "(.*Word[p, P]ress.*)", "Wordpress")
tef$Curso <- str_replace(tef$Curso, "(.*Marketing.*)", "Marketing_digital")
tef$Curso <- str_replace(tef$Curso, "(.*pág.*)", "Creacion_paginas_web")
tef$Curso <- str_replace(tef$Curso, "(.*Android.*)", "Creacion_android_apps")
tef$Curso <- str_replace(tef$Curso, "(.*HTML.*)", "Diseno_web_HTML5_CSS")
tef$Curso <- str_replace(tef$Curso, "(.*Emprend.*)", "Emprendimiento")
tef$Curso <- str_replace(tef$Curso, "(.*proyect.*)", "Metodologias_Agiles_Lean")
tef$Curso <- str_replace(tef$Curso, "(.*Hacking.*)", "Growth_Hacking")
tef$Curso <- str_replace(tef$Curso, "(.*[E, e]mpleo.*)", "Habilidades_para_empleo")
tef$Curso <- str_replace(tef$Curso, "(.*socioemo.*)", "Habilidades_socioemocionales")
tef$Curso <- str_replace(tef$Curso, "(.*Máq.*)", "Introduccion_Machine_Learning")
tef$Curso <- str_replace(tef$Curso, "(.*Mac.*)", "Introduccion_Machine_Learning")
tef$Curso <- str_replace(tef$Curso, "(.*programac.*)", "Introducción_programacion")
tef$Curso <- str_replace(tef$Curso, "(.*TICs.*)", "TICs_basico")

tef$Curso <- as.factor(tef$Curso)
table(tef$Curso)

# 'Estado' column - check the freq and the relationships
table(tef$Estado)
# Consider the different states and the relation with 'Fecha_inicio', 'Fecha_fin',
# 'Puntuacion'. How long to finish? Student with 'Iniciado' or 'Suspenso' status,
# What are the next steps according to FTE?

# 'Puntuacion' column 
summary(tef$Puntuacion)
# What is the meaning of '0'? is the same as NA? What is the grade system?

# 'Ciudad' column - check the freq and reducing the number of factors
table(tef$Ciudad)

# 'Ciudad' column to lowercase.
tef$Ciudad <- tolower(tef$Ciudad)

# In this case, '0' means NA
tef$Ciudad[tef$Ciudad == "0"] <- NA
tef$Ciudad <- as.factor(tef$Ciudad)
summary(tef$Ciudad)

# grouping cities into Provinces
tef$Provincia <- tef$Ciudad
tef$Provincia <- str_replace(tef$Provincia, "(.*alau.*)", "Chimborazo")
tef$Provincia <- str_replace(tef$Provincia, "(.*alfred.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*bato.*)", "Tungurahua")
tef$Provincia <- str_replace(tef$Provincia, "(.*amag.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*ante.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(.*dona.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(.*aren.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(.*atah.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*atun.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(.*azo.*)", "Cañar")
tef$Provincia <- str_replace(tef$Provincia, "(.*azu.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(.*baba.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(.*bah[i, í].*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*bals.*)", "Bolivar")
tef$Provincia <- str_replace(tef$Provincia, "(.*balz.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*bañ.*)", "Tungurahua")
tef$Provincia <- str_replace(tef$Provincia, "(.*boli.*)", "Bolivar")
tef$Provincia <- str_replace(tef$Provincia, "(.*borb.*)", "Esmeraldas")
tef$Provincia <- str_replace(tef$Provincia, "(.*buc.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*bue.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(.*calc.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*quit.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*calv.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(.*cañ.*)", "Cañar")
tef$Provincia <- str_replace(tef$Provincia, "(.*cañ.*)", "Cañar")
tef$Provincia <- str_replace(tef$Provincia, "(.*colim.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*triu.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*mej.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*pales.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*caria.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(.*casca.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(.*casco.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*coch.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(.*mayo.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(.*caya.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*centi.*)", "Zamora Chinchipe")
tef$Provincia <- str_replace(tef$Provincia, "(.*chaco.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(.*guarp.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(.*cham.*)", "Chimborazo")
tef$Provincia <- str_replace(tef$Provincia, "(.*chill.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(.*chone.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*punt.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(.*alam.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(.*coca.*)", "Orellana")
tef$Provincia <- str_replace(tef$Provincia, "(.*colon.*)", "Santa Elena")
tef$Provincia <- str_replace(tef$Provincia, "(.*colt.*)", "Chimborazo")
tef$Provincia <- str_replace(tef$Provincia, "(.*cota.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(.*coto.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(.*cotu.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(.*cuanc.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(.*cue.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(.*cuma.*)", "Chimborazo")
tef$Provincia <- str_replace(tef$Provincia, "daule", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*mui.*)", "Esmeraldas")
tef$Provincia <- str_replace(tef$Provincia, "(.*dele.*)", "Cañar")
tef$Provincia <- str_replace(tef$Provincia, "(.*quit.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*dur.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*nge.*)", "Carchi")
tef$Provincia <- str_replace(tef$Provincia, "(.*carm.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*emp.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "el eno", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(.*guab.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(.*pan.*)", "Azuay")
#tef$Provincia <- str_replace(tef$Provincia, "(.*pang.*)", "Zamora Chinchipe")
tef$Provincia <- str_replace(tef$Provincia, "(.*quinc.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*esmeraldas.*)", "Esmeraldas")
tef$Provincia <- str_replace(tef$Provincia, "(.*fla.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*orel.*)", "Orellana")
tef$Provincia <- str_replace(tef$Provincia, "(.*gene.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*gir.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(.*piz.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(.*ceo.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(.*quiz.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*gua[n, m].*)", "Chimborazo")
tef$Provincia <- str_replace(tef$Provincia, "(.*guara.*)", "Bolivar")
tef$Provincia <- str_replace(tef$Provincia, "(.*guaya.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*gus.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "gye", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*huam.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*huaq.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(.*iba.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(.*imb.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(.*inda.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*jara.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*jip.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*joy.*)", "Orellana")
tef$Provincia <- str_replace(tef$Provincia, "(.*jun.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*caro.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(.*con.*)", "Santo Domingo")
tef$Provincia <- str_replace(tef$Provincia, "(la man.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(.*tron.*)", "Cañar")
tef$Provincia <- str_replace(tef$Provincia, "(.*lago.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(.*nav.*)", "Bolivar")
tef$Provincia <- str_replace(tef$Provincia, "(lata.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(.*laur.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(lita.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "loja", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(lomas.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*oret.*)", "Orellana")
tef$Provincia <- str_replace(tef$Provincia, "(.*rios)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(lum.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(macar.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "macas", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "machachi", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(machal.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(malc.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(manab[i, í])", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "manta", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(marc.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(mir.*)", "Carchi")
tef$Provincia <- str_replace(tef$Provincia, "(moc.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(.*monta.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(monte.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(montu.*)", "Carchi")
tef$Provincia <- str_replace(tef$Provincia, "(.*moro.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*nap.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(nar.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(nob.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*nue.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(otav.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(paj.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(palo.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(pasa.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(past.*)", "Pastaza")
tef$Provincia <- str_replace(tef$Provincia, "(pat.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(pau.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(pede.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*carb.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*pel.*)", "Tungurahua")
tef$Provincia <- str_replace(tef$Provincia, "(pichi.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*jil.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(.*pill.*)", "Tungurahua")
tef$Provincia <- str_replace(tef$Provincia, "(pim.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(piñ.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(play.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*velo)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(.*tovi.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*shu.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(pueb.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(puerto ay.*)", "Galapagos")
tef$Provincia <- str_replace(tef$Provincia, "(.*ló.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(puy.*)", "Pastaza")
tef$Provincia <- str_replace(tef$Provincia, "(quev.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(.*nind.*)", "Esmeraldas")
tef$Provincia <- str_replace(tef$Provincia, "(quins.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(quir.*)", "Tungurahua")
tef$Provincia <- str_replace(tef$Provincia, "(riob.*)", "Chimborazo")
tef$Provincia <- str_replace(tef$Provincia, "(roc.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(sach.*)", "Orellana")
tef$Provincia <- str_replace(tef$Provincia, "(salc.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(salinas-.*)", "Santa Elena")
tef$Provincia <- str_replace(tef$Provincia, "salinas", "Santa Elena")
tef$Provincia <- str_replace(tef$Provincia, "(.*bolí.*)", "Bolivar")
tef$Provincia <- str_replace(tef$Provincia, "(salit.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(samb.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*crist[o, ó].*)", "Galapagos")
tef$Provincia <- str_replace(tef$Provincia, "(.*borj.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(.*gabr.*)", "Carchi")
tef$Provincia <- str_replace(tef$Provincia, "(.*golq.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*isid.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(.*yagu.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*bosc.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*lorenz.*)", "Esmeraldas")
tef$Provincia <- str_replace(tef$Provincia, "(.*mig.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(.*pab.*)", "Santa Elena")
tef$Provincia <- str_replace(tef$Provincia, "(.*huac.*)", "Carchi")
tef$Provincia <- str_replace(tef$Provincia, "(.*rafa.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(.*vice.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "santa ana", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "santa cruz", "Galapagos")
tef$Provincia <- str_replace(tef$Provincia, "(santa lu.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(santa ro.*)", "El Oro")
tef$Provincia <- str_replace(tef$Provincia, "(.*mend.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*tiw.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(.*domi.*)", "Santo Domingo")
tef$Provincia <- str_replace(tef$Provincia, "(saqui.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(sigc.*)", "Cotopaxi")
tef$Provincia <- str_replace(tef$Provincia, "(sigs.*)", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(simi.*)", "Bolivar")
tef$Provincia <- str_replace(tef$Provincia, "(suc.*)", "Sucumbios")
tef$Provincia <- str_replace(tef$Provincia, "(tab.*)", "Pichincha")
tef$Provincia <- str_replace(tef$Provincia, "(tai.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(tamb.*)", "Cañar")
tef$Provincia <- str_replace(tef$Provincia, "tena", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(tos.*)", "Manabi")
tef$Provincia <- str_replace(tef$Provincia, "(tres.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(tul.*)", "Carchi")
tef$Provincia <- str_replace(tef$Provincia, "(urc.*)", "Imbabura")
tef$Provincia <- str_replace(tef$Provincia, "(urd.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(vale.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(ven.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(vince.*)", "Los Rios")
tef$Provincia <- str_replace(tef$Provincia, "(yacu.*)", "Zamora Chinchipe")
tef$Provincia <- str_replace(tef$Provincia, "(yant.*)", "Zamora Chinchipe")
tef$Provincia <- str_replace(tef$Provincia, "(zam.*)", "Zamora Chinchipe")
tef$Provincia <- str_replace(tef$Provincia, "(zap.*)", "Loja")
tef$Provincia <- str_replace(tef$Provincia, "(zum.*)", "Zamora Chinchipe")

tef$Provincia <- str_replace(tef$Provincia, "^c$", "Azuay")
tef$Provincia <- str_replace(tef$Provincia, "(.*aros.*)", "Napo")
tef$Provincia <- str_replace(tef$Provincia, "(esm.*)", "Esmeraldas")
tef$Provincia <- str_replace(tef$Provincia, "(.*pla.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "(km.*)", "Guayas")
tef$Provincia <- str_replace(tef$Provincia, "(.*lib.*)", "Santa Elena")
tef$Provincia <- str_replace(tef$Provincia, "santa elena", "Santa Elena")
tef$Provincia <- str_replace(tef$Provincia, "(.*dpm.*)", "Santo Domingo")
tef$Provincia <- str_replace(tef$Provincia, "(.*logr.*)", "Morona Santiago")
tef$Provincia <- str_replace(tef$Provincia, "milagro", "Guayas")

prov <- tef %>% group_by(Ciudad, Provincia) %>% 
        summarize(Cantidad = n()) %>% 
        select(Ciudad, Provincia, Cantidad)

# let's check 'Provincia' after the feature engineering
table(tef$Provincia)

# 'Nivel_estudios' column - check the freq and reducing the number of factors
summary(tef$Nivel_estudios)

# 'Tiempo_exp_laboral' column - check the freq and reducing the number of factors
table(tef$Tiempo_exp_laboral)
tef$Tiempo_exp_laboral[tef$Tiempo_exp_laboral =="0"] <- NA
tef$Tiempo_exp_laboral <- droplevels(tef$Tiempo_exp_laboral)
table(tef$Tiempo_exp_laboral)

# 'Tiempo_reg_serv_emp' column - check the freq and reducing the number of factors
table(tef$Tiempo_reg_serv_emp)
tef$Tiempo_reg_serv_emp[tef$Tiempo_reg_serv_emp =="0"] <- NA
tef$Tiempo_reg_serv_emp <- droplevels(tef$Tiempo_reg_serv_emp)
table(tef$Tiempo_reg_serv_emp)

# 'Tiempo_desemp' column - check the freq and reducing the number of factors
table(tef$Tiempo_desemp)
tef$Tiempo_desemp[tef$Tiempo_desemp =="0"] <- NA
tef$Tiempo_desemp <- droplevels(tef$Tiempo_desemp)
table(tef$Tiempo_desemp)

# Missing Values ----
sum(is.na(tef))
missmap(tef, y.at = c(1), y.labels = c(""), col = c("yellow","black"))

# Plots ----
tef %>% ggplot(aes(Tiempo_curso, fill = Sexo)) +
        geom_histogram(bins = 15, col = "black")

tef %>% ggplot(aes(Puntuacion, fill = Sexo)) +
        geom_histogram(bins = 15, col = "black")

tef %>% ggplot(aes(Sexo, Edad, fill = Sexo)) +
        geom_boxplot()

tef %>% ggplot(aes(Sexo, Puntuacion, fill = Sexo)) +
        geom_boxplot()

tef %>% ggplot(aes(Edad, Puntuacion, col = Sexo, alpha = I(0.5))) +
        geom_point() +
        geom_smooth(aes(group = 1), method = "lm", se = F,
                    formula = y ~ log(x), col = "blue")

tef %>% ggplot(aes(Sexo)) +
        geom_bar()
# tables

df_curso <- tef %>% group_by(Curso) %>% 
        summarize(Cantidad = n()) %>% 
        arrange(desc(Cantidad))
df_curso

df_ciudad <- tef %>% group_by(Ciudad) %>% 
        summarize(Cantidad = n()) %>% 
        arrange(desc(Cantidad))
df_ciudad 

tef %>% filter(!is.na(Ciudad) & Estado == "Aprobado")


df_ID <- tef %>% group_by(ID) %>% 
        summarize(Cantidad = n()) %>% 
        arrange(desc(Cantidad))
df_ID

ID_5149 <- tef %>% select(ID, Curso, Fecha_inicio, Fecha_fin, Estado, Puntuacion, Ciudad, 
               Nivel_estudios, Edad) %>% 
        filter(ID == 5149)
ID_5149

# The final table wll consider only Pronvicia without NAs
fte_ec <- tef %>% filter(!is.na(Provincia))
write.csv(fte_ec, "training_center_ec.csv")

