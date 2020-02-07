library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)

rm(list=ls())

####Bases no vacias

no_na <- function(base){
  
  base_0 <- base %>%
    select(everything()) %>%  # replace to your needs
    summarise_all(funs(sum(is.na(.))))
  
  base_0 <- data.frame(Conteo_na = t(base_0))
  
  base_0['Columna'] <- row.names(base_0)
  
  Columnas_na <- filter(base_0, Conteo_na != dim(base)[1]) %>%
    select(Columna)
  
  base_0 <- select(base, one_of(as.vector(unlist(c(Columnas_na)))))
  
  return(base_0)
}

setwd("/home/carlos/Documentos/Adsocial/GWEP/CRM/")

#a <- data.frame(columnas = strsplit(list.files(),"_"), row.names = NULL)
#a <- data.frame(t(a), row.names = NULL)
#write.csv(a,"archivos.csv")
archivos <- read.csv("/home/carlos/Documentos/Adsocial/GWEP/archivos.csv")

#Leer todos los archivos
for(i in seq(1,length(unlist(list.files())))){
  eval(parse(text = (paste0(archivos[i,]," <- read.csv('",list.files()[i],"',stringsAsFactors = FALSE)"))))
}

lista = ls()

#Me quedo con archivos no vacios
for(i in seq(1,length(lista))){
  
  if(is.data.frame(eval(parse(text = lista[i])))){
    
    if(dim(eval(parse(text = lista[i]))[1])  == 0){
      
      rm(list = lista[i]) }
  }
    }

lista = ls()
i <- 1

#Me quedo con campos no vacios
for(i in seq(1,length(lista))){
  
  if(is.data.frame(eval(parse(text = lista[i])))){
    
    eval(parse(text = paste0(lista[i], " <- ", "no_na(",lista[i],")")
               )
        )
    }
      }

rm(archivos)

Potentials_001 <- read.csv("~/Documentos/Adsocial/GWEP/Data/Potentials_001.csv", stringsAsFactors = FALSE)
Potentials_001 <- no_na(Potentials_001)

str(Potentials_001)

Potentials <- Potentials_001 %>% select(ID.de.Contacto,ID.de.Oportunidad, Importe, Ingresos.esperados,Duración.del.ciclo.de.ventas,Tipo.de.vivienda, Tipo.de.dispositivo, Tipo.de.clic, Valor.de.la.vivienda, Precio.de.preventa, Precio.final, Precio.de.venta.final.LETRA,  )
str(Potentials)

#####

Leads_001 <- read.csv("~/Documentos/Adsocial/GWEP/Data/Leads_001.csv", stringsAsFactors = FALSE)
Leads_001 <- no_na(Leads_001)

str(Leads_001)

table(Leads$Nombre.de.la.campaña.de.anuncios)

Leads <- Leads_001 %>% select(Correo.electrónico, Correo.electrónico.secundario, Fuente.de.Posible.cliente, Estado.de.Posible.cliente,
                              Nombre.completo, Desarrollo, Nombre.de.la.campaña.de.anuncios, Nombre.del.grupo.de.anuncios, Estatus.KPI,
                              Descripción,Palabra.clave, Campaña.MKT, LP, Forma.de.contacto, Estado.de.Posible.cliente, Motivo.de.perdido,
                              Palabra.clave, Hora.de.creacion, Hora.de.modificacion, Hora.ultima.actividad, Hora.de.cita.web) 
                              
#Fecha de creacion, Desarrollo, fuente del lead

#¿Que fecha se crearon más?

tmp <- Leads %>%
  group_by(Hora.de.creacion) %>%
  summarise(Conteo = n())

#¿Como detecta mis campañas?
tmp <- Leads %>%
  group_by(Nombre.de.la.campaña.de.anuncios) %>%
  summarise(Conteo = n())

tmp <- Leads %>%
  group_by(Campaña.MKT) %>%
  summarise(Conteo = n())


#¿Fuente del lead?
tmp <- Leads %>%
  group_by(Fuente.de.Posible.cliente, Nombre.de.la.campaña.de.anuncios) %>%
  summarise(Conteo = n())

tmp <- Leads %>%
  filter(Fuente.de.Posible.cliente)

Leads %>% 
  group_by(Desarrollo) %>%
  summarise(Conteo = n())

str(Leads)

#####

Emails_001 <- read.csv("~/Documentos/Adsocial/GWEP/Data/Emails_001.csv", strip.white = FALSE)

str(Emails_001)
Emails <- no_na(Emails_001)

str(Emails)

Emails <- select(Emails,Cc, Sender, Primer.clic, Estado)

####

indicadores_diarios_C_001 <- read.csv("~/Documentos/Adsocial/GWEP/Data/indicadores_diarios_C_001.csv", stringsAsFactors = FALSE)
indiacdores <- no_na(indicadores_diarios_C_001)

str(indiacdores)

indicadores <- indicadores %>% select()
head(tmp)


head(tmp_1)

Lead <- read.csv("~/Documentos/Adsocial/GWEP/Lead.csv")

#Fuente Posible cliente
ggplot(Lead, aes(x = Hora.de.creacion, fill = Fuente.de.Posible.cliente)) + geom_bar() +
  theme(axis.text.x = element_text(angle = 90))

#Fuente Posible cliente y Estado del cliente
ggplot(tmp_1, aes(x = Hora.de.creacion, fill = Fuente.de.Posible.cliente)) + geom_bar() +
  theme(axis.text.x = element_text(angle = 90)) + facet_wrap(~Estado.de.Posible.cliente)

#Fuente Posible cliente y Estado del cliente
ggplot(filter(tmp_1, Estado.de.Posible.cliente %in% c("Contactado","Contactar en el futuro","Intento de contacto")), aes(x = Hora.de.creacion, fill = Fuente.de.Posible.cliente)) + geom_bar() +
  theme(axis.text.x = element_text(angle = 90)) + facet_wrap(~Estado.de.Posible.cliente)

#Estado de clientes por Desarrollo
names(Lead)
tmp <- Lead %>% filter(Estado.de.Posible.cliente %in% c("Contactado","Contactar en el futuro","Intento de contacto")) %>%
  group_by(Desarrollo) %>%
  summarise(Conteo_Lead_interes = n()) %>% 
  left_join(Lead  %>%
              group_by(Desarrollo) %>%
              summarise(Conteo_Todos = n()) ,by = "Desarrollo")
tmp
ggplot(tmp, aes(x = Desarrollo, y = Conteo_Todos)) + geom_col() +
  theme(axis.text.x = element_text(angle = 90))

a <- gather(tmp,"Lead","Conteo",-Desarrollo)

ggplot(a, aes(x = Desarrollo, y = Conteo, fill = Lead)) + geom_col() +
  theme(axis.text.x = element_text(angle = 90)) + 
  ggtitle("Son pocos los Leads de interes")

#¿Que ayuda a generar más Leads de calidad?

tmp <- Lead %>% filter(Estado.de.Posible.cliente %in% c("Contactado","Contactar en el futuro","Intento de contacto"))

names(tmp)

#Que keywords nos han funcionado mejor

a <- tmp %>% group_by(Palabra.clave) %>%
  summarise(Conteo = n())
  

#
library(tidyr)


library(dplyr)
# From http://stackoverflow.com/questions/1181060
stocks <- tibble(
  time = as.Date('2009-01-01') + 0:9,
  X = rnorm(10, 0, 1),
  Y = rnorm(10, 0, 2),
  Z = rnorm(10, 0, 4)
)









