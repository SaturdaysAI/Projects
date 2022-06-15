import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(11.7,8.27)})

from utils import *


mediciones = integratemetadata()

hours = ["H01","H02","H03","H04","H05","H06","H07","H08","H09","H10","H11","H12","H13","H14","H15","H16","H17","H18","H19","H20","H21","H22","H23","H24"]

long_mediciones = pd.melt(mediciones, id_vars=['ESTACIO', 'CONTAMINANTE', 'ANY','MES', 'DIA' ], value_vars=hours)

print(long_mediciones.head())
a = sns.FacetGrid(long_mediciones, col="ESTACIO", row="ANY")
a.map(sns.barplot, x='CONTAMINANTE', y='value', data=long_mediciones)
plt.savefig('any.png', dpi=900)

#m = sns.FacetGrid(long_mediciones, col="ESTACIO", row="mes")
#m.map(sns.barplot, x='CONTAMINANTE', y='value', data=long_mediciones)
#plt.savefig('mes.png', dpi=900)


