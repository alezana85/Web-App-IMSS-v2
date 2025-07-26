import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def buscar_archivos_zip(directorio_raiz):
    """
    Busca recursivamente todos los archivos .zip en el directorio y sus subcarpetas
    """
    archivos_zip = []
    
    for root, dirs, files in os.walk(directorio_raiz):
        for file in files:
            if file.lower().endswith('.zip'):
                ruta_completa = os.path.join(root, file)
                archivos_zip.append(ruta_completa)
    
    return archivos_zip


def descomprimir_archivo(ruta_zip, directorio_destino=None):
    """
    Descomprime un archivo .zip en el directorio especificado
    Si no se especifica directorio, se descomprime en la misma carpeta del .zip
    """
    try:
        if directorio_destino is None:
            directorio_destino = os.path.dirname(ruta_zip)
        
        with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
            # Obtener la lista de archivos en el zip
            archivos_en_zip = zip_ref.namelist()
            
            # Encontrar el directorio raíz común más profundo
            # Esto ayuda a extraer desde el nivel más interno cuando hay una sola carpeta contenedora
            directorios_raiz = set()
            archivos_en_raiz = []
            
            for archivo in archivos_en_zip:
                if '/' in archivo:
                    # Es un archivo o carpeta dentro de un directorio
                    primer_directorio = archivo.split('/')[0]
                    directorios_raiz.add(primer_directorio)
                else:
                    # Es un archivo en la raíz del zip
                    archivos_en_raiz.append(archivo)
            
            # Si hay solo un directorio raíz y no hay archivos en la raíz,
            # extraer desde ese directorio para evitar carpetas contenedoras innecesarias
            if len(directorios_raiz) == 1 and len(archivos_en_raiz) == 0:
                directorio_contenedor = list(directorios_raiz)[0]
                prefijo_a_remover = directorio_contenedor + '/'
                
                # Extraer removiendo el directorio contenedor
                for archivo in archivos_en_zip:
                    if archivo.startswith(prefijo_a_remover):
                        # Remover el prefijo del directorio contenedor
                        nueva_ruta = archivo[len(prefijo_a_remover):]
                        
                        if nueva_ruta:  # No procesar rutas vacías
                            ruta_destino_archivo = os.path.join(directorio_destino, nueva_ruta)
                            
                            # Si es un directorio, crearlo
                            if archivo.endswith('/'):
                                os.makedirs(ruta_destino_archivo, exist_ok=True)
                            else:
                                # Si es un archivo, crear el directorio padre y extraer
                                directorio_padre = os.path.dirname(ruta_destino_archivo)
                                if directorio_padre:
                                    os.makedirs(directorio_padre, exist_ok=True)
                                
                                # Leer el contenido del archivo del zip y escribirlo
                                with zip_ref.open(archivo) as source, open(ruta_destino_archivo, 'wb') as target:
                                    target.write(source.read())
            else:
                # Si hay múltiples directorios raíz o archivos en la raíz, extraer todo normalmente
                zip_ref.extractall(directorio_destino)
        
        return True, f"Descomprimido exitosamente: {os.path.basename(ruta_zip)}"
        
    except Exception as e:
        return False, f"Error al descomprimir {os.path.basename(ruta_zip)}: {str(e)}"


def procesar_archivos_zip(directorio_raiz, progreso_callback=None):
    """
    Procesa todos los archivos .zip encontrados en el directorio y subcarpetas
    """
    archivos_zip = buscar_archivos_zip(directorio_raiz)
    
    if not archivos_zip:
        return "No se encontraron archivos .zip en el directorio seleccionado."
    
    resultados = []
    total_archivos = len(archivos_zip)
    
    for i, ruta_zip in enumerate(archivos_zip):
        if progreso_callback:
            progreso_callback(i + 1, total_archivos, os.path.basename(ruta_zip))
        
        exito, mensaje = descomprimir_archivo(ruta_zip)
        resultados.append(mensaje)
    
    return resultados


class InterfazDescompresor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Descompresor de Archivos ZIP en Subcarpetas")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.directorio_seleccionado = tk.StringVar()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Descompresor de Archivos ZIP", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de directorio
        ttk.Label(main_frame, text="Directorio a procesar:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(main_frame, textvariable=self.directorio_seleccionado, 
                 width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        ttk.Button(main_frame, text="Seleccionar", 
                  command=self.seleccionar_directorio).grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Información
        info_text = """
Instrucciones:
1. Selecciona el directorio que contiene las subcarpetas con archivos .zip
2. El script buscará recursivamente todos los archivos .zip
3. Los archivos se descomprimirán en la misma carpeta donde se encuentra cada .zip
4. Si un .zip contiene solo una carpeta contenedora, se extraerá sin esa carpeta extra
5. Si un .zip tiene múltiples carpetas/archivos en la raíz, se extraerá normalmente
        """
        
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT, 
                              background="lightgray", relief="sunken", padding="10")
        info_label.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Botón de procesar
        self.btn_procesar = ttk.Button(main_frame, text="Descomprimir Archivos ZIP", 
                                      command=self.procesar_archivos, state="disabled")
        self.btn_procesar.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(main_frame, mode='determinate')
        self.progreso.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Label de estado
        self.label_estado = ttk.Label(main_frame, text="Selecciona un directorio para comenzar")
        self.label_estado.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Área de resultados
        ttk.Label(main_frame, text="Resultados:").grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        # Frame para el área de texto con scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Área de texto para resultados
        self.text_resultados = tk.Text(text_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar.set)
        
        self.text_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar el grid para que el área de texto se expanda
        main_frame.rowconfigure(7, weight=1)
    
    def seleccionar_directorio(self):
        directorio = filedialog.askdirectory(title="Seleccionar directorio con archivos ZIP")
        if directorio:
            self.directorio_seleccionado.set(directorio)
            self.btn_procesar.config(state="normal")
            self.label_estado.config(text=f"Directorio seleccionado: {directorio}")
            
            # Contar archivos .zip
            archivos_zip = buscar_archivos_zip(directorio)
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, f"Se encontraron {len(archivos_zip)} archivos .zip en el directorio y subcarpetas.\n\n")
            
            if archivos_zip:
                self.text_resultados.insert(tk.END, "Archivos encontrados:\n")
                for archivo in archivos_zip:
                    self.text_resultados.insert(tk.END, f"- {archivo}\n")
    
    def actualizar_progreso(self, actual, total, archivo_actual):
        porcentaje = (actual / total) * 100
        self.progreso['value'] = porcentaje
        self.label_estado.config(text=f"Procesando ({actual}/{total}): {archivo_actual}")
        self.root.update_idletasks()
    
    def procesar_archivos(self):
        directorio = self.directorio_seleccionado.get()
        
        if not directorio:
            messagebox.showerror("Error", "Por favor selecciona un directorio")
            return
        
        self.btn_procesar.config(state="disabled")
        self.text_resultados.delete(1.0, tk.END)
        self.progreso['value'] = 0
        
        try:
            resultados = procesar_archivos_zip(directorio, self.actualizar_progreso)
            
            self.text_resultados.insert(tk.END, "=== PROCESO COMPLETADO ===\n\n")
            
            if isinstance(resultados, str):
                # No se encontraron archivos
                self.text_resultados.insert(tk.END, resultados)
            else:
                # Mostrar resultados
                for resultado in resultados:
                    self.text_resultados.insert(tk.END, f"{resultado}\n")
            
            self.label_estado.config(text="Proceso completado")
            messagebox.showinfo("Completado", "El proceso de descompresión ha finalizado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el proceso: {str(e)}")
            self.text_resultados.insert(tk.END, f"ERROR: {str(e)}\n")
        
        finally:
            self.btn_procesar.config(state="normal")
            self.progreso['value'] = 100
    
    def ejecutar(self):
        self.root.mainloop()


def main():
    """
    Función principal - puede ejecutarse con interfaz gráfica o desde línea de comandos
    """
    import sys
    
    if len(sys.argv) > 1:
        # Modo línea de comandos
        directorio = sys.argv[1]
        if os.path.exists(directorio):
            print(f"Procesando directorio: {directorio}")
            resultados = procesar_archivos_zip(directorio)
            
            if isinstance(resultados, str):
                print(resultados)
            else:
                print("=== RESULTADOS ===")
                for resultado in resultados:
                    print(resultado)
        else:
            print(f"El directorio '{directorio}' no existe")
    else:
        # Modo interfaz gráfica
        app = InterfazDescompresor()
        app.ejecutar()


if __name__ == "__main__":
    main()