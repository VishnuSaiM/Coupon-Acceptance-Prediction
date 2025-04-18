# -*- coding: utf-8 -*-
"""invehicle_coupon_recommendation .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16DEv6PgHOtpxITxirMtPtZvy-fzgWhst

# I-Business Understanding:
***
## 1-Overview:
Coupon systems have been widely used to market products, and services and engage customers to use their products and services often. Coupons create a win-win situation for both companies and customers so, by offering a correct coupon to users, which can lead users to become frequent customers and it is enhancing a brand’s impact on its customers.

How to know which coupon to provide a customer can be a rather complex task, since each customer profile responds differently to each other, and frequently offering them bad coupons or deals might drag them away from your business. To overcome this problem, machine learning techniques can be used to build a better coupon recommendations system.
## 2-Business Objective:
Predicting whether the customer will accept the coupon or not is a difficult problem, and we can not just recommend it to everyone because of the costs concerned so, in this problem, we will predict whether a customer will accept or reject the offered coupon based on the customer’s profile and history.

This prediction helps the company in offering a correct coupon so that more customers will use their services which leads to more business for the company.

## 3-DS Objective:
The goal of the prediction problem is to predict whether a customer will accept or reject the coupon for a specific venue based on demographic and contextual attributes. If the customers accept the coupon are labeled as Y=1 and if the customers reject the coupon are labeled as Y=0. This problem can be posed as a binary class classification problem.
# II-Data Understanding:
***
## 1-Importing Libraries:
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os

"""## 2-Loading Data:"""

df = pd.read_csv("/content/in-vehicle-coupon-recommendation.csv")

"""## 3-Explanation of Dataset attributes/features:
### 3.1-User attributes:
>__1. Gender:__ Female, Male<br>
>__2. Age:__ 21, 46, 26, 31, 41, 50plus, 36, below21<br>
>__3. Marital Status:__ Unmarried partner, Single, Married partner, Divorced, Widowed<br>
>__4. has_Children:__ 1: has children, 0: No children<br>
>__5. Education:__ Some college — no degree, Bachelors degree, Associates degree, High School Graduate, Graduate degree (Masters or Doctorate), Some High School<br>
>__6. Occupation:__ unique 25 number of occupation of users (Unemployed, Architecture & Engineering, Student,Education&Training&Library, Healthcare Support,Healthcare Practitioners & Technical, Sales & Related, Management,Arts Design Entertainment Sports & Media, Computer & Mathematical,Life Physical Social Science, Personal Care & Service, Community & Social Services, Office & Administrative Support, Construction & Extraction, Legal, Retired, Installation Maintenance & Repair, Transportation & Material Moving, Business & Financial, Protective Service, Food Preparation & Serving Related, Production Occupations, Building & Grounds Cleaning & Maintenance, Farming Fishing & Forestry)<br>
>__7. Income:__ income of user (Less than \\\$12500, \\\$12500 — \\\$24999, \\\$25000 — \\\$37499, \\\$37500 — \\\$49999, \\\$50000 — \\\$62499, \\\$62500 — \\\$74999, \\\$75000 — \\\$87499, \\\$87500 — \\\$99999, \\\$100000 or More)<br>
>__8. Car :__ Description of vehicle which driven by user (Scooter and motorcycle, crossover, Mazda5) (99% of values are missing in this feature)<br>
>__9. Bar:__ how many times does the user go to a bar every month? (never, less1, 1\~3, 4\~8, gt8, nan)<br>
>__10. CoffeeHouse:__ how many times does the user go to a coffeehouse every month? (never, less1, 1\~3, 4\~8, gt8, nan)<br>
>__11. CarryAway:__ how many times does the user get take-away food every month? (never, less1, 1\~3, 4\~8, gt8, nan)<br>
>__12. RestaurantLessThan20:__ how many times does the user go to a restaurant with an average expense per person of less than \\\$20 every month? (never, less1, 1\~3, 4\~8, gt8, nan)<br>
>__13. Restaurant20To50:__ how many times does the user go to a restaurant with average expense per person of \\\$20 — \\\$50 every month? (never, less1, 1\~3, 4\~8, gt8, nan)<br>
### 3.2-Contextual attributes:
>__1. Destination:__ destination of user (No Urgent Place, Home, Work)<br>
>__2. Passenger:__ who are the passengers in the car (Alone, Friend(s), Kid(s), Partner)<br>
>__3. Weather:__ weather when user is driving (Sunny, Rainy, Snowy)<br>
>__5. Time:__ time when user driving (2PM, 10AM, 6PM, 7AM, 10PM)<br>
>__6. toCoupon_GEQ5min:__ driving distance to the restaurant/cafe/bar for using the coupon is greater than 5 minutes (0,1)<br>
>__7. toCoupon_GEQ15min:__ driving distance to the restaurant/cafe/bar for using the coupon is greater than 15 minutes (0,1)<br>
>__8. toCoupon_GEQ25min:__ driving distance to the restaurant/cafe/bar for using the coupon is greater than 25 minutes (0,1)<br>
>__9. direction_same:__ whether the restaurant/cafe/bar is in the same direction as user’s current destination (0,1)<br>
>__10. direction_opp:__ whether the restaurant/cafe/bar is in the opposite direction as user’s current destination (0,1)<br>
### 3.3-Coupon attributes:
>__1. Coupon:__ coupon type offered by company (Restaurant(<\\\$20), Coffee House, Carry out & Take away, Bar, Restaurant(\\\$20-\\\$50)). Here, <\\\$20 is the average pay per user in a not too expensive restaurant, Restaurant(\\\$20-\\\$50) means the average pay per user is between \\\$20 to \\\$50 which little bit expensive restaurant.<br>
>__2. Expiration:__ coupon expires in 1 day or in 2 hours (1d, 2h)<br>
### 3.4-Target attribute:
>__1. Y:__ whether the coupon is accepted or rejected, 1:accepted, 0:rejected

# III-Data Preparation
***
## 1- Overview
"""

df.info()

"""We can see that most features are categorical and a few are numeric categorical types. Some features have null values, so need to check for the missing value in attributes.

## 2-Remove duplicates
***
"""

print(df.shape)
df = df.drop_duplicates()
print(df.shape)

"""## 3-Dealing with Missing values
***
"""

def missing_percentage(df):
    total = df.isnull().sum().sort_values(ascending = False)
    percent = round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2)
    return pd.concat([total, percent], axis=1, keys=['Total','Percent'])

missing_percentage(df)

"""We can see that the total 6 attributes have missing values, from that 'car' feature has 99% of the missing value so we need to drop this feature.<br>
Other features like 'bar', 'coffeehouse', 'carryaway', 'RestaurantLessThan20', and 'Restaurant20To50' have approx 1% of missing value, so we need to fill these missing values with some other value, for that we will use mode imputation.
"""

df.drop(['car'], axis=1, inplace=True)

df['CoffeeHouse'].fillna(df['CoffeeHouse'].mode()[0], inplace=True)
df['Restaurant20To50'].fillna(df['Restaurant20To50'].mode()[0], inplace=True)
df['CarryAway'].fillna(df['CarryAway'].mode()[0], inplace=True)
df['RestaurantLessThan20'].fillna(df['RestaurantLessThan20'].mode()[0], inplace=True)
df['Bar'].fillna(df['Bar'].mode()[0], inplace=True)

"""## 4-Visualization and Feature Relations
***
### 4.1-Correlation of Features
"""

numeric_categorical_features = df.select_dtypes(include=['int', 'float']).columns
df_numeric_categorical = df[numeric_categorical_features]
df_numeric_categorical.corr()

"""1-Feature 'direction_same' is perfectly correlated with 'direction_opp', both have the same variance.<br>
2-'toCoupon_GEQ5min' feature has no correlation with any feature because it has the same value '1' for all data points, which means all the restaurants/bars are at least more than five minutes away from the driver.<br>

so, drop both 'direction_opp' and 'toCoupon_GEQ5min' features.
"""

df.drop(['direction_opp','toCoupon_GEQ5min'], axis=1, inplace=True)

# correaltion heatmap

# Calculate the correlation matrix
correlation_matrix = df_numeric_categorical.corr()

# Exclude specified columns from the correlation matrix
columns_to_exclude = ['direction_opp', 'toCoupon_GEQ5min']
correlation_matrix = correlation_matrix.drop(columns=columns_to_exclude, index=columns_to_exclude)

# Create the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Numeric/Categorical Features')
plt.show()

"""### 4.2-Univariate Analysis

#### A-direction_same
"""

def percent_value_counts(df, feature):
    data = pd.DataFrame(sorted(list(df[feature].unique())),columns=[feature])
    data['Total_Count'] = list(df.groupby(feature).Y.count())
    data['Total_%'] = round(data['Total_Count']/df[feature].shape[0]*100,3)
    data['Accepted'] = list(df[df.Y==1].groupby(feature).Y.count())
    data['Rejected'] = list(df[df.Y==0].groupby(feature).Y.count())
    data['%Accepted'] = round(data['Accepted']/data['Total_Count']*100,3)
    data['%Rejected'] = round(data['Rejected']/data['Total_Count']*100,3)
    return data

def univariate_analysis(df, feature):
    df_EDA = percent_value_counts(df, feature)
    df_EDA = df_EDA.sort_values(by='Total_Count', ascending=False)

    fig = plt.subplots(figsize =(8, 4))
    plt.barh(df_EDA[feature],df_EDA['Total_Count'])
    plt.barh(df_EDA[feature],df_EDA['Accepted'])
    plt.legend(labels=['Total','Accepted'])
    plt.xlabel('Counts')
    plt.title(feature+' wise accepted coupons')
    plt.show()
    return df_EDA

univariate_analysis(df,'direction_same')

"""**Observations:**

direction_same feature has 78% value is '0', and 22% value is '1'. Both value has almost similar acceptance ratio. so this feature not more usefull. So, we drop 'direction_same' feature.
"""

df.drop(['direction_same'], axis=1, inplace=True)

"""#### B-coupon"""

univariate_analysis(df,'coupon')

"""**Observations:**
- Maximum coupons offered are for Coffee House coupons.
- Maximum coupons accepted by users are Carry out & Take away and Restaurant(<20) coupons.
- Bar coupon has a very low acceptance ratio.

#### C- age
"""

univariate_analysis(df,'age')

"""**Observations:**
- Most users in this data have ages between 21 to 26 years.
- The users whose age is below 21 years have the highest coupon acceptance ratio.
- The users whose age is above 50 years have the highest coupon rejection ratio.

#### D- education
"""

univariate_analysis(df,'education')

"""**Observations:**
- Most users have at least a Bachelor's degree or Some college - no degree.
- In this data, very few users have only Some High School education, and those users have the highest coupon acceptance ratio.
- Users who have a Graduate degree (Masters or Doctorate) have the least coupon acceptance ratio.

#### E- income
"""

univariate_analysis(df,'income')

"""**Observations:**
- Most users in this data have income in between \\\$12500 and \\\$49999
- Users who have low income and high income accept more coupons than others.
- Users who have medium-range income are mostly rejecting the coupon.

#### F- destination
"""

univariate_analysis(df,'destination')

"""**Observations:**
- Most of the users go to No Urgent Place.
- The users who have destination No Urgent Place are accepting more coupons than others.
- The users who have destination Home and Work have almost similar coupon acceptance ratios.

#### G- passanger
"""

univariate_analysis(df,'passanger')

"""**Observations:**
- Most of the time users go out Alone.
- The users who go out with Friends or Partner have more coupon acceptance ratios than Alone users.
- The users who go out with Friends are accepting more coupons than other co-passengers.

#### H- weather
"""

univariate_analysis(df,'weather')

"""**Observations:**
- In Sunny weather, users go out more and accept more coupons than other wethers.

#### I- temperature
"""

univariate_analysis(df,'temperature')

"""**Observations:**
- Most of the time users go out when the temperature is 80 F.
- When the temperature is 80 F, user's coupon acceptance ratio is approx 59.86%.rs.

#### J- time
"""

univariate_analysis(df,'time')

"""**Observations:**
- Most of the time users go out when the time is 6 PM and 7 AM.
- The users mostly accept coupons when the time is 2 PM and 10 AM.

#### K- gender
"""

univariate_analysis(df,'gender')

"""**Observations:**
- Male and Female both have almost similar coupon acceptance ratios.

**Observations:**
- Most users in this data have ages between 21 to 26 years.
- The users whose age is below 21 years have the highest coupon acceptance ratio.
- The users whose age is above 50 years have the highest coupon rejection ratio.

#### L- maritalStatus
"""

univariate_analysis(df,'maritalStatus')

"""**Observations:**
- Most users in this data are Single or have Married partner.
- Single users accept more coupons than others.

### 4.3-Bivariate Analysis

#### Q - What time do users go to Work, Home, or No Urgent Place, and with whom?
"""

# Define the order of unique values for each variable
destination_order = df['destination'].unique()
passenger_order = df['passanger'].unique()
time_order = df['time'].unique()

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot for 'destination' vs 'passenger', Y=0
sns.countplot(x='destination', hue='passanger', data=df[df['Y'] == 0], ax=axes[0, 0], order=destination_order, hue_order=passenger_order)
axes[0, 0].set_title('destination vs passenger (count), Y=0')
axes[0, 0].legend().remove()


# Plot for 'destination' vs 'passenger', Y=1
sns.countplot(x='destination', hue='passanger', data=df[df['Y'] == 1], ax=axes[0, 1], order=destination_order, hue_order=passenger_order)
axes[0, 1].set_title('destination vs passenger (count), Y=1')

# Set legend on the right
axes[0, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Plot for 'destination' vs 'time', Y=0
sns.countplot(x='destination', hue='time', data=df[df['Y'] == 0], ax=axes[1, 0], order=destination_order, hue_order=time_order)
axes[1, 0].set_title('destination vs time (count), Y=0')
axes[1, 0].legend().remove()


# Plot for 'destination' vs 'time', Y=1
sns.countplot(x='destination', hue='time', data=df[df['Y'] == 1], ax=axes[1, 1], order=destination_order, hue_order=time_order)
axes[1, 1].set_title('destination vs time (count), Y=1')

# Set legend on the right
axes[1, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()
plt.show()

"""**Observations:**
- The users who go with Friends have only No Urgent Place destination.
- Maximum users accept coupons when the time is 2 PM and 10 AM, the destination is No Urgent Place, and the co-passanger is Friends.
- The users who have destination Home and Work have almost similar coupon acceptance ratios.

#### Q - At what time, which coupon acceptance ratio is high?
"""

# Define the order of unique values for each variable
coupon_order = df['coupon'].unique()
time_order = df['time'].unique()

fig, axes = plt.subplots(1, 2, figsize=(15, 10))

# Plot for 'destination' vs 'passenger', Y=0
sns.countplot(x='time', hue='coupon', data=df[df['Y'] == 0], ax=axes[0], order=time_order, hue_order=coupon_order)
axes[0].set_title('time vs coupon (count), Y=0')
axes[0].legend().remove()


# Plot for 'destination' vs 'passenger', Y=1
sns.countplot(x='time', hue='coupon', data=df[df['Y'] == 1], ax=axes[1], order=time_order, hue_order=coupon_order)
axes[1].set_title('time vs coupon (count), Y=1')

# Set legend on the right
axes[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))


fig.tight_layout()
plt.show()

"""**Observations:**
- At 10AM, 2 PM and 6 PM, users mostly accept Restaurant(<20), Carry out and coffee house coupons.
- At 7 AM, 10AM, 2PM and 6 PM, Coffee House coupon ask is maximum.
- At 10 PM, mostly Carry out & Take away and Restaurant(<20) coupons are accepted, and Restaurant(20–50) coupons are rejected.
- Users mostly reject coupons for Bar at 7 AM, 10 AM, and 2 PM.

### 4.4-Feature Engineering
#### to_Coupon
‘toCoupon_GEQ15min’ and ‘toCoupon_GEQ25min’ features tell the driving distance to the restaurant/coffee house/bar, so we can combine them and make a new feature called ‘to_coupon’.

‘toCoupon_GEQ15min’ and ‘toCoupon_GEQ25min’ features have two categorical values 0 & 1 and ‘to_coupon’ has three categorical value 0,1 & 2.
> 0: driving distance is less than or equal to 15 min<br>
> 1: driving distance is greater than 15 min and less than or equal to 25 min<br>
> 2: driving distance is greater than 25 min<br>
"""

df['to_Coupon'] = 2
df.loc[df['toCoupon_GEQ15min'] == 0, 'to_Coupon'] = 0
df.loc[(df['toCoupon_GEQ15min'] == 1) & (df['toCoupon_GEQ25min'] == 0), 'to_Coupon'] = 1

print('Unique values:', df['to_Coupon'].unique())
print('-' * 50)

print(df['to_Coupon'].describe())

univariate_analysis(df,'to_Coupon')

"""We can see that most coupons offered are nearby within 25 minutes. Also, users generally accept coupons that are less than 25 minutes distance."""

df.drop(['toCoupon_GEQ15min','toCoupon_GEQ25min'], axis=1, inplace=True)

"""#### coupon_freq

‘coupon_freq’ is a combination of five features, RestaurantLessThan20, CoffeeHouse, CarryAway, Bar, and Restaurant20To50. These five features tell how frequently a user is going to RestaurantLessThan20, CoffeeHouse, CarryAway, Bar, and Restaurant20To50.

Every user is asked for a single coupon, so we need only the frequency of that one coupon type, other coupon details are not needed. so we create a new feature that tells how frequently a user used the asked coupon.
"""

coupon_map = {
    'Restaurant(<20)': 'RestaurantLessThan20',
    'Coffee House': 'CoffeeHouse',
    'Carry out & Take away': 'CarryAway',
    'Bar': 'Bar',
    'Restaurant(20-50)': 'Restaurant20To50'
}

# Use the map function to create the 'coupon_freq' column
df['coupon_freq'] = df['coupon'].map(coupon_map)
df['coupon_freq'] = df.apply(lambda row: row[row['coupon_freq']], axis=1)
# Print unique values
print('Unique values:', df['coupon_freq'].unique())
print('-' * 50)

# Describe the 'coupon_freq' column
print(df['coupon_freq'].describe())

# Define the order of unique values for each variable
coupon_order = df['coupon'].unique()
coupon_freq_order = df['coupon_freq'].unique()

fig, axes = plt.subplots(1, 2, figsize=(15, 10))

# Plot for 'destination' vs 'passenger', Y=0
sns.countplot(x='coupon_freq', hue='coupon', data=df[df['Y'] == 0], ax=axes[0], order=coupon_freq_order, hue_order=coupon_order)
axes[0].set_title('coupon_freq vs coupon (count), Y=0')
axes[0].legend().remove()


# Plot for 'destination' vs 'passenger', Y=1
sns.countplot(x='coupon_freq', hue='coupon', data=df[df['Y'] == 1], ax=axes[1], order=coupon_freq_order, hue_order=coupon_order)
axes[1].set_title('coupon_freq vs coupon (count), Y=1')

# Set legend on the right
axes[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))


fig.tight_layout()
plt.show()

"""Most users in this data have visited more than one time Restaurant(<$20) and Carry Away services and also they have the highest coupon acceptance ratio.<br>
Users who visited Coffee House 1to3 times and 4to8 times have also higher coupon acceptance ratio.<br>
Most users visited an expensive Restaurant only once and users who visited an expensive Restaurant greater than 4 times have the highest coupon acceptance ratio for an expensive Restaurant.<br>
Most users in this data never visit a Bar and most of them reject the bar coupon and users who visited Bar 1to3 times or 4to8 times have a higher coupon acceptance ratio.<br>
"""

df.drop(['RestaurantLessThan20','CoffeeHouse', 'CarryAway', 'Bar', 'Restaurant20To50'], axis=1, inplace=True)

"""#### occupation_class

occupation feature has 25 no of distinct values, which creates very sparsity in the data matrix after encoding so we can try to convert it into a new feature called occupation_class.

We will divide them into five categories in the order of acceptance ratio of coupons:
>4: High<br>
>3: Medium_high<br>
>2: medium<br>
>1: Medium_low<br>
>0: Low<br>
"""

occupation_acceptance_rate = df.groupby("occupation")["Y"].mean()

quintiles = pd.qcut(occupation_acceptance_rate, 5, labels=False)

occupation_class = pd.Series(quintiles, index=occupation_acceptance_rate.index)

df["occupation_class"] = df["occupation"].map(occupation_class)

df.head()

univariate_analysis(df,'occupation_class')

df.drop(['occupation'], axis=1, inplace=True)

"""### 4.5-Encoding

"""

from sklearn.preprocessing import OrdinalEncoder

order = [['Work','Home','No Urgent Place'],
         ['Kid(s)','Alone','Partner','Friend(s)'],
         ['Rainy','Snowy','Sunny'],
         [30,55,80],
         ['7AM','10AM','2PM','6PM','10PM'],
         ['Bar','Restaurant(20-50)','Coffee House','Restaurant(<20)','Carry out & Take away'],
         ['2h','1d'],
         ['Female','Male'],
         ['below21','21','26','31','36','41','46','50plus'],
         ['Widowed','Divorced','Married partner','Unmarried partner','Single'],
         ['Some High School','High School Graduate','Some college - no degree','Associates degree','Bachelors degree','Graduate degree (Masters or Doctorate)'],
         ['Less than $12500','$12500 - $24999','$25000 - $37499','$37500 - $49999','$50000 - $62499','$62500 - $74999','$75000 - $87499','$87500 - $99999','$100000 or More'],
         ['never','less1','1~3','4~8','gt8']]
Ordinal_enc = OrdinalEncoder(categories=order)
columns_to_encode = ['destination', 'passanger', 'weather', 'temperature', 'time', 'coupon', 'expiration', 'gender', 'age', 'maritalStatus', 'education', 'income', 'coupon_freq']
data_to_encode = df[columns_to_encode]
df_Ordinal_encoding = Ordinal_enc.fit_transform(data_to_encode)
df[columns_to_encode] = df_Ordinal_encoding
df.head()

"""### 4.6-Pre-Modeling Tasks
#### 1-Separating dependent and independent variables
"""

# separating our independent and dependent variable
X = df.drop(['Y'], axis = 1)
y = df["Y"]

"""#### 2-Splitting the training data"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = .20, random_state=0)

"""#### 3-Feature Scaling"""

from sklearn.preprocessing import StandardScaler
st_scale = StandardScaler()

## transforming "train_x"
X_train = st_scale.fit_transform(X_train)
## transforming "test_x"
X_test = st_scale.transform(X_test)

"""# IV-Modelling
***
## 1- LogisticRegression
"""

from sklearn.linear_model import LogisticRegression

# Train a logistic regression model on the training data
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = clf.predict(X_test)

"""## 2- Random Forest"""

from sklearn.ensemble import RandomForestClassifier

# Train a Random Forest classifier on the training data
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred_rf = rf_clf.predict(X_test)

"""## 3- SVM"""

from sklearn.svm import SVC

# Train an SVM classifier on the training data
svm_clf = SVC(kernel='linear', C=1)
svm_clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred_svm = svm_clf.predict(X_test)

"""## 4- K-NN"""

from sklearn.neighbors import KNeighborsClassifier

# Train a KNN classifier on the training data
knn_clf = KNeighborsClassifier(n_neighbors=5)
knn_clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred_knn = knn_clf.predict(X_test)

"""## 5- xgboost"""

from xgboost import XGBClassifier
# Train an XGBoost classifier on the training data
xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred_xgb = xgb_clf.predict(X_test)

"""## 8- Neural Network: Multilayer perceptron"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.dropout1(out)
        out = self.fc2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.dropout2(out)
        out = self.fc3(out)
        out = self.sigmoid(out)
        return out

# Convert the data to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

# Define the dataset class
class CustomDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Create the DataLoader
train_dataset = CustomDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Set the device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import torch.optim.lr_scheduler as lr_scheduler

# Define the model, loss function, and optimizer
input_size = X_train.shape[1]
hidden_size = 64
output_size = 1

model = MLP(input_size, hidden_size, output_size).to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Create the learning rate scheduler
scheduler = lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

# Train the model
num_epochs = 100
for epoch in range(num_epochs):
    running_loss = 0.0
    # Update the learning rate for each epoch
    scheduler.step()

    for inputs, labels in train_loader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, labels.unsqueeze(1))
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    epoch_loss = running_loss / len(train_loader)
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}')

"""# V-Evaluation
***
"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def evaluate_classification(y_pred, y_test):
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # Calculate precision
    precision = precision_score(y_test, y_pred)
    print("Precision:", precision)

    # Calculate recall
    recall = recall_score(y_test, y_pred)
    print("Recall:", recall)

    # Calculate F1 score
    f1 = f1_score(y_test, y_pred)
    print("F1 Score:", f1)

    # Calculate AUC-ROC
    auc_roc = roc_auc_score(y_test, y_pred)
    print("AUC-ROC:", auc_roc)

"""## 1- LogisticRegression"""

evaluate_classification(y_pred, y_test)

"""## 2- Random Forest"""

evaluate_classification(y_pred_rf, y_test)

"""## 3- SVM"""

evaluate_classification(y_pred_svm, y_test)

"""## 4- K-NN"""

evaluate_classification(y_pred_knn, y_test)

"""## 5- xgboost"""

evaluate_classification(y_pred_xgb, y_test)

importances = xgb_clf.feature_importances_

# Sort feature importances in descending order
indices = np.argsort(importances)[::-1]

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.title("Feature Importance")
plt.bar(range(X_train.shape[1]), importances[indices], align="center")
plt.xticks(range(X_train.shape[1]), [X.columns[i] for i in indices], rotation=90)
plt.tight_layout()
plt.show()

"""## 8- Neural Network: Multilayer perceptron"""

# Evaluate the model
with torch.no_grad():
    y_pred_mlp = model(X_test_tensor).round().squeeze().numpy()
evaluate_classification(y_pred_mlp, y_test)

"""## 9- Results:

### XGBoost had the best performance so let's try fine-tuning it using optuna

## 10- Fine-Tuning
"""

!pip install optuna

import optuna

def objective(trial):
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear']),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.001, 0.1),
        'subsample': trial.suggest_uniform('subsample', 0.5, 1),
        'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1),
        'gamma': trial.suggest_loguniform('gamma', 0.001, 1),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10)
    }

    model = XGBClassifier(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return accuracy_score(y_test, y_pred)

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

best_params = study.best_params

final_model = XGBClassifier(**best_params)
final_model.fit(X_train, y_train)

y_pred_fm = final_model.predict(X_test)

evaluate_classification(y_pred_fm, y_test)

evaluate_classification(y_pred_xgb, y_test)

"""### We have achived a 2% increase in performance after fine-tuning the xgboost model

Saving the trained model
"""

import pickle

filename = 'trained_model.pkl'
pickle.dump(xgb_clf, open(filename, 'wb'))

# Loading the save model
loaded_model = pickle.load(open(filename, 'rb'))

pip install streamlit

!pip install pyngrok streamlit

from pyngrok import ngrok
ngrok.set_auth_token("2t0Selvvg3F6PGIMbTKX62b10UH_7i1YxC5hsoFRMUdVMRMuc")

!streamlit run appp.py &>/dev/null&

# Get the public URL from ngrok
public_url = ngrok.connect(8501).public_url
print(f"Public URL: {public_url}")

