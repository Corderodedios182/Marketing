library(tidyverse)
library(ggplot2)
library(lubridate)
library(car)
library(plotly)

#Datos de Entrada
base <- read.csv("C:/Users/crf005r/Documents/3_GitHub/Marketing/Extendo/Dataset Events Febrero - Abril - Sheet1.csv")
base$fecha <- ymd(as.Date(base$fecha))
base["semana"] <- week(base$fecha)
base["dia"] <- day(base$fecha)

#Funcion Algoritmo Etiquetado
semaforo_eventos <- function(base){
  
  base <- base
  
  a <- list()
  
  for(i in seq(1,length(unique(base$ga.eventCategory)))){
    
    tmp <- filter(base,ga.eventCategory == unique(base$ga.eventCategory)[i])
    
    tmp <- if(dim(tmp)[1] < 3){
      tmp <- rbind(tmp, tmp[2,])
    }else{
      tmp
    }
    
    if(dim(tmp)[1] == length(rep(seq(1, round(dim(tmp)[1]/3), 1), each = 3))){
      tmp["rango_3_dias"] <- rep(seq(1, floor(dim(tmp)[1]/3), 1), each = 3)
    }else if(dim(tmp)[1] > length(rep(seq(1, round(dim(tmp)[1]/3), 1), each = 3))){
      tmp["rango_3_dias"] <- c(rep(seq(1, floor(dim(tmp)[1]/3), 1), each = 3),max(rep(seq(1, floor(dim(tmp)[1]/3), 1), each = 3)) + 1)
    }else{
      tmp["rango_3_dias"] <- c(rep(seq(1, floor(dim(tmp)[1]/3), 1), each = 3),max(rep(seq(1, floor(dim(tmp)[1]/3), 1), each = 3)) + 1,1)
    }
    
    df <- tmp %>% 
      group_by(ga.eventCategory, rango_3_dias) %>%
      summarise(
        max_fecha = max(fecha),
        suma = sum(ga.totalEvents),
        promedio = mean(ga.totalEvents),
        sd = sd(ga.totalEvents),
        mediana = median(ga.totalEvents),
        minimo = min(ga.totalEvents),
        max = max(ga.totalEvents))
    
    #Crear rango con el maximo 
    df["dif_event_dia_ant"] <- c(0,diff(df$max))
    
    df["dia_ant"] <- if(df["dif_event_dia_ant"] < 0){
      df$max + abs(df$dif_event_dia_ant)
    }else{
      df$max - df$dif_event_dia_ant
    }
    
    diferencia <- function(x,y){
      if(x <= y){
        (x/y - 1) * 100
      }else{
        (y/x)*100
      }
    }
    
    df["diferencia"] <- round(diferencia(df$max,df$dia_ant))
    
    #Etiquetar con el Maximo el Rango por Evento
    
    df["etiquetado"] <- ""
    df[df["diferencia"] >= -34,"etiquetado"] <- "verde"
    df[(df["diferencia"] <= -35) & (df["diferencia"] >= -50),"etiquetado"] <- "amarillo"
    df[(df["diferencia"] < -50) & (df["diferencia"] >= -89),"etiquetado"] <- "naranja"
    df[df["diferencia"] <= -90,"etiquetado"] <- "rojo"
    
    df["diferencia"] <- df["diferencia"]/100 
    
    a[[i]] <- df
    
  }
  
  base <- do.call(rbind, a)
  return(base)
}

base <- semaforo_eventos(base)

group_by(base, etiquetado) %>% count(conteo = n())
group_by(base, ga.eventCategory, etiquetado) %>% count(conteo = n())

#Analisis Estadistico Quantiles
filtrado <- filter(base, ga.eventCategory == unique(base$ga.eventCategory)[4])

qqPlot(filtrado$max, pch=19,
       main='QQplot para max de Eventos',
       xlab='Cuantiles teóricos',
       ylab='Cuantiles muestrales')
#Intervalo de Confianza 
t.test(x=filtrado$max, conf.level=0.60)$conf.int


#--Graficas Resultados--#
ggplotly(
  ggplot(filtrado, aes(x = max_fecha, y = diferencia)) +
  geom_line() + 
  geom_hline(yintercept=0, linetype="dashed", color = "green", size =1) +
  geom_hline(yintercept=-.35, linetype="dashed", color = "yellow", size =1) +
  geom_hline(yintercept=-.50, linetype="dashed", color = "orange", size =1) +
  geom_hline(yintercept=-.90, linetype="dashed", color = "red", size =1) +
  annotate("rect", xmin = 3, xmax = 4.2, ymin = 3, ymax = 5,alpha = .2) +
  ggtitle("Monitoreo de Caídas Eventos"))

ggplot(base, aes(x = max_fecha, y = diferencia)) +
  geom_line() + 
  geom_hline(yintercept=0, linetype="dashed", color = "green", size =1) +
  geom_hline(yintercept=-.35, linetype="dashed", color = "yellow", size =1) +
  geom_hline(yintercept=-.50, linetype="dashed", color = "orange", size =1) +
  geom_hline(yintercept=-.90, linetype="dashed", color = "red", size =1) +
  facet_wrap(~ga.eventCategory) +
  ggtitle("Monitoreo de Caídas Eventos")

#-Grafica Plotly-
print_percentage <- scales::label_comma(accuracy = 0.1, scale = 100, suffix = '%')

plot_ly(
  data = filtrado,
  x = ~max_fecha,
  hoverinfo = 'text'
) %>%
  add_lines(y = ~diferencia,
            name = 'Eventos diferencia porcentual',
            marker = list(color = "#0052ce"),
            line = list(color = '#0052ce', width = 2),
            fill = '#0052ce',
            text = ~max_fecha
  ) %>%
  add_annotations(
    x = filtrado$max_fecha,
    y = filtrado$diferencia,
    text = ~print_percentage(diferencia),
    yanchor = 'bottom',
    showarrow = FALSE
  ) %>%
  layout(
    title = paste0('Monitoreo de Eventos cada 3 días:  ', unique(filtrado$ga.eventCategory)),
    xaxis = list(title = "Revisar días que sobre pasan la Línea Crítica", tickangle = 0),
    yaxis = list(
      title = 'Diferencia Respecto a los días anteriores',
      range = c(min(filtrado$diferencia)/.35, max(filtrado$diferencia)/.95),
      tickformat = '%,2.f'
    ),
    legend = list(x = .40, y = -.15, orientation = 'h'),
    margin = list(r = -2),
    hovermode = 'compare',
    shapes = lines
  ) %>%
  add_lines(y=-.90,
            name = 'Línea Crítica',
            line = list(color = '#ce0015', width = 1),
            text = "-90%"
  )%>%
  add_lines(y=-.35,
            name = 'Alerta I',
            line = list(color = '#cfc625', width = 1),
            text = "-35%"
  )%>%
  add_lines(y=-.50,
          name = 'Alerta II',
          line = list(color = '#ce6e00', width = 1),
          text = "-50%")






