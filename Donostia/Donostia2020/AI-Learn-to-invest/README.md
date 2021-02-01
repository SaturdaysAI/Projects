# AI Learn to invest - for Saturdays AI Euskadi.

## Machine Learning project applied to make investing easier to understand for newbies.

### 1. Investing ratios webscrapping. 
We have scrapped with beautifoulSoup investing data related to the companies selected from NYSE market. 

### 2. Dataset creation.
We have randomly simulated 500.000 investments in the last 10 years with a horizon between 1 day and 2 years.  The dataset has been cleaned and prepared for machine-learning modelling by applying categorization or normalization techniques among others. Resulting dataset has been saved into 'datasets/transactions_variables.csv' if you want to use it. 

### 3. Data Modelling and optimization. 
After screening with pycaret which classification models were better for our problem, we have selected Decission Trees for its easier interpretation. Keep in mind that our goal is not to make better investments but to make investment accessible to a broader spectrum of people. 
Decission tree has been optimized and results have been visualized thanks to Graphviz. 

### 4. Data Deployment and test on REST API server. 
The last step of this project has been to test our model in a postman REST API server. For doing this we have deployed the decission tree classifier developped on step 3 and we have launched a Flask server. Thanks to postman, we have send a couple of json objects corresponding to two lines of the general dataset and we have received correctly their classifications as GOOD or BAD investment. 

Further work will be to make this from user inputs and present our results with the pedagogical information on a web application.

