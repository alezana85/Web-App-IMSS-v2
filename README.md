# Aplicación Web IMSS v2

Sistema de gestión web desarrollado con Flet para el Instituto Mexicano del Seguro Social (IMSS).

## 📁 Estructura del Proyecto

```
Web App IMSS v2/
├── .env                    # Variables de entorno y configuraciones
├── app.py                  # Clase principal de la aplicación
├── main.py                 # Punto de entrada principal
├── config.py               # Configuración centralizada
├── assets/                 # Recursos multimedia
│   ├── foto.png           # Imagen de perfil por defecto
│   └── logo.png           # Logo del IMSS
├── data/                   # Datos persistentes
│   └── users.csv          # Base de datos de usuarios
└── pages/                  # Páginas de la aplicación
    ├── __init__.py        # Inicializador del módulo
    └── login.py           # Página de inicio de sesión
```

## 🛠️ Descripción de Archivos

### `.env`
Variables de entorno para configuraciones sensibles como:
- Configuración de ventana (dimensiones, colores)
- Rutas de archivos
- Configuración de seguridad
- Configuración de logging

### `config.py`
Clase de configuración centralizada que:
- Carga variables del archivo `.env`
- Proporciona valores por defecto
- Gestiona rutas de archivos
- Centraliza configuraciones de la aplicación

### `main.py`
Punto de entrada principal que:
- Inicializa la aplicación Flet
- Configura la función main()
- Ejecuta la aplicación

### `app.py`
Clase principal `IMSSApp` que maneja:
- Navegación entre páginas
- Estado global de la aplicación
- Gestión de sesiones de usuario
- Configuración de UI centralizada
- Sistema de notificaciones

### `assets/`
Recursos multimedia de la aplicación:
- **foto.png**: Imagen de perfil por defecto
- **logo.png**: Logotipo oficial del IMSS

### `data/`
Almacenamiento de datos persistentes:
- **users.csv**: Base de datos de usuarios con formato:
  ```csv
  usuario,contraseña
  admin,admin123
  usuario1,password1
  ```

### `pages/`
Módulos de páginas de la aplicación:
- **login.py**: Página de inicio de sesión con validación de credenciales

## 🚀 Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install flet
   ```

2. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```

## 🎨 Características

### Diseño
- ✅ Interfaz moderna y responsive
- ✅ Tema corporativo IMSS (colores morado/violeta)
- ✅ Componentes Material Design
- ✅ Ventana redimensionable con tamaños mínimos

### Funcionalidad
- ✅ Sistema de autenticación con CSV
- ✅ Validación de formularios
- ✅ Mensajes de error y éxito
- ✅ Navegación entre páginas
- ✅ Gestión de estado de sesión

### Arquitectura
- ✅ Configuración centralizada
- ✅ Separación de responsabilidades
- ✅ Estructura modular escalable
- ✅ Manejo de errores robusto

## 🔧 Configuración

La aplicación se puede configurar mediante el archivo `.env`:

```env
# Configuración de ventana
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800

# Colores del tema
PRIMARY_COLOR=#9146ff
SECONDARY_COLOR=#772ce8

# Configuración de seguridad
MAX_LOGIN_ATTEMPTS=3
SESSION_TIMEOUT=3600
```

## 🔐 Usuarios por Defecto

La aplicación incluye usuarios de prueba en `data/users.csv`. Puedes agregar o modificar usuarios editando este archivo.

## 📋 Próximas Funcionalidades

- [ ] Dashboard principal post-login
- [ ] Gestión de usuarios
- [ ] Módulo de reportes
- [ ] Configuración de perfiles
- [ ] Sistema de logging avanzado
- [ ] Base de datos SQL

## 🤝 Contribución

Para agregar nuevas páginas:

1. Crear archivo en `pages/nueva_pagina.py`
2. Implementar clase con método `build(page, app)`
3. Agregar al diccionario `pages` en `IMSSApp`
4. Usar `app.navigate_to("nueva_pagina")` para navegar

## 📝 Licencia

Desarrollado para uso interno del IMSS.
