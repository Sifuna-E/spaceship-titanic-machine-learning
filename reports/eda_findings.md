# Independent Exploratory Data Analysis

## 1. Introduction

This analysis independently investigates passenger characteristics and their relationship with the `Transported` target variable in the Spaceship Titanic competition.

## 2. Dataset Overview

The training dataset contains 8,693 observations and 14 variables.

## 3. Categorical Variable Findings

### HomePlanet

<img width="2400" height="1500" alt="HomePlanet_relationship" src="https://github.com/user-attachments/assets/24103836-efa4-46ee-886d-73318a8e2bbc" />


### CryoSleep

<img width="2400" height="1500" alt="CryoSleep_relationship" src="https://github.com/user-attachments/assets/16fa7fc8-d6c7-4952-b756-64d7140a4509" />


### Destination

<img width="2400" height="1500" alt="Destination_relationship" src="https://github.com/user-attachments/assets/7712a131-db16-49c8-b476-761bcc376943" />


### VIP

<img width="2400" height="1500" alt="VIP_relationship" src="https://github.com/user-attachments/assets/55240b9c-62c2-40ac-b0ad-e2c5de474263" />


4. Age and Passenger Transportation

To see if there was an association between the likelihood of being transported and age, age was examined. The descriptive statistics show that passengers who were not transported had a mean age of 29.92 years and a median age of 27 years. Passengers who were transported had a mean age of 27.75 years and median age of 26 years, in contrast.

This means that the average age of transported passengers was a bit lower than that of those who were not transported. The difference between the two groups is, however, rather small. The mean ages of passengers who were and were not transported were 36.5 years and 37.1 years, respectively, with standard deviations of 13.70 years and 15.15 years, respectively. This indicates that there was a large range of age within each age group.

In general, age in itself offers a bit of information that could be helpful in predicting transportation status, but the small difference between the average and median ages indicates that it should not be used alone as a strong predictor. Its predictive ability needs to be considered in conjunction with other passengers traits.

5. Passenger Spending and Transportation

Five expenditure variables (RoomService, FoodCourt, ShoppingMall, Spa, VRDeck) were used to analyse the passenger expenditures. To compare spending between transported vs. non-transported passengers, the median was used due to the possibility of unusually high values in the data that could impact the mean.

The results reveal that the median of the spending values were in fact zero or near zero for both groups. If not transported, the median spending for passengers was: 1 for RoomService, 0 for FoodCourt, 0 for ShoppingMall, 4 for Spa, and 1 for VRDeck. The median was 0 for all five spending categories for transported passengers.

The results indicate that in both groups half or more of the passengers reported no expenditure (or very low expenditure) for most of the categories recorded. When compared using median spending values the differences between groups are not particularly high.

While there is not a significant difference in average expenditure on the day between those transported and those who were not transported, the variables of spending may provide some useful information. For instance, the distribution of spending, number of passengers who spent money and spending levels that were higher than the median may show patterns that wouldn't be seen by the median alone. These variables should therefore not be ruled out only because they have a median value but should be retained to be further assessed in the modelling phase.

The most important findings from the EDA are listed below.

There were a number of relationships between passenger characteristics and transportability that emerged from the exploratory analysis.

CryoSleep: This variable exhibited one of the most noticeable differences between the groups. Some 82% of passengers were transported, while some 33% were not in CryoSleep. This indicates that CryoSleep can be a key element for predicting transportation status.

The approximate transportation rate of HomePlanet was 66% for Passengers from Europa and 42% for Passengers from Earth. About 52% of passengers from Mars. These disparities indicate that there might be a relationship between a passenger's home planet and transportation status.

Destination: Passengers travelling to 55 Cancri e had an approximate transportation rate of 61%. The rate was around 50% for PSO J318.5-22 and 47% for TRAPPIST-1e. This means that the destination could also contain relevant information for the prediction task.

VIP status: About 50% of passengers who were recorded as non-VIP were transported, while 38% who were recorded as VIP were transported. The group without VIP information were approximately 51% transported. This indicates that there may be a correlation between VIP status and transportation, but this should be interpreted with caution due to the lack of values.

Average age: average age of transported passengers was slightly younger, 27.75 years, as compared to 29.92 years for those not transported. The difference is relatively small and the age range of the groups is quite large.

Passenger spending: Median spending values were either zero or very low for the five spending categories. In all five categories, medians for transported passengers were zero, with slightly higher medians for non-transported passengers for RoomService, Spa and VRDeck. Such differences are minor and, in isolation, do not provide a strong link between spending and transportation.

Percentages as shown on the categorical charts are approximate visual estimates. They are helpful for identifying patterns, but percentages should be determined from the data if the exact numerical comparisons are needed.

7. Implications for Machine Learning

The exploratory findings serve as a guide for the machine learning part of the project. CryoSleep doesn't seem to have that many relationships with other features, but it's certainly an important one for transportation status, and that's why it's listed here. HomePlanet and Destination can also provide helpful data as the transportation rates vary by HomePlanet and Destination.

The status of "VIP" may include extra predictive information but it must be treated correctly if it is missing. The age might be included in the model, but the difference between transported and non-transported passengers is quite small relative to the other features and should be evaluated in conjunction with the other features.

The spending variables should not be automatically deleted because they have low median values. The distributions of these can be useful, especially that of passengers who have non-zero or unusually high expenditure. Their contribution needs to be evaluated in the process of training the model and evaluating the features.

The observations are exploratory and do not constitute a proof of causing transportation of a passenger by any individual feature. The value of each feature in predicting the outcome needs to be evaluated with an appropriate validation procedure.

8. Limitations and Conclusion

There are a number of cautions in interpreting the exploratory analysis. First of all, there are some missing values in the passenger data. These values can impact comparisons and should be treated with care in preprocessing. Second, there may be extremely skewed distributions and extreme values in the spending variables, which can make median comparisons less representative of spending patterns. Third, the percentages on the categorical charts are not actual statistics, but rather an “eye estimate” by the viewer.

In addition, the association that can be observed in exploratory data analysis does not indicate causality. A feature that is heavily correlated with transportation status will not necessarily be the most useful in a predictive model. To avoid making conclusions solely based on the training data, its contribution should be tested on the validation data.

Finally, the analysis revealed a number of potential associations between the characteristics of the passengers and their transportation status. The differences were clearly seen in the group CryoSleep and were apparent in the groups HomePlanet and Destination as well. Averaged over the transported passengers, a slight difference in age was observed, where these were slightly younger. The student spending medians were generally zero or very low in both groups, and more attention needs to be paid to the distributions of passenger spending.

The results indicate a foundation for feature selection, preprocessing, and model development for the subsequent phase of the project. Each feature's final importance will be determined by the evaluation and comparison of the models.
