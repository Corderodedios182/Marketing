options(scipen=999)

library(gridExtra)
library(tidyr)
library(dplyr)
library(ggplot2)
library(lubridate)
library(stringr)
library(cowplot)
library(ggthemes)
library(readxl)
#funcion de apoyo para el formato de numeros
fn <- function(x){
  format(x, digits=9, decimal.mark=".",
         big.mark=",",small.mark=",", small.interval=3)  
}

# Necesitamos tener la certeza que la información de la base master roas sea la misma que en sus archivos base

#¿Cuanta inversión total tenemos en el archivos de kpis?
KPIS <- read_excel("~/Dropbox/ROAS 2020/KPIS 2020 .xlsx",sheet = "KPIS MP 2020", skip = 2)

KPIS$`Inversión Total` <- as.integer(KPIS$`Inversión Total`)
KPIS$Plataforma <- trimws(KPIS$Plataforma)
KPIS$Plataforma <- str_replace_all(KPIS$Plataforma," ","")
KPIS$NOMENCLATURA <- tolower(KPIS$NOMENCLATURA)

KPIS$Plataforma <- str_replace_all(KPIS$Plataforma, c("Adform" = "DSP",
                                                      "AdsMovil" = "PV_AdsMovil",
                                                      "Content" = "PV_Content",
                                                      "DisplayAd" = "DSP",
                                                      "Facebook/Instagram" = "FB",
                                                      "Facebook" = "FB",
                                                      "Instagram" = "FB",
                                                      "GoogleSearch" = "SEM",
                                                      "GoogleGDN" = "SEM",
                                                      "Google" = "SEM",
                                                      "Mobile" = "PV_Mobile",
                                                      "Programmatic\\(Herolense-Acuity\\)" = "DSP",
                                                      "Programmatic\\(Herolense\\)" = "DSP",
                                                      "Programmatic" = "DSP",
                                                      "PushNotification" = "PV_Push Notification",
                                                      "Spotify&Others" = "PV_Spotify & Others",
                                                      "Waze" = "PV_Waze"))

table(KPIS$Plataforma)

KPIS['llave_unica_mp'] <- paste0(KPIS$NOMENCLATURA,"_",KPIS$Plataforma,"_",KPIS$Versión)

kpis_1 <- KPIS %>%
  group_by(Mes,Plataforma,Versión,NOMENCLATURA, llave_unica_mp) %>%
  summarize(Conteo = n(), inversión_total = sum(`Inversión Total`,na.rm = TRUE))

kpis_2 <- kpis_1 %>% 
  group_by(Mes,Plataforma,Versión) %>%
  summarize(Conteo = n(), inversion_cuadra_kpis = sum(inversión_total,na.rm = TRUE))

data.frame(registros = sum(kpis_1$Conteo),
           inversion_kpis = fn(sum(kpis_1$inversión_total)))

#¿Esta misma inversión se mantiene en el archivo de base master roas?
base_roas <- read.csv("~/Documentos/3_Adsocial/Marketing/Analytics/base_roas.csv", stringsAsFactors = FALSE)

table(base_roas$plataforma_x,base_roas$plataforma_abreviacion)

base_roas$fecha_inicio_plan <- as.Date(base_roas$fecha_inicio_plan)
base_roas$fecha_fin_plan <- as.Date(base_roas$fecha_fin_plan)
base_roas$inicio_campaña <- as.Date(base_roas$inicio_campaña)
base_roas$fin_campaña <- as.Date(base_roas$fin_campaña)
base_roas$inicio_reporte <- as.Date(base_roas$inicio_reporte)
base_roas$fin_reporte <- as.Date(base_roas$fin_reporte)
base_roas$inicio <- as.Date(base_roas$inicio)
base_roas$fin <- as.Date(base_roas$fin)

base_roas$dias_totales_campaña <- (base_roas$fecha_fin_plan) - (base_roas$fecha_inicio_plan)

base_roas_asistidas <- base_roas %>% 
  filter(base_roas$comentario == "conversiones asistidas campañas que no tengo en el mp")

#¿Que debe cuadrar con el mp?
table(base_roas$comentario)
#Esta información viene directo del archivo kpis
base_roas_kpis <- base_roas %>% 
  filter(base_roas$comentario != "conversiones asistidas campañas que no tengo en el mp")

#Conteo de campañas por mes
cuadrar_1 <- base_roas_kpis %>%
  group_by(Año.Mes,mes_plan,plataforma_abreviacion,plataforma_x,versión,llave_unica_mp) %>%
  summarize(Conteo = n(), inversión_total = sum(inversión_total,na.rm = TRUE)) %>%
  mutate(inversion_cuadra_mp = inversión_total / Conteo)

#Cruzamos kpis_1 y cuadrar_1 para validar que todas las cifras sean correctas
tmp <- left_join(cuadrar_1,
                 select(KPIS, llave_unica_mp, `Inversión Total`),
                 by = c("llave_unica_mp" = "llave_unica_mp"))

fn(sum(cuadrar_1$inversion_cuadra_mp))

cuadrar_2 <- cuadrar_1 %>% 
  group_by(Año.Mes,plataforma_abreviacion,versión) %>%
  summarize(Conteo = n(), inversion_cuadra_mp = sum(inversion_cuadra_mp,na.rm = TRUE))

cuadrar_2$versión <- str_replace_all(cuadrar_2$versión, c("V1" = "Versión Normal",
                               "V2" = "Versión Normal",
                               "V3" = "Versión Normal",
                               "V4" = "Versión Normal",
                               "V5" = "Versión Normal",
                               "VC1" = "Versión Cliente",
                               "VC2" = "Versión Cliente",
                               "VC3" = "Versión Cliente"))

cuadrar_3 <- cuadrar_2 %>% 
  group_by(Año.Mes,plataforma_abreviacion,versión) %>%
  summarize(inversion_cuadra_mp = sum(inversion_cuadra_mp,na.rm = TRUE))

fn(sum(cuadrar_3$inversion_cuadra_mp))

#Graficas Inversion total base master roas
inversion_todos <- ggplot(cuadrar_3, aes(x = Año.Mes, y = inversion_cuadra_mp, fill = plataforma_abreviacion)) +
  geom_col(alpha = 0.8) +
  facet_wrap(~versión) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(inversion_cuadra_mp), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 5,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Inversión MP")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

inversion_todos

#Analisis de la información de los reportes
names(base_roas_kpis)

table(base_roas_kpis$inicio_reporte)

cuadrar_1_plt <- base_roas_kpis %>%
  group_by(Año.Mes,mes_plan,plataforma_abreviacion,plataforma_x,versión,llave_unica_mp,inicio_reporte) %>%
  summarize(Conteo = n(), dinero_gastado = sum(dinero_gastado,na.rm = TRUE))

cuadrar_2_plt <- cuadrar_1_plt %>% 
  group_by(Año.Mes,plataforma_abreviacion,versión) %>%
  summarize(Conteo = n(), dinero_gastado = sum(dinero_gastado, na.rm = TRUE))

cuadrar_2_plt$versión <- str_replace_all(cuadrar_2$versión, c("V1" = "Versión Normal",
                               "V2" = "Versión Normal",
                               "V3" = "Versión Normal",
                               "V4" = "Versión Normal",
                               "V5" = "Versión Normal",
                               "VC1" = "Versión Cliente",
                               "VC2" = "Versión Cliente",
                               "VC3" = "Versión Cliente"))

cuadrar_3_plt <- cuadrar_2_plt %>% 
  group_by(Año.Mes,plataforma_abreviacion,versión) %>%
  summarize(dinero_gastado = sum(dinero_gastado, na.rm = TRUE))

dinero_gastado <- ggplot(cuadrar_3_plt, aes(x = Año.Mes, y = dinero_gastado, fill = plataforma_abreviacion)) +
  geom_col(alpha = 0.8) +
  facet_wrap(~versión) +
  geom_text(aes(label = paste0("$",formatC(as.numeric(dinero_gastado), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 5,check_overlap = TRUE) +
  theme(axis.text.x = element_text(angle = 90)) +
  ggtitle(paste0("Dinero gastado plataformas")) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("")

dinero_gastado

grid.arrange(inversion_todos, dinero_gastado, nrow = 2, ncol = 1, as.table = TRUE)
