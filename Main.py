import warnings

import numpy.random

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

cars = pd.read_csv('CarPrice_Assignment.csv')
# print(cars.head())

CompanyName = cars['CarName'].apply(lambda x: x.split(' ')[0])

cars.insert(3, "CompanyName", CompanyName)
cars.drop(['CarName'], axis=1, inplace=True)
cars.CompanyName = cars.CompanyName.str.lower()


def replace_name(a, b):
    cars.CompanyName.replace(a, b, inplace=True)


replace_name("maxda", "mazda")
# print(cars.CompanyName.unique())
replace_name('porcshce', 'porsche')
replace_name('toyouta', 'toyota')
replace_name('vokswagen', 'volkswagen')
replace_name('vw', 'volkswagen')

plt.figure(figsize=(25, 6))

plt.subplot(1,2, 1)
plt.title('Car price distribution')
sns.distplot(cars.price)

plt.subplot(1, 2, 2)
plt.title('Car Price Spreed')
sns.boxplot(y=cars.price)

# plt.show()


plt.figure(figsize=(25, 6))
plt.subplot(1, 3, 1)
plt1 = cars.CompanyName.value_counts().plot(kind='bar')
# plt1.title('Companies Histogram')
plt1.set(xlabel='Car Company', ylabel='Frequency of Company')

plt.subplot(1,3,2)
plt1 = cars.fueltype.value_counts().plot(kind='bar')
plt1.set(xlabel = 'Fuel Type', ylabel='Frequency of fuel type')

plt.subplot(1,3,3)
plt1 = cars.carbody.value_counts().plot(kind='bar')
plt1.set(xlabel = 'Car Type', ylabel='Frequency of Car type')


plt.figure(figsize=(20,8))

plt.subplot(1,2,1)
plt.title('Symboling Histogram')
sns.countplot(cars.symboling, palette=("cubehelix"))

plt.subplot(1,2,2)
plt.title('Symboling vs Price')
sns.boxplot(x=cars.symboling, y=cars.price, palette=("cubehelix"))


plt.figure(figsize=(20,8))
plt.subplot(1,2,1)
plt.title('Engine Type Histogram')
sns.countplot(cars.enginetype, palette=("Blues_d"))

plt.subplot(1,2,2)
plt.title('Engine Type vs Price')
sns.boxplot(x=cars.enginetype, y=cars.price, palette=("PuBuGn"))


df = pd.DataFrame(cars.groupby(['enginetype'])['price'].mean().sort_values(ascending = False))
df.plot.bar(figsize=(8,6))
plt.title('Engine Type vs Average Price')
plt.tight_layout()

plt.figure(figsize=(50,50))

df = pd.DataFrame(cars.groupby(['CompanyName'])['price'].mean().sort_values(ascending=False))
df.plot.bar()
plt.title('Company Name vs Average Price')
plt.tight_layout()
# plt.show()

df = pd.DataFrame(cars.groupby(['fueltype'])['price'].mean().sort_values(ascending=False))
df.plot.bar()
plt.title('Fuel Type vs Average Price')
# plt.show()


df = pd.DataFrame(cars.groupby(['carbody'])['price'].mean().sort_values(ascending=False))
df.plot.bar()
plt.title('Car Type vs Average Price')
# plt.show()

plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
plt.title('Door Number Histogram')
sns.countplot(cars.doornumber, palette=("plasma"))

plt.subplot(1,2,2)
plt.title('Door Number vs Price')
sns.boxplot(x=cars.doornumber, y=cars.price, palette=("plasma"))

# plt.show()

plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
plt.title('Aspiration Histogram')
sns.countplot(cars.aspiration, palette=("plasma"))

plt.subplot(1,2,2)
plt.title('Aspiration vs Price')
sns.boxplot(x=cars.aspiration, y=cars.price, palette=("plasma"))
# plt.show()

def plot_count(x,fig):
    plt.subplot(4,2,fig)
    plt.title(x+' Histogram')
    sns.countplot(cars[x],palette=("magma"))
    plt.subplot(4,2,(fig+1))
    plt.title(x+' vs price')
    sns.boxplot(x=cars[x],y=cars.price,  palette=("magma"))

plt.figure(figsize=(15,20))

plot_count('enginelocation',1)
plot_count('cylindernumber',3)
plot_count('fuelsystem',5)
plot_count('drivewheel',7)

plt.tight_layout()
# plt.show()

def scatter(x,fig):
    plt.subplot(2,2,fig)
    plt.scatter(cars[x],cars['price'])
    plt.title(x + ' vs Price')
    plt.ylabel('Price')
    plt.xlabel(x)

plt.figure(figsize=(10,20))

scatter('carlength',1)
scatter('carwidth',2)
scatter('carheight',3)
scatter('curbweight',4)

plt.tight_layout()
# plt.show()

def pp(x,y,z):
    sns.pairplot(cars, x_vars=[x,y,z], y_vars='price',size=4, aspect=1, kind='scatter')
    # plt.show()

pp('enginesize', 'boreratio', 'stroke')
pp('compressionratio', 'horsepower', 'peakrpm')
pp('wheelbase', 'citympg', 'highwaympg')

# to check relations between car length and car width
np.corrcoef(cars['carlength'], cars['carwidth'])[0, 1]

cars['fueleconomy'] = (0.55 * cars['citympg']) + (0.45 * cars['highwaympg'])
cars['price'] = cars['price'].astype('int')
temp = cars.copy()
table = temp.groupby(['CompanyName'])['price'].mean()
temp = temp.merge(table.reset_index(), how='left',on='CompanyName')
bins = [0,10000,20000,40000]
cars_bin=['Budget','Medium','Highend']
cars['carsrange'] = pd.cut(temp['price_y'],bins,right=False,labels=cars_bin)
# print(cars.head())

plt.figure(figsize=(8,6))

plt.title('Fuel economy vs Price')
sns.scatterplot(x=cars['fueleconomy'],y=cars['price'],hue=cars['drivewheel'])
plt.xlabel('Fuel Economy')
plt.ylabel('Price')

# plt.show()
plt.tight_layout()

plt.figure(figsize=(25, 6))

df = pd.DataFrame(cars.groupby(['fuelsystem','drivewheel','carsrange'])['price'].mean().unstack(fill_value=0))
df.plot.bar()
plt.title('Car Range vs Average Price')
# plt.show()
# plt.tight_layout()


cars_lr = cars[['price', 'fueltype', 'aspiration','carbody', 'drivewheel','wheelbase',
                  'curbweight', 'enginetype', 'cylindernumber', 'enginesize', 'boreratio','horsepower',
                    'fueleconomy', 'carlength','carwidth', 'carsrange']]
cars_lr.head()

sns.pairplot(cars_lr)
# plt.show()

# Defining the map function
def dummies(x,df):
    temp = pd.get_dummies(df[x], drop_first = True)
    df = pd.concat([df, temp], axis = 1)
    df.drop([x], axis = 1, inplace = True)
    return df

# Applying the function to the cars_lr
cars_lr = dummies('fueltype',cars_lr)
cars_lr = dummies('aspiration',cars_lr)
cars_lr = dummies('carbody',cars_lr)
cars_lr = dummies('drivewheel',cars_lr)
cars_lr = dummies('enginetype',cars_lr)
cars_lr = dummies('cylindernumber',cars_lr)
cars_lr = dummies('carsrange',cars_lr)

cars_lr.head()

cars_lr.shape


np.random.seed(0)
df_train, df_test = train_test_split(cars_lr, train_size = 0.7, test_size = 0.3, random_state = 100)

scaler = MinMaxScaler()
num_vars = ['wheelbase', 'curbweight', 'enginesize', 'boreratio', 'horsepower','fueleconomy','carlength','carwidth','price']
df_train[num_vars] = scaler.fit_transform(df_train[num_vars])

df_train.head()
df_train.describe()

plt.figure(figsize = (30, 25))
sns.heatmap(df_train.corr(), annot = True, cmap="YlGnBu")
# plt.show()

y_train = df_train.pop('price')
X_train = df_train

from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

lm = LinearRegression()
lm.fit(X_train,y_train)
rfe = RFE(lm,step =10)
rfe = rfe.fit(X_train, y_train)

rfe.ranking_

list(zip(X_train.columns,rfe.support_,rfe.ranking_))

X_train.columns[rfe.support_]

X_train_rfe = X_train[X_train.columns[rfe.support_]]
# print(X_train_rfe.head())

def build_model(X,y):
    X = sm.add_constant(X)
    lm = sm.OLS(y,X).fit()
    print(lm.summary()) # model summary
    return X

def checkVIF(X):
    vif = pd.DataFrame()
    vif['Features'] = X.columns
    vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif['VIF'] = round(vif['VIF'], 2)
    vif = vif.sort_values(by = "VIF", ascending = False)
    return(vif)

#model-1
X_train_new = build_model(X_train_rfe,y_train)
X_train_new = X_train_rfe.drop(["twelve"], axis = 1)
#model-2
X_train_new = build_model(X_train_new,y_train)
X_train_new = X_train_new.drop(["fueleconomy"], axis = 1)
#model-3
X_train_new = build_model(X_train_new,y_train)
checkVIF(X_train_new)
X_train_new = X_train_new.drop(["curbweight"], axis = 1) #high VIF value
#model-4
X_train_new = build_model(X_train_new,y_train)
checkVIF(X_train_new)
X_train_new = X_train_new.drop(["sedan"], axis = 1) #high VIF value
#model-5
X_train_new = build_model(X_train_new,y_train)
checkVIF(X_train_new)
X_train_new = X_train_new.drop(["wagon"], axis = 1) #high p-value
#model-6
X_train_new = build_model(X_train_new,y_train)
checkVIF(X_train_new)
#model-7
X_train_new = X_train_new.drop(["dohcv"], axis = 1)
X_train_new = build_model(X_train_new,y_train)
checkVIF(X_train_new)

lm = sm.OLS(y_train,X_train_new).fit()
y_train_price = lm.predict(X_train_new)

fig = plt.figure()
sns.distplot((y_train - y_train_price), bins = 20)
fig.suptitle('Error Terms', fontsize = 20)
plt.xlabel('Errors', fontsize = 18)

num_vars = ['wheelbase', 'curbweight', 'enginesize', 'boreratio', 'horsepower','fueleconomy','carlength','carwidth','price']
df_test[num_vars] = scaler.fit_transform(df_test[num_vars])
y_test = df_test.pop('price')
X_test = df_test

X_train_new = X_train_new.drop('const',axis=1)
X_test_new = X_test[X_train_new.columns]
X_test_new = sm.add_constant(X_test_new)
y_pred = lm.predict(X_test_new)

from sklearn.metrics import r2_score
r2_score(y_test, y_pred)

fig = plt.figure()
plt.scatter(y_test,y_pred)
fig.suptitle('y_test vs y_pred', fontsize=20)
plt.xlabel('y_test', fontsize=18)
plt.ylabel('y_pred', fontsize=16)














