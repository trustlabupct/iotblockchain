import pandas as pd
import openpyxl
import ast  # Para convertir strings que representan diccionarios a diccionarios reales

def round_nested_dict_values(data, decimal_places=3):
    if isinstance(data, dict):
        return {k: round(v, decimal_places) if isinstance(v, float) else v for k, v in data.items()}
    return data

def convert_csv_to_excel(csv_file, excel_file):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)
    
    # Redondear los valores de los diccionarios en columnas específicas
    columns_to_process = ['Exit Probability Multi-Agent', 'Cumulative Weight Multi-Agent', 'Confirmation Confidence Multi-Agent']
    for column in columns_to_process:
        df[column] = df[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)  # Convertir a diccionario
        df[column] = df[column].apply(lambda x: round_nested_dict_values(x))  # Redondear valores dentro del diccionario
    
    # Redondear otros valores numéricos a 3 decimales
    df = df.round(3)
    
    # Escribir el DataFrame a un archivo Excel
    writer = pd.ExcelWriter(excel_file, engine='openpyxl')
    df.to_excel(writer, index=False)
    
    # Obtener el libro y la hoja activa
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # Establecer ancho de columna y alineación centrada para todas las columnas
    for col in worksheet.columns:
        for cell in col:
            cell.alignment = openpyxl.styles.Alignment(horizontal='center')
        max_length = max(len(str(cell.value)) for cell in col)
        adjusted_width = (max_length + 2) * 1.2  # Ajustar un poco más que el contenido máximo
        worksheet.column_dimensions[col[0].column_letter].width = adjusted_width
    
    # Guardar y cerrar el writer
    
    writer.close()

# Usar la función
convert_csv_to_excel('data2.csv', 'data2.xlsx')
