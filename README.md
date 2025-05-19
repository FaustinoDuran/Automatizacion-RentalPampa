# Automatización de Envío de Alertas por Email desde Google Sheets

Este proyecto automatiza el envío de correos electrónicos de alerta basados en los datos contenidos en distintas hojas de cálculo de Google Sheets. Está diseñado para usarse en entornos de mantenimiento y gestión operativa, como el seguimiento de servicios de transportes, inspecciones de extintores, control de equipos y facturación.

## ¿Qué hace este proyecto?

- Extrae datos de diferentes hojas de Google Sheets (`TRANSPORTES`, `EXTINTORES`, `EQUIPOS`, `FACTURACIÓN`).
- Evalúa condiciones específicas por tipo de hoja para determinar si se debe enviar una alerta.
- Genera mensajes de correo personalizados según el tipo de alerta.
- Envía esos correos a destinatarios definidos.
- Registra cada alerta enviada en una hoja de `REGISTRO_ALERTAS` para evitar envíos duplicados.

## Tecnologías y herramientas utilizadas

- Python 3.12
- Google Cloud Functions
- Google Cloud Scheduler
- Google Sheets API
- OAuth2 (autenticación con servicio de cuenta)
- `pandas` para manipulación de datos
- `smtplib` y `email` para el envío de correos

## Estructura del proyecto

- `main.py`: Punto de entrada principal para ejecutar todo el flujo.
- `extraccion.py`: Se encarga de conectarse a Google Sheets, obtener y registrar información.
- `generar_email.py`: Genera el contenido de los correos según el tipo de alerta.
- `enviar_mail.py`: Maneja el envío de correos electrónicos.
- `requirements.txt`: Lista de dependencias del proyecto.
- `README.md`: Documentación general del proyecto.
- `documento_cliente.md`: Instrucciones y detalles específicos para el cliente final.

## Despliegue

- La función se despliega en Google Cloud Functions como una función HTTP.
- Está programada para ejecutarse automáticamente todos los días a las 9 AM (hora de Buenos Aires) mediante Google Cloud Scheduler.

## Autor

Faustino Duran 
📧 faustigzmd@gmail.com

