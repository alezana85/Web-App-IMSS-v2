import flet as ft
import os
import sys
from pathlib import Path

# Agregar el directorio scripts al path para importar las funciones
scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

# Importaciones de los scripts con manejo de errores
try:
    from estructurar_sua_mod import estructurar_1sua_destino, estructurar_varios_suas
    from estructurar_emision_mod import estrucurar_varias_emisiones_destino, estructurar_1emision
    from estructurar_visor import estructurar_visor
    from confronta import sua_vs_emision
except ImportError as e:
    print(f"Error importando módulos: {e}")
    # Definir funciones dummy para evitar errores en tiempo de ejecución
    def estructurar_1sua_destino(*args, **kwargs):
        print("Función estructurar_1sua_destino no disponible")
        return None
    
    def estructurar_varios_suas(*args, **kwargs):
        print("Función estructurar_varios_suas no disponible")
        return None
    
    def estrucurar_varias_emisiones_destino(*args, **kwargs):
        print("Función estrucurar_varias_emisiones_destino no disponible")
        return None
    
    def estructurar_1emision(*args, **kwargs):
        print("Función estructurar_1emision no disponible")
        return None
        
    def estructurar_visor(*args, **kwargs):
        print("Función estructurar_visor no disponible")
        return None
        
    def sua_vs_emision(*args, **kwargs):
        print("Función sua_vs_emision no disponible")
        return None

class ConfrontasPage(ft.Container):
    def __init__(self, page: ft.Page, navigate_to_home_callback=None, navigate_to_checklist_callback=None, navigate_to_webscrap_callback=None):
        super().__init__(expand=True)
        self.page = page
        self.navigate_to_home = navigate_to_home_callback
        self.navigate_to_checklist = navigate_to_checklist_callback
        self.navigate_to_webscrap = navigate_to_webscrap_callback
        self.page.title = "Confrontas"
        
        # Colores del tema (siguiendo el mismo esquema que home.py)
        self.bg_color = "#ffffff"
        self.dark_white = "#e7e6e9"
        self.grey_color = "#a9acb6"
        self.yellow_color = "#ece5d5"
        
        # Estado actual de la opción seleccionada
        self.current_option = "1_sua_vs_n_em"
        
        # Variables para almacenar paths seleccionados
        self.selected_sua_file = None
        self.selected_sua_folder = None
        self.selected_emission_file = None
        self.selected_emissions_folder = None
        self.selected_cedula_file = None
        self.selected_nomina_file = None
        self.selected_output_folder = None
        self.selected_visor_folder = None
        
        # Referencias a elementos
        self.main_content_ref = ft.Ref[ft.Container]()
        self.terminal_ref = ft.Ref[ft.Container]()
        
        # Referencias para las opciones del menú
        self.menu_options = {}
        
        self.content = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self._create_navigation_menu(),
                self._create_main_content()
            ]
        )

    def _create_navigation_menu(self):
        """Crear el menú lateral de navegación"""
        return ft.Container(
            width=60,
            margin=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.HOME, icon_color="black",
                                                     on_click=self.navigate_to_home)
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
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.yellow_color,
                                 content=ft.IconButton(ft.Icons.REQUEST_PAGE_OUTLINED, icon_color="black")
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

    def _create_confrontas_menu(self):
        """Crear el menú de opciones de confrontas"""
        return ft.Container(
            width=220,
            bgcolor=self.bg_color,
            border=ft.border.only(right=ft.BorderSide(1, self.grey_color)),
            content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                # Título del menú
                ft.Container(
                height=50,
                bgcolor=self.grey_color,
                alignment=ft.alignment.center,
                content=ft.Text(
                    "Menu",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER
                )
                ),
                # Opciones del menú
                ft.Container(
                expand=True,
                padding=ft.padding.all(10),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    controls=[
                    self._create_menu_option("📄SUA vs 📁Emision", "1_sua_vs_n_em"),
                    self._create_menu_option("📁SUA vs 📄Emision", "n_sua_vs_1_em"),
                    self._create_menu_option("📁SUA vs 📁Emision", "equal_sua_vs_equal_em"),
                    self._create_menu_option("📄SUA vs 📄Emision", "1_sua_vs_1_em"),
                    self._create_menu_option("📁SUA vs 📁Visor", "1_ced_vs_1_em"),
                    self._create_menu_option("SUA vs Nomina", "sua_vs_nomina"),
                    ]
                )
                )
            ]
            )
        )

    def _create_menu_option(self, text, option_id):
        """Crear una opción del menú"""
        is_selected = self.current_option == option_id
        
        # Crear referencia para esta opción si no existe
        if option_id not in self.menu_options:
            self.menu_options[option_id] = ft.Ref[ft.Container]()
        
        option_container = ft.Container(
            ref=self.menu_options[option_id],
            height=50,
            bgcolor=self.yellow_color if is_selected else "transparent",
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            content=ft.TextButton(
                text=text,
                style=ft.ButtonStyle(
                    color="black",
                    text_style=ft.TextStyle(
                        size=14,
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL
                    )
                ),
                on_click=lambda e, opt=option_id: self._change_option(opt)
            )
        )
        return option_container

    def _create_main_content(self):
        """Crear el contenido principal"""
        return ft.Container(
            expand=True,
            bgcolor=self.bg_color,
            content=ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    self._create_confrontas_menu(),
                    self._create_content_area()
                ]
            )
        )

    def _create_content_area(self):
        """Crear el área de contenido con 2 columnas"""
        return ft.Container(
            ref=self.main_content_ref,
            expand=True,
            bgcolor=self.bg_color,
            content=ft.Row(
                expand=True,
                spacing=20,
                controls=[
                    # Primera columna - Funciones de confronta
                    ft.Container(
                        width=400,
                        expand=False,
                        padding=ft.padding.all(20),
                        content=self._get_content_for_option(self.current_option)
                    ),
                    # Segunda columna - Instrucciones y Terminal
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            spacing=20,
                            controls=[
                                # Área de instrucciones (parte superior)
                                ft.Container(
                                    height=250,
                                    padding=ft.padding.all(20),
                                    content=self._get_instructions_for_option(self.current_option)
                                ),
                                # Área de terminal (parte inferior)
                                self._create_terminal_area()
                            ]
                        )
                    )
                ]
            )
        )

    def _create_terminal_area(self):
        """Crear el área de terminal estática"""
        return ft.Container(
            ref=self.terminal_ref,
            expand=True,
            bgcolor=self.dark_white,
            border_radius=10,
            padding=ft.padding.all(15),
            content=ft.ListView(
                expand=True,
                spacing=5,
                padding=ft.padding.all(10),
                controls=[
                    ft.Text(
                        "Esperando acción...",
                        size=12,
                        color="black",
                        font_family="Consolas"
                    )
                ]
            )
        )

    def _get_content_for_option(self, option):
        """Obtener el contenido según la opción seleccionada"""
        content_map = {
            "1_sua_vs_n_em": self._create_1_sua_vs_n_em_content(),
            "n_sua_vs_1_em": self._create_n_sua_vs_1_em_content(),
            "equal_sua_vs_equal_em": self._create_equal_sua_vs_equal_em_content(),
            "1_sua_vs_1_em": self._create_1_sua_vs_1_em_content(),
            "1_ced_vs_1_em": self._create_1_ced_vs_1_em_content(),
            "sua_vs_nomina": self._create_sua_vs_nomina_content(),
        }
        return content_map.get(option, self._create_default_content())

    def _create_1_sua_vs_n_em_instructions(self):
        """Instrucciones para 1 SUA vs ∞ EM"""
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Indicaciones:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                self._create_instructions_container([
                    "• Selecciona un archivo .SUA individual",
                    "• Selecciona la carpeta que contiene múltiples emisiones",
                    "• Se confrontará el archivo SUA contra todas las emisiones de la carpeta",
                    "• Útil para verificar un registro específico contra múltiples períodos"
                ])
            ]
        )

    def _get_instructions_for_option(self, option):
        """Obtener las instrucciones según la opción seleccionada"""
        instructions_map = {
            "1_sua_vs_n_em": self._create_1_sua_vs_n_em_instructions(),
            "n_sua_vs_1_em": self._create_n_sua_vs_1_em_instructions(),
            "equal_sua_vs_equal_em": self._create_equal_sua_vs_equal_em_instructions(),
            "1_sua_vs_1_em": self._create_1_sua_vs_1_em_instructions(),
            "1_ced_vs_1_em": self._create_1_ced_vs_1_em_instructions(),
            "sua_vs_nomina": self._create_sua_vs_nomina_instructions(),
        }
        return instructions_map.get(option, self._create_default_instructions())

    def _create_button_style(self, is_primary=False):
        """Crear estilo consistente para botones"""
        if is_primary:
            return ft.ButtonStyle(
                bgcolor=ft.Colors.with_opacity(0.8, self.grey_color),
                color="black",
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
            )
        else:
            return ft.ButtonStyle(
                bgcolor=ft.Colors.with_opacity(0.6, self.grey_color),
                color="black",
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
            )

    def _create_instructions_container(self, instructions):
        """Crear contenedor de instrucciones consistente"""
        return ft.Container(
            bgcolor=self.dark_white,
            border_radius=10,
            padding=ft.padding.all(15),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(instruction, size=14, color="black") 
                    for instruction in instructions
                ]
            )
        )

    def _create_1_sua_vs_n_em_content(self):
        """Contenido para 1 SUA vs ∞ EM"""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text(
                    "📄SUA vs 📁Emision",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                # Botones en fila horizontal
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            text="📄 .SUA",
                            width=150,
                            height=50,
                            style=self._create_button_style(True),
                            on_click=self._select_sua_file
                        ),
                        ft.ElevatedButton(
                            text="📁 Emisiones",
                            width=150,
                            height=50,
                            style=self._create_button_style(),
                            on_click=self._select_emissions_folder
                        ),
                    ]
                ),
                # Botón para carpeta de destino
                ft.ElevatedButton(
                    text="📂 Carpeta Destino",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.7, self.grey_color),
                        color="black",
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                    ),
                    on_click=self._select_output_folder
                ),
                # Botón Confrontar
                ft.ElevatedButton(
                    text="⚔️ Confrontar",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=self.yellow_color,
                        color="black",
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=lambda e: self._execute_confronta("1_sua_vs_n_em")
                )
            ]
        )

    def _create_n_sua_vs_1_em_content(self):
        """Contenido para ∞ SUA vs 1 EM"""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text("📁SUA's vs 📄Emision", size=24, weight=ft.FontWeight.BOLD, color="black"),
                # Botones en fila horizontal
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            text="📁 .SUA's",
                            width=150,
                            height=50,
                            style=self._create_button_style(True),
                            on_click=self._select_sua_folder
                        ),
                        ft.ElevatedButton(
                            text="📄 Emisión",
                            width=150,
                            height=50,
                            style=self._create_button_style(),
                            on_click=self._select_emission_file
                        ),
                    ]
                ),
                # Botón para carpeta de destino
                ft.ElevatedButton(
                    text="📂 Carpeta Destino",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.7, self.grey_color),
                        color="black",
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                    ),
                    on_click=self._select_output_folder
                ),
                # Botón Confrontar
                ft.ElevatedButton(
                    text="⚔️ Confrontar",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=self.yellow_color,
                        color="black",
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=lambda e: self._execute_confronta("n_sua_vs_1_em")
                )
            ]
        )

    def _create_n_sua_vs_1_em_instructions(self):
        """Instrucciones para ∞ SUA vs 1 EM"""
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Indicaciones:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                self._create_instructions_container([
                    "• Selecciona la carpeta que contiene múltiples archivos .SUA",
                    "• Selecciona un archivo de emisión específico",
                    "• Se confrontarán todos los SUA's contra la emisión seleccionada",
                    "• Ideal para verificar múltiples registros contra un período específico"
                ])
            ]
        )

    def _create_equal_sua_vs_equal_em_content(self):
        """Contenido para = SUA vs = EM"""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text("📁SUA's vs 📁Emisiones", size=24, weight=ft.FontWeight.BOLD, color="black"),
                # Botones en fila horizontal
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            text="📁 .SUA's",
                            width=150,
                            height=50,
                            style=self._create_button_style(True),
                            on_click=self._select_sua_folder
                        ),
                        ft.ElevatedButton(
                            text="📁 Emisiones",
                            width=150,
                            height=50,
                            style=self._create_button_style(),
                            on_click=self._select_emissions_folder
                        ),
                    ]
                ),
                # Botón para carpeta de destino
                ft.ElevatedButton(
                    text="📂 Carpeta Destino",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.7, self.grey_color),
                        color="black",
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                    ),
                    on_click=self._select_output_folder
                ),
                # Botón Confrontar
                ft.ElevatedButton(
                    text="⚔️ Confrontar",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=self.yellow_color,
                        color="black",
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=lambda e: self._execute_confronta("equal_sua_vs_equal_em")
                )
            ]
        )

    def _create_equal_sua_vs_equal_em_instructions(self):
        """Instrucciones para = SUA vs = EM"""
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Indicaciones:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                self._create_instructions_container([
                    "• Selecciona la carpeta con múltiples archivos .SUA",
                    "• Selecciona la carpeta con múltiples emisiones", 
                    "• Se confrontarán todos los SUA's contra todas las emisiones",
                    "• Procesamiento masivo para análisis completo"
                ])
            ]
        )

    def _create_1_sua_vs_1_em_content(self):
        """Contenido para 1 SUA vs 1 EM"""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text("📄SUA vs 📄Emision", size=24, weight=ft.FontWeight.BOLD, color="black"),
                # Botones en fila horizontal
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            text="📄 .SUA",
                            width=150,
                            height=50,
                            style=self._create_button_style(True),
                            on_click=self._select_sua_file
                        ),
                        ft.ElevatedButton(
                            text="📄 Emisión",
                            width=150,
                            height=50,
                            style=self._create_button_style(),
                            on_click=self._select_emission_file
                        ),
                    ]
                ),
                # Botón para carpeta de destino
                ft.ElevatedButton(
                    text="📂 Carpeta Destino",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.7, self.grey_color),
                        color="black",
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                    ),
                    on_click=self._select_output_folder
                ),
                # Botón Confrontar
                ft.ElevatedButton(
                    text="⚔️ Confrontar",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=self.yellow_color,
                        color="black",
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=lambda e: self._execute_confronta("1_sua_vs_1_em")
                )
            ]
        )

    def _create_1_ced_vs_1_em_content(self):
        """Contenido para 📁SUA vs 📁Visor"""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text("📁SUA vs 📁Visor", size=24, weight=ft.FontWeight.BOLD, color="black"),
                # Botones en fila horizontal
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            text="📁 SUA's",
                            width=150,
                            height=50,
                            style=self._create_button_style(True),
                            on_click=self._select_sua_folder
                        ),
                        ft.ElevatedButton(
                            text="📁 Visor",
                            width=150,
                            height=50,
                            style=self._create_button_style(),
                            on_click=self._select_visor_folder
                        ),
                    ]
                ),
                # Botón para carpeta de destino
                ft.ElevatedButton(
                    text="📂 Carpeta Destino",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.7, self.grey_color),
                        color="black",
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                    ),
                    on_click=self._select_output_folder
                ),
                # Botón Confrontar
                ft.ElevatedButton(
                    text="⚔️ Confrontar",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=self.yellow_color,
                        color="black",
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=lambda e: self._execute_confronta("1_ced_vs_1_em")
                )
            ]
        )

    def _create_sua_vs_nomina_content(self):
        """Contenido para SUA vs Nomina"""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text("SUA vs Nomina", size=24, weight=ft.FontWeight.BOLD, color="black"),
                # Botones en fila horizontal
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.ElevatedButton(
                            text="📄.SUA",
                            width=150,
                            height=50,
                            style=self._create_button_style(True),
                            on_click=self._select_sua_file
                        ),
                        ft.ElevatedButton(
                            text="📄Nómina",
                            width=150,
                            height=50,
                            style=self._create_button_style(),
                            on_click=self._select_nomina_file
                        ),
                    ]
                ),
                # Botón para carpeta de destino
                ft.ElevatedButton(
                    text="📂 Carpeta Destino",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.7, self.grey_color),
                        color="black",
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                    ),
                    on_click=self._select_output_folder
                ),
                # Botón Confrontar
                ft.ElevatedButton(
                    text="⚔️ Confrontar",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=self.yellow_color,
                        color="black",
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=lambda e: self._execute_confronta("sua_vs_nomina")
                )
            ]
        )

    def _create_default_content(self):
        """Contenido por defecto"""
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Text(
                "Selecciona una opción del menú",
                size=18,
                color=self.grey_color
            )
        )

    def _change_option(self, option_id):
        """Cambiar la opción seleccionada"""
        old_option = self.current_option
        self.current_option = option_id
        
        # Actualizar el estilo de la opción anterior (quitarle el highlight)
        if old_option in self.menu_options and self.menu_options[old_option].current:
            self.menu_options[old_option].current.bgcolor = "transparent"
            # Actualizar el estilo del botón anterior
            old_button = self.menu_options[old_option].current.content
            old_button.style = ft.ButtonStyle(
                color="black",
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.NORMAL)
            )
        
        # Actualizar el estilo de la nueva opción seleccionada
        if option_id in self.menu_options and self.menu_options[option_id].current:
            self.menu_options[option_id].current.bgcolor = self.yellow_color
            # Actualizar el estilo del botón seleccionado
            new_button = self.menu_options[option_id].current.content
            new_button.style = ft.ButtonStyle(
                color="black",
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600)
            )
        
        # Actualizar el contenido del área principal
        if self.main_content_ref.current:
            # Actualizar la primera columna (funciones)
            self.main_content_ref.current.content.controls[0].content = self._get_content_for_option(option_id)
            # Actualizar la segunda columna - área de instrucciones
            self.main_content_ref.current.content.controls[1].content.controls[0].content = self._get_instructions_for_option(option_id)
            
        self.page.update()

    def _add_terminal_message(self, message, color="black"):
        """Agregar mensaje al terminal"""
        if self.terminal_ref.current:
            terminal_listview = self.terminal_ref.current.content
            terminal_listview.controls.append(
                ft.Text(
                    message,
                    size=12,
                    color=color,
                    font_family="Consolas"
                )
            )
            # Auto-scroll al final
            terminal_listview.scroll_to(
                offset=-1,
                duration=300
            )
            self.page.update()

    def _clear_terminal(self):
        """Limpiar el terminal"""
        if self.terminal_ref.current:
            terminal_listview = self.terminal_ref.current.content
            terminal_listview.controls.clear()
            terminal_listview.controls.append(
                ft.Text(
                    "Terminal limpia - Esperando acción...",
                    size=12,
                    color="black",
                    font_family="Consolas"
                )
            )
            self.page.update()

    def _execute_confronta(self, confronta_type):
        """Ejecutar la confrontación seleccionada"""
        self._add_terminal_message(f"[INFO] Iniciando confrontación: {confronta_type}", "black")
        
        if confronta_type == "1_sua_vs_n_em":
            self._execute_1_sua_vs_n_em()
        elif confronta_type == "n_sua_vs_1_em":
            self._execute_n_sua_vs_1_em()
        elif confronta_type == "equal_sua_vs_equal_em":
            self._execute_equal_sua_vs_equal_em()
        elif confronta_type == "1_sua_vs_1_em":
            self._execute_1_sua_vs_1_em()
        elif confronta_type == "1_ced_vs_1_em":
            self._execute_1_ced_vs_1_em()
        elif confronta_type == "sua_vs_nomina":
            self._execute_sua_vs_nomina()
        else:
            self._add_terminal_message(f"[ERROR] Tipo de confrontación no reconocido: {confronta_type}", "red")

    def _execute_1_sua_vs_n_em(self):
        """Ejecutar confrontación: 1 SUA vs N Emisiones"""
        try:
            # Verificar que todos los paths estén seleccionados
            if not self.selected_sua_file:
                self._add_terminal_message("[ERROR] No se ha seleccionado archivo .SUA", "red")
                return
            
            if not self.selected_emissions_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de emisiones", "red")
                return
                
            if not self.selected_output_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de destino", "red")
                return
            
            self._add_terminal_message("[INFO] Verificando archivos seleccionados...", "black")
            self._add_terminal_message(f"[INFO] Archivo SUA: {os.path.basename(self.selected_sua_file)}", "black")
            self._add_terminal_message(f"[INFO] Carpeta emisiones: {os.path.basename(self.selected_emissions_folder)}", "black")
            self._add_terminal_message(f"[INFO] Carpeta destino: {os.path.basename(self.selected_output_folder)}", "black")
            
            # Paso 1: Estructurar archivo SUA
            self._add_terminal_message("[INFO] Estructurando archivo .SUA...", "black")
            sua_excel_path = self._estructurar_sua_with_output_folder(self.selected_sua_file, self.selected_output_folder)
            
            if not sua_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivo .SUA", "red")
                return
            
            self._add_terminal_message(f"[SUCCESS] SUA estructurado: {os.path.basename(sua_excel_path)}", "black")
            
            # Paso 2: Estructurar emisiones
            self._add_terminal_message("[INFO] Estructurando archivos de emisión...", "black")
            emision_excel_path = self._estructurar_emisiones_with_output_folder(self.selected_emissions_folder, self.selected_output_folder)
            
            if not emision_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivos de emisión", "red")
                return
                
            self._add_terminal_message(f"[SUCCESS] Emisiones estructuradas: {os.path.basename(emision_excel_path)}", "black")
            
            # Paso 3: Realizar confrontación
            self._add_terminal_message("[INFO] Iniciando confrontación SUA vs Emisión...", "black")
            confronta_result = sua_vs_emision(sua_excel_path, emision_excel_path, self.selected_output_folder)
            
            if confronta_result:
                self._add_terminal_message(f"[SUCCESS] Confrontación completada: {os.path.basename(confronta_result)}", "black")
                self._add_terminal_message("[INFO] Proceso finalizado exitosamente", "green")
            else:
                self._add_terminal_message("[ERROR] Error durante la confrontación", "red")
                
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error inesperado: {str(e)}", "red")

    def _estructurar_sua_with_output_folder(self, sua_path, output_folder):
        """Estructurar archivo SUA guardando en la carpeta de destino"""
        try:
            # Usar la función modificada que acepta carpeta de destino
            result_path = estructurar_1sua_destino(sua_path, output_folder)
            
            if result_path and os.path.exists(result_path):
                return result_path
            return None
            
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error al estructurar SUA: {str(e)}", "red")
            return None

    def _estructurar_emisiones_with_output_folder(self, emissions_folder, output_folder):
        """Estructurar emisiones guardando en la carpeta de destino"""
        try:
            # Usar la función modificada que acepta carpeta de destino
            result_path = estrucurar_varias_emisiones_destino(emissions_folder, output_folder)
            
            if result_path and os.path.exists(result_path):
                return result_path
            return None
            
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error al estructurar emisiones: {str(e)}", "red")
            return None

    def _estructurar_varios_suas_with_output_folder(self, sua_folder, output_folder):
        """Estructurar múltiples archivos SUA guardando en la carpeta de destino"""
        try:
            # Usar la función modificada que acepta carpeta de destino
            result_path = estructurar_varios_suas(sua_folder, output_folder)
            
            if result_path and os.path.exists(result_path):
                return result_path
            return None
            
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error al estructurar múltiples SUA: {str(e)}", "red")
            return None

    def _estructurar_1emision_with_output_folder(self, emision_path, output_folder):
        """Estructurar archivo de emisión individual guardando en la carpeta de destino"""
        try:
            # Usar la función modificada que acepta carpeta de destino
            result_path = estructurar_1emision(emision_path, output_folder)
            
            if result_path and os.path.exists(result_path):
                return result_path
            return None
            
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error al estructurar emisión: {str(e)}", "red")
            return None

    # Funciones placeholder para otros tipos de confrontación
    def _execute_n_sua_vs_1_em(self):
        """Ejecutar confrontación: N SUA vs 1 Emisión"""
        try:
            # Verificar que todos los paths estén seleccionados
            if not self.selected_sua_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de archivos .SUA", "red")
                return
            
            if not self.selected_emission_file:
                self._add_terminal_message("[ERROR] No se ha seleccionado archivo de emisión", "red")
                return
                
            if not self.selected_output_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de destino", "red")
                return
            
            self._add_terminal_message("[INFO] Verificando archivos seleccionados...", "black")
            self._add_terminal_message(f"[INFO] Carpeta SUA: {os.path.basename(self.selected_sua_folder)}", "black")
            self._add_terminal_message(f"[INFO] Archivo emisión: {os.path.basename(self.selected_emission_file)}", "black")
            self._add_terminal_message(f"[INFO] Carpeta destino: {os.path.basename(self.selected_output_folder)}", "black")
            
            # Paso 1: Estructurar carpeta de archivos SUA
            self._add_terminal_message("[INFO] Estructurando archivos .SUA de la carpeta...", "black")
            sua_excel_path = self._estructurar_varios_suas_with_output_folder(self.selected_sua_folder, self.selected_output_folder)
            
            if not sua_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivos .SUA", "red")
                return
            
            self._add_terminal_message(f"[SUCCESS] SUA's estructurados: {os.path.basename(sua_excel_path)}", "black")
            
            # Paso 2: Estructurar archivo de emisión
            self._add_terminal_message("[INFO] Estructurando archivo de emisión...", "black")
            emision_excel_path = self._estructurar_1emision_with_output_folder(self.selected_emission_file, self.selected_output_folder)
            
            if not emision_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivo de emisión", "red")
                return
                
            self._add_terminal_message(f"[SUCCESS] Emisión estructurada: {os.path.basename(emision_excel_path)}", "black")
            
            # Paso 3: Realizar confrontación
            self._add_terminal_message("[INFO] Iniciando confrontación SUA vs Emisión...", "black")
            confronta_result = sua_vs_emision(sua_excel_path, emision_excel_path, self.selected_output_folder)
            
            if confronta_result:
                self._add_terminal_message(f"[SUCCESS] Confrontación completada: {os.path.basename(confronta_result)}", "black")
                self._add_terminal_message("[INFO] Proceso finalizado exitosamente", "green")
            else:
                self._add_terminal_message("[ERROR] Error durante la confrontación", "red")
                
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error inesperado: {str(e)}", "red")

    def _execute_equal_sua_vs_equal_em(self):
        """Ejecutar confrontación: N SUA vs N Emisión"""
        try:
            # Verificar que todos los paths estén seleccionados
            if not self.selected_sua_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de archivos .SUA", "red")
                return
            
            if not self.selected_emissions_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de emisiones", "red")
                return
                
            if not self.selected_output_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de destino", "red")
                return
            
            self._add_terminal_message("[INFO] Verificando archivos seleccionados...", "black")
            self._add_terminal_message(f"[INFO] Carpeta SUA: {os.path.basename(self.selected_sua_folder)}", "black")
            self._add_terminal_message(f"[INFO] Carpeta emisiones: {os.path.basename(self.selected_emissions_folder)}", "black")
            self._add_terminal_message(f"[INFO] Carpeta destino: {os.path.basename(self.selected_output_folder)}", "black")
            
            # Paso 1: Estructurar carpeta de archivos SUA
            self._add_terminal_message("[INFO] Estructurando archivos .SUA de la carpeta...", "black")
            sua_excel_path = self._estructurar_varios_suas_with_output_folder(self.selected_sua_folder, self.selected_output_folder)
            
            if not sua_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivos .SUA", "red")
                return
            
            self._add_terminal_message(f"[SUCCESS] SUA's estructurados: {os.path.basename(sua_excel_path)}", "black")
            
            # Paso 2: Estructurar carpeta de emisiones
            self._add_terminal_message("[INFO] Estructurando archivos de emisión de la carpeta...", "black")
            emision_excel_path = self._estructurar_emisiones_with_output_folder(self.selected_emissions_folder, self.selected_output_folder)
            
            if not emision_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivos de emisión", "red")
                return
                
            self._add_terminal_message(f"[SUCCESS] Emisiones estructuradas: {os.path.basename(emision_excel_path)}", "black")
            
            # Paso 3: Realizar confrontación
            self._add_terminal_message("[INFO] Iniciando confrontación SUA vs Emisión...", "black")
            confronta_result = sua_vs_emision(sua_excel_path, emision_excel_path, self.selected_output_folder)
            
            if confronta_result:
                self._add_terminal_message(f"[SUCCESS] Confrontación completada: {os.path.basename(confronta_result)}", "black")
                self._add_terminal_message("[INFO] Proceso finalizado exitosamente", "green")
            else:
                self._add_terminal_message("[ERROR] Error durante la confrontación", "red")
                
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error inesperado: {str(e)}", "red")

    def _execute_1_sua_vs_1_em(self):
        """Ejecutar confrontación: 1 SUA vs 1 Emisión"""
        try:
            # Verificar que todos los paths estén seleccionados
            if not self.selected_sua_file:
                self._add_terminal_message("[ERROR] No se ha seleccionado archivo .SUA", "red")
                return
            
            if not self.selected_emission_file:
                self._add_terminal_message("[ERROR] No se ha seleccionado archivo de emisión", "red")
                return
                
            if not self.selected_output_folder:
                self._add_terminal_message("[ERROR] No se ha seleccionado carpeta de destino", "red")
                return
            
            self._add_terminal_message("[INFO] Verificando archivos seleccionados...", "black")
            self._add_terminal_message(f"[INFO] Archivo SUA: {os.path.basename(self.selected_sua_file)}", "black")
            self._add_terminal_message(f"[INFO] Archivo emisión: {os.path.basename(self.selected_emission_file)}", "black")
            self._add_terminal_message(f"[INFO] Carpeta destino: {os.path.basename(self.selected_output_folder)}", "black")
            
            # Paso 1: Estructurar archivo SUA
            self._add_terminal_message("[INFO] Estructurando archivo .SUA...", "black")
            sua_excel_path = self._estructurar_sua_with_output_folder(self.selected_sua_file, self.selected_output_folder)
            
            if not sua_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivo .SUA", "red")
                return
            
            self._add_terminal_message(f"[SUCCESS] SUA estructurado: {os.path.basename(sua_excel_path)}", "black")
            
            # Paso 2: Estructurar archivo de emisión
            self._add_terminal_message("[INFO] Estructurando archivo de emisión...", "black")
            emision_excel_path = self._estructurar_1emision_with_output_folder(self.selected_emission_file, self.selected_output_folder)
            
            if not emision_excel_path:
                self._add_terminal_message("[ERROR] Error al estructurar archivo de emisión", "red")
                return
                
            self._add_terminal_message(f"[SUCCESS] Emisión estructurada: {os.path.basename(emision_excel_path)}", "black")
            
            # Paso 3: Realizar confrontación
            self._add_terminal_message("[INFO] Iniciando confrontación SUA vs Emisión...", "black")
            confronta_result = sua_vs_emision(sua_excel_path, emision_excel_path, self.selected_output_folder)
            
            if confronta_result:
                self._add_terminal_message(f"[SUCCESS] Confrontación completada: {os.path.basename(confronta_result)}", "black")
                self._add_terminal_message("[INFO] Proceso finalizado exitosamente", "green")
            else:
                self._add_terminal_message("[ERROR] Error durante la confrontación", "red")
                
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error inesperado: {str(e)}", "red")

    def _execute_1_ced_vs_1_em(self):
        """Ejecutar confrontación: 📁SUA vs 📁Visor"""
        try:
            if not self.selected_sua_folder:
                self._add_terminal_message("[ERROR] Por favor selecciona la carpeta de SUA's", "red")
                return
            
            if not self.selected_visor_folder:
                self._add_terminal_message("[ERROR] Por favor selecciona la carpeta del Visor", "red")
                return
                
            if not self.selected_output_folder:
                self._add_terminal_message("[ERROR] Por favor selecciona la carpeta de destino", "red")
                return
            
            self._add_terminal_message("[INFO] Iniciando proceso SUA vs Visor...", "blue")
            
            # Paso 1: Estructurar varios SUA's
            self._add_terminal_message("[INFO] Paso 1/3: Estructurando archivos SUA...", "blue")
            sua_result = estructurar_varios_suas(self.selected_sua_folder, self.selected_output_folder)
            
            if sua_result:
                self._add_terminal_message(f"[SUCCESS] Archivo SUA estructurado: {sua_result}", "green")
            else:
                self._add_terminal_message("[ERROR] Error al estructurar archivos SUA", "red")
                return
            
            # Paso 2: Estructurar Visor
            self._add_terminal_message("[INFO] Paso 2/3: Estructurando archivos del Visor...", "blue")
            visor_result = estructurar_visor(self.selected_visor_folder)
            
            if visor_result:
                self._add_terminal_message(f"[SUCCESS] Archivo Visor estructurado: {visor_result}", "green")
                
                # Mover el archivo del visor a la carpeta de destino si no está allí
                import shutil
                visor_filename = os.path.basename(visor_result)
                visor_destino = os.path.join(self.selected_output_folder, visor_filename)
                
                if visor_result != visor_destino:
                    shutil.copy2(visor_result, visor_destino)
                    self._add_terminal_message(f"[INFO] Archivo Visor copiado a: {visor_destino}", "blue")
                    visor_result = visor_destino
                
            else:
                self._add_terminal_message("[ERROR] Error al estructurar archivos del Visor", "red")
                return
            
            # Paso 3: Ejecutar confrontación SUA vs Emisión (Visor)
            self._add_terminal_message("[INFO] Paso 3/3: Ejecutando confrontación...", "blue")
            confronta_result = sua_vs_emision(sua_result, visor_result, self.selected_output_folder)
            
            if confronta_result:
                self._add_terminal_message(f"[SUCCESS] Confrontación completada: {confronta_result}", "green")
                self._add_terminal_message("[SUCCESS] ¡Proceso SUA vs Visor completado exitosamente!", "green")
                self._add_terminal_message(f"[INFO] Archivos generados en: {self.selected_output_folder}", "blue")
            else:
                self._add_terminal_message("[ERROR] Error durante la confrontación", "red")
                
        except Exception as e:
            self._add_terminal_message(f"[ERROR] Error inesperado: {str(e)}", "red")

    def _execute_sua_vs_nomina(self):
        """Ejecutar confrontación: SUA vs Nómina"""
        self._add_terminal_message("[WARNING] Función en desarrollo - SUA vs Nómina", self.grey_color)

    # Funciones de callback para los botones (placeholders)
    def _select_sua_file(self, e):
        print("Seleccionar archivo .SUA")
        self._add_terminal_message("[INFO] Abriendo selector de archivo .SUA...", "black")
        
        # Crear FilePicker para archivos .SUA
        file_picker = ft.FilePicker(
            on_result=self._on_sua_file_selected
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abrir el selector con filtro para archivos .SUA
        file_picker.pick_files(
            dialog_title="Seleccionar archivo .SUA",
            allowed_extensions=["SUA"],
            allow_multiple=False
        )

    def _on_sua_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_sua_file = e.files[0].path
            filename = os.path.basename(self.selected_sua_file)
            self._add_terminal_message(f"[SUCCESS] Archivo .SUA seleccionado: {filename}", "black")
        else:
            self._add_terminal_message("[WARNING] No se seleccionó archivo .SUA", self.grey_color)
        self._add_terminal_message("[SUCCESS] Archivo .SUA seleccionado correctamente", "black")

    def _select_sua_folder(self, e):
        print("Seleccionar carpeta de .SUA's")
        self._add_terminal_message("[INFO] Abriendo selector de carpeta .SUA...", "black")
        
        # Crear DirectoryPicker para carpetas con archivos .SUA
        directory_picker = ft.FilePicker(
            on_result=self._on_sua_folder_selected
        )
        self.page.overlay.append(directory_picker)
        self.page.update()
        
        # Abrir el selector de carpeta
        directory_picker.get_directory_path(
            dialog_title="Seleccionar carpeta con archivos .SUA"
        )

    def _on_sua_folder_selected(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.selected_sua_folder = e.path
            folder_name = os.path.basename(self.selected_sua_folder)
            self._add_terminal_message(f"[SUCCESS] Carpeta .SUA seleccionada: {folder_name}", "black")
        else:
            self._add_terminal_message("[WARNING] No se seleccionó carpeta .SUA", self.grey_color)

    def _select_emission_file(self, e):
        print("Seleccionar archivo de emisión")
        self._add_terminal_message("[INFO] Abriendo selector de archivo de emisión...", "black")
        
        # Crear FilePicker para archivos de emisión (.xls)
        file_picker = ft.FilePicker(
            on_result=self._on_emission_file_selected
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abrir el selector con filtro para archivos .xls
        file_picker.pick_files(
            dialog_title="Seleccionar archivo de emisión",
            allowed_extensions=["xls"],
            allow_multiple=False
        )

    def _on_emission_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_emission_file = e.files[0].path
            filename = os.path.basename(self.selected_emission_file)
            self._add_terminal_message(f"[SUCCESS] Archivo de emisión seleccionado: {filename}", "black")
        else:
            self._add_terminal_message("[WARNING] No se seleccionó archivo de emisión", self.grey_color)

    def _select_emissions_folder(self, e):
        print("Seleccionar carpeta de emisiones")
        self._add_terminal_message("[INFO] Abriendo selector de carpeta de emisiones...", "black")
        
        # Crear DirectoryPicker para carpetas con archivos de emisión
        directory_picker = ft.FilePicker(
            on_result=self._on_emissions_folder_selected
        )
        self.page.overlay.append(directory_picker)
        self.page.update()
        
        # Abrir el selector de carpeta
        directory_picker.get_directory_path(
            dialog_title="Seleccionar carpeta con archivos de emisión"
        )

    def _on_emissions_folder_selected(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.selected_emissions_folder = e.path
            folder_name = os.path.basename(self.selected_emissions_folder)
            self._add_terminal_message(f"[SUCCESS] Carpeta de emisiones seleccionada: {folder_name}", "black")
        else:
            self._add_terminal_message("[WARNING] No se seleccionó carpeta de emisiones", self.grey_color)

    def _select_cedula_file(self, e):
        print("Seleccionar archivo de cédula")
        self._add_terminal_message("[INFO] Seleccionando archivo de cédula...", "black")
        # Aquí irá la lógica para seleccionar archivo de cédula
        self._add_terminal_message("[SUCCESS] Archivo de cédula seleccionado correctamente", "black")

    def _select_nomina_file(self, e):
        print("Seleccionar archivo de nómina")
        self._add_terminal_message("[INFO] Seleccionando archivo de nómina...", "black")
        # Aquí irá la lógica para seleccionar archivo de nómina
        self._add_terminal_message("[SUCCESS] Archivo de nómina seleccionado correctamente", "black")

    def _select_visor_folder(self, e):
        print("Seleccionar carpeta del Visor")
        self._add_terminal_message("[INFO] Abriendo selector de carpeta del Visor...", "black")
        
        # Crear DirectoryPicker para carpetas con archivos del Visor
        directory_picker = ft.FilePicker(
            on_result=self._on_visor_folder_selected
        )
        self.page.overlay.append(directory_picker)
        self.page.update()
        
        # Abrir el selector de carpeta
        directory_picker.get_directory_path(
            dialog_title="Seleccionar carpeta con archivos del Visor"
        )

    def _on_visor_folder_selected(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.selected_visor_folder = e.path
            folder_name = os.path.basename(self.selected_visor_folder)
            self._add_terminal_message(f"[SUCCESS] Carpeta del Visor seleccionada: {folder_name}", "black")
        else:
            self._add_terminal_message("[WARNING] No se seleccionó carpeta del Visor", self.grey_color)

    def _select_output_folder(self, e):
        print("Seleccionar carpeta destino")
        self._add_terminal_message("[INFO] Abriendo selector de carpeta de destino...", "black")
        
        # Crear DirectoryPicker para la carpeta de destino
        directory_picker = ft.FilePicker(
            on_result=self._on_output_folder_selected
        )
        self.page.overlay.append(directory_picker)
        self.page.update()
        
        # Abrir el selector de carpeta
        directory_picker.get_directory_path(
            dialog_title="Seleccionar carpeta de destino"
        )

    def _on_output_folder_selected(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.selected_output_folder = e.path
            folder_name = os.path.basename(self.selected_output_folder)
            self._add_terminal_message(f"[SUCCESS] Carpeta de destino seleccionada: {folder_name}", "black")
        else:
            self._add_terminal_message("[WARNING] No se seleccionó carpeta de destino", self.grey_color)

    def _create_1_sua_vs_1_em_instructions(self):
        """Instrucciones para 1 SUA vs 1 EM"""
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Indicaciones:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                self._create_instructions_container([
                    "• Selecciona un archivo .SUA específico",
                    "• Selecciona un archivo de emisión específico",
                    "• Confrontación individual y detallada",
                    "• Ideal para verificaciones puntuales"
                ])
            ]
        )

    def _create_1_ced_vs_1_em_instructions(self):
        """Instrucciones para 📁SUA vs 📁Visor"""
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Indicaciones:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                self._create_instructions_container([
                    "• Selecciona la carpeta que contiene archivos .SUA",
                    "• Selecciona la carpeta que contiene archivos del Visor",
                    "• Selecciona la carpeta donde guardar los resultados",
                    "• Se generarán 3 archivos: MULTI_SUA, VISOR_EMISION y CONFRONTA",
                    "• Proceso completo: estructuración + confrontación automática"
                ])
            ]
        )

    def _create_sua_vs_nomina_instructions(self):
        """Instrucciones para SUA vs Nomina"""
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Indicaciones:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black"
                ),
                self._create_instructions_container([
                    "• Selecciona un archivo .SUA",
                    "• Selecciona el archivo de nómina correspondiente",
                    "• Confrontación entre datos del SUA y nómina",
                    "• Verificación de consistencia salarial"
                ])
            ]
        )

    def _create_default_instructions(self):
        """Instrucciones por defecto"""
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Text(
                "Selecciona una opción del menú para ver las instrucciones",
                size=16,
                color=self.grey_color
            )
        )
