import flet as ft
import asyncio
import random
import time

class WebScrapPage(ft.Container):
    def __init__(self, page: ft.Page, navigate_to_home_callback=None, navigate_to_checklist_callback=None, navigate_to_confrontas_callback=None):
        super().__init__(expand=True)
        self.page = page
        self.navigate_to_home = navigate_to_home_callback
        self.navigate_to_checklist = navigate_to_checklist_callback
        self.navigate_to_confrontas = navigate_to_confrontas_callback
        self.page.title = "WebScrap Tool"
        self.bg_color = "#ffffff"
        self.dark_white = "#e7e6e9"
        self.grey_color = "#a9acb6"
        self.yellow_color = "#ece5d5"
        
        # Estados de la conversación
        self.current_step = 0
        self.user_responses = []
        
        # Tipos de animaciones para diferentes respuestas
        self.animation_types = [
            "typewriter",  # Animación máquina de escribir tradicional
            "bounce",      # Texto que aparece rebotando letra por letra
            "wave",        # Texto que aparece como onda
            "zoom",        # Texto que aparece con zoom in
            "slide"        # Texto que desliza desde un lado
        ]
        self.current_animation = 0
        
        # Gradientes dinámicos
        self.gradients = [
            ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#667eea", "#764ba2"]
            ),
            ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#f093fb", "#f5576c"]
            ),
            ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#4facfe", "#00f2fe"]
            ),
            ft.LinearGradient(
                begin=ft.alignment.top_right,
                end=ft.alignment.bottom_left,
                colors=["#43e97b", "#38f9d7"]
            ),
            ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#fa709a", "#fee140"]
            )
        ]
        self.current_gradient_index = 0
        
        # Referencias a los elementos
        self.text_display = ft.Ref[ft.Text]()
        self.text_input = ft.Ref[ft.TextField]()
        self.main_container = ft.Ref[ft.Container]()
        self.emoji_container = ft.Ref[ft.Container]()
        
        self.content = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self._create_menu(),
                self._create_main_content()
            ]
        )
        
        # Iniciar animaciones
        self._start_background_animation()
        self._start_typing_animation()

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
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.dark_white,
                                 content=ft.IconButton(ft.Icons.CHECKLIST_OUTLINED, icon_color="black",
                                                     on_click=self.navigate_to_checklist)
                                 ),
                            ft.Divider(height=1, color=self.dark_white),
                            ft.Container(width=40, height=40, border_radius=10, bgcolor=self.yellow_color,
                                 content=ft.IconButton(ft.Icons.CLEANING_SERVICES_OUTLINED, icon_color="black")
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
            ref=self.main_container,
            expand=True,
            gradient=self.gradients[0],
            animate=ft.Animation(2000, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Stack(
                expand=True,
                controls=[
                    # Contenedor para emojis de fiesta que ocupa todo el espacio (en el fondo)
                    ft.Container(
                        ref=self.emoji_container,
                        expand=True,
                        content=ft.Stack(controls=[])
                    ),
                    # Contenido principal (en primer plano para que sea clickeable)
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=40,  # Reduje el spacing para dar más espacio al texto
                            controls=[
                                # Primera fila - Texto dinámico
                                ft.Container(
                                    width=900,
                                    height=200,  # Aumenté la altura para acomodar más texto
                                    alignment=ft.alignment.center,
                                    content=ft.Text(
                                        ref=self.text_display,
                                        value="",
                                        size=28,
                                        color="white",
                                        weight=ft.FontWeight.W_900,
                                        text_align=ft.TextAlign.CENTER,
                                        font_family="Courier New",  # Fuente más arcade/retro
                                        style=ft.TextStyle(
                                            shadow=ft.BoxShadow(
                                                spread_radius=2,
                                                blur_radius=15,
                                                color=ft.Colors.BLACK38,
                                                offset=ft.Offset(3, 3)
                                            ),
                                            letter_spacing=1.5  # Espaciado entre letras para efecto retro
                                        ),
                                        max_lines=5,  # Permitir hasta 5 líneas de texto
                                        overflow=ft.TextOverflow.VISIBLE  # Permitir que el texto sea visible aunque se desborde
                                    )
                                ),
                                # Segunda fila - Campo de texto
                                ft.Container(
                                    width=600,
                                    alignment=ft.alignment.center,
                                    margin=ft.margin.only(top=30),  # Agregar margen superior para separar del texto
                                    content=ft.TextField(
                                        ref=self.text_input,
                                        hint_text=">>> Escribe tu respuesta aquí...",
                                        hint_style=ft.TextStyle(
                                            color="white60", 
                                            font_family="Courier New",
                                            letter_spacing=1.2
                                        ),
                                        text_style=ft.TextStyle(
                                            color="white", 
                                            size=20, 
                                            font_family="Courier New",
                                            weight=ft.FontWeight.W_700,
                                            letter_spacing=1.5
                                        ),
                                        border_color="white70",
                                        focused_border_color="white",
                                        cursor_color="white",
                                        bgcolor=ft.Colors.with_opacity(0.2, "black"),
                                        border_radius=10,
                                        text_align=ft.TextAlign.LEFT,
                                        on_submit=self._on_text_submit,
                                        multiline=False,
                                        text_size=20,
                                        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                        border_width=2,
                                        focused_border_width=3,
                                        autofocus=False,
                                        can_reveal_password=False,
                                        enable_suggestions=True,
                                        keyboard_type=ft.KeyboardType.TEXT
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def _start_background_animation(self):
        """Inicia la animación del fondo que cambia gradientes"""
        def change_gradient():
            try:
                if self.main_container.current and self.page:
                    self.current_gradient_index = (self.current_gradient_index + 1) % len(self.gradients)
                    self.main_container.current.gradient = self.gradients[self.current_gradient_index]
                    self.page.update()
            except Exception:
                # Si hay error, terminar el hilo silenciosamente
                return False
            return True
        
        # Cambiar gradiente cada 3 segundos
        import threading
        def gradient_loop():
            while True:
                time.sleep(3)
                if not change_gradient():
                    break  # Terminar el hilo si hay error
        
        self._gradient_thread = threading.Thread(target=gradient_loop, daemon=True)
        self._gradient_thread.start()

    def _start_typing_animation(self):
        """Inicia la animación de texto tipo máquina de escribir"""
        initial_text = "¿Es la primera vez que usas esta herramienta de WebScrap?"
        
        def type_text():
            try:
                if self.text_display.current and self.page:
                    for i in range(len(initial_text) + 1):
                        if self.text_display.current and self.page:
                            self.text_display.current.value = initial_text[:i]
                            self.page.update()
                            time.sleep(0.06)  # Velocidad inicial más lenta para dramatismo
                        else:
                            break
            except Exception:
                pass  # Ignorar errores silenciosamente
        
        import threading
        thread = threading.Thread(target=type_text, daemon=True)
        thread.start()

    def _on_text_submit(self, e):
        """Maneja el envío de texto y cambia al siguiente paso"""
        user_input = e.control.value.strip().lower()
        self.user_responses.append(user_input)
        e.control.value = ""  # Limpiar el campo
        
        if self.current_step == 0:
            self._handle_first_response(user_input)
        elif self.current_step == 1:
            self._handle_second_response(user_input)
        elif self.current_step == 2:
            self._handle_third_response(user_input)
        
        self.page.update()

    def _handle_first_response(self, user_input):
        """Maneja la primera respuesta del usuario"""
        if "si" in user_input or "sí" in user_input or "yes" in user_input:
            self.current_step = 1
            self._show_celebration_and_next_text(
                "¡Muy bien! Te enseñaré a usar esta potente herramienta de WebScrap para hacer tu trabajo más rápido y eficiente 🚀",
                next_text="Primero hay que configurar nuestros accesos a los portales del IMSS 🏥, al portal del INFONAVIT, y al ESCRITORIO VIRTUAL.. Estas listo?"
            )
        else:
            self.current_step = 1
            self._show_celebration_and_next_text(
                "¡Perfecto! Entonces ya tienes experiencia. Vamos a optimizar aún más tu flujo de trabajo ⚡",
                next_text="¿Qué proceso te gustaría automatizar hoy? 💻"
            )

    def _handle_second_response(self, user_input):
        """Maneja la segunda respuesta del usuario"""
        if "emision" in user_input or "emision" in user_input:
            self.current_step = 2
            self._type_new_text("¡Excelente elección! Las emisiones son fundamentales. Configuremos el bot para descargarlas automáticamente 📄✨")
        elif "opinion" in user_input or "cumplimiento" in user_input:
            self.current_step = 2
            self._type_new_text("¡Perfecto! Las opiniones de cumplimiento son cruciales. Vamos a automatizar su descarga 📊💼")
        else:
            self.current_step = 2
            self._type_new_text("Interesante... Cuéntame más detalles sobre lo que necesitas automatizar 🔍")

    def _handle_third_response(self, user_input):
        """Maneja la tercera respuesta del usuario"""
        self._type_new_text("¡Entendido! Iniciando configuración del WebScrap Bot... 🤖⚙️")
        # Aquí puedes agregar más lógica según las necesidades

    def _show_celebration_and_next_text(self, celebration_text, next_text):
        """Muestra celebración con emojis y luego el siguiente texto"""
        # Primero mostrar el texto de celebración
        self._type_new_text(celebration_text, size=32, weight=ft.FontWeight.W_900)
        
        # Después de 3 segundos, mostrar emojis de fiesta
        def show_celebration():
            time.sleep(3)
            self._show_party_emojis()
            time.sleep(2)
            self._type_new_text(next_text, size=24, weight=ft.FontWeight.BOLD)
        
        import threading
        thread = threading.Thread(target=show_celebration, daemon=True)
        thread.start()

    def _show_party_emojis(self):
        """Muestra emojis de fiesta aleatoriamente en todo el contenedor"""
        party_emojis = ["🎉", "🎊", "🥳", "🎈", "✨", "🎆", "🎇", "🌟", "💫", "🎁", "🔥", "⚡", "🌈", "🦄", "💎"]
        
        if self.emoji_container.current:
            emoji_controls = []
            
            # Obtener dimensiones estimadas del contenedor (ajustar según la ventana)
            container_width = 1200  # Ancho estimado del contenedor principal
            container_height = 600  # Alto estimado del contenedor principal
            
            # Crear más emojis distribuidos en todo el contenedor
            for _ in range(25):  # Más emojis para mejor efecto
                # Posiciones aleatorias en todo el contenedor
                left_pos = random.randint(50, container_width - 100)
                top_pos = random.randint(50, container_height - 100)
                
                # Dar prioridad a las posiciones de abajo y los lados
                if random.random() < 0.6:  # 60% de probabilidad de aparecer en la parte inferior
                    top_pos = random.randint(container_height // 2, container_height - 80)
                
                emoji = ft.Text(
                    value=random.choice(party_emojis),
                    size=random.randint(24, 50),
                    left=left_pos,
                    top=top_pos,
                    animate_opacity=ft.Animation(1200, ft.AnimationCurve.EASE_OUT),
                    animate_scale=ft.Animation(1200, ft.AnimationCurve.BOUNCE_OUT),
                    animate_rotation=ft.Animation(1200, ft.AnimationCurve.EASE_IN_OUT),
                    opacity=1,
                    scale=1,
                    rotate=random.uniform(-0.2, 0.2)  # Rotación ligera para más dinamismo
                )
                emoji_controls.append(emoji)
            
            # Agregar algunos emojis específicamente en las esquinas y bordes
            corner_positions = [
                (50, 50), (container_width - 100, 50),  # Esquinas superiores
                (50, container_height - 100), (container_width - 100, container_height - 100),  # Esquinas inferiores
                (container_width // 4, container_height - 80),  # Parte inferior central-izquierda
                (3 * container_width // 4, container_height - 80),  # Parte inferior central-derecha
                (100, container_height // 2),  # Lado izquierdo
                (container_width - 150, container_height // 2)  # Lado derecho
            ]
            
            for pos in corner_positions:
                emoji = ft.Text(
                    value=random.choice(party_emojis),
                    size=random.randint(30, 45),
                    left=pos[0],
                    top=pos[1],
                    animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_OUT),
                    animate_scale=ft.Animation(1500, ft.AnimationCurve.BOUNCE_OUT),
                    opacity=1,
                    scale=1
                )
                emoji_controls.append(emoji)
            
            self.emoji_container.current.content = ft.Stack(controls=emoji_controls)
            self.page.update()
            
            # Desvanecer emojis después de 2 segundos
            def fade_emojis():
                time.sleep(2)
                for emoji in emoji_controls:
                    emoji.opacity = 0
                    emoji.scale = 0.2
                    emoji.rotate = random.uniform(-1, 1)  # Rotación al desvanecerse
                self.page.update()
                time.sleep(1.2)
                self.emoji_container.current.content = ft.Stack(controls=[])
                self.page.update()
            
            import threading
            thread = threading.Thread(target=fade_emojis, daemon=True)
            thread.start()

    def _type_new_text(self, text, size=28, weight=ft.FontWeight.W_700):
        """Escribe nuevo texto con diferentes animaciones según el step"""
        # Cambiar al siguiente tipo de animación
        self.current_animation = (self.current_animation + 1) % len(self.animation_types)
        animation_type = self.animation_types[self.current_animation]
        
        def animated_text():
            try:
                if self.text_display.current and self.page:
                    # Limpiar texto actual
                    self.text_display.current.value = ""
                    self.text_display.current.size = size
                    self.text_display.current.weight = weight
                    self.text_display.current.font_family = "Courier New"
                    self.page.update()
                    
                    if animation_type == "typewriter":
                        self._typewriter_animation(text)
                    elif animation_type == "bounce":
                        self._bounce_animation(text)
                    elif animation_type == "wave":
                        self._wave_animation(text)
                    elif animation_type == "zoom":
                        self._zoom_animation(text)
                    elif animation_type == "slide":
                        self._slide_animation(text)
            except Exception:
                pass  # Ignorar errores silenciosamente
        
        import threading
        thread = threading.Thread(target=animated_text, daemon=True)
        thread.start()

    def _typewriter_animation(self, text):
        """Animación clásica de máquina de escribir"""
        for i in range(len(text) + 1):
            if self.text_display.current and self.page:
                self.text_display.current.value = text[:i]
                if i < len(text) and text[i] in '.,!?':
                    self.text_display.current.value += "|"  # Cursor parpadeante en puntuación
                    self.page.update()
                    time.sleep(0.1)
                    self.text_display.current.value = text[:i]
                self.page.update()
                time.sleep(0.04)
            else:
                break

    def _bounce_animation(self, text):
        """Animación donde cada palabra aparece rebotando"""
        words = text.split(' ')
        current_text = ""
        
        for word_idx, word in enumerate(words):
            if self.text_display.current and self.page:
                # Agregar la palabra completa de una vez
                current_text += word
                
                # Efecto de rebote con la palabra completa
                self.text_display.current.value = current_text + " ⭐"
                self.page.update()
                time.sleep(0.15)
                
                self.text_display.current.value = current_text + " ✨"
                self.page.update()
                time.sleep(0.15)
                
                self.text_display.current.value = current_text + " 🎯"
                self.page.update()
                time.sleep(0.15)
                
                # Mostrar palabra final sin efecto
                self.text_display.current.value = current_text
                self.page.update()
                time.sleep(0.2)
                
                # Agregar espacio para la siguiente palabra (excepto en la última)
                if word_idx < len(words) - 1:
                    current_text += " "
                    self.text_display.current.value = current_text
                    self.page.update()
            else:
                break

    def _wave_animation(self, text):
        """Animación de onda - las letras aparecen en grupos"""
        wave_size = 3  # Tamaño de cada onda
        for i in range(0, len(text), wave_size):
            if self.text_display.current and self.page:
                segment = text[i:i+wave_size]
                current_value = text[:i]
                
                # Mostrar el segmento apareciendo gradualmente
                for j in range(len(segment)):
                    current_value += segment[j]
                    self.text_display.current.value = current_value + "🌊"
                    self.page.update()
                    time.sleep(0.03)
                
                self.text_display.current.value = current_value
                self.page.update()
                time.sleep(0.05)
            else:
                break

    def _zoom_animation(self, text):
        """Animación de zoom - todo el texto aparece con efecto zoom"""
        if self.text_display.current and self.page:
            # Simular zoom con diferentes tamaños, limitando el tamaño máximo
            original_size = self.text_display.current.size
            sizes = [8, 12, 18, 24, original_size]
            
            for size in sizes:
                self.text_display.current.value = text
                self.text_display.current.size = size
                self.page.update()
                time.sleep(0.12)
            
            # Efecto de brillo final con menos parpadeo
            for _ in range(2):
                self.text_display.current.value = text + " ✨"
                self.page.update()
                time.sleep(0.15)
                self.text_display.current.value = text
                self.page.update()
                time.sleep(0.15)

    def _slide_animation(self, text):
        """Animación de deslizamiento - texto aparece desde el lado"""
        if self.text_display.current and self.page:
            # Simular deslizamiento con espacios y caracteres
            max_padding = 10
            
            for padding in range(max_padding, -1, -1):
                display_text = "🚀 " + " " * padding + text
                self.text_display.current.value = display_text
                self.page.update()
                time.sleep(0.08)
            
            # Limpiar y mostrar texto final
            self.text_display.current.value = text
            self.page.update()
