from extraccion import cargar_hoja, obtener_registro_alertas, registrar_alerta
from enviar_mail import enviar_correo
from generar_email import (
    generar_mensajes_transportes,
    generar_mensajes_equipos,
    generar_mensaje_facturas,
    generar_mensaje_vencimientos
)

def main(request):
    # Cargar hojas
    df_transportes = cargar_hoja('Hoja 1', columnas_deseadas=['TRANSPORTES','KM HASTA PROX SERVICE', 'UBICACION T'])
    df_extintores = cargar_hoja('Hoja 2', columnas_deseadas=[
        'TIPO', 'UNIDADES', 'VTV PROV', 'VTV NAC', 'RUL', '1KG', '5KG o +',
        'DUT', 'TASA DE FISC', 'MICROTRCK', 'Certificado Hidrooruga',
        'N° POLIZA', 'VIGENCIA', 'VTO FACTURACION', 'COBERTURA', 'C. DE PAGO'
    ])
    df_equipos = cargar_hoja('Hoja 3', columnas_deseadas=['EQUIPOS','HS HASTA PROXIMO SERVICE'])
    df_facturas = cargar_hoja('Hoja 4', columnas_deseadas=[
        'Empresa', 'Fecha de facturacion', 'N° factura', 'Vencimiento FC',
        'Fecha de pago', 'Reclamo de pago', 'Observacion F'
    ])

    # Obtener registro de alertas anteriores
    registro = obtener_registro_alertas()

    # Generar mensajes con registro actual
    mensajes_transportes = generar_mensajes_transportes(df_transportes, registro)
    mensajes_equipos = generar_mensajes_equipos(df_equipos, registro)
    mensajes_facturas = generar_mensaje_facturas(df_facturas, registro)
    mensajes_vencimientos = generar_mensaje_vencimientos(df_extintores, registro)

    # Enviar correos y registrar alertas
    for msg in mensajes_transportes:
        enviar_correo(msg['asunto'], msg['cuerpo'])
        registrar_alerta(msg['tipo'], msg['identificador'], msg.get('detalle', ''))

    for msg in mensajes_equipos:
        enviar_correo(msg['asunto'], msg['cuerpo'])
        registrar_alerta(msg['tipo'], msg['identificador'])

    for msg in mensajes_facturas:
        enviar_correo(msg['asunto'], msg['cuerpo'])
        registrar_alerta(msg['tipo'], msg['identificador'])

    for msg in mensajes_vencimientos:
        enviar_correo(msg['asunto'], msg['cuerpo'])
        registrar_alerta(msg['tipo'], msg['identificador'])

    return "Proceso de alertas ejecutado correctamente", 200


