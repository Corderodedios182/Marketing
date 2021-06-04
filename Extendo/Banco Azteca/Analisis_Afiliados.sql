SELECT 
--campos categoricos
media_source, 
af_prt,
--calculado
CASE 
WHEN REGEXP_CONTAINS(media_source, "ACAI") THEN "prueba" END,
--campos fechas
fecha,
event_time_selected_timezone, --me deja filtrar por
attributed_touch_time_selected_timezone, --Atributed_Touch_Type_Selected_Timezone (Atribución similar a click)
install_time_selected_timezone, --Install Time Selected Timezone (Momento en que se abre por primera vez la app)
device_download_time_selected_timezone, --Device Download Time Selected Zone (Posible evento de instalación)
FROM `bancoazteca-master-hub.appsflyer_data.appsflyer_events_data` 
--rango de tiempo
WHERE DATE(event_time_selected_timezone) = "2021-04-21" AND 
where media_source = 'ACAI'
LIMIT 10

--CORRE ESTADISTICAS POR MES
SELECT 
MES,
AVG(SEGUNDOS) AS PROMEDIO,
MIN(SEGUNDOS) AS MINIMO,
MAX(SEGUNDOS) AS MAXIMO,
APPROX_QUANTILES(SEGUNDOS, 2) AS QUANTILE
FROM
(SELECT 
EXTRACT(MONTH FROM event_time_selected_timezone) AS MES,
DATETIME_DIFF(TIMESTAMP(device_download_time_selected_timezone), TIMESTAMP(attributed_touch_time_selected_timezone), SECOND) AS SEGUNDOS
FROM `bancoazteca-master-hub.appsflyer_data.appsflyer_events_data` 
--rango de tiempo
WHERE DATE(event_time_selected_timezone) = "2021-04-21" AND media_source = 'Facebook Ads'
LIMIT 100)
GROUP BY MES

--corre todos los datos de un dia
SELECT 
media_source,
af_prt,
EXTRACT(MONTH FROM event_time_selected_timezone) AS MES,
EXTRACT(DAY FROM event_time_selected_timezone) AS DIA,
EXTRACT(HOUR FROM event_time_selected_timezone) AS HORA,
DATETIME_DIFF(TIMESTAMP(device_download_time_selected_timezone), TIMESTAMP(attributed_touch_time_selected_timezone), SECOND) AS SEGUNDOS
FROM `bancoazteca-master-hub.appsflyer_data.appsflyer_events_data` 
WHERE DATE(event_time_selected_timezone) = "2021-04-26"
