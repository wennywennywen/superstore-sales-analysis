import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('outputs', exist_ok=True)

df = pd.read_csv('../Sample - Superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# Chart 1 — Sales by Year
yearly_sales = df.groupby('Year')['Sales'].sum()
print(yearly_sales)
plt.figure(figsize=(10, 5))
plt.plot(yearly_sales.index, yearly_sales.values, marker='o', color='steelblue', linewidth=2)
plt.title('Total Sales by Year')
plt.xlabel('Year')
plt.ylabel('Sales ($)')
plt.xticks([2014, 2015, 2016, 2017])
plt.tight_layout()
plt.savefig('outputs/sales_by_year.png', dpi=150, bbox_inches='tight')
plt.show()

# Chart 2 — Monthly Sales by Year
pivot = df.groupby(['Year', 'Month'])['Sales'].sum().unstack(level=0)
print(pivot)
pivot.plot(figsize=(12, 6))
plt.title('Monthly Sales by Year')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.xticks(range(1,13), ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=45)
plt.legend(title='Year')
plt.tight_layout()
plt.savefig('outputs/monthly_sales_by_year.png', dpi=150, bbox_inches='tight')
plt.show()

# Chart 3 — Monthly Profit by Category
pivot2 = df.groupby(['Month', 'Category'])['Profit'].sum().unstack()
pivot2.plot(figsize=(12, 6))
plt.title('Monthly Profit by Category')
plt.xlabel('Month')
plt.ylabel('Profit ($)')
plt.xticks(range(1,13), ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=45)
plt.legend(title='Category')
plt.tight_layout()
plt.savefig('outputs/monthly_profit_by_category.png', dpi=150, bbox_inches='tight')
plt.show()
