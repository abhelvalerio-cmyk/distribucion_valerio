# CASO 1: Gestor de inventario de herramientas
# Que plataforma conviene: Android (para celulares o tablets).
# Justificacion considerando:
# - Tipo de interesaccion y perifericos: Se usa con pantalla táctil y la cámara integrada del celular para escanear los códigos QR
#  de forma rápida.
# - Restricciones de conectividad y portabilidad: Necesita portabilidad absoluta para caminar por todo el taller y funcionar bien 
# aunque la señal de internet sea inestable.
# - Dependencias locales y hardware: Requiere uso directo de la cámara del dispositivo y almacenamiento local temporal.
# - Facilidad de instalación y actualización: Se instala fácilmente mediante un archivo APK en los celulares del personal.

# CASO 2: Monitor de diagnostico de hardware y red
# Que plataforma conviene: Desktop (computadoras de escritorio o laptops con Windows o Linux).
# Justificacion considerando:
# - Tipo de interesaccion y perifericos: Se interactúa mediante teclado y mouse en una estación de trabajo técnica.
# - Restricciones de conectividad y portabilidad: Está pensado para equipos fijos o de revisión técnica directa.
# - Dependencias locales y hardware: Necesita acceso profundo y sin restricciones al sistema operativo para leer el uso del CPU,
#  disco y red, además de guardar reportes directamente en el disco local.
# - Facilidad de instalación y actualización: Se distribuye mediante un programa ejecutable nativo para computadoras.

# CASO 3: Portal de autogestion de turnos y consultas institucionales
# Que plataforma conviene: Web.
# Justificacion considerando:
# - Tipo de interesaccion y perifericos: Interacción estándar mediante teclado, mouse o pantalla táctil desde cualquier navegador.
# - Restricciones de conectividad y portabilidad: Permite acceso inmediato desde cualquier dispositivo y lugar, sin requerir 
# instalaciones previas por parte de los usuarios.
# - Dependencias locales y hardware: No depende de hardware especial ni de accesos internos al sistema operativo del usuario.
# - Facilidad de instalación y actualización: Los datos se centralizan en el servidor y las mejoras se aplican automáticamente 
# sin que el usuario tenga que actualizar nada en su equipo.

# CASO 4: Punto de cobro y facturacion para cantina o kiosco
# Que plataforma conviene: Desktop (Windows o Linux).
# Justificacion considerando:
# - Tipo de interesaccion y perifericos: Uso intensivo de periféricos de escritorio como teclado numérico físico y atajos, 
# además de conexión directa por USB a una impresora térmica.
# - Restricciones de conectividad y portabilidad: Al ser una terminal fija, requiere estabilidad operativa total sin depender
#  de la latencia de la red.
# - Dependencias locales y hardware: Necesita comunicación directa por puertos USB con la impresora de tickets
#  y hardware de la caja.
# - Facilidad de instalación y actualización: Se instala una sola vez en la computadora fija del negocio.

# CASO 5: Registro y control de asistencia de campo
# Que plataforma conviene: Android (celulares o tablets).
# Justificacion considerando:
# - Tipo de interesaccion y perifericos: Diseñado para un manejo ágil con una sola mano mediante pantalla táctil.
# - Restricciones de conectividad y portabilidad: Debe poder transportarse fácilmente en un bolsillo o mochila, 
# funcionando al aire libre sin conexión permanente a internet y guardando los datos para sincronizarlos después.
# - Dependencias locales y hardware: Requiere almacenamiento local en el dispositivo móvil para guardar la asistencia sin internet.
# - Facilidad de instalación y actualización: Se instala de forma sencilla como aplicación móvil para el personal que sale a campo.


import flet as ft
from datetime import date, timedelta

# ---------------------------------------------------------------
# Tus materias y fechas de exámenes simuladas
# ---------------------------------------------------------------
EXAMENES = [
    {"materia": "Programación 2", "fecha": "2026-11-09", "hora": "09:00", "aula": "Lab 2"},
    {"materia": "Introducción a la IA", "fecha": "2026-11-11", "hora": "14:00", "aula": "Lab 1"},
    {"materia": "Ciencia de Datos", "fecha": "2026-11-13", "hora": "18:30", "aula": "Lab 3"},
    {"materia": "Estadística y Probabilidad", "fecha": "2026-11-16", "hora": "10:00", "aula": "Aula 7"},
    {"materia": "Lógica", "fecha": "2026-11-18", "hora": "08:30", "aula": "Aula 4"},
    {"materia": "Práctica 2", "fecha": "2026-11-20", "hora": "16:00", "aula": "Aula de Campo / Institución"},
]

TRAMITES = {
    "2026-0001": {"tipo": "Certificado de alumno regular", "estado": "Listo para retirar",
                  "detalle": "Retirar en Secretaría de 8 a 13 hs."},
    "2026-0002": {"tipo": "Equivalencias", "estado": "En proceso",
                  "detalle": "Derivado al Departamento de Alumnos."},
    "2026-0003": {"tipo": "Cambio de comisión", "estado": "Rechazado",
                  "detalle": "Sin cupo disponible en la comisión solicitada."},
    "2026-0004": {"tipo": "Constancia de examen", "estado": "Recibido",
                  "detalle": "Pendiente de revisión."},
}

# Áreas comunes y conocidas
TIPOS_TURNO = [
    "Departamento de Alumnos",
    "Secretaría Académica",
    "Tesorería / Pagos",
    "Biblioteca",
    "Mesa de Entradas",
]

HORARIOS = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00"]

COLOR_ESTADO = {
    "Listo para retirar": ft.Colors.GREEN,
    "En proceso": ft.Colors.ORANGE,
    "Recibido": ft.Colors.BLUE,
    "Rechazado": ft.Colors.RED,
}


def proximos_dias_habiles(n=7):
    dias, d = [], date.today()
    while len(dias) < n:
        d += timedelta(days=1)
        if d.weekday() < 5:
            dias.append(d.isoformat())
    return dias


def main(page: ft.Page):
    page.title = "Portal Institucional"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.padding = 0

    mis_turnos = []  # estado de la sesión

    def aviso(texto):
        page.show_dialog(ft.SnackBar(ft.Text(texto)))

    # ------------------------- Vista: Exámenes -------------------------
    def vista_examenes():
        lista = ft.Column(spacing=8)

        def render(filtro=""):
            lista.controls.clear()
            res = [e for e in EXAMENES if filtro.lower() in e["materia"].lower()]
            if not res:
                lista.controls.append(ft.Text("No se encontraron exámenes."))
            for e in res:
                lista.controls.append(
                    ft.Card(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.EVENT),
                            title=ft.Text(e["materia"], weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f'{e["fecha"]} · {e["hora"]} hs · {e["aula"]}'),
                        )
                    )
                )

        def al_buscar(ev):
            render(buscador.value or "")
            page.update()

        buscador = ft.TextField(
            label="Buscar materia",
            prefix_icon=ft.Icons.SEARCH,
            on_change=al_buscar,
        )
        render()
        return ft.Column([
            ft.Text("Fechas de examen", size=22, weight=ft.FontWeight.BOLD),
            buscador,
            lista,
        ], spacing=12)

    # ------------------------- Vista: Trámites -------------------------
    def vista_tramites():
        resultado = ft.Column()
        campo = ft.TextField(label="N.º de expediente", hint_text="Ej: 2026-0001")

        def consultar(ev):
            resultado.controls.clear()
            num = (campo.value or "").strip()
            t = TRAMITES.get(num)
            if t is None:
                resultado.controls.append(
                    ft.Text("No se encontró el expediente. Verificá el número.",
                            color=ft.Colors.RED)
                )
            else:
                resultado.controls.append(
                    ft.Card(content=ft.Container(
                        padding=16,
                        content=ft.Column([
                            ft.Text(t["tipo"], size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Estado: {t['estado']}", size=16,
                                    color=COLOR_ESTADO.get(t["estado"]),
                                    weight=ft.FontWeight.W_600),
                            ft.Text(t["detalle"]),
                        ], spacing=6),
                    ))
                )
            page.update()

        return ft.Column([
            ft.Text("Estado de trámites", size=22, weight=ft.FontWeight.BOLD),
            ft.Text("Probá con: 2026-0001, 2026-0002, 2026-0003 o 2026-0004",
                    size=12, color=ft.Colors.GREY),
            campo,
            ft.Button(content=ft.Text("Consultar"), icon=ft.Icons.SEARCH, on_click=consultar),
            resultado,
        ], spacing=12)

    # ------------------------- Vista: Turnos -------------------------
    def vista_turnos():
        nombre = ft.TextField(label="Nombre y apellido")
        dni = ft.TextField(label="DNI", keyboard_type=ft.KeyboardType.NUMBER)
        tipo = ft.Dropdown(
            label="Área",
            options=[ft.DropdownOption(key=t, text=t) for t in TIPOS_TURNO],
        )
        fecha = ft.Dropdown(
            label="Fecha",
            options=[ft.DropdownOption(key=d, text=d) for d in proximos_dias_habiles()],
        )
        hora = ft.Dropdown(
            label="Horario",
            options=[ft.DropdownOption(key=h, text=h) for h in HORARIOS],
        )
        lista = ft.Column(spacing=8)

        def render_lista():
            lista.controls.clear()
            if not mis_turnos:
                lista.controls.append(ft.Text("Todavía no solicitaste turnos."))
            for i, t in enumerate(mis_turnos):
                lista.controls.append(
                    ft.Card(content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.CONFIRMATION_NUMBER),
                        title=ft.Text(f'{t["tipo"]} · {t["fecha"]} {t["hora"]} hs'),
                        subtitle=ft.Text(f'{t["nombre"]} (DNI {t["dni"]})'),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Cancelar turno",
                            on_click=lambda ev, idx=i: cancelar(idx),
                        ),
                    ))
                )

        def cancelar(idx):
            mis_turnos.pop(idx)
            render_lista()
            aviso("Turno cancelado.")
            page.update()

        def solicitar(ev):
            n, d = (nombre.value or "").strip(), (dni.value or "").strip()
            if not n or not d.isdigit() or not (7 <= len(d) <= 8):
                aviso("Completá nombre y un DNI válido (7 u 8 dígitos).")
                return
            if not (tipo.value and fecha.value and hora.value):
                aviso("Elegí área, fecha y horario.")
                return
            if any(t["fecha"] == fecha.value and t["hora"] == hora.value for t in mis_turnos):
                aviso("Ya tenés un turno en ese día y horario.")
                return
            mis_turnos.append({"nombre": n, "dni": d, "tipo": tipo.value,
                               "fecha": fecha.value, "hora": hora.value})
            render_lista()
            aviso("¡Turno solicitado con éxito!")
            page.update()

        render_lista()
        return ft.Column([
            ft.Text("Solicitar turno", size=22, weight=ft.FontWeight.BOLD),
            nombre, dni, tipo, fecha, hora,
            ft.Button(content=ft.Text("Solicitar turno"), icon=ft.Icons.CHECK, on_click=solicitar),
            ft.Divider(),
            ft.Text("Mis turnos", size=18, weight=ft.FontWeight.BOLD),
            lista,
        ], spacing=12)

    # ------------------------- Navegación -------------------------
    VISTAS = [vista_examenes, vista_tramites, vista_turnos]
    cuerpo = ft.Container(padding=20, expand=True)
    contenedor = ft.Column([cuerpo], scroll=ft.ScrollMode.AUTO, expand=True)

    def cambiar(ev):
        cuerpo.content = VISTAS[int(ev.control.selected_index)]()
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Portal de Autogestión"),
        bgcolor=ft.Colors.INDIGO_100,
    )
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=cambiar,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EVENT, label="Exámenes"),
            ft.NavigationBarDestination(icon=ft.Icons.ASSIGNMENT, label="Trámites"),
            ft.NavigationBarDestination(icon=ft.Icons.CONFIRMATION_NUMBER, label="Turnos"),
        ],
    )

    cuerpo.content = vista_examenes()
    page.add(contenedor)


ft.run(main)