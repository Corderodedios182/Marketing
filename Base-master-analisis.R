library(readxl) ; library(gridExtra) ; library(tidyr) ; library(dplyr) ; library(ggplot2) ; library(lubridate) ; library(stringr) ;library(cowplot) ; library(ggthemes) ; library(readxl); library("modeest"); library(corrplot) ; library(scales) ; library(ggthemes)
options(repr.plot.width=10, repr.plot.height=8)

is.nan.data.frame <- function(x)
  do.call(cbind, lapply(x, is.nan))

#Importación de datos
base = read.csv('/home/carlos/Documentos/3_Adsocial/Marketing/Base master Roas - semanal normal.csv', stringsAsFactors = FALSE)
base$total_revenue <- round(base$total_revenue)
base_od <-  base %>% filter(cliente_nomenclatura == 'od') %>%
  select("Año.Mes", mes_plan, inicio_reporte, fin_reporte, semana, dias_mes, campaña_nomenclatura, plataforma, divisa, dinero_gastado,
          impresiones, clics,total_conversiones, total_revenue) %>%
  mutate(ROI = round(((total_revenue - dinero_gastado)/total_revenue )*100) )
base_od$ROI[base_od$ROI == '-Inf'] <- 0
base_od$inicio_reporte <- as.Date(base_od$inicio_reporte)
base_od$fin_reporte <- as.Date(base_od$inicio_reporte)

head(base_od, 3)
names(base_od)

#Variable de interes total_revenue
summary(base_od$total_revenue)
summary(base_od$ROI)

#--Boxplot total revenue--#
box_plot <- function(base, x, y, title ){

    a <- ggplot(base, aes(x = x, y = y), color = dose) +
      geom_boxplot(color = "brown") +
      scale_y_continuous(labels = dollar) +
      ggtitle(title) +
      ggthemes::theme_economist()
    
    return(a)

    }

menor <- filter(base_od, total_revenue < 100000)
mayor <- filter(base_od, total_revenue > 100000)

list(grid.arrange(box_plot(base_od, x = "", y = base_od$total_revenue, title = "Total revenue") ,
                  tableGrob(data.frame(estadisticas = round(unclass(summary(base_od$total_revenue))))),
                  box_plot(menor, x = "", y = menor$total_revenue, title = "Revenue menor a $100,000") ,
                  box_plot(mayor, x = "", y = mayor$total_revenue, title = "Revenue mayor a $100,000"),
                  nrow = 2, ncol = 2, as.table = TRUE))

rm(a,b,c, base)
###########################
#--Numero de campañas por plataforma --#
base_od[base_od$inicio_reporte == '2020-01-01',]

a <- mayor %>%
  group_by(plataforma,campaña_nomenclatura) %>%
  summarise(revenue = sum(total_revenue), dinero_gastado = sum(dinero_gastado)) %>%
  mutate(ROI = round(((revenue - dinero_gastado)/revenue )*100) )
a$ROI[a$ROI == '-Inf'] <- 0
head(a)
table(a$plataforma)

ggplot(a, aes(x = campaña_nomenclatura, y = ROI, color = plataforma)) +
  geom_point() +
  geom_hline(aes(yintercept=0), color="blue",linetype="dashed") + 
  theme(axis.text.x = element_text(angle = 45,hjust = 1)) +
  ggtitle("ROI 92 campañas, Facebook: 42, Google Search: 21, Programmatic: 29", 
          subtitle = "En general se cuenta con un ROI positivo")

#ROI mensual
a <- mayor %>%
  group_by(plataforma,campaña_nomenclatura,Año.Mes) %>%
  summarise(revenue = sum(total_revenue), dinero_gastado = sum(dinero_gastado)) %>%
  mutate(ROI = round(((revenue - dinero_gastado)/revenue )*100) )
a$ROI[a$ROI == '-Inf'] <- 0
head(a)

ggplot(a, aes(x = campaña_nomenclatura, y = ROI, color = plataforma)) +
  geom_point() +
  geom_hline(aes(yintercept=0), color="blue",linetype="dashed") + 
  theme(axis.text.x = element_text(angle = 45,hjust = 1)) +
  ggtitle("ROI mensual campañas", 
          subtitle = "Veamos el seguimiento mensual")

#ROI semanal
a <- mayor %>%
  group_by(plataforma,campaña_nomenclatura,inicio_reporte) %>%
  summarise(revenue = sum(total_revenue), dinero_gastado = sum(dinero_gastado)) %>%
  mutate(ROI = round(((revenue - dinero_gastado)/revenue )*100) )
a$ROI[a$ROI == '-Inf'] <- 0
head(a)

ggplot(a, aes(x = campaña_nomenclatura, y = ROI, color = plataforma)) +
  geom_point() +
  geom_hline(aes(yintercept=0), color="blue",linetype="dashed") + 
  facet_wrap(~inicio_reporte) +
  theme(axis.text.x = element_text(angle = 45,hjust = 1)) +
  ggtitle("ROI semanal campañas", 
          subtitle = "")



#Acotar el ROI
summary(base_od$ROI)
menor <- filter(base_od, ROI < -100) #Mal ROI
mayor <- filter(base_od, ROI > -100) #Buen ROI

ggplot(base_od, aes(x = inicio_reporte, y = ROI, color = plataforma)) +
  geom_point() +
  theme(axis.text.x = element_text(angle = 45)) + 
  ggtitle("ROI 97 campañas, Facebook: 47, Google Search: 21, Programmatic: 29", 
          subtitle = "ROI semanal de las campañas, podemos ver que no es muy claro ya que tenemos ROI muy negativos.")

ggplot(menor, aes(x = inicio_reporte, y = ROI, color = plataforma)) +
  geom_point() +
  theme(axis.text.x = element_text(angle = 45)) + 
  ggtitle("ROI menor a -100", 
          subtitle = "")

ggplot(mayor, aes(x = inicio_reporte, y = ROI, color = plataforma)) +
  geom_point() +
  geom_hline(aes(yintercept=0), color="blue",linetype="dashed") + 
  theme(axis.text.x = element_text(angle = 45)) + 
  ggtitle("Campañas con ROI mayor a -100", 
          subtitle = "")




tmp <- base_od %>%
  group_by(plataforma, Año.Mes, inicio_reporte) %>%
  summarise(Conteo = n(), revenue = sum(total_revenue), gastado = sum(dinero_gastado)) %>%
  mutate(ROA = revenue/gastado ) +
  mutate(ROI = round(((revenue - gastado)/revenue )*100) )
  
tmp <- tmp %>% gather(Variable, valor, -plataforma, -Año.Mes) ; tmp

ggplot(tmp, aes(x=Año.Mes, y=valor, color=plataforma)) + geom_point() + scale_y_continuous(labels = dollar) + facet_wrap(~Variable)

#- CPC
#- CPL
#- CPA
  
ggplot(mayor, aes(x = dinero_gastado, y = total_revenue)) +
  geom_point(aes(color = plataforma)) +
  scale_x_continuous(labels = dollar) +
  scale_y_continuous(labels = dollar) +
  ggtitle("") +
  facet_wrap(~plataforma)
