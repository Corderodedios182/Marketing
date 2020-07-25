library(gridExtra) ; library(tidyr) ; library(dplyr) ; library(ggplot2) ; library(lubridate) ; library(stringr) ;library(cowplot) ; library(ggthemes)

###########################################################################
#Objectivo: ¿Como incrementar el número de leads?                         #
# - Una gráfica de leads vs auidiencia (concatenando dia_sexo_region_edad)#
###########################################################################
setwd("/home/carlos/Documentos/3_Adsocial/Marketing/GWEP/Modelos_parque_hacienda/bases/")
getwd()
list.files()

########################
#Fuentes de información#
########################

fechas_facebook <- function(base){
  
  base$Inicio.del.informe <- as.Date(base$Inicio.del.informe, format = "%Y-%m-%d")
  base$Inicio.del.informe <- ymd(base$Inicio.del.informe)
  base['año'] <- year(base$Inicio.del.informe)
  base['mes'] <- month(base$Inicio.del.informe)
  base['dia'] <- day(base$Inicio.del.informe)
  
  base <- base %>% select(-c(Fin.del.informe,Inicio,Finalización,Indicador.de.resultado, Registros.completados, Registros.completados.en.el.sitio.web, Clientes.potenciales.en.el.sitio.web))
  
  return(base)
  
}

  #hora
f_hora <- read.csv("facebook/Parque-Hacienda-Campañas-1-may-2020-31-may-2020_hora.csv", stringsAsFactors = FALSE)
f_hora['llave_facebook'] = paste0(f_hora$Nombre.de.la.campaña,"-", f_hora$Inicio.del.informe)
f_hora["hora"] = as.integer(str_split_fixed(f_hora$Hora.del.día..zona.horaria.de.la.cuenta.publicitaria., pattern = ":",2)[,1])
f_hora["dia_hora"] <- ymd_h(paste0(f_hora$Inicio.del.informe, "-",f_hora$hora))
f_hora <- f_hora %>% select(Inicio.del.informe,hora, Importe.gastado..MXN., Impresiones, Clics.en.el.enlace, Resultados,
                            Costo.por.resultados, CPC..costo.por.clic.en.el.enlace...MXN.,Clientes.potenciales)
names(f_hora) <- c("inicio_informe","hora","dinero_gastado","impresiones","clics","resultados",
                     "costo_x_resultado","cpc","clientes_potenciales")
f_hora[, 3:9][is.na(f_hora[, 3:9])] <- 0

f_hora['ctr'] = (f_hora$clics / f_hora$impresiones) * 100

ggplot(data = f_hora, aes(x = hora, y = clientes_potenciales, group = 1)) +
  geom_line(color = "red") +
  facet_wrap(facets = vars(inicio_informe)) +
  labs(x = "hora", y = "impresiones", 
       title = "Clientes potenciales por hora")

ggplot(data = f_hora, aes(x = hora, y = ctr, group = 1)) +
  geom_line(color = "green") +
  geom_hline(aes(yintercept=2), color="blue",linetype="dashed") + 
  facet_wrap(facets = vars(inicio_informe)) +
  labs(x = "hora", y = "impresiones", 
       title = "Mes de mayo ctr por hora")

ggplot(data = f_hora, aes(x = hora, y = cpc, group = 1)) +
  geom_line(color = "blue") +
  geom_hline(aes(yintercept=2), color="red",linetype="dashed") + 
  facet_wrap(facets = vars(inicio_informe)) +
  labs(x = "hora", y = "impresiones", 
       title = "Mes de mayo cpc por hora")

  #region
f_region <- read.csv("facebook/Parque-Hacienda-Campañas-1-may-2020-31-may-2020_region.csv")
f_region['llave_facebook'] = paste0(f_region$Nombre.de.la.campaña,"-", f_region$Inicio.del.informe)
f_region <- f_region %>% select(llave_facebook, Inicio.del.informe, Región, Importe.gastado..MXN., Alcance, Frecuencia, Impresiones, Clics.en.el.enlace, Resultados,
                                Costo.por.resultados,Costo.por.mil.personas.alcanzadas..MXN., CPC..costo.por.clic.en.el.enlace...MXN., Clientes.potenciales,Clientes.potenciales.en.Facebook)

names(f_region) <- c("llave_facebook","fecha","nivel","dinero_gastado","alcance","frecuencia","impresiones","clics","resultados","costo_x_resultado","costo_xmil_personas","cpc","clientes_potenciales","clientes_potenciales_fb")
f_region[, 4:14][is.na(f_region[, 4:14])] <- 0
  
  #sexo
f_sexo <- read.csv("facebook/Parque-Hacienda-Campañas-1-may-2020-31-may-2020_sexoYedad.csv")
f_sexo['llave_facebook'] = paste0(f_sexo$Nombre.de.la.campaña,"-", f_sexo$Inicio.del.informe)
f_sexo['nivel'] = paste0(f_sexo$Edad,"-", f_sexo$Sexo)
f_sexo <- f_sexo %>% select(llave_facebook, Inicio.del.informe, nivel, Importe.gastado..MXN.,Alcance, Frecuencia, Impresiones, Clics.en.el.enlace, Resultados, Costo.por.resultados,
                            Costo.por.mil.personas.alcanzadas..MXN., CPC..costo.por.clic.en.el.enlace...MXN., Clientes.potenciales,Clientes.potenciales.en.Facebook)
names(f_sexo) <- c("llave_facebook","fecha","nivel","dinero_gastado","alcance","frecuencia","impresiones","clics","resultados","costo_x_resultado","costo_xmil_personas","cpc","clientes_potenciales","clientes_potenciales_fb")
f_sexo[, 4:14][is.na(f_sexo[, 4:14])] <- 0

  #ubicacion
f_ubicacion <- read.csv("facebook/Parque-Hacienda-Campañas-1-may-2020-31-may-2020_ubicacionYdispositivo.csv")
f_ubicacion['llave_facebook'] = paste0(f_ubicacion$Nombre.de.la.campaña,"-", f_ubicacion$Inicio.del.informe)
f_ubicacion['nivel'] = paste0(f_ubicacion$Plataforma,"-", f_ubicacion$Ubicación,"-", f_ubicacion$Plataforma.de.dispositivos,"-", f_ubicacion$Dispositivo.de.la.impresión)
f_ubicacion <- f_ubicacion %>% select(llave_facebook, Inicio.del.informe, nivel, Importe.gastado..MXN.,Alcance, Frecuencia, Impresiones, Clics.en.el.enlace, Resultados, Costo.por.resultados,
                            Costo.por.mil.personas.alcanzadas..MXN., CPC..costo.por.clic.en.el.enlace...MXN., Clientes.potenciales,Clientes.potenciales.en.Facebook)
names(f_ubicacion) <- c("llave_facebook","fecha","nivel","dinero_gastado","alcance","frecuencia","impresiones","clics","resultados","costo_x_resultado","costo_xmil_personas","cpc","clientes_potenciales","clientes_potenciales_fb")
f_ubicacion[, 4:14][is.na(f_ubicacion[, 4:14])] <- 0

#base para ver cifras por reporte
data.frame(cbind( hora = lapply(f_hora[7:17], sum),
                  region = lapply(f_region[7:17], sum),
                  sexo = lapply(f_sexo[8:18], sum),
                  ubicacion = lapply(f_ubicacion[10:20], sum)))

names(f_sexo)

tmp_s = f_sexo %>% filter(`fecha` == '2020-05-31')
tmp_r = f_region %>% filter(`fecha` == '2020-05-31')
tmp_u = f_ubicacion %>% filter(`fecha` == '2020-05-31')

tmp = rbind(tmp_s, tmp_r, tmp_u)
tmp_a = tmp %>% filter(clientes_potenciales > 0)
tmp_a = tmp_a %>% select(llave_facebook, fecha, nivel, clientes_potenciales)



sum(tmp_a$dinero_gastado)/3

tmp = rbind(f_sexo, f_region, f_ubicacion)
tmp_a = tmp %>% filter(clientes_potenciales > 0)

tmp_cruze = left_join(tmp_r, tmp_s, by = c("llave_facebook_region","llave_facebook_sexo"))

utils::View(tmp_s)
utils::View(tmp_r)
utils::View(tmp_u)

data.frame(cbind(region = lapply(tmp_r[7:17], sum),
                  sexo = lapply(tmp_s[8:18], sum),
                  ubicacion = lapply(tmp_u[10:20], sum)))



tmp = f_sexo %>% group_by(dia, Edad, Sexo) %>% summarise(Conteo = n())

#Union de los archivos de facebook

  #Reportes de Adwords

#Aquí debemos hacer la limpieza de adwords y unir los archivos.

  #Reportes de Zoho (trabajando con los datos de leads, un reporte personalizado para parque hacienda)
leads <- read.csv("zoho_parque_hacienda_v1/union_leads.csv", stringsAsFactors = FALSE)
leads$Email <- as.character(leads$Email)
#Formato de datos
leads <- leads %>% select(Created.Time, Email, Lead.Status, Lead.Source, 
                          Subject..Activity., Subject, Ad.Campaign.Name, 
                          Campaña.MKT, Keyword, Ad.Click.Date, First.Page.Visited,
                          Cost.per.Click, Cost.per.Conversion) %>% 
                    group_by(Created.Time, Email) %>%
                    summarise(Conteo = n()) %>%
                    separate(Created.Time,c("dia_creacion","Hora","AM/PM"),sep = " ") %>%
                    mutate(dia_creacion = ymd(as.Date(dia_creacion, format = "%d/%m/%Y")))

leads$dia_creacion <- as.Date(leads$dia_creacion,
                              format = "%Y-%m-%d")

names(leads) <- c("dia_creacion","hora","am_pm","email","conteo")
leads$hora <- as.integer(str_split_fixed(leads$hora, pattern = ":",2)[,1])
leads$hora <- paste0(leads$hora,"-",leads$am_pm)

tmp_am <- leads %>% filter(am_pm == "AM") 
tmp_pm <- leads %>% filter(am_pm == "PM") 
tmp_am["hora"] <- str_replace_all(tmp_am$hora, c("1-AM"="1","2-AM"="2","3-AM"="3","4-AM"="4","5-AM"="5","6-AM"="6","7-AM"="7","8-AM"="8","9-AM"="9","10-AM"="10","11-AM"="11","12-AM"="12"))
tmp_pm["hora"] <- str_replace_all(tmp_pm$hora,c("3-PM"="15","4-PM"="16","5-PM"="17","6-PM"="18","7-PM"="19","8-PM"="20","9-PM"="21","10-PM"="22","11-PM"="23","12-PM"="24"))
tmp_pm["hora"] <- str_replace_all(tmp_pm$hora,c("1-PM"="13","2-PM"="14"))

leads <- rbind(tmp_am, tmp_pm) %>% select(-am_pm) ; rm(tmp_am, tmp_pm)
leads["hora_creacion"] <- ymd_h(paste0(leads$dia_creacion,"-",leads$hora))

leads <- leads %>% filter(dia_creacion < '2020-06-01')
leads$hora <- as.integer(leads$hora)
leads$conteo <- as.integer(leads$conteo)
leads <- leads[order(leads$dia_creacion,leads$hora),]
leads <- leads %>% group_by(dia_creacion,hora) %>% summarise(conteo = n())
leads <- data.frame(leads)

str(leads)
head(leads)

ggplot(data = tmp, aes(x = hora, y = conteo, group = 1)) +
  geom_line(color = "red") +
  facet_wrap(facets = vars(dia_creacion)) +
  labs(x = "hora", y = "impresiones", 
       title = "Clientes potenciales por hora")


head(leads,3)



ggplot(data = leads, aes(x = Hora, y = , group = 1)) +
  geom_line(color = "green") +
  geom_hline(aes(yintercept=2), color="blue",linetype="dashed") + 
  facet_wrap(facets = vars(inicio_informe)) +
  labs(x = "hora", y = "impresiones", 
       title = "Mes de mayo ctr por hora")



#Conteo de unicos




######################################
#Cruzes para tener una base homogenea#
######################################

############################
#Analisis de la información#
############################

  #En que días, horas tengo un mayor flujo de leads (todos e interes)

  #¿Como es la interacción con las plataformas y zoho? (variables que se relacionan)

  #Analisis descriptivo de las audiencias, seteo de campañas, numero de campañas, inversiones, resultados, seteos, audiencias.

##############################
#Modelo propuesto y hallazgos#
##############################

  #-Preparación de los datos para el modelo

  #-Modelo

  #-Visualización

  #-Predicciones

  #-Uso

######################################################################################################
#¿Que podemos agregar y cuales serían otras fuentes o tablas importantes que enriquescan el analisis?#
######################################################################################################

#Otras tablas de zoho para el funnel de leads












