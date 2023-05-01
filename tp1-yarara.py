import pandas as pd
from inline_sql import sql, sql_val

# Importamos archivos necesarios
padron = pd.read_csv("padron-de-operadores-organicos-certificados.csv", index_col=0, encoding='latin-1')
salarios = pd.read_csv("w_median_depto_priv_clae2.csv")
localidades = pd.read_csv("localidades-censales.csv")
dicc_deptos = pd.read_csv("diccionario_cod_depto.csv")
dicc_clases = pd.read_csv("diccionario_clae2.csv")

# Le agregamos una columna id a la tabla padrón
id_registro = [i for i in range(padron.shape[0])]
padron['id_registro'] = id_registro


# Hicimo una función para separar valores
def separar1FN(data, columna, separador):
    # Crea un diccionario vacío para almacenar los resultados\n",
    dict_separar_data = {'id_registro': [], columna:[]}
    
    # Itera por cada registro en el DataFrame\n",
    for i in range(len(data)):        
        # Obtiene la cadena de valores del registro actual\n",
        columna_str = data.iloc[i][columna]
        
        # Verifica si la cadena de valores es nula o vacía\n",
        if pd.isnull(columna_str) or columna_str == '':
            # Asigna una lista vacía como valor predeterminado\n",
            columna_list = []
        else:
            # Separa los valores en una lista utilizando el separador especificado\n",
            columna_list = columna_str.split(separador)
    
        # Agrega los datos a los diccionarios\n",
        for valor in columna_list:
            dict_separar_data['id_registro'].append(data.iloc[i]['id_registro'])
            dict_separar_data[columna].append(valor)
    
    # Crea un nuevo DataFrame a partir del diccionario\n",
    data_separada = pd.DataFrame(dict_separar_data)
    
    return data_separada
  

# Separamos productos en padr
lista_separadores = [', ',' Y ','?','-',' + ']
data_separada = padron
columna = 'productos'

for separador in lista_separadores:
    data_separada = separar1FN(data_separada, columna, separador)
