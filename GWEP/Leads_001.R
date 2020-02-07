options(scipen=999)

library(tidyr)
library(dplyr)
library(ggplot2)
library(lubridate)
library(stringr)

#Actualizar el historico
Lead_001 <- read.csv('Documentos/Adsocial/GWEP/Data/Enero_Leads_001.csv', stringsAsFactors = FALSE, )

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

tmp <- c(Lead %>% group_by(Desarrollo) %>% 
           summarise(Conteo = n()) %>%
           filter(Conteo > 20 & !Desarrollo %in% c("Parque Satélite","Vidarte","La Purísima")))[1]

Lead <- Lead %>% filter(Desarrollo %in% tmp$Desarrollo & ym > '2018-12-01')
table(Lead$ym)

#Historico por Mes Desarrollo
Conteo <- Lead %>% group_by(ym,Desarrollo) %>% summarise(Conteo = n()) %>% filter(!is.na(ym))

head(Conteo)
sum(Conteo$Conteo)

ggplot(Conteo, aes(x = ym, y = Conteo)) + geom_point(color = "#00AFBB") +
  geom_line(color = "#00AFBB") +
  theme(axis.text.x = element_text(angle = 90)) +
  geom_text(aes(label = Conteo), position = position_stack(vjust = 1.4), size = 3) +
  facet_wrap(~ Desarrollo) + 
  ggtitle("Conteo de Todos Leads por Desarrollo", 
          subtitle = paste0("Tenemos ",sum(Conteo$Conteo)," Leads desde Enero-2019 (No todos son buenos)")) +
  xlab("Hora de Creación") +
  ylab("Todos los Leads")

#Fuente de Leads por Desarrollo y mes
Fuente_clientes <- c("Facebook Ads","Facebook orgánico","Google Adwords","Google orgánico","Instagram","Langind page","Página web")

Conteo <- Lead %>%
  group_by(Hora.de.creación, Desarrollo , Fuente.de.Posible.cliente, Estado.de.Posible.cliente) %>%
  summarise(Conteo = n()) %>%
  filter(Fuente.de.Posible.cliente %in% Fuente_clientes & Desarrollo != "La Purísima")

ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, fill = Fuente.de.Posible.cliente)) +
  geom_col(position = "stack") +
  labs(colour = "Fuente Posible Cliente") +
  facet_wrap(~ Desarrollo) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle("2019 Fuente Posibles Clientes todos los Leads", subtitle = paste0(sum(Conteo$Conteo),"  de Plataformas digitales"))

#Lead de Interes por Desarrollo
Tipo_Lead <- c("Contactado","Contactar en el futuro","Visita agendada","Intento de contacto")

Conteo <- filter(Conteo, Estado.de.Posible.cliente %in% Tipo_Lead)

ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, color = Estado.de.Posible.cliente)) +
  geom_point() +
  labs(colour = "Leads de Interés") +
  facet_wrap(~ Desarrollo) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle("2019 Leads buenos 934",
          subtitle = paste0("Contactado : ",table(Conteo$Estado.de.Posible.cliente)[1],
                            ", Contactar en el futuro : ",table(Conteo$Estado.de.Posible.cliente)[2],
                            ", Intento de contacto : ",table(Conteo$Estado.de.Posible.cliente)[3],
                            ", Visita agendada :",table(Conteo$Estado.de.Posible.cliente)[4]))

table(Conteo$Estado.de.Posible.cliente)

#Leads de Interes Plataformas
ggplot(Conteo, aes(x = Hora.de.creación, y = Conteo, color = Fuente.de.Posible.cliente)) +
  geom_point() +
  labs(colour = "Fuente Leads buenos") +
  facet_wrap(~ Desarrollo) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle("2019 Fuente Leads de Interés 934",
          subtitle = paste0("Facebook : ",539,
                            ", Google : ",190,
                            ", Página web : ",166,
                            ", Instagram : ",39))

table(Conteo$Fuente.de.Posible.cliente)

#¿Que plataformas registra el CRM las campañas arrojan mayor número de conversiones en Facebook?

#############################
#Información de las campañas#
#############################
Plataformas <- read.csv("~/Documentos/Adsocial/GWEP/Campañas/campañas.csv")

tmp_Fb <- Plataformas %>% filter(Plataforma == "Faceboock")
tmp_Go <- Plataformas %>% filter(Plataforma == "Google")

tmp_Fb$Fecha_Inicio <- as.Date(tmp_Fb$Fecha_Inicio, format = "%Y-%m-%d")
tmp_Fb$Fecha_Inicio <- ymd(tmp_Fb$Fecha_Inicio)
tmp_Fb['ym'] <- ymd(paste0(year(tmp_Fb$Fecha_Inicio),"-",month(tmp_Fb$Fecha_Inicio) ,"-01"))

tmp_Go$Fecha_Inicio <- as.Date(tmp_Go$Fecha_Inicio, format = "%d/%m/%Y")
tmp_Go$Fecha_Inicio <- ymd(tmp_Go$Fecha_Inicio)
tmp_Go['ym'] <- ymd(paste0(year(tmp_Go$Fecha_Inicio),"-",month(tmp_Go$Fecha_Inicio) ,"-01"))

Plataformas <- rbind(tmp_Fb,tmp_Go) ; rm(tmp_Fb,tmp_Go)

Plataformas <- filter(Plataformas, ym > "2018-12-01" & Desarrollo %in% c("Aurum","Cumbre Herradura","El Cortijo","Parque Hacienda","Real de Lutecia","Reserva del Sur"))

#Por Mes numero de Campañas
ggplot(Plataformas, aes(x = ym, fill = Plataforma)) +
  geom_bar(position = "stack") +
  ggtitle("2019 Numero de Campañas por Mes", subtitle = "")

#Campañas por Mes, Desarrollo y plataforma
Conteo <- Plataformas %>% group_by(ym, Plataforma, Desarrollo) %>% summarise(Conteo = n())
head(Conteo, 2)

ggplot(Conteo, aes(x = ym, y = Conteo, fill = Plataforma)) +
  geom_col() +
  geom_text(aes(label = Conteo), position = position_stack(vjust = 0.5), size = 3) +
  labs(colour = "Leads de Interés") +
  facet_wrap(~ Desarrollo) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle("2019 número de Campañas Plataformas Digitales", subtitle = "Los Desarrollo con mayor número de Campañas : Real de Lutecia, Reserva del Sur")

#Resultados de Campañas por Mes, Desarrollo
#¿Que Plataforma da mejores Resultados?
tmp <- Plataformas %>% select(Desarrollo, Plataforma, ym, Impresiones, Clics, Conversiones, Costo)
tmp_0 <- gather(tmp, "metrica","valor",-ym,-Plataforma, -Desarrollo)

table(tmp_0$metrica)

tmp_0 <- tmp_0 %>% group_by(Desarrollo, Plataforma,ym, metrica) %>% 
            summarise(suma = sum(valor, na.rm = TRUE))

head(tmp_0)

ggplot(filter(tmp_0, metrica == "Conversiones"), aes(x = ym, y = suma, fill = Plataforma)) +
  geom_col() +
  geom_text(aes(label = suma), position = position_stack(vjust = 0.5), size = 3) +
  labs(colour = "metrica") +
  facet_wrap(~ Desarrollo) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle("2019 Conversiones Plataformas Digitales", subtitle = "Faceboock da el mayor número de Conversiones, ¿Cuál es el costo?")

ggplot(filter(tmp_0, metrica == "Costo"), aes(x = ym, y = suma, fill = Plataforma)) +
  geom_col() +
  geom_text(aes(label = paste0("$",formatC(as.numeric(suma), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  labs(colour = "metrica") +
  facet_wrap(~ Desarrollo) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle("2019 Inversión Plataformas Digitales", subtitle = "")

filter(tmp_0, metrica == "Costo") %>%
  group_by(Desarrollo, Plataforma) %>%
  summarise(Suma_T = sum(suma)) %>%
  mutate(Porcentaje = Suma_T /sum(Suma_T))

#
#CPC Y CPL
#poner tablitas




