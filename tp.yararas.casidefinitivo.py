#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Importamos archivos necesarios
padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", index_col=0, encoding='latin-1')
salarios = pd.read_csv("~/Descargas/w_median_depto_priv_clae2.csv")
localidades = pd.read_csv("~/Descargas/localidades-censales.csv")
dicc_deptos = pd.read_csv("~/Descargas/diccionario_cod_depto.csv")
dicc_clases = pd.read_csv("~/Descargas/diccionario_clae2.csv")
rubro_clae = pd.read_csv("~/Descargas/Rubro_clae.csv")

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

# Asigno el codigo de departamento correspondiente a CABA
padron.loc[padron['departamento'] == 'CIUDAD AUTONOMA BUENOS AIRES', 'departamento_id_3'] = 2000

padron[padron['departamento_id_3']== 2000][['departamento', 'departamento_id_3']]

# Veo cuantos nulls quedaron finalmente en la columna departamento_id_2
print('Antes de corregir los departamentos que son localidades:\n')
print(sql^"""
SELECT count(*) AS departamentos_sin_codigo
FROM padron
WHERE departamento_id = 0
""")
print('\nDespues de la corrección:\n')
print(sql^"""
SELECT count(*) AS departamentos_sin_codigo
FROM padron
WHERE departamento_id_3 = 0
""")


# Decidimos eliminar los registros a los que no les podemos asignar un codigo
# de departamento

print(padron.shape)
padron = sql^"""
SELECT DISTINCT p.id_registro, p.provincia_id, p.departamento,
                    p.localidad, p.categoria_id, p.Certificadora_id, p.razon_social, 
                    p.establecimiento, p.departamento_id_3
FROM padron as p
WHERE p.departamento_id_3 != 0
"""
print(padron.shape)

# Limpieza de los datos de salarios
salarios['w_median'].value_counts()
salarios[salarios['w_median'] == -99] = np.nan

# checkeo
salarios['w_median'].value_counts()
salarios[salarios['w_median'] == -99]

# Queremos que todos los registros de salario tengan fecha
# cuantos registros hay que tengan na en fecha
salarios['fecha'].isna().sum()

# decidimos eliminar estos registros
salarios = salarios.dropna(subset=['fecha'])
salarios['fecha'].isna().sum()

###################################################################
# pregunta i

# i (están todas las provincias)
provincias_con_operadores = sql^"""
SELECT DISTINCT provincia_id
FROM padron
"""
provincias_con_operadores = sql^"""
SELECT DISTINCT count(*)
FROM provincias_con_operadores
"""
provincias_con_operadores


# ii 
departamentos_sin_operadores = sql^"""
SELECT DISTINCT l.departamento_nombre_2, l.departamento_id
FROM localidades AS l
LEFT OUTER JOIN padron AS p
ON p.provincia_id = l.provincia_id AND l.departamento_id = p.departamento_id_3
WHERE p.id_registro IS NULL
"""
# Hay 307 departamentos sin operadores, datos en departamentos_sin_operadores

# TEST consulta ii
#departamentos_sin_operadores[departamentos_sin_operadores['departamento_nombre_2'] == 'AVELLANEDA']
#padron[padron['departamento'] == 'AVELLANEDA' ]

# iii
# Consideramos los rubros como actividades
rubro['rubro'].value_counts()
# fruticultura (432)

# iv
# Buscamos el clae2 que corresponde al rubro fruticultura
rubro_clae[rubro_clae['rubro'] == 'FRUTICULTURA']
# clae de fruticultura es 1
promedio_2022_1 = sql^"""
SELECT avg(w_median)
FROM salarios
WHERE clae2 = 1 AND fecha LIKE '2022-12-01'
"""
#v 
salarios = sql^"""
SELECT *, SUBSTRING(fecha, 1, 4) AS anio
FROM salarios
"""

promedio_anual_pais = sql^"""
SELECT anio, avg(w_median) AS promedio_anual, stddev(w_median) AS desvio_anual
FROM salarios
GROUP BY anio
ORDER BY anio ASC
"""
salarios['id_provincia_indec'].isna().sum()
salarios.shape
# como la columna id_provincia_indec tiene ~0.36% valores nulos
# decidimos eliminar esos valores para realizar la siguiente consulta
salarios = salarios.dropna(subset=['id_provincia_indec'])
salarios['id_provincia_indec'].isna().sum()

promedio_anual_provincia = sql^"""
SELECT id_provincia_indec, p.provincia_nombre_2, anio, avg(w_median) AS promedio_anual, stddev(w_median) AS desvio_anual
FROM salarios AS s
JOIN provincia AS p
ON s.id_provincia_indec = p.provincia_id
GROUP BY s.anio, s.id_provincia_indec, p.provincia_nombre_2
ORDER BY anio ASC, p.provincia_nombre_2 ASC
"""
# ajutar por la inflacion
# fuente externa: datos de inflación anual


#### GRAFICOS
# Grafico 1

# plot a bar chart
conteo_provincia = pd.DataFrame(padron['provincia_id'].value_counts())
conteo_provincia.reset_index(inplace= True)
conteo_provincia.columns = ['id_provincia', 'Cantidad']

# ahora unimos conteo_provincia con provincia segun su id
conteo_provincia = sql^"""
                        SELECT p.provincia_nombre_2 AS Provincia, c.Cantidad
                        FROM conteo_provincia AS c
                        JOIN provincia AS p
                        ON p.provincia_id = c.id_provincia
                       """
                       
                       
plt.figure(figsize=(13, 7))
ax = sns.barplot(
    x="Cantidad", 
    y="Provincia", 
    data=conteo_provincia, 
    estimator=sum, 
    ci=None, 
    color='#B6D6CC');   
    
for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{width:.2f}', (x + width, y + height/2), ha='left', va='center')

plt.show()
plt.close()                 

# Grafico 2
conteo_productos = pd.DataFrame(productos['id_registro'].value_counts())
conteo_productos.reset_index(inplace= True)
conteo_productos.columns= ['id_registro', 'Cantidad_productos']

# Unimos conteo_productos con padron segun id_registro
conteo_productos = sql^"""
                        SELECT p.provincia_id, c.Cantidad_productos
                        FROM conteo_productos AS c
                        JOIN padron AS p
                        ON p.id_registro = c.id_registro
                       """

#conteo_provincia['provincia_id'].value_counts().shape

# Usamos el id de cada provincia para determinar su nombre
conteo_productos = sql^"""
                        SELECT p.provincia_nombre_2 AS Provincia, c.Cantidad_productos
                        FROM conteo_productos AS c
                        JOIN provincia AS p
                        ON p.provincia_id = c.provincia_id
                       """

# boxplot
plt.figure(figsize=(10, 7))
ax = sns.boxplot(y='Provincia', x='Cantidad_productos', data=conteo_productos, 
                 showfliers = False, orient = 'h')
# agregar puntos individuales
ax = sns.stripplot(y='Provincia', x='Cantidad_productos',
                   data=conteo_productos, color="grey", jitter=0.2, size=2.7,
                   orient = 'h')

# agregar titulo al grafico
plt.title("Boxplot de cantidad de productos por operador por provincia", loc="left")

# Agregar titulos a los ejes
ax.set(xlabel='Cantidad de Productos', ylabel='Provincia')

plt.show()

# Grafico 3


