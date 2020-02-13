#Tablas comparativos
library(gridExtra) ; library(tidyr) ; library(dplyr) ; library(ggplot2) ; library(lubridate) ; library(stringr) ;library(cowplot) ; library(ggthemes)
setwd("~")

Lead_001 <- read.csv('Documentos/3_Adsocial/GWEP/Data/Leads_001.csv', stringsAsFactors = FALSE)
  
#Son los datos de 2019 que se obtuvieron de copia de seguridad
Lead_2019 <- Lead_001 %>% 
    select(Fuente.de.Posible.cliente, Estado.de.Posible.cliente, Desarrollo, Hora.de.creación) %>%
    mutate(Archivo = 'Enero_Leads_001.csv (Copia de seguridad)',
           Hora.de.creación = ymd(as.Date(Lead_001$Hora.de.creación, format = "%Y-%m-%d")))
  
Lead_2019 <- Lead_2019 %>%
    mutate(ym = ymd(paste0(year(Lead_2019$Hora.de.creación),"-",month(Lead_2019$Hora.de.creación) ,"-01")))
    
Lead_2019 <- filter(Lead_2019,Lead_2019$ym < '2020-01-01')
  
#write.csv(Lead_2019, "Documentos/3_Adsocial/GWEP/Data/Reporte/Lead_2019.csv", row.names = FALSE)
Lead_2019 <- read.csv('Documentos/3_Adsocial/GWEP/Data/Reporte/Lead_2019.csv', stringsAsFactors = FALSE)
Lead_2019$Hora.de.creación  <- as.Date(Lead_2019$Hora.de.creación, format = "%Y-%m-%d")
Lead_2019$ym  <- as.Date(Lead_2019$ym, format = "%Y-%m-%d")
  
#Mes actual
Enero <- read.csv('Documentos/3_Adsocial/GWEP/Data/Reporte/TEST_AdSocial_Enero.csv', stringsAsFactors = FALSE, skip = 1)
  
Enero_2020 <- Enero %>% 
    select(Fuente.de.Posible.cliente, Estado.de.Posible.cliente, Desarrollo, Hora.de.creación) %>%
    mutate(Archivo = 'TEST_Adsocial_Enero.csv',
           Hora.de.creación = ymd(as.Date(Enero$Hora.de.creación, format = "%d/%m/%Y")))
  
Enero_2020 <- Enero_2020 %>%
    mutate(ym = ymd(paste0(year(Enero_2020$Hora.de.creación),"-",month(Enero_2020$Hora.de.creación) ,"-01")))
  
Enero_2020 <- filter(Enero_2020, Enero_2020$ym == '2020-01-01')
  
Enero_2020$Hora.de.creación  <- as.Date(Enero_2020$Hora.de.creación, format = "%Y-%m-%d")
Enero_2020$ym  <- as.Date(Enero_2020$ym, format = "%Y-%m-%d")
  
str(Enero_2020)
str(Lead_2019)

#Union historico con mes actual
Leads_Final <- rbind(Lead_2019, Enero_2020)
#write.csv(Leads_Final,"Documentos/3_Adsocial/GWEP/Data/Reporte/Leads_Final.csv", row.names = FALSE)

################################################################################
#Hubo varias limpiezas de los archivos 2019 y enero 2020
#Cuidando las columnas importantes Estado.cliente, Fuente.cliente y las fechas
#implementar mejores prácticas para la limpieza
################################################################################
#Hubo varias limpiezas de los archivos 2019 y enero 2020
Leads_Final <- read.csv('/home/carlos/Documentos/3_Adsocial/GWEP/Data/Reporte/Leads_Final.csv', stringsAsFactors = FALSE)

Leads_Final$Hora.de.creación <-as.Date(Leads_Final$Hora.de.creación, format = "%Y-%m-%d")
Leads_Final$Hora.de.creación <- ymd(Leads_Final$Hora.de.creación)
Leads_Final['ym'] <- ymd(paste0(year(Leads_Final$Hora.de.creación),"-",month(Leads_Final$Hora.de.creación) ,"-01"))

head(select(Leads_Final, ym, Hora.de.creación, Desarrollo, Fuente.de.Posible.cliente, Estado.de.Posible.cliente, Archivo))

#Funciones que ayudan al formato de los números
specify_decimal <- function(x, k) as.numeric(trimws(format(round(x, k), nsmall=k)))
format_number <- function(x,k) formatC(as.numeric(x),format="f",digit=0,big.mark = ",")

Desarrollo_interes <- c(Leads_Final %>% group_by(Desarrollo) %>% 
                          summarise(Conteo = n()) %>%
                          filter(Conteo > 20 & !Desarrollo %in% c("Parque Satélite","Vidarte","La Purísima")))[1]

Leads_Final$Estado.de.Posible.cliente <- str_replace_all(Leads_Final$Estado.de.Posible.cliente,
                                                         c("Contactado"="Contactado",
                                                           "Contactar en el futuro"="Contactar",
                                                           "Visita agendada"="Agendada",
                                                           "Intento de contacto"="Intento",
                                                           "Intento x20 de x20 contacto"="Intento",
                                                           "Contactar x20 en x20 el x20 futuro"="Contactar",
                                                           "Visita x20 agendada"="Agendada"))

Leads_Final$Fuente.de.Posible.cliente <- str_replace_all(Leads_Final$Fuente.de.Posible.cliente, c("Facebook Ads"="Facebook",
                                                                                                  "Facebook orgánico"="Facebook",
                                                                                                  "Inbox Facebook"="Facebook",
                                                                                                  "Google Adwords"="Google",
                                                                                                  "Google orgánico"="Google"))

#Función que realiza las 4 gráficas de Zoho
Zoho <- function(desarrollo){
  #Colocamos el desarrollo de interés a gráficar
  desarrollo <- as.character(desarrollo)
  
  Desarrollo_interes <- c(Leads_Final %>% group_by(Desarrollo) %>% 
                            summarise(Conteo = n()) %>%
                            filter(Conteo > 20 & !Desarrollo %in% c("Parque Satélite","Vidarte","La Purísima")))[1]
  
  Leads_Final <- Leads_Final %>%
    filter(Desarrollo %in% Desarrollo_interes$Desarrollo & ym > '2018-12-01')
  
  Conteo <- Leads_Final %>%
    group_by(ym,Desarrollo) %>%
    summarise(Conteo = n()) %>%
    filter(!is.na(ym) & Desarrollo == desarrollo)
  
  ###############
  #Todo_Registro#
  ###############
  
  Todo_Registro <- ggplot(Conteo, aes(x = ym, y = Conteo)) + geom_point(color = "#00AFBB") +
    geom_line(color = "#00AFBB") +
    theme(axis.text.x = element_text(angle = 90)) +
    geom_text(aes(label = Conteo), position = position_stack(vjust = 1.1), size = 4) + 
    ggtitle(paste0("Zoho, ",unique(Conteo$Desarrollo)), 
            subtitle = paste0(format_number(sum(Conteo$Conteo))," Son todos los registros, no todos los Leads aquí son buenos")) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
  #################
  #Fuentes_interes#
  #################
  Fuente_clientes <- c("Facebook","Google","Instagram","Langind page","Página web")
  
  Conteo <- Leads_Final %>%
    group_by(Hora.de.creación, Desarrollo , Fuente.de.Posible.cliente, Estado.de.Posible.cliente) %>%
    summarise(Conteo = n()) %>%
    filter(Fuente.de.Posible.cliente %in% Fuente_clientes & Desarrollo == desarrollo ) 
  
  Porcentajes <- data.frame(Conteo) %>%
    mutate(Porcentaje = Conteo/sum(Conteo)) %>%
    group_by(Fuente.de.Posible.cliente) %>%
    summarise(a = specify_decimal(sum(Porcentaje),2))
  
  Porcentajes$b <- sprintf("%.f%%", 100*Porcentajes$a)
  A <- c()
  for(i in 1:dim(Porcentajes)[1]){ A[i] <- paste0( Porcentajes$Fuente.de.Posible.cliente[i], " ", Porcentajes$b[i] ) }
  subtitle <- str_replace_all(paste0(A[1] ," ", A[2] ," " , A[3] ," ", A[4]," ", A[5]," ", A[6]),"NA","")
  
  Fuentes_interes <- ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Fuente.de.Posible.cliente)) +
    geom_col(position = "stack") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle(paste0(format_number(sum(Conteo$Conteo)), " registros de plataformas digitales"),
            subtitle = subtitle) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
  #####################
  #Interese_Desarrollo#
  #####################
  Tipo_Lead <- c("Contactado","Contactar","Agendada","Intento")
  
  Conteo <- filter(Conteo, Estado.de.Posible.cliente %in% Tipo_Lead)
  
  Porcentajes <- data.frame(Conteo %>% group_by(Estado.de.Posible.cliente,Desarrollo) %>%
                              summarise(Suma = sum(Conteo))) %>%
                              mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  
  Porcentajes$b <- sprintf("%.f%%", 100*Porcentajes$Porcentaje) ; Porcentajes
  
  for(i in 1:dim(Porcentajes)[1]){ A[i] <- paste0(Porcentajes$Estado.de.Posible.cliente[i], " ", Porcentajes$Suma[i], " (",Porcentajes$b[i] , ")") }
  subtitle <- str_replace_all(paste0(A[1] ," ", A[2] ," " , A[3] ," ", A[4]," ", A[5]," ", A[6]),"NA","")
  
  Interes_Desarrollo <- ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Estado.de.Posible.cliente)) +
    geom_col(position = "stack") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle(paste0(format_number(sum(Conteo$Conteo))," Leads de Interés "),
            subtitle = subtitle) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
  ####################
  #Interes_Plataforma# 
  ####################
  Leads_Zoho <- Conteo %>% 
                    group_by(Desarrollo,Hora.de.creación,Fuente.de.Posible.cliente) %>%
                    summarize(Leads = sum(Conteo))
  Leads_Zoho$Mes <- month(Leads_Zoho$Hora.de.creación, label = TRUE)
  Leads_Zoho$Año <- year(Leads_Zoho$Hora.de.creación)
  Leads_Zoho <- Leads_Zoho %>% group_by(Año,Mes,Fuente.de.Posible.cliente) %>% summarize(Leads = sum(Leads))
  names(Leads_Zoho) <- c("Año", "Mes", "Plataforma", "Leads Interés")
  
  Porcentajes <- data.frame(Conteo %>%
                              group_by(Fuente.de.Posible.cliente, Desarrollo) %>% 
                              summarise(Suma = sum(Conteo))) %>% 
    mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  
  Porcentajes$b <- sprintf("%.f%%", 100*Porcentajes$Porcentaje) ; Porcentajes
  
  for(i in 1:dim(Porcentajes)[1]){ A[i] <- paste0(Porcentajes$Fuente.de.Posible.cliente[i], " ", Porcentajes$Suma[i], " (",Porcentajes$b[i] , ")") }
  subtitle <- str_replace_all(paste0(A[1] ," ", A[2] ," " , A[3] ," ", A[4]," ", A[5]," ", A[6]),"NA","")
  
  Interes_Plataforma <- ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Fuente.de.Posible.cliente)) +
    geom_col(position = "stack") +
    theme(axis.text.x = element_text(angle = 90)) +
    ggtitle("Lead de Interés por Plataforma",
            subtitle = subtitle) +
    labs(fill = "") +
    ggthemes::theme_economist() +
    xlab("") +
    ylab("")
  
  #options(repr.plot.width = 20, repr.plot.height = 10)
  
  Salida <- list(grid.arrange(Todo_Registro, Fuentes_interes ,
                      Interes_Desarrollo, Interes_Plataforma,
                      nrow = 2, ncol = 2, as.table = TRUE), Leads_Zoho)
  
  return(Salida)
}

#############################
#Información de las campañas#
#############################
Plataformas <- read.csv("~/Documentos/3_Adsocial/GWEP/Campañas/campañas.csv")
  
Plataformas_graficas <- function(desarrollo){
  
  desarrollo <- desarrollo
    
  #Union_Facebook 
  #Archivo plataforma
  #Nombre de la campaña,	Inicio_del_reporte,	Finalización_reporte,	Importe gastado (MXN), Impresiones,	Clics en el enlace, Indicador de resultado,
  #Costo por resultados, CPC (costo por clic en el enlace), (MXN) Clientes potenciales en Facebook
  #Nuevos nombres
  #Campaña,	Fecha_Inicio,	Fecha_Fin,	Costo, Impresiones,	Clics, Costo_conversion, CPC_promedio, Conversiones
    
  #De googgle tomó
  #Campaña,	Fecha_Inicio_reporte,	Fecha_Fin_reporte,	Costo, Impresiones,	Clics, Costo_conversion, CPC_promedio, Conversiones
  #En ocasiones el formato de fecha cambia d/m/y ó d-m-y
    
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
    
  Numero_Campañas <- ggplot(Conteo, aes(x = ym, y = Conteo, fill = Plataforma)) +
      geom_col(alpha = 0.8) +
      geom_text(aes(label = Conteo), position = position_stack(vjust = 0.5), size = 5) +
      theme(axis.text.x = element_text(angle = 90)) +
      ggtitle(paste0("Número de Campañas ", desarrollo, " 2019")) +
      labs(fill = "") +
      ggthemes::theme_economist() +
      xlab("") +
      ylab("")
    
  #Resultados de Campañas por Mes, Desarrollo
  #¿Que Plataforma da mejores Resultados?
  tmp <- Plataformas %>% select(Desarrollo, Plataforma, ym, Impresiones, Clics, Conversiones, Costo)
  tmp_0 <- gather(tmp, "metrica","valor",-ym,-Plataforma, -Desarrollo) %>% 
      filter(valor != 0)
    
  table(tmp_0$metrica)
    
  tmp_0 <- tmp_0 %>% group_by(Desarrollo, Plataforma,ym, metrica) %>% 
      summarise(suma = round(sum(valor, na.rm = TRUE))) %>% filter(Desarrollo == desarrollo)
    
  tmp_p <- filter(tmp_0, metrica == "Clics") %>% group_by(Plataforma) %>% summarize(Suma = sum(suma)) %>% mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  tmp_p$Porcentaje <- sprintf("%.f%%", 100*tmp_p$Porcentaje) ; tmp_p
    
  tmp_p$Suma <- paste0(formatC(as.numeric(tmp_p$Suma), format="f", digits=0, big.mark=","))
    
  Clics <- ggplot(filter(tmp_0, metrica == "Clics"), aes(x = ym, y = suma, fill = Plataforma)) +
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
  
  #Conversiones
  tmp_p <- filter(tmp_0, metrica == "Conversiones") %>% group_by(Plataforma) %>% summarize(Suma = sum(suma)) %>% mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  tmp_p$Porcentaje <- sprintf("%.f%%", 100*tmp_p$Porcentaje) ; tmp_p
    
  Conversiones <- ggplot(filter(tmp_0, metrica == "Conversiones"), aes(x = ym, y = round(suma), fill = Plataforma)) +
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
  
  #Dinero gastado
  tmp_p <- filter(tmp_0, metrica == "Costo") %>% group_by(Plataforma) %>% summarize(Suma = sum(suma)) %>% mutate(Porcentaje = specify_decimal(Suma/sum(Suma),2))
  tmp_p$Porcentaje <- sprintf("%.f%%", 100*tmp_p$Porcentaje) ; tmp_p
  tmp_p$Suma <- paste0("$",formatC(as.numeric(tmp_p$Suma), format="f", digits=0, big.mark=",")) ; tmp_p
    
  Dinero_gastado <- ggplot(filter(tmp_0, metrica == "Costo"), aes(x = ym, y = suma, fill = Plataforma)) +
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
    
  #Tabla Resumen de Campañas
  Resumen_Campañas <- Plataformas %>% group_by(ym, Plataforma) %>%
                                      filter(Desarrollo == desarrollo) %>%
                                      summarize(Clics = sum(Clics,na.rm = TRUE),
                                                Conversiones = sum(Conversiones,na.rm = TRUE),
                                                Inversión = sum(Costo,na.rm = TRUE))
  
  names(Resumen_Campañas) <- c("Fecha","Plataforma","Clics","Conversión","Inversión")
  Resumen_Campañas$Inversión <-  paste0("$",formatC(as.numeric(Resumen_Campañas$Inversión), format="f", digits=0, big.mark=","))
  Resumen_Campañas$Clics <- paste0(formatC(as.numeric(Resumen_Campañas$Clics), format="f", digits=0, big.mark=","))
  Resumen_Campañas['Mes'] <- month(Resumen_Campañas$Fecha, label = TRUE)
  Resumen_Campañas['Año'] <- year(Resumen_Campañas$Fecha)
  
  Resumen_Campañas <- data.frame(Resumen_Campañas) %>% select(Año, Mes, Plataforma, Clics, Conversión, Inversión)
  
  Salida <- list(grid.arrange(Clics, Dinero_gastado , Conversiones, nrow = 2, ncol = 2, as.table = TRUE), Resumen_Campañas)
  
  return(Salida)
  
  }

#Ruta donde dejamos los nuevos archivos
setwd("/home/carlos/Documentos/3_Adsocial/GWEP/Graficas/Por_Desarrollo_Enero/")
  
#Tablas resumen integrarlas a las funciones.
write.csv(data.frame(Zoho("Aurum")[2]),paste0("", "Aurum", "_LeadInterés.csv"), row.names = FALSE)
write.csv(data.frame(Plataformas_graficas("Aurum")[2]),paste0("", "Aurum", "_Plataformas.csv"), row.names = FALSE)

write.csv(data.frame(Zoho("Cumbres Herradura")[2]),paste0("", "Cumbres Herradura", "_LeadInterés.csv"), row.names = FALSE)
write.csv(data.frame(Plataformas_graficas("Cumbres Herradura")[2]),paste0("", "Cumbres Herradura", "_Plataformas.csv"), row.names = FALSE)

write.csv(data.frame(Zoho("El Cortijo")[2]),paste0("", "El Cortijo", "_LeadInterés.csv"), row.names = FALSE)
write.csv(data.frame(Plataformas_graficas("El Cortijo")[2]),paste0("", "El Cortijo", "_Plataformas.csv"), row.names = FALSE)

write.csv(data.frame(Zoho("Parque Hacienda")[2]),paste0("", "Parque Hacienda", "_LeadInterés.csv"), row.names = FALSE)
write.csv(data.frame(Plataformas_graficas("Parque Hacienda")[2]),paste0("", "Parque Hacienda", "_Plataformas.csv"), row.names = FALSE)

write.csv(data.frame(Zoho("Real de Lutecia")[2]),paste0("", "Real de Lutecia", "_LeadInterés.csv"), row.names = FALSE)
write.csv(data.frame(Plataformas_graficas("Real de Lutecia")[2]),paste0("", "Real de Lutecia", "_Plataformas.csv"), row.names = FALSE)

write.csv(data.frame(Zoho("Reserva del sur")[2]),paste0("", "Reserva del sur", "_LeadInterés.csv"), row.names = FALSE)
write.csv(data.frame(Plataformas_graficas("Reserva del sur")[2]),paste0("", "Reserva del sur", "_Plataformas.csv"), row.names = FALSE)

