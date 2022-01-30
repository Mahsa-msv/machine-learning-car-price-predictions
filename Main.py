import warnings

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# plt.show()

plt.subplot(1, 2, 2)
plt.title('Car Price Spreed')
sns.boxplot(y=cars.price)

plt.show()


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

# plt.show()

plt.figure(figsize=(20,8))

plt.subplot(1,2,1)
plt.title('Symboling Histogram')
sns.countplot(cars.symboling, palette=("cubehelix"))

plt.subplot(1,2,2)
plt.title('Symboling vs Price')
sns.boxplot(x=cars.symboling, y=cars.price, palette=("cubehelix"))

# plt.show()

plt.figure(figsize=(20,8))
plt.subplot(1,2,1)
plt.title('Engine Type Histogram')
sns.countplot(cars.enginetype, palette=("Blues_d"))

plt.subplot(1,2,2)
plt.title('Engine Type vs Price')
sns.boxplot(x=cars.enginetype, y=cars.price, palette=("PuBuGn"))

# plt.show()

df = pd.DataFrame(cars.groupby(['enginetype'])['price'].mean().sort_values(ascending = False))
df.plot.bar(figsize=(8,6))
plt.title('Engine Type vs Average Price')
plt.show()














