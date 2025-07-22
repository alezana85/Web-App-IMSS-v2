import flet as ft

class CheckListsPage(ft.Container):
    def __init__(self, page: ft.Page, navigate_to_home_callback=None, navigate_to_webscrap_callback=None, navigate_to_confrontas_callback=None):
        super().__init__(expand=True)
        self.page = page
        self.navigate_to_home = navigate_to_home_callback
        self.navigate_to_webscrap = navigate_to_webscrap_callback
        self.navigate_to_confrontas = navigate_to_confrontas_callback
        self.page.title = "Check Lists"
        self.bg_color = "#ffffff"
        self.dark_white = "#e7e6e9"
        self.grey_color = "#a9acb6"
        self.yellow_color = "#ece5d5"
        self.page.bgcolor = self.bg_color

        # Estado de las tareas (checkbox states)
        self.task_states = {
            'section1': [False] * 5,
            'section2': [False] * 4,
            'section3': [False] * 6,
            'section4': [False] * 5
        }

        self.content = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self._create_menu(),
                self._create_main_content()
            ]
        )

    def _create_menu(self):
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
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.yellow_color,
                                 content=ft.IconButton(ft.Icons.CHECKLIST_OUTLINED, icon_color="black")
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

    def _create_main_content(self):
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                spacing=20,
                controls=[
                    ft.Text("Listas de Verificación", size=24, weight=ft.FontWeight.BOLD, color="black"),
                    # Una sola fila con los 4 contenedores
                    ft.Row(
                        expand=True,
                        spacing=20,
                        controls=[
                            self._create_checklist_section(
                                title="Actividades IMSS",
                                image_src="assets/imss.png",
                                tasks=[
                                    "Revisar correos electrónicos",
                                    "Actualizar expedientes",
                                    "Generar reportes diarios",
                                    "Atender consultas",
                                    "Revisar pendientes"
                                ],
                                section_key='section1',
                                bg_color=ft.Colors.with_opacity(0.5, self.grey_color)
                            ),
                            self._create_checklist_section(
                                title="Actividades INFONAVIT",
                                image_src="assets/infonavit.png",
                                tasks=[
                                    "Verificar afiliaciones",
                                    "Procesar incapacidades",
                                    "Revisar movimientos",
                                    "Validar documentos"
                                ],
                                section_key='section2',
                                bg_color=self.dark_white
                            ),
                            self._create_checklist_section(
                                title="Actividades ISN",
                                image_src="assets/infonavit.png",
                                tasks=[
                                    "Revisar procesos",
                                    "Verificar cumplimiento",
                                    "Auditar expedientes",
                                    "Validar información",
                                    "Generar métricas",
                                    "Implementar mejoras"
                                ],
                                section_key='section3',
                                bg_color=self.yellow_color
                            ),
                            self._create_checklist_section(
                                title="Actividades FONACOT",
                                image_src="assets/portal_infonavit.png",
                                tasks=[
                                    "Revisar estadísticas",
                                    "Generar reportes mensuales",
                                    "Evaluar rendimiento",
                                    "Planificar mejoras",
                                    "Documentar resultados"
                                ],
                                section_key='section4',
                                bg_color=ft.Colors.with_opacity(0.5, self.grey_color)
                            )
                        ]
                    )
                ]
            )
        )

    def _create_checklist_section(self, title, image_src, tasks, section_key, bg_color):
        def on_checkbox_change(e, task_index):
            self.task_states[section_key][task_index] = e.control.value
            self.page.update()

        return ft.Container(
            expand=True,
            bgcolor=bg_color,
            border_radius=15,
            padding=20,
            content=ft.Column(
                expand=True,
                spacing=15,
                controls=[
                    # Título de la sección
                    ft.Text(
                        title,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    # Imagen
                    ft.Container(
                        height=100,
                        content=ft.Image(
                            src=image_src,
                            width=80,
                            height=80,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        alignment=ft.alignment.center
                    ),
                    
                    # Lista de tareas con checkboxes
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Container(
                                    padding=ft.padding.symmetric(vertical=5, horizontal=10),
                                    bgcolor=ft.Colors.with_opacity(0.3, "white"),
                                    border_radius=8,
                                    content=ft.Row(
                                        controls=[
                                            ft.Checkbox(
                                                value=self.task_states[section_key][i],
                                                on_change=lambda e, idx=i: on_checkbox_change(e, idx),
                                                fill_color=ft.Colors.GREEN_400
                                            ),
                                            ft.Text(
                                                task,
                                                size=12,
                                                color="black",
                                                expand=True,
                                                text_align=ft.TextAlign.LEFT
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.START
                                    )
                                ) for i, task in enumerate(tasks)
                            ]
                        )
                    )
                ]
            )
        )