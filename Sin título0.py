import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

df = pd.read_csv('./datos_clase_clustering.csv')

df.columns

df['ppm'] = df['price']/df['surface_covered']

sns.scatterplot(data = df, x = 'lon', y = 'lat', hue = 'ppm' )
plt.show()
plt.close()

#####
k = 3
X = df[['surface_covered', 'price']].values
kmeansps = KMeans(n_clusters=k, random_state=0)
kmeansps.fit(X)
df['cluster'] = kmeansps.labels_

sns.scatterplot(data = df, x = 'lon', y = 'lat', hue = 'cluster' )
plt.close()

################### LA MEJOR OPCION #############################
k = 3
X = df[['ppm']].values
kmeansps = KMeans(n_clusters=k, random_state=0)
kmeansps.fit(X)
df['cluster'] = kmeansps.labels_

sns.scatterplot(data = df, x = 'lon', y = 'lat', hue = 'cluster' )
plt.show()
plt.close()

sns.scatterplot(data = df, x = 'surface_covered', y = 'price', hue = 'cluster' )
plt.show()
plt.close() # Es como agrepar por la pendiente!
################################################################
k = 4
X = df[['ppm']].values
kmeansps = KMeans(n_clusters=k, random_state=0)
kmeansps.fit(X)
df['cluster'] = kmeansps.labels_

sns.scatterplot(data = df, x = 'lon', y = 'lat', hue = 'cluster' )
plt.show() # Horrendo
plt.close()

k = 3
X = df[['ppm', 'surface_total']].values
kmeansps = KMeans(n_clusters=k, random_state=0)
kmeansps.fit(X)
df['cluster'] = kmeansps.labels_

sns.scatterplot(data = df, x = 'lon', y = 'lat', hue = 'cluster' )
plt.show()
plt.close()

k = 4
X = df[['lat', 'lon']].values
kmeansps = KMeans(n_clusters=k, random_state = 0)
kmeansps.fit(X)
df['cluster'] = kmeansps.labels_

sns.scatterplot(data = df, x = 'lon', y = 'lat', hue = 'cluster' )
plt.show()
plt.close()