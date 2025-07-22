import flet as ft
import math
import datetime

class HomePage(ft.Container):
    def __init__(self, page: ft.Page, navigate_to_checklist_callback=None, navigate_to_webscrap_callback=None, navigate_to_confrontas_callback=None):
        super().__init__(expand=True)
        self.page = page
        self.navigate_to_checklist = navigate_to_checklist_callback
        self.navigate_to_webscrap = navigate_to_webscrap_callback
        self.navigate_to_confrontas = navigate_to_confrontas_callback
        self.page.title = "Home"
        self.bg_color = "#ffffff"
        self.dark_white = "#e7e6e9"
        self.grey_color = "#a9acb6"
        self.yellow_color = "#ece5d5"
        self.page.bgcolor = self.bg_color

        # Referencia para el log de actividades
        self.log_ref = ft.Ref[ft.Text]()
        # Referencia para el log de incapacidades
        self.log_incapacidades_ref = ft.Ref[ft.Text]()

        self.menu = ft.Container(
            width=60,
            margin=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=40, height=40, border_radius=10, bgcolor=self.yellow_color,
                                 content=ft.IconButton(ft.Icons.HOME, icon_color="black")
                                 ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.CHECKLIST_OUTLINED, icon_color="black", 
                                                     on_click=self.navigate_to_checklist)
                                 ),
                            ft.Divider(height=1, color=self.dark_white),
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.CLEANING_SERVICES_OUTLINED, icon_color="black",
                                                     on_click=self.navigate_to_webscrap)
                                 ),
                            ft.Divider(height=1, color=self.dark_white),
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.REQUEST_PAGE_OUTLINED, icon_color="black",
                                                     on_click=self.navigate_to_confrontas)
                                 ),
                            ft.Divider(height=1, color=self.dark_white),
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.BUILD_OUTLINED, icon_color="black")
                                 ),
                            ft.Divider(height=1, color=self.dark_white),
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.DESCRIPTION_OUTLINED, icon_color="black")
                                 ),
                            ft.Divider(height=1, color=self.dark_white),
                        ]
                    ),
                    ft.Column([
                        ft.Image(src="assets/logo.png", width=40, height=40, border_radius=20)
                    ])
                ]
            )
        )

        self.column_1 = ft.Column(
            expand=3,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.Stack(
            expand=True,
            alignment=ft.alignment.center,
            controls=[
            ft.Container(
            border_radius=15,
            expand=True,
            content=ft.Image(
            src="assets/foto.png",
            fit=ft.ImageFit.COVER,
            height=1000,
            width=1200,
            )
            ),
            ft.Container(expand=True, bgcolor="transparent",
             border_radius=15, padding=10, margin=ft.margin.only(right=30),
             alignment=ft.alignment.top_center,
             content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                ft.Container(height=30, width=160, border_radius=15,
                bgcolor=self.dark_white,
                content=ft.Row(
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                    ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, color="black"),
                    ft.Text(f"Hoy: {datetime.datetime.now().strftime('%d/%m/%Y')}", color="black", size=12)
                    ]
                )),
                ft.Container(height=30, width=220, border_radius=15,
                bgcolor=self.dark_white,
                content=ft.Row(
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                    ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, color="black"),
                    ft.Text(f"Periodo a Pagar: {get_previous_month_spanish()}", color="black", size=12)
                    ]
                )
                ),
                ft.Container(height=30, width=220, border_radius=15,
                bgcolor=self.dark_white,
                content=ft.Row(
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                    ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color="black"),
                    ft.Text(f"Fecha Limite: {get_payment_date()}", color="black", size=12)
                    ]
                )),
             ]
             ))
            ]
            ),
            ft.Row(
            expand=True,
            controls=[
            ft.Container(
            expand=True, bgcolor=self.dark_white,
            border_radius=15, padding=10,
            content=ft.Column(
                spacing=2,
                controls=[
                    ft.Text("Check List IMSS", color=ft.Colors.with_opacity(0.5, "black")),
                    ft.Row(
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Cedulas", weight="bold", color="black", size=12, data="text"),
                        ft.Switch(thumb_color="black", active_track_color="white",
                              value=False, track_outline_color="transparent",
                              inactive_track_color="white", width=40, data="switch"),
                        ft.Text("Confrontas", weight="bold", color="black", size=12, data="text"),
                        ft.Switch(thumb_color="black", active_track_color="white",
                              value=False, track_outline_color="transparent",
                              inactive_track_color="white", width=40, data="switch"),
                        ft.Text("SIPARES", weight="bold", color="black", size=12, data="text"),
                        ft.Switch(thumb_color="black", active_track_color="white",
                              value=False, track_outline_color="transparent",
                              inactive_track_color="white", width=40, data="switch")
                    ]
                    ),
                    ft.Container(
                    alignment=ft.alignment.center,
                    padding=15,
                    content=ft.Image(src="assets/imss.png", width=170, height=170)
                    ),
                    ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                        border_radius=20, width=120, height=40,
                        on_click=self.toggle_color,
                        bgcolor=ft.Colors.with_opacity(0.5, self.grey_color), padding=5,
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                            ft.Icon(name=ft.Icons.FOLDER_ZIP_OUTLINED, color="black", data="icon"),
                            ft.Column(
                                spacing=0,
                                controls=[
                                ft.Text("Descargar", color="black", weight="bold", size=12, data="text"),
                                ft.Text("Emisiones", color=ft.Colors.with_opacity(0.5, "black"), size=10)
                                ]
                            )
                            ]
                        )
                        ),
                        ft.Container(
                        border_radius=20, width=120, height=40,
                        on_click=self.toggle_color,
                        bgcolor=ft.Colors.with_opacity(0.5, self.grey_color), padding=5,
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                            ft.Icon(name=ft.Icons.ACCESSIBLE_FORWARD_OUTLINED, color="black", data="icon"),
                            ft.Column(
                                spacing=0,
                                controls=[
                                ft.Text("Descargar", color="black", weight="bold", size=12, data="text"),
                                ft.Text("Incapacidades", color=ft.Colors.with_opacity(0.5, "black"), size=10)
                                ]
                            )
                            ]
                        )
                        ),
                        ft.Container(
                        border_radius=20, width=120, height=40,
                        on_click=self.toggle_color,
                        bgcolor=ft.Colors.with_opacity(0.5, self.grey_color), padding=5,
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                            ft.Icon(name=ft.Icons.THUMB_UP_ALT_OUTLINED, color="black", data="icon"),
                            ft.Column(
                                spacing=0,
                                controls=[
                                ft.Text("Descargar", color="black", weight="bold", size=12, data="text"),
                                ft.Text("Opiniones", color=ft.Colors.with_opacity(0.5, "black"), size=10)
                                ]
                            )
                            ]
                        )
                        )
                    ]
                    )
                ]
                )
            ),
            ft.Container(
            expand=True, bgcolor=self.grey_color,
            border_radius=15, padding=10,
            content=ft.Column(
                spacing=2,
                controls=[
                    ft.Text("Check List INFONAVIT", color=ft.Colors.with_opacity(0.5, "black")),
                    ft.Row(
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Cedulas", weight="bold", color="black", size=12, data="text"),
                        ft.Switch(thumb_color="black", active_track_color="white",
                              value=False, track_outline_color="transparent",
                              inactive_track_color="white", width=40, data="switch"),
                        ft.Text("Confrontas", weight="bold", color="black", size=12, data="text"),
                        ft.Switch(thumb_color="black", active_track_color="white",
                              value=False, track_outline_color="transparent",
                              inactive_track_color="white", width=40, data="switch"),
                        ft.Text("SIPARES", weight="bold", color="black", size=12, data="text"),
                        ft.Switch(thumb_color="black", active_track_color="white",
                              value=False, track_outline_color="transparent",
                              inactive_track_color="white", width=40, data="switch")
                    ]
                    ),
                    ft.Container(
                    alignment=ft.alignment.center,
                    padding=15,
                    content=ft.Image(src="assets/infonavit.png", width=170, height=170)
                    ),
                    ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                        border_radius=20, width=120, height=40,
                        on_click=self.toggle_color2,
                        bgcolor=ft.Colors.with_opacity(0.5, self.dark_white), padding=5,
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                            ft.Icon(name=ft.Icons.DESCRIPTION_OUTLINED, color="black", data="icon"),
                            ft.Column(
                                spacing=0,
                                controls=[
                                ft.Text("Descargar", color="black", weight="bold", size=12, data="text"),
                                ft.Text("Avisos CSV", color=ft.Colors.with_opacity(0.5, "black"), size=10)
                                ]
                            )
                            ]
                        )
                        ),
                        ft.Container(
                        border_radius=20, width=120, height=40,
                        on_click=self.toggle_color2,
                        bgcolor=ft.Colors.with_opacity(0.5, self.dark_white), padding=5,
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                            ft.Icon(name=ft.Icons.PICTURE_AS_PDF_OUTLINED, color="black", data="icon"),
                            ft.Column(
                                spacing=0,
                                controls=[
                                ft.Text("Descargar", color="black", weight="bold", size=12, data="text"),
                                ft.Text("Avisos PDF", color=ft.Colors.with_opacity(0.5, "black"), size=10)
                                ]
                            )
                            ]
                        )
                        ),
                        ft.Container(
                        border_radius=20, width=120, height=40,
                        on_click=self.toggle_color2,
                        bgcolor=ft.Colors.with_opacity(0.5, self.dark_white), padding=5,
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                            ft.Icon(name=ft.Icons.FOLDER_ZIP_OUTLINED, color="black", data="icon"),
                            ft.Column(
                                spacing=0,
                                controls=[
                                ft.Text("Descargar", color="black", weight="bold", size=12, data="text"),
                                ft.Text("Avisos ZIP", color=ft.Colors.with_opacity(0.5, "black"), size=10)
                                ]
                            )
                            ]
                        )
                        )
                    ]
                    )
                ]
            )
            )
            ]
            )
            ]
        )

        self.column_2 = ft.Column(
            expand=1, spacing=5,
            alignment=ft.MainAxisAlignment.START,
            controls=[
            ft.Container(expand=True, border_radius=15, padding=10,
             height=350, width=300,
             gradient=ft.LinearGradient(
             rotation=math.radians(90),
             colors=[ft.Colors.with_opacity(0.5, self.grey_color), self.dark_white, self.yellow_color]
            ),
            content=ft.Column(
            controls=[
            ft.Text("Consulta de Incapacidades", color=ft.Colors.with_opacity(0.5, "black")),
            ft.Container(
            margin=ft.margin.only(top=-30),
            content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
            ft.Image(src="assets/escritorio_virtual.png", width=80, height=80)
            ]
            )
            ),
            ft.Container(
            margin=ft.margin.only(top=-20),
            content=ft.Column(
            spacing=4,
            controls=[
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
            ft.TextField(
            label="RFC Persona Física",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=False,
            multiline=False,
            max_length=13,
            bgcolor="white",
            focused_bgcolor="white",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            ),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.ElevatedButton(
            text=".cer",
            width=120,
            height=35,
            color="#154f3a",
            bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
            ),
            ft.ElevatedButton(
            text=".key",
            width=120,
            height=35,
            color="#154f3a",
            bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
            )
            ]
            ),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
            ft.TextField(
            label="Contraseña",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=True,
            multiline=False,
            bgcolor="white",
            focused_bgcolor="white",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            ),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
            ft.TextField(
            label="Numero de Seguro Social",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=False,
            multiline=False,
            max_length=11,
            on_change=self.validate_exact_length,
            bgcolor="white",
            focused_bgcolor="white",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            ),
            ft.Container(
            margin=ft.margin.only(top=3),
            content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.ElevatedButton(
            text="Consultar",
            width=120,
            height=35,
            color="#154f3a",
            bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
            ),
            ft.ElevatedButton(
            text="Abrir Carpeta",
            width=120,
            height=35,
            color="#154f3a",
            bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
            )
            ]
            )
            ),
            ft.Container(
            margin=ft.margin.only(left=5, right=5, top=3),
            padding=ft.padding.all(10),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.1, "black"),
            width=280,
            content=ft.Column(
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
            controls=[
            ft.Text("Esperando consulta de incapacidades...", size=12, color=self.grey_color, ref=self.log_incapacidades_ref)
            ]
            )
            )
            ]
            )
            )
            ]
            )
            ),
            ft.Container(
            expand=True, border_radius=15, bgcolor=self.dark_white,
            height=350, width=300, padding=5,
            content=ft.Column(
            spacing=4,
            controls=[
            ft.Text("Consulta de Credito Nuevo Ingreso", color=ft.Colors.with_opacity(0.5, "black")),
            ft.Container(
            margin=ft.margin.only(top=-20),
            content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
            ft.Image(src="assets/portal_infonavit.png", width=80, height=80)
            ]
            )
            ),
            ft.Container(
            margin=ft.margin.only(top=-10),
            content=ft.Column(
            spacing=4,
            controls=[
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
            ft.TextField(
            label="Numero de Registro Patronal",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=False,
            multiline=False,
            max_length=11,
            on_change=self.validate_exact_length,
            bgcolor="transparent",
            focused_bgcolor="transparent",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            ),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.TextField(
            label="Correo Electronico",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=False,
            multiline=False,
            bgcolor="transparent",
            focused_bgcolor="transparent",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            ),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.TextField(
            label="Contraseña",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=True,
            multiline=False,
            bgcolor="transparent",
            focused_bgcolor="transparent",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            ),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.TextField(
            label="Numero de Seguro Social",
            width=250,
            height=35,
            label_style=ft.TextStyle(color="black", size=12),
            border_radius=15,
            password=False,
            multiline=False,
            max_length=11,
            on_change=self.validate_exact_length,
            bgcolor="transparent",
            focused_bgcolor="transparent",
            focused_border_color=self.grey_color,
            border_color=self.grey_color,
            cursor_color=self.grey_color,
            color="black",
            cursor_height=15
            )
            ]
            )
            ]
            )
            ),
            ft.Container(
            margin=ft.margin.only(top=3),
            content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.ElevatedButton(
            text="Consultar",
            width=120,
            height=35,
            color="#1976D2",
            bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
            ),
            ft.ElevatedButton(
            text="Abrir Carpeta",
            width=120,
            height=35,
            color="#1976D2",
            bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
            )
            ]
            )
            ),
            ft.Container(
            margin=ft.margin.only(left=5, right=5, top=3),
            padding=ft.padding.all(10),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.1, "black"),
            width=290,
            content=ft.Column(
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
            controls=[
            ft.Text("Esperando consulta de Credito...", size=12, color=self.grey_color, ref=self.log_ref)
            ]
            )
            )
            ]
            )
            )
            ]
        )

        self.page.add(
            ft.Row(
                expand=True,
                controls=[
                    self.menu,
                    self.column_1,
                    self.column_2
                ]
            )
        )

    def validate_exact_length(self, e, length=11):
        """Validar que el campo tenga exactamente la longitud especificada"""
        if e.control.value and len(e.control.value) != length:
            e.control.error_text = f"Debe tener exactamente {length} dígitos"
        else:
            e.control.error_text = None
        self.page.update()

    def update_log_incapacidades(self, message: str, color: str = None):
        """Método para actualizar el log de incapacidades"""
        if self.log_incapacidades_ref.current:
            self.log_incapacidades_ref.current.value = message
            if color:
                self.log_incapacidades_ref.current.color = color
            else:
                self.log_incapacidades_ref.current.color = "black"
            self.page.update()

    def update_log(self, message: str, color: str = None):
        """Método para actualizar el log de actividades"""
        if self.log_ref.current:
            self.log_ref.current.value = message
            if color:
                self.log_ref.current.color = color
            else:
                self.log_ref.current.color = "black"
            self.page.update()

    def toggle_color(self, e):
        """Método para manejar el evento de clic y cambiar colores"""
        # Cambiar el color de fondo del contenedor
        if e.control.bgcolor == ft.Colors.with_opacity(0.5, self.grey_color):
            e.control.bgcolor = "green"
        else:
            e.control.bgcolor = ft.Colors.with_opacity(0.5, self.grey_color)
        
        # Actualizar la página para reflejar los cambios
        self.page.update()

    def toggle_color2(self, e):
        """Método para manejar el evento de clic y cambiar colores"""
        # Cambiar el color de fondo del contenedor
        if e.control.bgcolor == ft.Colors.with_opacity(0.5, self.dark_white):
            e.control.bgcolor = "green"
        else:
            e.control.bgcolor = ft.Colors.with_opacity(0.5, self.dark_white)
        
        # Actualizar la página para reflejar los cambios
        self.page.update()


def get_previous_month_spanish():
    today = datetime.datetime.now()
    if today.month == 1:
        prev_month = 12
    else:
        prev_month = today.month - 1
    
    months_spanish = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    
    return months_spanish[prev_month]


def get_payment_date():
    today = datetime.datetime.now()
    
    # Empezar con el día 17 del mes actual
    payment_date = datetime.datetime(today.year, today.month, 17)
    
    # Verificar si es fin de semana (5=Sábado, 6=Domingo) o viernes (4)
    while payment_date.weekday() >= 4:  # Viernes, sábado o domingo
        payment_date += datetime.timedelta(days=1)
    
    # Formatear como "17 de Agosto"
    months_spanish = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    
    return f"{payment_date.day} de {months_spanish[payment_date.month]}"

if __name__ == "__main__":
    ft.app(target=HomePage)