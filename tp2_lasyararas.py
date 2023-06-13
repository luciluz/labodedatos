#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# Laboratorio de Datos - TP 2
# Clasificación y validación cruzada
# Autores: Altamirano Ailen, Rio Francisco, Ruz Veloso Luciano
# --------------------------------------------------------------
# ********************** las_yararas ***************************

# Impotamos bibliotecas necesarias
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
#%%
def columnaACoordenada(n):
    """ Funcion que dada un numero de columna devuelve
    la coordenada de pixel correspondiente a la imagen 28x28"""
    return (n//28, n%28)

def CoordenadaAColumna(fila, columna):
  """ Funcion que dada una coordenada devuelve
    el número de columna donde está ese valor"""
    return fila*28 + columna
#%%
################################ Carga del dataframe ########################################
df = pd.read_csv('mnist_desarrollo.csv', header = None)
#%%
#################################Ejercicio 1 ################################################
# 1. Realizar un análisis exploratorio de los datos. Ver, entre otras cosas,
# cantidad de datos, cantidad y tipos de atributos, cantidad de clases de la
# variable de interés (el dígito) y otras características que consideren
# relevantes. ¿Cuáles parecen ser atributos relevantes? ¿Cuáles no? Se
# pueden hacer gráficos para abordar estas preguntas.

####### Exploración del df
df.head()
df.info()

# La primer columna corresponde a los digitos que se representan en cada imagen
df[0].value_counts()

# Grafico de cuantos registros corresponden a cada dígito
df[0].value_counts().sort_index().plot(kind='bar')
plt.xlabel('Dígito')
plt.ylabel('Cantidad de registros')
plt.show()

# Exploramos la cantidad de filas y columnas del df
df.shape
# La tabla tiene 60000 registros
# Y tiene 784 atributos, correspondientes a cada pixel de la imagen


## Análisis de atributos

## Se quiere ver si los bordes son relevantes o no

primeraFila = df.iloc[:, 1:29].values.flatten()
primeraColumna = df.iloc[:, 1::28].values.flatten()
ultimaFila = df.iloc[:, 757:].values.flatten()
ultimaColumna = df.iloc[:, 1:29].values.flatten()

borde_count = pd.Series(
    [*primeraFila, *primeraColumna, *ultimaFila, *ultimaColumna]
)

borde_count.value_counts()

# En todo el borde, 6717742/6720000 registros el unico valor es cero
# Estos atributos no resultarian informativos


# Calculamos y graficamos la correlacion entre los distintos atributos 
X = df.iloc[:, 1:]

#correlacion = X.corr(method = 'spearman') # spearman es no parametrico, no requiere que los datos sigan dist. normal
#sns.heatmap(correlacion)
#plt.show()
# Todo lo blanco representa coeficientes de correlacion muy alta en todos los digitos,
# no son atributos que aporten info para diferenciarlos

# %%
################################## Ejercicio 2 #############################################
# 2. Construir un dataframe con el subconjunto que contiene solamente los
# dígitos 0 y 1.
unos_o_ceros = (df[0] == 1) | (df[0] == 0) # Filtro 
df = df[unos_o_ceros] # Aplico el filtro
# %%
################################# Ejercicio 3 ##############################################
# Para este subconjunto de datos, ver cuántas muestras se tienen y determinar 
# si está balanceado entre las clases.
muestras_totales = df.shape[0]

# Cantidad de muestras por clase
conteos = df[0].value_counts()
muestras_uno = conteos[1]
muestras_cero = conteos[0]

# Calculo proporciones correspondientes a cada clase
proporcion_uno = muestras_uno/muestras_totales
proporcion_cero = muestras_cero/muestras_totales

print('Proporcion de ceros en el subconjunto de los datos: ', proporcion_cero)
print('Proporcion de unos en el subconjunto de los datos: ', proporcion_uno)

# %% 
################################# Ejercicio 4 ####################################
# Ajustar un modelo de knn considerando pocos atributos, por ejemplo 3.
# Probar con distintos conjuntos de 3 atributos y comparar resultados.
# Analizar utilizando otras cantidades de atributos

#### Busqueda de atributos que parezcan relevantes para clasificar en
## 0 o 1
# Heatmap para 0 y 1

#  Pensamos que puede ser relvante el pixel central 
CoordenadaAColumna(13,14) # 378
# el df tiene una columna extra --> la etiqueta, le sumamos 1 a los valores
# que devuelve a funcion
df.iloc[:,379]
# Buscamos pixeles alrededor de ese 
CoordenadaAColumna(14,14) # 406 +1 = 407
CoordenadaAColumna(15,14) # 435

# Pixeles en diagonal
CoordenadaAColumna(17, 19) # 496
CoordenadaAColumna(10, 12) # 293
CoordenadaAColumna(13, 6)  # 370

# Exploramos dicho pixel y pixeles a su alrededor
plt.subplot(2, 3, 1)
sns.kdeplot(data = df , x = 379 , hue = 0).set(xlabel = 'Intensidad', title = 'Columna 379')
plt.grid()
plt.subplot(2, 3, 2)
sns.kdeplot(data = df , x = 407 , hue = 0).set(xlabel = 'Intensidad', title = 'Columna 407')
plt.grid()
plt.subplot(2, 3, 3)
sns.kdeplot(data = df , x = 435 , hue = 0).set(xlabel = 'Intensidad', title = 'Columna 435')
plt.grid()
plt.subplot(2, 3, 4)
sns.kdeplot(data = df , x = 371 , hue = 0).set(xlabel = 'Intensidad', title = 'Columna 371')
plt.grid()
plt.subplot(2, 3, 5)
sns.kdeplot(data = df , x = 293 , hue = 0).set(xlabel = 'Intensidad', title = 'Columna 293')
plt.grid()
plt.subplot(2, 3, 6)
sns.kdeplot(data = df , x = 496 , hue = 0).set(xlabel = 'Intensidad', title = 'Columna 496')
plt.grid()
plt.show()

# Grafico de puntos posteriormente elegidos para KNN
columnaACoordenada(495)
columnaACoordenada(292)
columnaACoordenada(370)
columnaACoordenada(435)

img = np.array(X.iloc[1222]).reshape((28,28))
plt.imshow(img, cmap='gray')
puntos_x = [14, 19, 12, 6, 15]
puntos_y = [13, 17, 10, 13, 15]
plt.scatter(puntos_x,puntos_y,color='red')
plt.show()
print(df.iloc[1222, 0])

img = np.array(X.iloc[1000]).reshape((28,28))
plt.imshow(img, cmap='gray')
puntos_x = [14, 19, 12, 6, 15]
puntos_y = [13, 17, 10, 13, 15]
plt.scatter(puntos_x,puntos_y,color='red')
plt.show()
print(df.iloc[1000, 0])

######################## Modelos KNN ######################################
# Usamos knn probando con combinaciones de 3 atributos
Nrep = 5
valores_atributos = [[379,407,435],[351,379,407],[378,379,380],[406,407,408],[350,380,408]]
Y = df.iloc[:, 0]

Nrep = 5

resultados_test = np.zeros((Nrep, len(valores_atributos)))
resultados_train = np.zeros((Nrep, len(valores_atributos)))

# Para probar usamos k = 5

for n,lista_atributos in enumerate(valores_atributos):
  X = df.iloc[:,lista_atributos]
  for i in range(Nrep):
          k=5
          X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
          model = KNeighborsClassifier(n_neighbors = k)
          model.fit(X_train, Y_train) 
          Y_pred = model.predict(X_test)
          Y_pred_train = model.predict(X_train)
          acc_test = metrics.accuracy_score(Y_test, Y_pred)
          acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
          resultados_test[i, n] = acc_test
          resultados_train[i, n] = acc_train
        
# Como las columnas representan las distintas combinaciones de atributos
# Hay que promediar los valores de accuracy c/columna
promedios_train = np.mean(resultados_train, axis = 0) 
promedios_test = np.mean(resultados_test, axis = 0) 

# El valor mas alto de accuracy se obtuvo usando [379,407,435]

# Usamos knn probando con combinaciones de hasta 5 atributos
Nrep = 5
valores_atributos = [[293,292,265],[379,407,435,293],[496,293,371,435], [496,293,379,435], [496,293,371,379,435], [379, 380, 407, 408]]
Y = df.iloc[:, 0]

resultados_test = np.zeros((Nrep, len(valores_atributos)))
resultados_train = np.zeros((Nrep, len(valores_atributos)))

# Para probar usamos k = 5

for n,lista_atributos in enumerate(valores_atributos):
  X = df.iloc[:,lista_atributos]
  for i in range(Nrep):
          k=5
          X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
          model = KNeighborsClassifier(n_neighbors = k)
          model.fit(X_train, Y_train) 
          Y_pred = model.predict(X_test)
          Y_pred_train = model.predict(X_train)
          acc_test = metrics.accuracy_score(Y_test, Y_pred)
          acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
          resultados_test[i, n] = acc_test
          resultados_train[i, n] = acc_train
        
promedios_train = np.mean(resultados_train, axis = 0) 
promedios_test = np.mean(resultados_test, axis = 0)
# Maximo en test se obtiene con [496,293,371,379,435]
#%% 
######################### EJERCICIO 5 ###########################
# Para comparar modelos, utilizar validación cruzada. Comparar modelos
# con distintos atributos y con distintos valores de k (vecinos). Para el análisis
# de los resultados, tener en cuenta las medidas de evaluación (por ejemplo,
# la exactitud) y la cantidad de atributos

# Utilizamos la mejor combinacion de atributos que encontramos 
# (aquella con la que se obtiene accuracy mayor en test, [496,293,371,435])
# para buscar el mejor valor de k con validacion cruzada
nsplit = 5
valores_k = range(1,15)
X = df.iloc[:,[496,293,371,379,435]]

resultados_test = np.zeros((nsplit, len(valores_k)))
resultados_train = np.zeros((nsplit, len(valores_k)))

skf = StratifiedKFold(n_splits=nsplit, shuffle=True)

for i, (train_index, test_index) in enumerate(skf.split(X, Y)):
    x_train_fold, x_test_fold = X.iloc[train_index,:], X.iloc[test_index,:]
    y_train_fold, y_test_fold = Y.iloc[train_index], Y.iloc[test_index]
    for k in valores_k:
        model = KNeighborsClassifier(n_neighbors = k)
        model.fit(x_train_fold, y_train_fold) 
        Y_pred = model.predict(x_test_fold)
        Y_pred_train = model.predict(x_train_fold)
        acc_test = metrics.accuracy_score(y_test_fold, Y_pred)
        acc_train = metrics.accuracy_score(y_train_fold, Y_pred_train)
        resultados_test[i, k-1] = acc_test
        resultados_train[i, k-1] = acc_train
        
promedios_train = np.mean(resultados_train, axis = 0) 
promedios_test = np.mean(resultados_test, axis = 0) 

plt.plot(valores_k, promedios_train, label = 'Train')
plt.plot(valores_k, promedios_test, label = 'Test')
plt.legend()
plt.xlabel('Cantidad de vecinos')
plt.ylabel('Accuracy')
plt.grid()
plt.show()
# Max con 3 vecinos
# %%
############################ EJERCICIO 6 ###############################
# Trabajar nuevamente con el dataset de todos los dígitos. Ajustar un
# modelo de árbol de decisión. Analizar distintas profundidades

# Cargamos nuevamente el df
df = pd.read_csv('mnist_desarrollo.csv', header = None)
X = df.iloc[:,1:]
Y = df.iloc[:, 0]

#Evaluo con las siguientes profundidades y criterios
depth = [4,6,8,10,11,12,13,14]
criterio = ['entropy', 'gini']
comb = [(d,c) for d in depth for c in criterio]

resultados_test = np.zeros((nsplit, len(valores_k)))
resultados_train = np.zeros((nsplit, len(valores_k)))

skf = StratifiedKFold(n_splits=nsplit, shuffle=True)

dicc = {combinacion: [[],[]] for combinacion in comb}


for i, (train_index, test_index) in enumerate(skf.split(X, Y)):
    #Separar data en train y test
    x_train_fold, x_test_fold = X.iloc[train_index,:], X.iloc[test_index,:]
    y_train_fold, y_test_fold = Y.iloc[train_index], Y.iloc[test_index]

    for depth, criterio in comb:
            clf_info = tree.DecisionTreeClassifier(criterion = criterio, max_depth= depth)
            clf_info = clf_info.fit(x_train_fold, y_train_fold)
            
            # Predicciones para el set test
            pred_test = clf_info.predict(x_test_fold)
          
            # Calculo accuracy usando el set de test
            score_test = metrics.accuracy_score(y_test_fold, pred_test)
            print('Para un arbol con profundidad maxima ', depth,\
                  'y criterio ', criterio, '\nAccuracy en test:', score_test)
            
            # Calculo accuracy para el set train (espero que aumente conforme aumenta
            # la complejidad del modelo)
            pred_train = clf_info.predict(x_train_fold)
            score_train = metrics.accuracy_score(y_train_fold, pred_train)
            print('Accuracy en train:', score_train, '\n')

            #Guardo los resultados en dicc
            dicc[(depth, criterio)][0].append(score_test)
            dicc[(depth, criterio)][1].append(score_train)

promedios = {combinacion: [] for combinacion in comb}

for key in promedios.keys():
     promedios[key].append(sum(dicc[key][0])/len(dicc[key][0])) # Accuracy promedio en test
     promedios[key].append(sum(dicc[key][1])/len(dicc[key][1])) # Accuracy promedio en train

df_promedios = pd.Series(promedios).reset_index()
df_promedios.columns = ['Profundidad', 'Criterio', 'Promedios']   
df_promedios[['Accuracy_test','Accuracy_train']] = pd.DataFrame(df_promedios.Promedios.tolist(), index= df_promedios.index)
df_promedios

# Grafico
sns.lineplot(x = 'Profundidad', y = 'Accuracy_test',  data=df_promedios, hue='Criterio')
plt.text(10, 0.82, "Test", horizontalalignment='left', size='medium', color='black', weight='semibold')
sns.lineplot(x = 'Profundidad', y = 'Accuracy_train',  data=df_promedios, hue='Criterio', linestyle='--', legend = None)
plt.text(12, 0.93, "Train", horizontalalignment='left', size='medium', color='black', weight='semibold')
plt.ylabel('Accuracy')
plt.grid()
plt.show()

Documento de Ailu Altamirano.py
Mostrando Documento de Ailu Altamirano.py
