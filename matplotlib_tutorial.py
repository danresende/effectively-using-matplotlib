import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Setup matplotlib style and create a format function for later
plt.style.use('seaborn-whitegrid')

def currency(x, pos):
    'The two args are the value and tick position'
    if x >= 1000000:
        return '${:1.1f}M'.format(x * 1e-6)
    elif x >= 1000:
        return '${:1.1f}K'.format(x * 1e-3)
    else:
        return x

# Get data
df = pd.read_excel("https://github.com/chris1610/pbpython/blob/master/data/sample-salesv3.xlsx?raw=true")

# Preprocessing to get the top 10 sales
top_10 = (df.groupby('name')['ext price', 'quantity'].agg({'ext price': 'sum', 'quantity': 'count'}).sort_values(by='ext price', ascending=False))[:10].reset_index()
top_10.rename(columns={'name': 'Name', 'ext price': 'Sales', 'quantity':'Purchases'}, inplace=True)
avg_sales = top_10['Sales'].mean()
avg_purchases = top_10['Purchases'].mean()

# Ploting the top 10 sales

## Create the figure and the axes
fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(7, 4))

## Plot the data
top_10.plot(kind='barh', y='Sales', x='Name', ax=ax0)
top_10.plot(kind='barh', y='Purchases', x='Name', ax=ax1)

## Set the x limit, labels and titles
ax0.set_xlim([-10000, 140000])
ax0.set(title='Revenue',
        xlabel='Total Revenue',
        ylabel='Customer')
ax1.set(title='Units',
        xlabel='Total Units',
        ylabel='Customer')

## Add a line for the average
ax0.axvline(x=avg_sales, color='r', label='Average Sales', linestyle='--', linewidth=1)
ax1.axvline(x=avg_purchases, color='r', label='Average Purchases', linestyle='--', linewidth=1)

## Format the currency
formatter = FuncFormatter(currency)
ax0.xaxis.set_major_formatter(formatter)

## Hide the legend
ax0.legend().set_visible(False)
ax1.legend().set_visible(False)

## Add a title to the figure
fig.suptitle('2014 Sales Analysis', fontsize=14, fontweight='bold')

## Show plot
fig.savefig('sales.png', transparent=False, dpi=80, bbox_inches='tight')

print('Plot saved')
