# R.O.A.D System

Classify type of activities with your Strava profile

guide lines Goal: classify bike lanes/roads based on gyroscope data to come up
with a sense on how safe they care. Labels!! Classes:

1. Bump
2. Pothole
3. …

First case: Geo-data +3D: Of a certain places is there any issue? -> indicate map
in a city -> potential out put A to B -> safety grade Classification routes

Second case: 3D Is there any issues -> classification -> x% of accuracy that a
sample in a specific kind of issue.

Steps to follow:

1. Append data set and get the mean -> df.app(type).mean()
2. Our research point is safety
3. Add a column to define the data for example CSV for bum give it B, CSV for
   pothole is P.
4. Distribute tasks between group members
5. Define the key factor for example in our case is the height -> Z ax -> up and
   down factor
6. - value is up to the level of the street
7. – value is down the level of the street
8. in cotrast to our project, the planet project use we use fixed length they
   use fourier transform==> the transformation will help use identifying the
   pattern. data effect of cyckling
9. we have an empirical example of using scipy-fft

https://realpython.com/python-scipy-fft/
