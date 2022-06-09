# Project “Monta” - EValuating Charge Points

We start by exporting two datasets:
  1. Charge_points(dfpoints), dataset containing the information about charge
points in Denmark. The dataset contains these rows: Charge point ID, Name, Visibility, Charge count, total kWh, Address, City, Created at, latitude and longitude.
  2. Charges(dfcharge) dataset contains these columns: Charge_ID, State, Vehicle, kwh limit, Charge_point_id, kwh, price, currency, created, failed_at, stopped_by_user, start_after, team_price_group, soc, cable_plugged_in_at, soc_source, last_stop_attempt_at, socs, soc_start.

To match the two datasets we use Charge_point_id column, we can assign every charge to a dedicated charge point using **dfcharge['charge point id'].isin(dfpoints['id']).value_counts()**

Now we have 28196 out of 28919 rows of charges matching to charge points and we assign it to dfcharge.
We filter the dfpoints dataset by “visibility” to see only the public charge points and we have 15100 rows left.

Additionally, we clean our data by dropping unusable columns (soc source, soc start, promotion code) and we filter out charges that have start (cable_plugged_in_at) and stop (last_stop_attempt_at) times and create a new dataframe called df_charge3.

Now since we have the start and stop times of some of the charges, we use astype(‘datetime63[ns]’) to change it to the right time format, in order to help us find the duration of each charge from df_charge4 dataframe.

We create a new column ‘duration’ and calculate the duration by subtracting “cable plugged in at” from “last stop attempt at”.
Now it’s time to visualize the data using boxplots. We start with the newly created ‘duration’ column.
We use seaborn to visualize. Following, we calculate the quantiles and interquartile values.
Afterwards, we get a return of the boolean array of the rows with any non-outlier column value.

And later we filter out the dataframe based on the condition created and save it in the new df_charge5 dataframe.

After analyzing the data frames we are leaning to a hypothesis that 80% of the charges were made by only 20% of the charge points.

We are filtering the data frame once again, eliminating the private charge points and keeping only those that have more than one charge registered on them.

Moving forward, we import shapely.geometry, geopandas and GeoDataFrame. These libraries will enable us to map out the charge points and their activity based on our data frames.

We would map out the charge points and their charging activity based on time and location.

Location can be accurately displayed using the longitude ‘lng' and latitude ‘lat', and time will be displayed using existing timestamps.

Rest of the data frame(let's say df_charges6), without timestamps will be calculated manually by finding the average speed of chargers from the previous dataset and then by dividing the ‘kwh’ field in df_charges6 by the average speed that we found on dataset with the timestamps.

As we have later discovered, our dataset wasn’t sufficient enough to predict or solve the initial problem or question, we have changed our direction somewhere around at this point.

With the datasets we had until this point, we have created some violin plot graphs to visualize charge duration in minutes and total kilowatt hours per charge. After analyzing these graphs we decided to separate our results based on the city, because we noticed that some city names are duplicated.

After the data sorted by cities were combined, we started consolidating the top ten cities. The cities are Copenhagen, Århus, Aalborg, Odense, Frederiksberg, Randers, Esbjerg, Kolding, Vejle, Horsens.
With the combined dataset of ten biggest cities we then started to explore the trends among them in terms of charge point usage.

We have also exported the combined dataset as df_combined to a csv file.
At this point we have stopped exploring and cleaning data, now we moved on to the machine learning algorithm, clustering method.

To start off with clustering, we import numpy, pandas, plotly.graph_objects and plotly.express for visualizing.
Then we import df_charge dataset, we leave charge_points dataset to be added after the clustering is done because we want it for the analysis and not the algorithm itself, for instance histogram of cluster by any value from charge_points dataset.
Now, to continue with clustering we add coordinates. Before dropping charge_point_id we use it to concatenate the coordinates into the dataset.
[225]
We continue to prepare the dataset for clustering by dropping the unnecessary columns, such as state, vehicle, et cetera.
Afterwards we add dummies and we import sklearn.decomposition and matplotlib.pyplot. Now we start to use principal component analysis using our previously imported sklearn.decomposition to get a graph which we draw as ‘number of components’ on X axis and ‘cumulative explained variance’ on Y. Now we continue by creating a scatter plot of the components and we see our first clustering results.
From sklearn.cluster we import KMeans to further improve our model, we use it for the elbow method.
“The elbow method runs k-means clustering on the dataset for a range of values for k (say from 1-10) and then for each value of k computes an average score for all clusters. By default, the distortion score is computed, the sum of square distances from each point to its assigned center.” - as explained in Yellowbrick v1.4 documentation.
