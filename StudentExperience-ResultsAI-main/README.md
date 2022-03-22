# Student Experience and Results AI
### A project from SaturdaysAI
## Authors:
- [Iñaki Fernández López-zuazo](https://github.com/InakiFLZ)
- [Rubén García Pedrejón](https://github.com/rubengp39)
- [Gorka Legarreta Ibarra](https://github.com/GorkaLegarreta)

## [Medium Post](https://ilopezzuazo.medium.com/875f26677ebf)

## Motivation
We were presented with a dataset of surveys done by students of a university valorating their experience with teachers.
- The university student population is set to increase by 27% in 2035 compared to 2018 (GEPS).
- The average satisfaction of the university population is 6.4 (Studia XXI).
- Teacher influence is reflected in student academic achievement and performance (PISA).

## [DATASET](https://github.com/rubengp39/StudentExperience-ResultsAI/blob/main/encuestasv2.xlsx)
This dataset has over 20.000 surveys from 2015 to 2020. We can find four different categories between the attributes in this dataset:
- Precise answers

To evaluate the teacher knowledge, how he/she explains, metodology and feedback he/she gives.

- Average Score

The average of all the group, not individual score.

- Identifying information

Such as: Gender, Age range, Campus, Subject, Year ...

- Text Fields

Things the teacher should improve or mantain. Interesting for NLP.

## 1. EDA
#### Exploratory Data Analysis

We had a huge dataset created in different years and not very well kept. We had to delete NaN registers, make some changes in one model of education where there were three teachers at the same time and we wanted to have each information separated.

We also decided to group the scores given to the teachers in three groups by following the Net Promoter Score (Detractor 0-6, Passive 7-8 and Promotor 9-10) and the Average Score of the class (Suspense 0-5, Approved 6-7, Outstanding 8-10).

Correlations between teachers' grades
![image](https://user-images.githubusercontent.com/62309228/124256590-c596c080-db2b-11eb-8a44-2aa04cb4532d.png)

Age - Gender - Average Grade Variation

![image](https://user-images.githubusercontent.com/62309228/124256764-f4149b80-db2b-11eb-9a29-02afcda150c0.png)


## 2. Supervised Learning
### Linear Regresion

We chose the main four variables, "Explicar", "Conocer", "Metodología" and "Feed_back" to train with the "General" score of the professor so we could predice what score would they get.

For that we used linear regression method, Lasso and Ridge and we got our best score with Ridge with a 67% score.

![image](https://user-images.githubusercontent.com/62309228/124259436-cc730280-db2e-11eb-824f-98be2212a678.png)


### Asociation Rules

To know if there is any relation between the average score of the group and a good teacher we implemented the apriory function from apyori. Then we chose the ones with a lift > 1 which are the ones who appear more often. We can conclude that if the group has a high average score then they will talk great about the teacher and if they have worst score they might be passive on their comments.

![image](https://user-images.githubusercontent.com/62309228/124260790-625b5d00-db30-11eb-980f-51a0811b8c3f.png)

### Decision Trees

Our first scores of decision trees were not very high, with a depth of 2 we only reached 35% but once we deepen a little bit more it increased.

The results where as expected and we saw that the score in Explain was the most important one.
![image](https://user-images.githubusercontent.com/62309228/124262409-4fe22300-db32-11eb-9ab4-f7a991390fce.png)

You can find deeper decision trees in the [notebook](https://github.com/rubengp39/StudentExperience-ResultsAI/blob/main/StudentExperience.ipynb).

## 3. Unsupervised Learning
### Clustering

We used the elbow rule to decide what was the most effective number of clusters.


![image](https://user-images.githubusercontent.com/62309228/124262253-19a4a380-db32-11eb-850b-037eb316eca9.png) ![image](https://user-images.githubusercontent.com/62309228/124262309-2b864680-db32-11eb-93c0-9f44a3ca59dc.png)


Some of the results were that only the groups with not great average score are the ones that gives less marks to the teachers.


## 4. NLP
#### Natural Language Processing

We had little time to work in NLP and our idea was to compare what marks will the student give to the teacher by studying the feedback they give, what they have to improve or what they have to maintain. We started counting what words were more used and wanted to compare and know if they were possitive comments or negative ones. We also encountered the problem that some of them were in different languages so we had to figure out how to work with it.

You can see some more insights in the [NLP document](https://github.com/rubengp39/StudentExperience-ResultsAI/blob/main/NLP-RESULTS.pdf).

# Conclusion

We have learned a lot both about Artificial Intelligence and Customer/Student Satisfaction and we want to give a shout out to all the group of SaturdaysAI Bilbao who have worked really hard and have shared their experience with us.
