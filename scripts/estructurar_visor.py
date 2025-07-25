import os
import pandas as pd
from datetime import datetime
import glob

def estructurar_visor(visor_path):
    """
    Procesa archivos CDEMMO99.txt y CDEBMO99.txt con sus respectivos archivos complementarios
    para generar un archivo Excel con las hojas EMA y EBA.
    
    Args:
        visor_path (str): Ruta de la carpeta donde buscar los archivos
    
    Returns:
        str: Ruta del archivo Excel generado
    """
    
    def buscar_archivos(directorio, patron, max_depth=5):
        """Busca archivos con patrón específico hasta una profundidad máxima"""
        archivos = []
        for nivel in range(max_depth + 1):
            patron_busqueda = os.path.join(directorio, *(['*'] * nivel), patron)
            archivos.extend(glob.glob(patron_busqueda))
        return archivos
    
    def procesar_cdemmo99(archivo_path):
        """Procesa un archivo CDEMMO99.txt"""
        datos = []
        try:
            with open(archivo_path, 'r', encoding='UTF-8') as file:
                for linea in file:
                    if len(linea.strip()) >= 142:
                        registro = {
                            'RP': linea[0:11].strip(),
                            'NSS': linea[23:34].strip(),
                            'TIP_MOV': int(linea[35:36]) if linea[35:36].isdigit() else 0,
                            'FECHA_MOV': linea[36:46].strip(),
                            'DIAS': int(linea[46:48]) if linea[46:48].strip().isdigit() else 0,
                            'SDI': float(linea[48:54]) / 100 if linea[48:54].strip().replace('-', '').isdigit() else 0.0,
                            'CF': float(linea[56:62]) / 100 if linea[56:62].strip().replace('-', '').isdigit() else 0.0,
                            'EXC_PAT': float(linea[64:70]) / 100 if linea[64:70].strip().replace('-', '').isdigit() else 0.0,
                            'EXC_OBR': float(linea[72:78]) / 100 if linea[72:78].strip().replace('-', '').isdigit() else 0.0,
                            'PD_PAT': float(linea[80:86]) / 100 if linea[80:86].strip().replace('-', '').isdigit() else 0.0,
                            'PD_OBR': float(linea[88:94]) / 100 if linea[88:94].strip().replace('-', '').isdigit() else 0.0,
                            'GMP_PAT': float(linea[96:102]) / 100 if linea[96:102].strip().replace('-', '').isdigit() else 0.0,
                            'GMP_OBR': float(linea[104:110]) / 100 if linea[104:110].strip().replace('-', '').isdigit() else 0.0,
                            'RT': float(linea[112:118]) / 100 if linea[112:118].strip().replace('-', '').isdigit() else 0.0,
                            'IV_PAT': float(linea[120:126]) / 100 if linea[120:126].strip().replace('-', '').isdigit() else 0.0,
                            'IV_OBR': float(linea[128:134]) / 100 if linea[128:134].strip().replace('-', '').isdigit() else 0.0,
                            'GPS': float(linea[136:142]) / 100 if linea[136:142].strip().replace('-', '').isdigit() else 0.0
                        }
                        # Calcular TOTAL
                        registro['TOTAL'] = (registro['CF'] + registro['EXC_PAT'] + registro['EXC_OBR'] + 
                                           registro['PD_PAT'] + registro['PD_OBR'] + registro['GMP_PAT'] + 
                                           registro['GMP_OBR'] + registro['RT'] + registro['IV_PAT'] + 
                                           registro['IV_OBR'] + registro['GPS'])
                        datos.append(registro)
        except Exception as e:
            print(f"Error procesando {archivo_path}: {e}")
        return datos
    
    def procesar_cdemas99(archivo_path):
        """Procesa un archivo CDEMAS99.txt"""
        datos = []
        try:
            with open(archivo_path, 'r', encoding='UTF-8') as file:
                for linea in file:
                    # Usar longitud real conservando espacios, solo quitando \n si existe
                    linea_sin_salto = linea[:-1] if linea.endswith('\n') else linea
                    if len(linea_sin_salto) >= 109:
                        registro = {
                            'RP': linea[0:11].strip(),
                            'NSS': linea[23:34].strip(),  # 11 caracteres a partir del carácter 24
                            'NOMBRE_ASEGURADO': linea[35:85].strip().replace('$', ' '),  # 50 caracteres corregido
                            'CURP': linea[88:106].strip()  # 18 caracteres a partir del carácter 89
                        }
                        datos.append(registro)
                            
        except Exception as e:
            print(f"Error procesando {archivo_path}: {e}")
        
        return datos
    
    def procesar_cdebmo99(archivo_path):
        """Procesa un archivo CDEBMO99.txt"""
        datos = []
        try:
            with open(archivo_path, 'r', encoding='UTF-8') as file:
                for linea in file:
                    if len(linea.strip()) >= 100:
                        registro = {
                            'RP': linea[0:11].strip(),
                            'NSS': linea[21:32].strip(),
                            'TIP_MOV': int(linea[33:34]) if linea[33:34].isdigit() else 0,
                            'FECHA_MOV': linea[34:44].strip(),
                            'DIAS': int(linea[44:46]) if linea[44:46].strip().isdigit() else 0,
                            'SDI': float(linea[46:52]) / 100 if linea[46:52].strip().replace('-', '').isdigit() else 0.0,
                            'RETIRO': float(linea[54:60]) / 100 if linea[54:60].strip().replace('-', '').isdigit() else 0.0,
                            'CEAV_PAT': float(linea[62:68]) / 100 if linea[62:68].strip().replace('-', '').isdigit() else 0.0,
                            'CEAV_OBR': float(linea[70:76]) / 100 if linea[70:76].strip().replace('-', '').isdigit() else 0.0,
                            'APORTACION_PAT': float(linea[85:92]) if linea[85:92].strip().replace('.', '').replace('-', '').isdigit() else 0.0,
                            'AMORTIZACION': float(linea[92:100]) if linea[92:100].strip().replace('.', '').replace('-', '').isdigit() else 0.0
                        }
                        # Calcular TOTAL_RCV
                        registro['TOTAL_RCV'] = registro['RETIRO'] + registro['CEAV_PAT'] + registro['CEAV_OBR']
                        datos.append(registro)
        except Exception as e:
            print(f"Error procesando {archivo_path}: {e}")
        return datos
    
    def procesar_cdebas99(archivo_path):
        """Procesa un archivo CDEBAS99.txt"""
        datos = []
        try:
            with open(archivo_path, 'r', encoding='UTF-8') as file:
                for linea in file:
                    if len(linea.strip()) >= 150:
                        t_credito = linea[119:120].strip()
                        # Mapear T_CREDITO según especificaciones
                        if t_credito == '0':
                            t_credito = '-'
                        elif t_credito == '1':
                            t_credito = '%'
                        elif t_credito == '2':
                            t_credito = 'CF'
                        elif t_credito == '3':
                            t_credito = 'VSM'
                        
                        registro = {
                            'RP': linea[0:11].strip(),
                            'NSS': linea[21:32].strip(),
                            'NOMBRE_ASEGURADO': linea[33:83].strip().replace('$', ' '),
                            'CURP': linea[86:104].strip(),
                            'T_CREDITO': t_credito,
                            'V_CREDITO': float(linea[120:129]) if linea[120:129].strip().replace('.', '').replace('-', '').isdigit() else 0.0,
                            'N_CREDITO': linea[109:119].strip(),
                            'APORTACION_PAT': float(linea[85:92]) if linea[85:92].strip().replace('.', '').replace('-', '').isdigit() else 0.0,
                            'AMORTIZACION': float(linea[92:100]) if linea[92:100].strip().replace('.', '').replace('-', '').isdigit() else 0.0
                        }
                        # Calcular TOTAL_INF como suma de APORTACION_PAT + AMORTIZACION
                        registro['TOTAL_INF'] = registro['APORTACION_PAT'] + registro['AMORTIZACION']
                        datos.append(registro)
        except Exception as e:
            print(f"Error procesando {archivo_path}: {e}")
        return datos
    
    # Buscar archivos CDEMMO99.txt y sus complementarios
    archivos_cdemmo99 = buscar_archivos(visor_path, "CDEMMO99.txt")
    archivos_cdemas99 = buscar_archivos(visor_path, "CDEMAS99.txt")
    
    # Buscar archivos CDEBMO99.txt y sus complementarios
    archivos_cdebmo99 = buscar_archivos(visor_path, "CDEBMO99.txt")
    archivos_cdebas99 = buscar_archivos(visor_path, "CDEBAS99.txt")
    
    # Buscar archivo CDEMPA99.txt para obtener el periodo
    archivos_cdempa99 = buscar_archivos(visor_path, "CDEMPA99.txt")
    
    def obtener_periodo_archivo(archivo_path):
        """Extrae el periodo del archivo CDEMPA99.txt"""
        try:
            with open(archivo_path, 'r', encoding='UTF-8') as file:
                primera_linea = file.readline()
                if len(primera_linea) >= 103:  # Asegurar que tiene al menos 103 caracteres (99+4)
                    mes = primera_linea[95:97].strip()  # 2 caracteres a partir del 97 (índice 96)
                    año = primera_linea[97:101].strip()  # 4 caracteres a partir del 99 (índice 98)
                    if len(mes) == 2 and len(año) == 4:
                        return f"{mes}-{año}"
        except Exception as e:
            print(f"Error obteniendo periodo de {archivo_path}: {e}")
        return None
    
    excel_sheets = {}
    
    # Procesar archivos EMA (CDEMMO99 + CDEMAS99)
    if archivos_cdemmo99:
        print(f"Procesando {len(archivos_cdemmo99)} archivos CDEMMO99...")
        
        # Procesar todos los archivos CDEMMO99
        datos_ema = []
        for archivo in archivos_cdemmo99:
            datos_ema.extend(procesar_cdemmo99(archivo))
        
        if datos_ema:
            df_ema = pd.DataFrame(datos_ema)
            print(f"DataFrame EMA inicial: {len(df_ema)} registros")
            
            # Procesar archivos complementarios CDEMAS99
            datos_complemento = []
            for archivo in archivos_cdemas99:
                datos_complemento.extend(procesar_cdemas99(archivo))
            
            if datos_complemento:
                df_complemento = pd.DataFrame(datos_complemento)
                print(f"DataFrame complemento CDEMAS99: {len(df_complemento)} registros")
                print(f"Muestra de NSS en EMA: {df_ema['NSS'].head()}")
                print(f"Muestra de NSS en complemento: {df_complemento['NSS'].head()}")
                
                # Hacer merge con NSS
                df_ema_before_merge = len(df_ema)
                df_ema = df_ema.merge(df_complemento[['NSS', 'NOMBRE_ASEGURADO', 'CURP']], 
                                    on='NSS', how='left')
                print(f"Merge completado: {df_ema_before_merge} -> {len(df_ema)} registros")
                print(f"Registros con CURP no vacío: {df_ema['CURP'].notna().sum()}")
                print(f"Registros con NOMBRE_ASEGURADO no vacío: {df_ema['NOMBRE_ASEGURADO'].notna().sum()}")
            else:
                print("No se encontraron archivos CDEMAS99")
                # Si no hay archivos complementarios, agregar columnas vacías
                df_ema['NOMBRE_ASEGURADO'] = ''
                df_ema['CURP'] = ''
            
            # Eliminar filas con TIP_MOV = 2
            df_ema = df_ema[df_ema['TIP_MOV'] != 2]
            
            # Convertir FECHA_MOV a datetime para poder ordenar
            df_ema['FECHA_MOV'] = pd.to_datetime(df_ema['FECHA_MOV'], format='%d-%m-%Y', errors='coerce')
            
            # Agrupar por RP y NSS con manejo mejorado de SDI
            def get_latest_value(group, value_col, date_col):
                """Obtiene el valor más reciente basado en la fecha"""
                if group[date_col].isna().all():
                    return group[value_col].iloc[-1]
                latest_idx = group[date_col].idxmax()
                return group.loc[latest_idx, value_col]
            
            agg_functions = {
                'CURP': 'first',
                'NOMBRE_ASEGURADO': 'first',
                'DIAS': 'sum',
                'CF': 'sum',
                'EXC_PAT': 'sum',
                'EXC_OBR': 'sum',
                'PD_PAT': 'sum',
                'PD_OBR': 'sum',
                'GMP_PAT': 'sum',
                'GMP_OBR': 'sum',
                'RT': 'sum',
                'IV_PAT': 'sum',
                'IV_OBR': 'sum',
                'GPS': 'sum',
                'TOTAL': 'sum'
            }
            
            df_ema_grouped = df_ema.groupby(['RP', 'NSS']).agg(agg_functions).reset_index()
            
            # Obtener SDI más reciente por grupo
            sdi_latest = df_ema.groupby(['RP', 'NSS']).apply(
                lambda x: get_latest_value(x, 'SDI', 'FECHA_MOV')
            ).reset_index(name='SDI')
            
            # Merge con SDI
            df_ema_grouped = df_ema_grouped.merge(sdi_latest, on=['RP', 'NSS'])
            
            # Reordenar columnas
            columnas_ema = ['RP', 'NSS', 'CURP', 'NOMBRE_ASEGURADO', 'DIAS', 'SDI', 'CF', 'EXC_PAT', 
                           'EXC_OBR', 'PD_PAT', 'PD_OBR', 'GMP_PAT', 'GMP_OBR', 'RT', 'IV_PAT', 
                           'IV_OBR', 'GPS', 'TOTAL']
            df_ema_grouped = df_ema_grouped[columnas_ema]

            # Ordenar por RP y NOMBRE_ASEGURADO
            df_ema_grouped = df_ema_grouped.sort_values(['RP', 'NOMBRE_ASEGURADO']).reset_index(drop=True)

            excel_sheets['EMA'] = df_ema_grouped
            print(f"Hoja EMA creada con {len(df_ema_grouped)} registros")
    
    # Procesar archivos EBA (CDEBMO99 + CDEBAS99)
    if archivos_cdebmo99:
        print(f"Procesando {len(archivos_cdebmo99)} archivos CDEBMO99...")
        
        # Procesar todos los archivos CDEBMO99
        datos_eba = []
        for archivo in archivos_cdebmo99:
            datos_eba.extend(procesar_cdebmo99(archivo))
        
        if datos_eba:
            df_eba = pd.DataFrame(datos_eba)

            # Procesar archivos complementarios CDEBAS99                                                                                                                                                                                                                                                                                    
            datos_complemento_eba = []                                                                                                                                                                                                                                                                                  
            for archivo in archivos_cdebas99:                                                                                                                                                                                                                                                                                   
                datos_complemento_eba.extend(procesar_cdebas99(archivo))
            
            if datos_complemento_eba:
                df_complemento_eba = pd.DataFrame(datos_complemento_eba)
                # Hacer merge con NSS - incluir TOTAL_INF
                df_eba = df_eba.merge(df_complemento_eba[['NSS', 'NOMBRE_ASEGURADO', 'CURP', 
                                                        'T_CREDITO', 'V_CREDITO', 'N_CREDITO']], 
                                    on='NSS', how='left')
            else:
                # Si no hay archivos complementarios, agregar columnas vacías
                df_eba['NOMBRE_ASEGURADO'] = ''
                df_eba['CURP'] = ''
                df_eba['T_CREDITO'] = ''
                df_eba['V_CREDITO'] = 0.0
                df_eba['N_CREDITO'] = ''
            
            # Eliminar filas con TIP_MOV = 2
            df_eba = df_eba[df_eba['TIP_MOV'] != 2]
            
            # Convertir FECHA_MOV a datetime para poder ordenar
            df_eba['FECHA_MOV'] = pd.to_datetime(df_eba['FECHA_MOV'], format='%d-%m-%Y', errors='coerce')
            
            # Asegurar que TOTAL_INF existe y se calcula correctamente
            if 'TOTAL_INF' not in df_eba.columns:
                df_eba['TOTAL_INF'] = 0.0
            
            # Calcular TOTAL_INF como suma de APORTACION_PAT + AMORTIZACION para todos los registros
            # Si TOTAL_INF viene del merge pero es 0 o NaN, recalcular
            df_eba['TOTAL_INF'] = df_eba['APORTACION_PAT'] + df_eba['AMORTIZACION']
            
            # Calcular TOTAL para EBA
            df_eba['TOTAL'] = df_eba['TOTAL_RCV'] + df_eba['TOTAL_INF']
            
            # Agrupar por RP y NSS
            agg_functions_eba = {
                'CURP': 'first',
                'NOMBRE_ASEGURADO': 'first',
                'DIAS': 'sum',
                'RETIRO': 'sum',
                'CEAV_PAT': 'sum',
                'CEAV_OBR': 'sum',
                'TOTAL_RCV': 'sum',
                'APORTACION_PAT': 'sum',
                'N_CREDITO': 'first',
                'AMORTIZACION': 'sum',
                'TOTAL_INF': 'sum',
                'TOTAL': 'sum'
            }
            
            df_eba_grouped = df_eba.groupby(['RP', 'NSS']).agg(agg_functions_eba).reset_index()
            
            # Obtener valores más recientes por grupo para SDI, T_CREDITO y V_CREDITO
            latest_values = df_eba.groupby(['RP', 'NSS']).apply(
                lambda x: pd.Series({
                    'SDI': get_latest_value(x, 'SDI', 'FECHA_MOV'),
                    'T_CREDITO': get_latest_value(x, 'T_CREDITO', 'FECHA_MOV'),
                    'V_CREDITO': get_latest_value(x, 'V_CREDITO', 'FECHA_MOV')
                })
            ).reset_index()
            
            # Merge con valores más recientes
            df_eba_grouped = df_eba_grouped.merge(latest_values, on=['RP', 'NSS'])
            
            # Cambiar valores 0 por "-" en T_CREDITO, V_CREDITO y N_CREDITO
            df_eba_grouped['T_CREDITO'] = df_eba_grouped['T_CREDITO'].replace(0, '-')
            df_eba_grouped['V_CREDITO'] = df_eba_grouped['V_CREDITO'].replace(0.0, '-')
            df_eba_grouped['N_CREDITO'] = df_eba_grouped['N_CREDITO'].replace('0000000000', '-')
            
            # Reordenar columnas
            columnas_eba = ['RP', 'NSS', 'CURP', 'NOMBRE_ASEGURADO', 'DIAS', 'SDI', 'RETIRO', 
                           'CEAV_PAT', 'CEAV_OBR', 'TOTAL_RCV', 'APORTACION_PAT', 'T_CREDITO', 
                           'V_CREDITO', 'N_CREDITO', 'AMORTIZACION', 'TOTAL_INF', 'TOTAL']
            df_eba_grouped = df_eba_grouped[columnas_eba]

            # Ordenar por RP y NOMBRE_ASEGURADO
            df_eba_grouped = df_eba_grouped.sort_values(['RP', 'NOMBRE_ASEGURADO']).reset_index(drop=True)

            excel_sheets['EBA'] = df_eba_grouped
            print(f"Hoja EBA creada con {len(df_eba_grouped)} registros")
    
    # Generar archivo Excel
    if excel_sheets:
        # Obtener periodo del archivo CDEMPA99.txt
        periodo_str = None
        if archivos_cdempa99:
            periodo_str = obtener_periodo_archivo(archivos_cdempa99[0])
        
        # Formar nombre del archivo
        if periodo_str:
            nombre_archivo = f"{periodo_str}_VISOR_EMISION.xlsx"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_visor_{timestamp}.xlsx"
        
        output_path = os.path.join(visor_path, nombre_archivo)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in excel_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Formatear encabezados (fondo negro, texto blanco)
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                
                # Crear estilo para encabezados
                from openpyxl.styles import PatternFill, Font
                header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
                header_font = Font(color="FFFFFF", bold=True)
                
                # Aplicar formato a la primera fila (encabezados)
                for cell in worksheet[1]:
                    cell.fill = header_fill
                    cell.font = header_font
        
        print(f"Archivo Excel generado: {output_path}")
        return output_path
    else:
        print("No se encontraron archivos para procesar")
        return None

estructurar_visor(r'F:\01 TRABAJO\BPO\11 ENTREGA\PAGOS\06 JUNIO 2025\FERUCI\EMISIONES')