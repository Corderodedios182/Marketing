#Resumen 

  #Tablas comparativos
  library(gridExtra)
  library(tidyr)
  library(dplyr)
  library(ggplot2)
  library(lubridate)
  library(stringr)
  library(cowplot)
  library(ggthemes)
  setwd("~")
  
  specify_decimal <- function(x, k) as.numeric(trimws(format(round(x, k), nsmall=k)))
  format_number <- function(x,k) formatC(as.numeric(x),format="f",digit=0,big.mark = ",")

  Lead_001 <- read.csv('Documentos/Adsocial/GWEP/Data/Enero_Leads_001.csv', stringsAsFactors = FALSE)
  
  Lead_001$Estado.de.Posible.cliente <- trimws(Lead_001$Estado.de.Posible.cliente)
  Lead_001$Estado.de.Posible.cliente <- str_replace_all(Lead_001$Estado.de.Posible.cliente,"Contactar en el futuro","Contactar")
  Lead_001$Estado.de.Posible.cliente <- str_replace(Lead_001$Estado.de.Posible.cliente,names(table(test)[9]),"Agendada")
  Lead_001$Estado.de.Posible.cliente <- str_replace_all(Lead_001$Estado.de.Posible.cliente,"Intento de contacto","Intento")
  
  Lead <- Lead_001 %>% 
    select(`Correo.electrónico`, `Correo.electrónico.secundario`, Fuente.de.Posible.cliente, 
           Estado.de.Posible.cliente, Nombre.completo, Desarrollo, Nombre.de.la.campaña.de.anuncios,
           Nombre.del.grupo.de.anuncios, Estatus.KPI, Descripción, Campaña.MKT, LP, Forma.de.contacto,
           Motivo.de.perdido, Palabra.clave, Hora.de.creación, Hora.de.modificación, Hora.de.la.última.actividad,
           Hora.de.cita.web)
  
  #Lead$Hora.de.creación <- as.data.frame(matrix(unlist(strsplit(Lead$Hora.de.creación," ")),ncol = 2, byrow = TRUE))[1]
  Lead$Hora.de.creación <-as.Date(Lead$Hora.de.creación, format = "%Y-%m-%d")
  Lead$Hora.de.creación <- ymd(Lead$Hora.de.creación)
  Lead['ym'] <- ymd(paste0(year(Lead$Hora.de.creación),"-",month(Lead$Hora.de.creación) ,"-01"))
  
  #Desarrollo
  Lead$Desarrollo <- str_replace_all(Lead$Desarrollo, "&#x20;", " ")
  Lead$Desarrollo <- str_replace_all(Lead$Desarrollo, "&#x20;", " ")
  Lead$Desarrollo <- str_replace_all(Lead$Desarrollo, "&e", "é")
  Lead$Desarrollo <- str_replace_all(Lead$Desarrollo, ";", "é")
  
  Lead$Fuente.de.Posible.cliente <- str_replace_all(Lead$Fuente.de.Posible.cliente, "Faceboock", "Facebook")
  
  tmp <- c(Lead %>% group_by(Desarrollo) %>% 
             summarise(Conteo = n()) %>%
             filter(Conteo > 20 & !Desarrollo %in% c("Parque Satélite","Vidarte","La Purísima")))[1]
  
  Lead <- Lead %>% filter(Desarrollo %in% tmp$Desarrollo & ym > '2018-12-01')
  table(Lead$ym)
  
  #Historico por Mes Desarrollo
  table(Lead$Desarrollo)
  desarrollo <- "Real de Lutecia"
  
  Conteo <- Lead %>% group_by(ym,Desarrollo) %>% summarise(Conteo = n()) %>%
    filter(!is.na(ym) & Desarrollo == desarrollo)
  
  head(Conteo) ; table(Conteo$Desarrollo)
  
  tabla_1 <- ggplot(Conteo, aes(x = ym, y = Conteo)) + geom_point(color = "#00AFBB") +
    geom_line(color = "#00AFBB") +
    theme(axis.text.x = element_text(angle = 90)) +
    geom_text(aes(label = Conteo), position = position_stack(vjust = 1.1), size = 4) + 
    ggtitle(paste0("Zoho, ",unique(Conteo$Desarrollo)), 
            subtitle = paste0(format_number(sum(Conteo$Conteo))," Son todos los registros, no todos los Leads aquí son buenos")) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_1
  #Fuente de Lead por Desarrollo mes
  Fuente_clientes <- c("Facebook","Google","Instagram","Langind page","Página web")
  
  Conteo <- Lead %>%
    group_by(Hora.de.creación, Desarrollo , Fuente.de.Posible.cliente, Estado.de.Posible.cliente) %>%
    summarise(Conteo = n()) %>%
    filter(Fuente.de.Posible.cliente %in% Fuente_clientes & Desarrollo == desarrollo ) 
    
  Porcentajes <- data.frame(Conteo) %>%
    mutate(Porcentaje = Conteo/sum(Conteo)) %>%
    group_by(Fuente.de.Posible.cliente) %>%
    summarise(a = specify_decimal(sum(Porcentaje),2))
    
  Porcentajes$b <- sprintf("%.f%%", 100*Porcentajes$a)
  
  for(i in 1:dim(Porcentajes)[1]){ A[i] <- paste0( Porcentajes$Fuente.de.Posible.cliente[i], " ", Porcentajes$b[i] ) }
  subtitle <- str_replace_all(paste0(A[1] ," ", A[2] ," " , A[3] ," ", A[4]," ", A[5]," ", A[6]),"NA","")
  
  head(Conteo) ; sum(Conteo$Conteo)
  
  tabla_2 <- ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Fuente.de.Posible.cliente)) +
    geom_col(position = "stack") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle(paste0(format_number(sum(Conteo$Conteo)), " registros de plataformas digitales"),
            subtitle = subtitle) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_2
  
  #Lead de Interes por Desarrollo
  #Tipo_Lead <- c("Contactado","Contactar en el futuro","Visita agendada","Intento de contacto")
  Tipo_Lead <- c("Contactado","Contactar","Agendada","Intento")
  
  Conteo <- filter(Conteo, Estado.de.Posible.cliente %in% Tipo_Lead)
  
  Porcentajes <- data.frame(Conteo %>% group_by(Estado.de.Posible.cliente,Desarrollo) %>%
    summarise(Suma = sum(Conteo))) %>%
    mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  
  Porcentajes$b <- sprintf("%.f%%", 100*Porcentajes$Porcentaje) ; Porcentajes
  
  for(i in 1:dim(Porcentajes)[1]){ A[i] <- paste0(Porcentajes$Estado.de.Posible.cliente[i], " ", Porcentajes$Suma[i], " (",Porcentajes$b[i] , ")") }
  subtitle <- str_replace_all(paste0(A[1] ," ", A[2] ," " , A[3] ," ", A[4]," ", A[5]," ", A[6]),"NA","")
  
  tabla_3 <- ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Estado.de.Posible.cliente)) +
    geom_col(position = "stack") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle(paste0(format_number(sum(Conteo$Conteo))," Leads de Interés "),
            subtitle = subtitle) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
 #tabla_3
  
  #Leads de Interes Plataformas
  Leads_Zoho <- Conteo %>% group_by(Desarrollo,Hora.de.creación,Fuente.de.Posible.cliente) %>% summarize(Leads = sum(Conteo))
  Leads_Zoho$Mes <- month(Leads_Zoho$Hora.de.creación, label = TRUE)
  Leads_Zoho$Año <- year(Leads_Zoho$Hora.de.creación)
  Leads_Zoho <- Leads_Zoho %>% group_by(Año,Mes,Fuente.de.Posible.cliente) %>% summarize(Leads = sum(Leads))
  names(Leads_Zoho) <- c("Año", "Mes", "Plataforma", "Leads Interés")
    
  Porcentajes <- data.frame(Conteo %>% group_by(Fuente.de.Posible.cliente, Desarrollo) %>% 
    summarise(Suma = sum(Conteo))) %>% 
    mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  
  Porcentajes$b <- sprintf("%.f%%", 100*Porcentajes$Porcentaje) ; Porcentajes
  
  for(i in 1:dim(Porcentajes)[1]){ A[i] <- paste0(Porcentajes$Fuente.de.Posible.cliente[i], " ", Porcentajes$Suma[i], " (",Porcentajes$b[i] , ")") }
  subtitle <- str_replace_all(paste0(A[1] ," ", A[2] ," " , A[3] ," ", A[4]," ", A[5]," ", A[6]),"NA","")
  
  tabla_4 <- ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Fuente.de.Posible.cliente)) +
    geom_col(position = "stack") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle("Lead de Interés por Plataforma",
            subtitle = subtitle) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_4
  
  #############################
  #Información de las campañas#
  #############################
  Plataformas <- read.csv("~/Documentos/Adsocial/GWEP/Campañas/campañas.csv")
  
  tmp_Fb <- Plataformas %>% filter(Plataforma == "Facebook")
  tmp_Go <- Plataformas %>% filter(Plataforma == "Google")
  
  tmp_Fb$Fecha_Inicio <- as.Date(tmp_Fb$Fecha_Inicio, format = "%Y-%m-%d")
  tmp_Fb$Fecha_Inicio <- ymd(tmp_Fb$Fecha_Inicio)
  tmp_Fb['ym'] <- ymd(paste0(year(tmp_Fb$Fecha_Inicio),"-",month(tmp_Fb$Fecha_Inicio) ,"-01"))
  
  tmp_Go$Fecha_Inicio <- as.Date(tmp_Go$Fecha_Inicio, format = "%d/%m/%Y")
  tmp_Go$Fecha_Inicio <- ymd(tmp_Go$Fecha_Inicio)
  tmp_Go['ym'] <- ymd(paste0(year(tmp_Go$Fecha_Inicio),"-",month(tmp_Go$Fecha_Inicio) ,"-01"))
  
  Plataformas <- rbind(tmp_Fb,tmp_Go) ; rm(tmp_Fb,tmp_Go)
  table(Plataformas$Desarrollo)
  
  Plataformas <- filter(Plataformas, ym > "2018-12-01" & Desarrollo %in% c("Aurum","Cumbres Herradura","El Cortijo","Parque Hacienda","Real de Lutecia","Reserva del sur"))
  table(Plataformas$Desarrollo)

  #Campañas por Mes, Desarrollo y plataforma
  Conteo <- Plataformas %>% group_by(ym, Plataforma, Desarrollo, Campaña) %>%
    summarise(Conteo = n()) %>%
    filter(Desarrollo == desarrollo) %>%
    group_by(ym, Plataforma) %>%
    summarise(Conteo = n())
  
  Conteo
  
  tabla_5 <- ggplot(Conteo, aes(x = ym, y = Conteo, fill = Plataforma)) +
    geom_col(alpha = 0.8) +
    geom_text(aes(label = Conteo), position = position_stack(vjust = 0.5), size = 5) +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle(paste0("Número de Campañas ", desarrollo, " 2019")) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_5
  
  #Resultados de Campañas por Mes, Desarrollo
  #¿Que Plataforma da mejores Resultados?
  tmp <- Plataformas %>% select(Desarrollo, Plataforma, ym, Impresiones, Clics, Conversiones, Costo)
  tmp_0 <- gather(tmp, "metrica","valor",-ym,-Plataforma, -Desarrollo)
  
  table(tmp_0$metrica)
  
  tmp_0 <- tmp_0 %>% group_by(Desarrollo, Plataforma,ym, metrica) %>% 
    summarise(suma = round(sum(valor, na.rm = TRUE))) %>% filter(Desarrollo == desarrollo)
  
  tmp_p <- filter(tmp_0, metrica == "Clics") %>% group_by(Plataforma) %>% summarize(Suma = sum(suma)) %>% mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  tmp_p$Porcentaje <- sprintf("%.f%%", 100*tmp_p$Porcentaje) ; tmp_p
  
  tmp_p$Suma <- paste0(formatC(as.numeric(tmp_p$Suma), format="f", digits=0, big.mark=","))
  
  tabla_6 <- ggplot(filter(tmp_0, metrica == "Clics"), aes(x = ym, y = suma, fill = Plataforma)) +
    geom_col(alpha = .8) +
    geom_text(aes(label = format_number(suma)), position = position_stack(vjust = 0.5), size = 3) +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle(paste0("Plataformas, " , desarrollo  , ", Clics"),
            subtitle = paste0("Facebook ", filter(tmp_p, Plataforma == 'Facebook') %>% select(Suma) ," (" , filter(tmp_p, Plataforma == 'Facebook') %>% select(Porcentaje) , ")  ",
                              "Google "  , filter(tmp_p, Plataforma == 'Google') %>% select(Suma) ," (" , filter(tmp_p, Plataforma == 'Google') %>% select(Porcentaje) , ")  ")) + 
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_6
  
  tmp_p <- filter(tmp_0, metrica == "Conversiones") %>% group_by(Plataforma) %>% summarize(Suma = sum(suma)) %>% mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  tmp_p$Porcentaje <- sprintf("%.f%%", 100*tmp_p$Porcentaje) ; tmp_p
  
  tabla_7 <- ggplot(filter(tmp_0, metrica == "Conversiones"), aes(x = ym, y = round(suma), fill = Plataforma)) +
    geom_col(alpha = .8) +
    geom_text(aes(label = format_number(suma)), position = position_stack(vjust = 0.5), size = 3) +
    labs(colour = "metrica") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle("Conversiones", subtitle = paste0("Facebook ", filter(tmp_p, Plataforma == 'Facebook') %>% select(Suma) ," (" , filter(tmp_p, Plataforma == 'Facebook') %>% select(Porcentaje) , ")  ",
                                              "Google "  , filter(tmp_p, Plataforma == 'Google') %>% select(Suma) ," (" , filter(tmp_p, Plataforma == 'Google') %>% select(Porcentaje) , ")")) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_7

  tmp_p <- filter(tmp_0, metrica == "Costo") %>% group_by(Plataforma) %>% summarize(Suma = sum(suma)) %>% mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  tmp_p$Porcentaje <- sprintf("%.f%%", 100*tmp_p$Porcentaje) ; tmp_p
  tmp_p$Suma <- paste0("$",formatC(as.numeric(tmp_p$Suma), format="f", digits=0, big.mark=",")) ; tmp_p
  
  tabla_8 <- ggplot(filter(tmp_0, metrica == "Costo"), aes(x = ym, y = suma, fill = Plataforma)) +
    geom_col() +
    geom_text(aes(label = paste0("$",formatC(as.numeric(suma), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle("Inversión", 
            subtitle = paste0("Facebook ", filter(tmp_p, Plataforma == 'Facebook') %>% select(Suma) ," (" , filter(tmp_p, Plataforma == 'Facebook') %>% select(Porcentaje) , ")  ",
                              "Google "  , filter(tmp_p, Plataforma == 'Google') %>% select(Suma) ," (" , filter(tmp_p, Plataforma == 'Google') %>% select(Porcentaje) , ")")) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
#  tabla_8

  #plot_grid(tabla_5, tabla_6,tabla_7, tabla_8, nrow = 2, ncol = 2, hjust = .5)
  
  grid.arrange(tabla_1,tabla_2 ,
               tabla_3, tabla_4 ,
               nrow = 2, ncol = 2, as.table = TRUE)

  grid.arrange(tabla_6, tabla_8 ,
               tabla_7,
               nrow = 2, ncol = 2, as.table = TRUE)
  
  #Tabla Resumen Campañas Y Zoho 
  Conteo <- Plataformas %>% group_by(ym, Plataforma) %>%
    filter(Desarrollo == desarrollo) %>%
    summarize(Clics = sum(Clics,na.rm = TRUE),Conversiones = sum(Conversiones,na.rm = TRUE), Inversión = sum(Costo,na.rm = TRUE))
  names(Conteo) <- c("Fecha","Plataforma","Clics","Conversión","Inversión")
  Conteo$Inversión <-  paste0("$",formatC(as.numeric(Conteo$Inversión), format="f", digits=0, big.mark=","))
  Conteo$Clics <- paste0(formatC(as.numeric(Conteo$Clics), format="f", digits=0, big.mark=","))
  Conteo['Mes'] <- month(Conteo$Fecha, label = TRUE)
  Conteo['Año'] <- year(Conteo$Fecha)
  
  Conteo <- data.frame(Conteo) %>% select(Año, Mes, Plataforma, Clics, Conversión, Inversión)

  #plot_grid(tabla_1, tabla_2,tabla_3, tabla_4,
  #  tabla_6, tabla_8,tabla_7, nrow = 4, ncol = 2, hjust = .5)
  setwd("/home/carlos/Documentos/Adsocial/GWEP/Graficas/Por_Desarrollo_Finales/")
  
  write.csv(Conteo,paste0("", desarrollo, "_Plataformas.csv"), row.names = FALSE)
  write.csv(Leads_Zoho,paste0("", desarrollo, "_LeadInterés.csv"), row.names = FALSE)
  
  #Leads_Zoho <- ggplot() + annotation_custom(tableGrob(Leads_Zoho)) + labs(title = 'Aurum Leads de Interés Zoho') #Está info viene de la tabla 4
  #Resultados_Plataformas <- ggplot() + annotation_custom(tableGrob(Conteo)) + labs(title = 'Aurum Resultados Plataformas')
  #grid.arrange(Resultados_Plataformas, Leads_Zoho, nrow = 2, ncol = 2, as.table = TRUE)
  
  
    
  
  
  
