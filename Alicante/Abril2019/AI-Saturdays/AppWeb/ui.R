###############################################################################################
### UI.R
###############################################################################################

###############################################################################################
### LIBRERÍAS
###############################################################################################

library(shiny)
library(shinydashboard)
library(dplyr)
library(shinyjs)
library(glue)
library(shinyauthr)

library(ggvis)
library(DT)

library(MASS)

library(ggthemes)

library(data.table)
library(tidyr)

library(shinyWidgets)

library(ggplot2)
library(rlang)

###############################################################################################
### COMIENZO DEL UI
###############################################################################################

ui <- dashboardPage(
  
  #############################################################################################
  ### CABECERA: TÍTULO, BOTÓN DESPLIEGUE MENÚ LATERAL, BOTÓN LOGOUT, BOTÓN AI SATURDAYS
  #############################################################################################
  
  dashboardHeader(title = "KERATOSCORE",
                  tags$li(class = "dropdown", style = "padding: 8px;",
                          shinyauthr::logoutUI(id = "logout", label = 'Cerrar sesion')),
                  tags$li(class = "dropdown", 
                          tags$a(icon("question-circle"), 
                                 href = "https://www.saturdays.ai/",
                                 title = "AI Saturdays"))
  ),
  
  #############################################################################################
  ### BARRA LATERAL ESCONDIDA
  #############################################################################################
  
  dashboardSidebar(disable = TRUE, collapsed = TRUE, 
                   div(textOutput("Bienvenido"), style = "padding: 20px")
  ),
  
  #############################################################################################
  ### PANEL PRINCIPAL
  #############################################################################################
  
  dashboardBody(
    shinyjs::useShinyjs(),
    tags$head(tags$style(".table{margin: 0 auto;}"),
              tags$script(src="https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.5.16/iframeResizer.contentWindow.min.js",
                          type="text/javascript"),
              includeScript("returnClick.js")
    ),
    shinyauthr::loginUI(id = "login", 
                        title = 'Calculador Keratoscore',
                        user_title = 'Usuario',
                        pass_title = 'Clave',
                        login_title = 'Login',
                        error_message = 'Usuario o clave incorrecta!'),
    uiOutput("login_help"),
    uiOutput("testUI"),
    HTML('<div data-iframe-height></div>')
  )
)
