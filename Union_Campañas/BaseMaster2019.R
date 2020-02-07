#Se busca tener un resumen mensual de la información de la base de ROAS GG

options(scipen=999)

#Tablas comparativos
library(gridExtra)
library(tidyr)
library(dplyr)
library(ggplot2)
library(lubridate)
library(stringr)
library(cowplot)
library(ggthemes)

tmp <- read.csv("~/Documentos/Adsocial/Bases AdSocial/Históricos GG/Union_Basemaster.csv",stringsAsFactors = FALSE)

tmp$INICIO <-as.Date(tmp$INICIO, format = "%d/%m/%Y")
tmp$INICIO <- ymd(tmp$INICIO)

tmp$FIN <-as.Date(tmp$FIN, format = "%d/%m/%Y")
tmp$FIN <- ymd(tmp$FIN)

tmp$MP <- as.numeric(tmp$MP)
tmp$MP <- round(tmp$MP)

fn <- function(x){
  format(x, digits=9, decimal.mark=".",
         big.mark=",",small.mark=",", small.interval=3)  
}

#Son resumenes para conocer la cifras por Plataforma, Mes, Marca

Conteo <- data.frame(tmp %>% group_by(Plataforma, Mes, MARCA) %>%
                       summarize(inversión = fn(sum(MP)), revenue = fn(sum(REVENUE_CONVERSIONES_ADSERVER)),
                                 impresiones = fn(sum(IMPRESIONES)), clicks = fn(sum(CLICKS)), conversiones = fn(sum(CONVERSiONES))))
Conteo

Conteo <- data.frame(tmp %>% group_by(Plataforma, Mes, MARCA, Hoja) %>%
                       summarize(inversión = sum(MP), revenue = sum(REVENUE_CONVERSIONES_ADSERVER),
                                 impresiones = sum(IMPRESIONES), clicks = sum(CLICKS), conversiones = sum(CONVERSiONES)))

Conteo

Conteo <- data.frame(tmp %>% group_by(Hoja) %>%
                       summarize(inversión = fn(sum(MP)), revenue = fn(sum(REVENUE_CONVERSIONES_ADSERVER)),
                                 impresiones = fn(sum(IMPRESIONES)), clicks = fn(sum(CLICKS)), conversiones = sum(CONVERSiONES)))


Conteo

#Inversión
Conteo <- data.frame(tmp %>% group_by(Plataforma, Año_Mes, MARCA, Hoja) %>%
                       summarize(inversión = sum(MP), revenue = sum(REVENUE_CONVERSIONES_ADSERVER),
                                 impresiones = sum(IMPRESIONES), clicks = sum(CLICKS), conversiones = sum(CONVERSiONES)))

Conteo

#Graficas de todas las Plataformas
inversion_todos <- ggplot(Conteo, aes(x = Año_Mes, y = inversión, fill = Plataforma)) +
  geom_col(alpha = 0.8) +
  facet_wrap(~MARCA) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(inversión), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Inversión todas las marcas")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

inversion_todos

#Revenue
revenue_todos <- ggplot(Conteo, aes(x = Año_Mes, y = revenue, fill = Plataforma)) +
  geom_col(alpha = 0.8) +
  facet_wrap(~MARCA) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(revenue), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Revenue todas las marcas")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

revenue_todos

grid.arrange(inversion_todos, revenue_todos, nrow = 2, ncol = 1, as.table = TRUE)

#Graficas por marcas
tabla_marca_inversión <- ggplot(filter(Conteo,MARCA == 'RadioShack'), aes(x = Año_Mes, y = inversión, fill = Plataforma)) +
  geom_col(alpha = 0.8) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(inversión), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Inversión RadioShack")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

tabla_marca_revenue <- ggplot(filter(Conteo, MARCA == 'RadioShack'), aes(x = Año_Mes, y = revenue, fill = Plataforma)) +
  geom_col(alpha = 0.8) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(revenue), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Revenue RadioShack")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

grid.arrange(tabla_marca_inversión, tabla_marca_revenue, nrow = 2, ncol = 1, as.table = TRUE)

#Pruebas
#ppf(), ppfm(), mkt(), 
#totales, analisis de los productos, 

Conteo
Metricas <- gather(Conteo, "metrica", "valor", -Plataforma, -Año_Mes, -MARCA,-Hoja)
Metricas_interes <- Metricas %>% filter(metrica %in% c("inversión","revenue") & MARCA == 'Office Depot')

tmp <- ggplot(Metricas_interes, aes(x = Año_Mes, y = valor, fill = Plataforma)) +
  geom_col(alpha = 0.8) +
  facet_wrap(~metrica) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(valor), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Revenue")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

tmp
