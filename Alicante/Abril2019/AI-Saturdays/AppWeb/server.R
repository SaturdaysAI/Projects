###############################################################################################
### SERVER.R
###############################################################################################

###############################################################################################
### DEFINICIÓN DE TIBBLE CON USUARIOS Y CLAVES
###############################################################################################

user_base <- tibble(
  user = c("user", "admin"),
  password_hash = sapply(c("user", "admin"), sodium::password_store), 
  permissions = c("admin", "standard"),
  name = c("Usuario", "Administrador")
)

###############################################################################################
### CARGA DE LOS MODELOS
###############################################################################################

modRegLog <- load(file='modRegLog')
modRegLogOrd <- load(file='modRegLogOrd')

###############################################################################################
### COMIENZO DE LAS FUNCIONES
###############################################################################################

server <- function(input, output, session) {
  
  #############################################################################################
  ### FORMULARIO DE LOGIN
  ### SE AÑADE BOTÓN DE LOGOUT TRAS AUTENTICACIÓN DE USUARIO
  #############################################################################################
  
  credentials <- callModule(shinyauthr::login, "login", 
                            data = user_base,
                            user_col = user,
                            pwd_col = password_hash,
                            sodium_hashed = TRUE,
                            log_out = reactive(logout_init()))
  
  logout_init <- callModule(shinyauthr::logout, "logout", reactive(credentials()$user_auth))
  
  #############################################################################################
  ### SE MUESTRA LA BARRA LATERAL TRAS AUTENTICACIÓN
  #############################################################################################
  
  observe({
    if(credentials()$user_auth) {
      shinyjs::removeClass(selector = "body", class = "sidebar-collapse")
    } else {
      shinyjs::addClass(selector = "body", class = "sidebar-collapse")
    }
  })
  
  #############################################################################################
  ### MOSTRAR LISTADO DE OPCIONES BAJO EL FORMULARIO DE LOGIN
  #############################################################################################
  
  output$login_help <- renderUI({

    if(credentials()$user_auth) return(NULL)
    
    tagList(
      tags$p("Para solicitar nuevos usuarios envíe un correo al administrador", 
             class = "text-center")
      )
    
  })
  
  #############################################################################################
  ### MOSTRAR NOMBRE DE USUARIO
  #############################################################################################
  
  output$welcome <- renderText({
    
    req(credentials()$user_auth)
    
    glue("User: {user_info()$name}")
    
  })
  
  #############################################################################################
  ### CÁLCULO DEL KERATOSCORE Y DEL GRADO DE LA PATOLOGÍA
  #############################################################################################
  
  observeEvent(input$button1, {
    
    req(credentials()$user_auth)
    
    score1 <- predict(mod_fit_two, 
                     newdata = data.frame(
                       Edad = as.numeric(input$param1),
                       Sexo = input$param2,
                       Volumen = as.numeric(input$param3),
                       AreaCaraAnterior = as.numeric(input$param4),
                       AreaCaraPosterior = as.numeric(input$param5),
                       AreaTotal = as.numeric(input$param6),
                       CentroMasasZ = as.numeric(input$param8),
                       Cilindro = as.numeric(input$param10),
                       Eje = as.numeric(input$param11)
                     ), 
                     type = c("response"))
    
    score2 <- predict(mod.reglog.ord, 
                      newdata = data.frame(
                        Edad = as.numeric(input$param1),
                        Sexo = input$param2,
                        Volumen = as.numeric(input$param3),
                        AreaCaraAnterior = as.numeric(input$param4),
                        AreaCaraPosterior = as.numeric(input$param5),
                        AreaTotal = as.numeric(input$param6),
                        CentroMasasY = as.numeric(input$param7),
                        CentroMasasZ = as.numeric(input$param8),
                        Esfera = as.numeric(input$param9),
                        Cilindro = as.numeric(input$param10),
                        Eje = as.numeric(input$param11),
                        EquivEsf = as.numeric(input$param12),
                        AVCC = as.numeric(input$param13)
                      ), 
                      type = c("class"))
    
    score1 <- paste('KERATOCONUS SCORE: ', round(100 * score1, 1), '%', sep='')
    score2 <- paste('GRADO: ', score2, sep='')
    
    output$textScore1 <- renderText({score1})
    output$textScore2 <- renderText({score2})
    
  })
  
  #############################################################################################
  ### BORRAR SCORE CALCULADO EN SESIONES ANTERIORES
  #############################################################################################
  
  observeEvent(req(credentials()$user_auth), {
    
    output$textScore <- renderText({''})
    
  })

  #############################################################################################
  ### NUEVO UI TRAS AUTENTICACIÓN
  ### VALORES POR DEFECTO DE PACIENTE CONTROL
  #############################################################################################
  
  output$testUI <- renderUI({
    
    req(credentials()$user_auth)
    
    fluidPage(
      
      fluidRow(
        column(12,
               wellPanel(
                 fluidRow(
                   column(3, textInput(inputId='param1', label='Edad', value='57')),
                   column(3, selectInput(inputId='param2', label='Sexo', 
                                         choices=list('Mujer' = 'mujer', 'Hombre' = 'hombre'))),
                   column(3, textInput(inputId='param3', label='Volumen', value='26.13')),
                   column(3, textInput(inputId='param4', label='Área Cara Anterior', value='43.072'))
                 ),
                 fluidRow(
                   column(3, textInput(inputId='param5', label='Área Cara Posterior', value='44.506')),
                   column(3, textInput(inputId='param6', label='Área Total', value='104.845')),
                   column(3, textInput(inputId='param7', label='Centro Masas Y', value='0.036')),
                   column(3, textInput(inputId='param8', label='Centro Masas Z', value='0.782'))
                 ),
                 fluidRow(
                   column(3, textInput(inputId='param9', label='Esfera', value='2.25')),
                   column(3, textInput(inputId='param10', label='Cilindro', value='-0.75')),
                   column(3, textInput(inputId='param11', label='Eje', value='40')),
                   column(3, textInput(inputId='param12', label='Equivalente Esférico', value='1.88'))
                 ),
                 fluidRow(
                   column(3, textInput(inputId='param13', label='AVCC', value='1'))
                 )
               ),
               fluidRow(
                 column(3, actionButton(inputId = 'button1', label='CALCULAR SCORE'))
               ),
               fluidRow(
                 column(12, h1(''))
               ),
               wellPanel(
                 fluidRow(
                   column(6, h1(textOutput('textScore1'))),
                   column(6, h1(textOutput('textScore2')))
                 )
               )
        )
      )
    )
    
  })
  
}

