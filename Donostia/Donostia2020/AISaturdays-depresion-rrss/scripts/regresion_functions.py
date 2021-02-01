import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from scipy import stats
import scipy.stats as stats
from scipy.stats import kstest


# La función "printHistograms" genera los histogramas de todos los indicadores del estudio.
# Útil para ver de forma gráfica, en un único vistazo, la distribución de los indicadores.

def printHistograms(data, pColor):

	sns.set_style("white")
	sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})
	data.plot.hist(subplots=True, layout=(2, 4), figsize=(15, 8), sharey=True,colormap=pColor)
	sns.despine()


# La función "printMatrixDiagram" genera gráficas de dispersión (2 a 2), involucrando todos los indicadores del estudio.
# Útil para ver de forma gráfica, en un único vistazo, los indicadores que están más correlacionados entre ellos.

def printMatrixDiagram(data):

	g = sns.PairGrid(data, height=1.2, corner=True)
	g.map_offdiag(sns.scatterplot)
	g.map_offdiag(sns.regplot)
	g.map_diag(plt.hist)


# La función "printPearsonCorrelations" genera un mapa de calor de las correlaciones de Pearson entre todos los indicadores del estudio.
# Útil para ver, en un único vistazo, los indicadores que están más correlacionados entre ellos y si hay multicolinealidad.

def printPearsonCorrelations(data):

	corr = data.corr()
	plt.figure(figsize = (10,10))
	cmap = sns.diverging_palette(220, 10, as_cmap=True)
	np.tril(np.ones(corr.shape)).astype(np.bool)[0:5, 0:5]
	corr2=corr.where(np.tril(np.ones(corr.shape)).astype(np.bool))
	sns.heatmap(corr2, xticklabels=corr.columns.values, yticklabels=corr.columns.values, annot=True, cmap=cmap, vmax=1, vmin=-1,center=0, square=True, linewidths=.5, cbar_kws={"shrink": .82})
	plt.title('Heatmap of Correlation Matrix')
	plt.show()


# La función "calculateRegression" ajusta un modelo de regresión lineal.
# Utiliza el método de estimación "backward", ya que a partir del modelo saturado con todas las variables independientes
# disponibles, va eliminando, una a una, dichas variables cuyo p-value > alpha (baja capacidad explicativa).
# La función utiliza un 80% de los datos para los ajustes, y reserva un 20% de los datos para los testeos.
# Además, calcula el RootMeanSquareError (RMSE) y el Coeficiente de Determinación (R2) para todos los ajustes.

def calculateRegression(data, label, resultsummary, alpha):

	X_train, X_test, y_train, y_test = train_test_split(data, label, test_size = 0.2, random_state = 50)
	reg = LinearRegression() # Create the Linear Regression estimator
	result=reg.fit (X_train, y_train)  # Perform the fitting

	mod = sm.OLS(y_train,X_train)
	fitt = mod.fit()
	p_values = fitt.summary2().tables[1]['P>|t|']                         # P-values para decidir qué variables x son importantes para explicar y.
	p_value_max = p_values.idxmax()

	RMSE_Training = np.sqrt(np.mean((reg.predict(X_train) - y_train)**2))
	RMSE_Testing = np.sqrt(np.mean((reg.predict(X_test) - y_test)**2))
	R2_Training = reg.score(X_train, y_train)
	R2_Testing = reg.score(X_test, y_test)

	influence = fitt.get_influence()
	standardized_residuals = influence.resid_studentized_internal

	if(p_values[p_value_max] > alpha):
		data.drop(p_value_max, axis=1, inplace=True)
		iteration = resultsummary['iteration'].max()
		if(np.isnan(iteration)):
			iteration=0
		else:
			iteration = iteration+1
		newrow ={'iteration': iteration, 'intercept':reg.intercept_ , 'RMSE_Training': RMSE_Training,'RMSE_Testing':RMSE_Testing,
		'R2_Training':R2_Training,'R2_Testing':R2_Testing,'p_value_max':p_values[p_value_max],'removed_var':p_value_max}
		resultsummary = resultsummary.append(newrow, ignore_index=True)

		data_list = calculateRegression(data, label, resultsummary, alpha)

	else:
		iteration = resultsummary['iteration'].max()+1
		newrow ={'iteration': iteration, 'intercept':reg.intercept_ , 'RMSE_Training': RMSE_Training,'RMSE_Testing':RMSE_Testing,
		'R2_Training':R2_Training,'R2_Testing':R2_Testing,'p_value_max':p_values[p_value_max],'removed_var':'-'}
		resultsummary = resultsummary.append(newrow,ignore_index=True)
		resultsummary = resultsummary.round(3)
		print(resultsummary.head(20))
		print()
		print("Modelo Final")
		print(list(data.columns))
		print(reg.coef_, reg.intercept_)
		X_train, X_test, y_train, y_test = train_test_split(data, label, test_size = 0.2, random_state = 50)
		print('RMSE of Linear Regression Model with Training Data: {0:.2f}'.format(np.sqrt(np.mean((reg.predict(X_train) - y_train) ** 2))))
		print('RMSE of Linear Regression Model with Testing Data: {0:.2f}'.format(np.sqrt(np.mean((reg.predict(X_test) - y_test) ** 2))))
		print('R2 Coefficient for Linear Regression Model with Training Data: {0:.3f}'.format(reg.score(X_train, y_train)))
		print('R2 Coefficient for Linear Regression Model with Testing Data: {0:.3f}'.format(reg.score(X_test, y_test)))
		data_list=[X_train, X_test, y_train, y_test, standardized_residuals, fitt, RMSE_Training, R2_Training, RMSE_Testing, R2_Testing]

	return data_list


# La función "eliminateOutliers" elimina los residuos estandarizados considerados "altos" (menores que -3 y mayores que +3),
# de cara a realizar posteriormente nuevos ajustes sin estos datos que muchas veces distorsionan los resultados.
# La función imprime los datos eliminados, posibilitando un control de lo que se está eliminando.

def eliminateOutliers(X_train, y_train, standardized_residuals):

	Outliers = X_train[np.array((standardized_residuals > 3) | (standardized_residuals < -3))].index.tolist()

	data_train_withoutoutliers = X_train.drop(Outliers)

	label_train_withoutoutliers = y_train.drop(Outliers)

	print("Participantes Outliers Eliminados: {}".format(Outliers))

	data_list=[data_train_withoutoutliers, label_train_withoutoutliers]
	return data_list


# La función "repeatRegression" vuelve a ajustar el modelo de regresión lineal final ajustado en "calculateRegression",
# ahora para los datos libres de "outliers".
# Además, vuelve a calcular el RootMeanSquareError (RMSE) y el Coeficiente de Determinación (R2).

def repeatRegression(X_train, y_train, X_test, y_test, resultsummary):

	reg = LinearRegression() # Create the Linear Regression estimator
	result=reg.fit (X_train, y_train)  # Perform the fitting

	mod = sm.OLS(y_train, X_train)
	fitt = mod.fit()
	p_values = fitt.summary2().tables[1]['P>|t|']

	RMSE_Training = np.sqrt(np.mean((reg.predict(X_train) - y_train)**2))
	RMSE_Testing = np.sqrt(np.mean((reg.predict(X_test) - y_test)**2))
	R2_Training = reg.score(X_train, y_train)
	R2_Testing = reg.score(X_test, y_test)

	influence = fitt.get_influence()
	standardized_residuals = influence.resid_studentized_internal

	iteration = 0
	newrow = {'iteration': iteration, 'intercept': reg.intercept_, 'RMSE_Training': RMSE_Training,
			  'RMSE_Testing': RMSE_Testing,
			  'R2_Training': R2_Training,
			  'R2_Testing': R2_Testing
			  }
	resultsummary = resultsummary.append(newrow, ignore_index=True)
	resultsummary = resultsummary.round(3)

	print(resultsummary.head(1))
	print()
	print("Modelo Final Sin Outlier")
	print(list(X_train.columns))
	print(reg.coef_, reg.intercept_)
	print('RMSE of Linear Regression Model with Training Data: {0:.2f}'.format(
		np.sqrt(np.mean((reg.predict(X_train) - y_train) ** 2))))
	print('RMSE of Linear Regression Model with Testing Data: {0:.2f}'.format(
		np.sqrt(np.mean((reg.predict(X_test) - y_test) ** 2))))
	print('R2 Coefficient for Linear Regression Model with Training Data: {0:.3f}'.format(reg.score(X_train, y_train)))
	print('R2 Coefficient for Linear Regression Model with Testing Data: {0:.3f}'.format(reg.score(X_test, y_test)))

	data_list=[X_train, y_train, standardized_residuals, fitt, RMSE_Training, R2_Training, RMSE_Testing, R2_Testing]
	return data_list


# La función "residualAnalysis" realiza el test de normalidad (Kolmogorov-Smirnov) de los residuos estandarizados.
# Imprime también 3 gráficas: Gráfica de Dispersión entre "Predicción" y "Residuos Estandarizados",
# Histograma de los Residuos Estandarizados, y "Normal Q-Q Plot" de los Residuos Estandarizados.

def residualAnalysis(fitt, standardized_residuals):

	statistic,pvalue=kstest(standardized_residuals, 'norm')
	print('Estadística prueba normalidad Kolmogorov-Smirnov=%.3f, pvalue=%.3f\n' % (statistic, pvalue))
	if pvalue>0.05:
		print('Probablemente Normal')
	else:
		print('Probablemente No Normal')

	plt.figure(figsize=(12,4))

	plt.subplot(1, 3, 1)
	plt.scatter(fitt.predict(), standardized_residuals)
	plt.xlabel('Prediccion', fontsize=10)
	plt.ylabel('Residuo estandarizado', fontsize=10)
	plt.title('Gráfica de Residuos', fontsize=12)

	plt.subplot(1, 3, 3)
	plt.hist(standardized_residuals)
	plt.xlabel('Standardized Residuals', fontsize=10)
	plt.ylabel('Frequency', fontsize=10)
	plt.title('Histograma Residuos Estandarizados', fontsize=12)

	plt.figure(figsize=(3.6,3.6))
	stats.probplot(standardized_residuals, dist="norm", plot=plt)
	plt.title("Normal Q-Q Plot")

	plt.show()
