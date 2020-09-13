Leads_Final <- read.csv("/home/carlos/Documentos/3_Adsocial/GWEP/Data/Reporte/Finales_actuales/Leads_Final_historico.csv")

Plataformas <- read.csv("~/Documentos/3_Adsocial/GWEP/Campañas/campañas_final_agosto.csv")

table(Leads_Final$Desarrollo)

desarrollo <- "Cumbres Herradura"

"El Cortijo"
"Parque Hacienda"
"Real de Lutecia"
"Reserva del sur"

#linea 199
Fuente_clientes <- c("Facebook","Google","Instagram","Langind page","Página web")

#Todos los Leads plataformas digitales
Conteo_todos <- Leads_Final %>%
  group_by(Hora.de.creación, Desarrollo , Fuente.de.Posible.cliente, Estado.de.Posible.cliente) %>%
  summarise(Conteo = n()) %>%
  filter(Fuente.de.Posible.cliente %in% Fuente_clientes & Desarrollo == desarrollo )
  
Conteo_todos$Fuente.de.Posible.cliente <- str_replace_all(Conteo_todos$Fuente.de.Posible.cliente,c("Instagram"="Facebook"))

table(Conteo_todos$Fuente.de.Posible.cliente)

sum(Conteo_todos$Conteo)

#Leads todos 
Leads_Zoho_todos <- Conteo_todos %>% 
  group_by(Desarrollo,Hora.de.creación,Fuente.de.Posible.cliente) %>%
  summarize(Leads = sum(Conteo))

Leads_Zoho_todos$Mes <- month(Leads_Zoho_todos$Hora.de.creación)
Leads_Zoho_todos$Año <- year(Leads_Zoho_todos$Hora.de.creación)
Leads_Zoho_todos <- Leads_Zoho_todos %>% group_by(Año,Mes,Fuente.de.Posible.cliente) %>% summarize(Leads = sum(Leads)) %>% mutate(tipo_lead = "todos")
Leads_Zoho_todos['llave'] <- paste0(Leads_Zoho_todos$Año,"_",Leads_Zoho_todos$Mes,"_",Leads_Zoho_todos$Fuente.de.Posible.cliente)

names(Leads_Zoho_todos) <- c("Año", "Mes", "Plataforma", "Conteo_Leads","Tipo_de_lead","llave")

sum(Leads_Zoho_todos$Conteo_Leads)

#Todos los lead interese plataformas digitales
Tipo_Lead <- c("Contactado","Contactar","Agendada","Intento")

Conteo_interes <- filter(Conteo_todos, Estado.de.Posible.cliente %in% Tipo_Lead)

#Leads de interes
Leads_Zoho_interes <- Conteo_interes %>% 
  group_by(Desarrollo,Hora.de.creación,Fuente.de.Posible.cliente) %>%
  summarize(Leads = sum(Conteo))
Leads_Zoho_interes$Mes <- month(Leads_Zoho_interes$Hora.de.creación)
Leads_Zoho_interes$Año <- year(Leads_Zoho_interes$Hora.de.creación)
Leads_Zoho_interes <- Leads_Zoho_interes %>% group_by(Año,Mes,Fuente.de.Posible.cliente) %>% summarize(Leads = sum(Leads)) %>% mutate(tipo_lead = "interes")
Leads_Zoho_interes['llave'] <- paste0(Leads_Zoho_interes$Año,"_",Leads_Zoho_interes$Mes,"_",Leads_Zoho_interes$Fuente.de.Posible.cliente)

names(Leads_Zoho_interes) <- c("Año", "Mes", "Plataforma", "Conteo_Leads","Tipo_de_lead","llave")

sum(Leads_Zoho_interes$Conteo_Leads)

################
#Dinero gastado#
################

specify_decimal <- function(x, k) as.numeric(trimws(format(round(x, k), nsmall=k)))
format_number <- function(x,k) formatC(as.numeric(x),format="f",digit=0,big.mark = ",")

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

tmp_Go$Fecha_Inicio <- str_replace_all(tmp_Go$Fecha_Inicio, c("ene"="01","feb"="02","mar"="03","abr"="04","may"="05","jun"="06",
                                                              "jul"="07","ago"="08","sep"="09","oct"="10","nov"="11","dic"="12"))

tmp_Go$Fecha_Inicio <- paste0("01-",tmp_Go$Fecha_Inicio)
tmp_Go$Fecha_Inicio <- as.Date(tmp_Go$Fecha_Inicio, format = "%d-%m-%y")
tmp_Go['ym'] <- ymd(tmp_Go$Fecha_Inicio)

Plataformas <- rbind(tmp_Fb,tmp_Go) ; rm(tmp_Fb,tmp_Go)
table(Plataformas$Desarrollo)
  
Plataformas <- filter(Plataformas, ym > "2018-12-01" & Desarrollo %in% c("Aurum","Cumbres Herradura","El Cortijo","Parque Hacienda","Real de Lutecia","Reserva del sur"))
table(Plataformas$Desarrollo)

Resumen_Campañas <- Plataformas %>% group_by(ym, Plataforma,Desarrollo) %>%
  filter(Desarrollo == desarrollo) %>%
  summarize(Clics = sum(Clics,na.rm = TRUE),
            Conversiones = sum(Conversiones,na.rm = TRUE),
            Inversión = sum(Costo,na.rm = TRUE))

names(Resumen_Campañas) <- c("Fecha","Plataforma","Desarrollo","Clics","Conversión","Inversión")
Resumen_Campañas$Inversión <-  as.numeric(Resumen_Campañas$Inversión)
Resumen_Campañas$Clics <- paste0(formatC(as.numeric(Resumen_Campañas$Clics), format="f", digits=0, big.mark=","))
Resumen_Campañas['Mes'] <- month(Resumen_Campañas$Fecha)
Resumen_Campañas['Año'] <- year(Resumen_Campañas$Fecha)

Resumen_Campañas <- data.frame(Resumen_Campañas) %>% select(Año, Mes, Plataforma,Desarrollo, Clics, Conversión, Inversión)

Resumen_Campañas['llave'] <- paste0(Resumen_Campañas$Año,"_",Resumen_Campañas$Mes,"_",Resumen_Campañas$Plataforma)
  
tmp_todos <- left_join(Leads_Zoho_todos, Resumen_Campañas, by = c("llave")) %>% filter(Año.x > 2018)
tmp_interes <- left_join(Leads_Zoho_interes, Resumen_Campañas, by = c("llave")) %>% filter(Año.x > 2018)

tmp_interes['cpl'] <- round(tmp_interes$Inversión / tmp_interes$Conteo_Leads,2)
tmp_todos['cpl'] <- round(tmp_todos$Inversión / tmp_todos$Conteo_Leads,2)

tmp_todos['test'] <- as.Date(paste0(tmp_todos$Año.x,"-",tmp_todos$Mes.x,"-1"))
tmp_interes['test'] <- as.Date(paste0(tmp_interes$Año.x,"-",tmp_interes$Mes.x,"-1"))

cpl_t <- ggplot(tmp_todos, aes(x = test, y = cpl, fill = Plataforma.x)) +
  geom_col() +
  geom_text(aes(label = paste0("$",formatC(as.numeric(cpl), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  ggtitle(paste0("cpl todos los Leads: " , desarrollo)) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.2))

cpl_i <- ggplot(tmp_interes, aes(x = test, y = cpl, fill = Plataforma.x)) +
  geom_col() +
  geom_text(aes(label = paste0("$",formatC(as.numeric(cpl), format="f", digits=0, big.mark=","))), position = position_stack(vjust = 0.5), size = 3,check_overlap = TRUE) +
  ggtitle(paste0("cpl leads de interes: " , desarrollo)) +
  labs(fill = "") +
  ggthemes::theme_economist() +
  xlab("") +
  ylab("") + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.2))

Salida <- list(grid.arrange(cpl_t, cpl_i, nrow = 1, ncol = 2, as.table = TRUE))


  



