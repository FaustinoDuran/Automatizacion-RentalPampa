from datetime import datetime, timedelta
from extraccion import alerta_ya_enviada, registrar_alerta

def generar_mensajes_transportes(df, registro):
    mensajes = []

    for _, fila in df.iterrows():
        try:
            km_restantes = int(fila['KM HASTA PROX SERVICE'])
        except ValueError:
            continue

        if km_restantes <= 1000:
            patente = fila.get('TRANSPORTES', 'N/D')
            if alerta_ya_enviada(registro, "transporte", patente):
                continue

            ubicacion = fila.get('UBICACION T', 'No especificada')

            asunto = f"🚨 ¡ATENCIÓN SERVICE TRANSPORTE! - {patente}"
            cuerpo = f"""\n¡Hola equipo!\n\n📢 ¡ATENCIÓN! El transporte ***{patente}*** está próximo al kilometraje de service.\n\n🔧 Detalles:\n\n- Patente: {patente}\n- Kilómetros restantes: {km_restantes} km\n- Ubicación actual: {ubicacion}\n\n⚠️ Acción requerida: Programar el service a la brevedad para evitar inconvenientes.\n\nSaludos,\n\nFaustino Duran  \nfaustigzmd@gmail.com"""

            mensajes.append({
                'asunto': asunto,
                'cuerpo': cuerpo,
                'tipo': 'transporte',
                'identificador': patente,
                'detalle': f'Ubicación: {ubicacion}'
            })

    return mensajes

def generar_mensajes_equipos(df, registro):
    mensajes = []

    for _, fila in df.iterrows():
        try:
            hs_restantes = int(fila['HS HASTA PROXIMO SERVICE'])
        except ValueError:
            continue

        if hs_restantes <= 100:
            equipo = fila.get('EQUIPOS', 'N/D')
            if alerta_ya_enviada(registro, "equipo", equipo):
                continue

            asunto = f"⏰ ¡ATENCIÓN SERVICE EQUIPO! - {equipo}"
            cuerpo = f"""\n¡Hola equipo!\n\n📢 ¡ALERTA! El equipo ***{equipo}*** se encuentra próximo al límite de horas para el próximo service.\n\n🔧 Detalles:\n\n- Equipo: {equipo}\n- Horas restantes: {hs_restantes} hs\n\n⚠️ Acción requerida: Coordinar el mantenimiento del equipo cuanto antes para evitar problemas.\n\nSaludos,\n\nFaustino Duran  \nfaustigzmd@gmail.com"""

            mensajes.append({
                'asunto': asunto,
                'cuerpo': cuerpo,
                'tipo': 'equipo',
                'identificador': equipo
            })

    return mensajes

def generar_mensaje_facturas(df, registro):
    hoy = datetime.now().date()
    alertas = []

    for _, fila in df.iterrows():
        alerta_lineas = []

        def parse_fecha(fecha_str):
            try:
                return datetime.strptime(fecha_str.strip(), "%d/%m/%Y").date()
            except:
                return None

        fecha_facturacion = parse_fecha(fila.get('Fecha de facturacion', ''))
        vencimiento_fc = parse_fecha(fila.get('Vencimiento FC', ''))
        fecha_pago = parse_fecha(fila.get('Fecha de pago', ''))
        reclamo_pago = parse_fecha(fila.get('Reclamo de pago', ''))

        empresa = fila.get('Empresa', 'Sin nombre')
        nro_factura = fila.get('N° factura', 'N/D')
        observacion = fila.get('Observacion F', '')

        identificador = f"Factura {nro_factura} - {empresa}"
        if alerta_ya_enviada(registro, "factura", identificador):
            continue

        if fecha_facturacion == hoy:
            alerta_lineas.append("📅 *Hoy es la fecha de facturación.*")
        if vencimiento_fc and vencimiento_fc - timedelta(days=5) == hoy:
            alerta_lineas.append("⏳ *Faltan 5 días para el vencimiento de la factura.*")
        if fecha_pago and fecha_pago - timedelta(days=1) == hoy:
            alerta_lineas.append("💸 *El pago está programado para mañana.*")
        if reclamo_pago and reclamo_pago - timedelta(days=1) == hoy:
            alerta_lineas.append("📢 *Mañana corresponde realizar el reclamo de pago.*")

        if alerta_lineas:
            texto_alerta = f"""
🧾 **Factura N° {nro_factura}** - {empresa}
{"".join("- " + linea + "\n" for linea in alerta_lineas)}
Observaciones: {observacion or 'Ninguna'}\n
"""
            alertas.append({
                'texto': texto_alerta,
                'identificador': identificador
            })

    if alertas:
        cuerpo = f"""\n¡Hola equipo!\n\n🔔 **Estas son las alertas de facturación para hoy ({hoy.strftime('%d/%m/%Y')}):**\n\n{"".join([a['texto'] for a in alertas])}\nRevisar y tomar acción según corresponda.\n\nSaludos,  \nFaustino Duran  \nfaustigzmd@gmail.com\n"""
        asunto = f"📋 Alerta de Facturación - {hoy.strftime('%d/%m/%Y')}"
        return [{
            'asunto': asunto,
            'cuerpo': cuerpo,
            'tipo': 'factura',
            'identificador': a['identificador']
        } for a in alertas]
    else:
        return []

ANTICIPACION = {
    'VTV PROV': 30,
    'VTV NAC': 30,
    'RUL': 20,
    '1KG': 7,
    '5KG o +': 7,
    'DUT': 7,
    'TASA DE FISC': 3,
    'Certificado Hidrooruga': 30,
    'VTO FACTURACION': 30,
    'C. DE PAGO': 7
}

def generar_mensaje_vencimientos(df_extintores, registro):
    hoy = datetime.today().date()
    alertas = []

    for index, fila in df_extintores.iterrows():
        equipo = fila.get('TIPO', 'Desconocido')
        for columna, dias_antes in ANTICIPACION.items():
            fecha_str = fila.get(columna, '').strip()
            if fecha_str:
                try:
                    fecha_evento = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                    identificador = f"{equipo} - {columna}"
                    if fecha_evento - timedelta(days=dias_antes) <= hoy <= fecha_evento:
                        if not alerta_ya_enviada(registro, "vencimiento", identificador):
                            alerta = f"- 📅 **{columna}** de *{equipo}* vence el {fecha_evento.strftime('%d/%m/%Y')}"
                            alertas.append({
                                'texto': alerta,
                                'identificador': identificador
                            })
                except ValueError:
                    continue

    if alertas:
        cuerpo = (
            "### **Alerta de Vencimientos Próximos**\n\n"
            "**Asunto:** 📅 Notificación de vencimientos - Documentación y Equipos\n\n"
            "¡Hola equipo!\n\n"
            "Se han detectado vencimientos próximos en la documentación y/o componentes registrados:\n\n"
            + "\n".join(a['texto'] for a in alertas) +
            "\n\n📌 **Acción requerida:** Verificar y renovar a la brevedad para mantener la operatividad y cumplimiento.\n\n"
            "Saludos,\n\nFaustino Duran\nfaustigzmd@gmail.com"
        )
        return [{
            'asunto': "📅 Notificación de vencimientos - Documentación y Equipos",
            'cuerpo': cuerpo,
            'tipo': 'vencimiento',
            'identificador': a['identificador']
        } for a in alertas]
    else:
        return []