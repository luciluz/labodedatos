#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from inline_sql import sql, sql_val

# Importamos archivos necesarios
padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", index_col=0, encoding='latin-1')
salarios = pd.read_csv("~/Descargas/w_median_depto_priv_clae2.csv")
localidades = pd.read_csv("~/Descargas/localidades-censales.csv")
dicc_deptos = pd.read_csv("~/Descargas/diccionario_cod_depto.csv")
dicc_clases = pd.read_csv("~/Descargas/diccionario_clae2.csv")

# Le agregamos una columna id a la tabla padrón y renombramos columna
# razon_social
id_registro = [i for i in range(padron.shape[0])]
padron['id_registro'] = id_registro
padron.rename(columns={'razón social':'razon_social'},inplace=True)


padron.columns

# Hicimo una función para separar valores
def separar1FN(data, columna, separador):
    # Crea un diccionario vacío para almacenar los resultados",
    dict_separar_data = {'id_registro': [], columna:[]}
    
    # Itera por cada registro en el DataFrame\n",
    for i in range(len(data)):        
        # Obtiene la cadena de valores del registro actual",
        columna_str = data.iloc[i][columna]
        
        # Verifica si la cadena de valores es nula o vacía",
        if pd.isnull(columna_str) or columna_str == '':
            # Asigna una lista vacía como valor predeterminado",
            columna_list = []
        else:
            # Separa los valores en una lista utilizando el separador especificado",
            columna_list = columna_str.split(separador)
    
        # Agrega los datos a los diccionarios",
        for valor in columna_list:
            dict_separar_data['id_registro'].append(data.iloc[i]['id_registro'])
            dict_separar_data[columna].append(valor)
    
    # Crea un nuevo DataFrame a partir del diccionario\n",
    data_separada = pd.DataFrame(dict_separar_data)
    
    return data_separada
  

# Separamos productos en padron
lista_separadores = [', ',' Y ','?','-',' + ']
productos = padron
columna = 'productos'

for separador in lista_separadores:
    productos = separar1FN(productos, columna, separador)   
    
    
# Separamos rubros en padron
lista_separadores = ['/',';']
rubro = padron
columna = 'rubro'


for separador in lista_separadores:
    rubro = separar1FN(rubro, columna, separador)
    


productos
rubro


# Eliminamos tildes y cambiamos a mayúsculas en localidades
localidades =        sql^ """
                    SELECT *, UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                    departamento_nombre, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u'))AS departamento_nombre
                    FROM localidades
                    """
localidades

# Eliminamos tildes y cambiamos a mayúsculas en dicc_deptos
dicc_deptos =        sql^ """
                    SELECT *, UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                    nombre_departamento_indec, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u'))AS nombre_departamento_indec
                    FROM dicc_deptos
                    """
dicc_deptos


# Eliminamos tildes y pasamos a mayusculas en la columna dicc_deptos
dicc_deptos =        sql^ """
                    SELECT *, UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                    nombre_provincia_indec, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u'))AS nombre_provincia_indec
                    FROM dicc_deptos
                    """
dicc_deptos

# Eliminamos tildes y pasamos a mayusculas en la columna provincia de localidades
localidades =        sql^ """
                    SELECT *, REPLACE(UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                   provincia_nombre, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u')), 'TIERRA DEL FUEGO, ANTARTIDA E ISLAS DEL ATLANTICO SUR',
                    'TIERRA DEL FUEGO')
                    AS provincia_nombre,
                    UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(municipio_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) AS municipio_nombre,
                    UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) AS nombre,
                    
                    FROM localidades
                    """
localidades

# Armamos tabla departamentos a partir del padron con consultas SQL
departamento = sql^ """
                    SELECT codigo_departamento_indec, nombre_departamento_indec
                    FROM dicc_deptos
                    """
departamento

# Armamos tabla certificadora a partir del padron con consultas SQL
certificadora = sql^ """
                    SELECT DISTINCT Certificadora_id, certificadora_deno
                    FROM padron
                    """
certificadora

# Armamos tabla categoria a partir del padron con consultas SQL
categoria =    sql^ """
                    SELECT DISTINCT categoria_id, categoria_desc
                    FROM padron
                    """
categoria

# Armamos tabla provincia a partir del padron con consultas SQL
provincia =    sql^ """
                    SELECT DISTINCT provincia_id, provincia_nombre_2
                    FROM localidades
                    """
provincia

# Armamos tabla clases a partir del padron con consultas SQL
clases =       sql^ """
                    SELECT DISTINCT clae2, clae2_desc, letra
                    FROM dicc_clases
                    """
clases

# Armamos tabla letra a partir del padron con consultas SQL
letra =        sql^ """
                    SELECT DISTINCT letra, letra_desc
                    FROM dicc_clases
                    """
letra


# Eliminar columnas del padron de operadores organicos
padron =        sql^ """
                    SELECT DISTINCT id_registro, provincia_id, departamento,
                    localidad, categoria_id, Certificadora_id, razon_social, 
                    establecimiento
                    FROM padron
                    """
padron

###### CALIDAD DE DATOS
# Chequeo inconsistencias de id provincias entre las 3 tablas
# En dicc_depto
DiccionarioDepto = """
SELECT DISTINCT dd.id_provincia_indec,dd.nombre_provincia_indec_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN dicc_deptos AS dd2
ON dd.nombre_provincia_indec_2 = dd2.nombre_provincia_indec_2
WHERE dd.id_provincia_indec != dd2.id_provincia_indec
"""
print(sql^ DiccionarioDepto)

# Entre dicc_depto y padron de operadores
DiccionarioDepto_PadronOpOrg = """
SELECT DISTINCT poo.provincia_id,poo.provincia_nombre_2,dd.id_provincia_indec,dd.nombre_provincia_indec_2
FROM provincia AS poo
LEFT OUTER JOIN dicc_deptos AS dd
ON poo.provincia_nombre_2 = dd.nombre_provincia_indec_2
WHERE poo.provincia_id != dd.id_provincia_indec
"""
print(sql^ DiccionarioDepto_PadronOpOrg)

# Entre dicc_depto y localidades
DiccionarioDepto_LocSensales = """
SELECT DISTINCT dd.id_provincia_indec,dd.nombre_provincia_indec_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN localidades AS lc
ON dd.nombre_provincia_indec_2 = lc.provincia_nombre_2
WHERE dd.id_provincia_indec != lc.provincia_id
"""
print(sql^ DiccionarioDepto_LocSensales)

# Comparamos el diccionario de departamentos con la informacion de localidades
# censales de indec

# Unimos las tablas por nombre de departamento y provincia
# comparamos los codigod de departamentos de cada tabla
DiccionarioDepto = """
SELECT DISTINCT dd.codigo_departamento_indec,loc.departamento_id,	dd.nombre_departamento_indec_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN localidades AS loc
ON dd.nombre_departamento_indec_2 = loc.departamento_nombre_2 AND dd.nombre_provincia_indec_2 = loc.provincia_nombre_2
WHERE dd.codigo_departamento_indec != loc.departamento_id OR dd.id_provincia_indec != loc.provincia_id
"""
# hay que corregir el caso de USUAHIA
# El codigo 'real' es el de localidades censales, fuente: wikipedia
print(sql^ DiccionarioDepto)

# Unimos las tablas segun los codigos de departamento y provincia
# comparamos los nombres de departamentos en los casos que los codigos
# coinciden
DiccionarioDepto = """
SELECT DISTINCT dd.nombre_departamento_indec_2, loc.departamento_nombre_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN localidades AS loc
ON dd.codigo_departamento_indec = loc.departamento_id AND dd.id_provincia_indec = loc.provincia_id
WHERE dd.nombre_departamento_indec_2 != loc.departamento_nombre_2 OR dd.nombre_provincia_indec_2 != loc.provincia_nombre_2
"""

print(sql^ DiccionarioDepto)
# Hay 9 casos que solucionar


#Chequeo que los departamentos de padron esten incluidos en localidades
col1_df1 = padron['departamento']
col1_df2 = localidades['departamento_nombre_2']
col2_df2 = localidades['municipio_nombre_2']
col3_df2 = localidades['nombre_2']

valores_unicos_df1 = set(col1_df1)
valores_unicos_c1_df2 = set(col1_df2)
valores_unicos_c2_df2 = set(col2_df2)
valores_unicos_c3_df2 = set(col3_df2)

valores_en_df1 = valores_unicos_df1.difference(valores_unicos_c1_df2)
valores_en_df1 = valores_en_df1.difference(valores_unicos_c3_df2)

i=0
for departamento in col1_df1:
  if departamento in valores_en_df1:
    i+=1
print(i,"/",len(col1_df1))
#hay 156 departamentos en padron que no corresponden a nombres de departamento,
#municipio o localidad en localidades censales.

# A cada departamento en padron le asignamos su codigo correspondiente
padron_provincia=sql^"""
SELECT DISTINCT p.*, prov.provincia_nombre_2 AS provincia
FROM padron as p
INNER JOIN provincia AS prov
ON p.provincia_id = prov.provincia_id
"""

padron = sql^"""
SELECT DISTINCT p.*, loc.departamento_id
FROM padron_provincia as p
LEFT OUTER JOIN localidades AS loc
ON p.departamento = loc.departamento_nombre_2 AND p.provincia = loc.provincia_nombre_2
"""


padron = sql^"""
SELECT DISTINCT p.id_registro, p.provincia_id, p.departamento,
                    p.localidad, p.categoria_id, p.Certificadora_id, p.razon_social, 
                    p.establecimiento, loc.departamento_id,p.departamento_id
FROM padron as p
LEFT OUTER JOIN localidades AS loc
ON p.departamento = loc.nombre_2 AND p.provincia = loc.provincia_nombre_2 AND p.departamento_id IS NULL
"""

padron['departamento_id'].value_counts().sum()
padron['departamento_id'] = padron['departamento_id'].fillna(0)
padron['departamento_id_2'] = padron['departamento_id_2'].fillna(0)
padron['departamento_id_3']=padron['departamento_id']+padron['departamento_id_2']

padron['departamento_id_3'].value_counts()

#vemos si hay localilades con dos departamentos distintos en la misma provincia(tuplas espureas)´
padron['id_registro'].value_counts()
padron[padron['id_registro']==983]
padron[padron['id_registro']==10]
#Los eliminamos
filtro = padron['departamento'] != 'LOS CARDALES'
padron = padron[filtro]

