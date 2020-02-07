library(ggplot2)
library(dplyr)
library(lubridate)
library(tidyr)

#Actualizar el historico
Potentials_001 <- read.csv('Documentos/Adsocial/GWEP/Data/Potentials_001.csv', stringsAsFactors = FALSE)
glimpse(Potentials_001)

Potentials <- Potentials_001 %>% 
  select(ID.de.Oportunidad, ID.de.Contacto, Nombre.de.Oportunidad , Desarrollo, Tipo.de.vivienda,
         Valor.de.la.vivienda, Fase, Fuente.de.Posible.cliente ,Fecha.creacion, Hora.creacion , Ingresos.esperados,
         `Duración.total.de.las.ventas`, `Duración.del.ciclo.de.ventas`,Importe,Nombre.de.la.campaña.de.anuncios,
         Motivo.de.perdida, Motivo.de.perdida2, Descuento.de.preventa, Precio.de.preventa,
         Nombre.de.Unidad, Descuentos...Sobrecobros, Precio.de.preventa, Meses.del.enganche.diferido,
         Precio.final, Enganche.diferido,Campaña.MKT,Torre, Forma.de.contacto)

Potentials$Fecha.creacion <- dmy(Potentials$Fecha.creacion)

glimpse(Potentials)

table(Potentials$Fase)

#Desarrollo, Fase de Lead, Fuente de Lead

#Apartado validado enganche validado
ggplot(filter(Potentials, Fase %in% c("Apartado validado (x contabilidad)", "Validación de apartado (x gerente)","Apartado (x gerente)")),
       aes(x = Desarrollo, fill = Fase)) +
        geom_bar() +
          theme(axis.text.x = element_text(angle = 90))

#Historico
ggplot(Potentials, aes(x = Fecha.creacion)) + geom_histogram() +
  theme(axis.text.x = element_text(angle = 90)) +
    ggtitle("Fecha de Creación Potentials")






