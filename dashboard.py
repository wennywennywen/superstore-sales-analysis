import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================
# SECTION 1: DATA LOADING
# ============================================
st.title('SuperStore Sales Dashboard')
st.write('An analysis of sales, profit, and discounts across regions, categories, and products.')

df = pd.read_csv('Sample - Superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

pd.options.display.float_format = '{:,.2f}'.format

# ============================================
# SECTION 2: REGIONAL PERFORMANCE
# ============================================
st.header('Regional Performance')
region = df.groupby('Region')[['Sales', 'Profit']].sum().sort_values('Sales', ascending=False)
st.dataframe(region)

# ============================================
# SECTION 3: SALES TREND
# ============================================

# sales trend by year
st.header('Sales Trend by Year')
yearly_sales = df.groupby('Year')['Sales'].sum()
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(yearly_sales.index, yearly_sales.values, marker='o', color='steelblue', linewidth=2)
ax.set_xlabel('Year')
ax.set_ylabel('Sales ($)')
plt.xticks([2014, 2015, 2016, 2017])
plt.tight_layout()
st.pyplot(fig)

# monthly sales by year
st.header('Monthly Sales by Year')
fig, ax = plt.subplots(figsize=(12, 5))
monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().unstack(level=0)
monthly_sales.plot(ax=ax)
ax.set_xlabel('Month')
ax.set_ylabel('Sales ($)')
ax.set_xticks(range(1,13))
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=45)
plt.tight_layout()
st.pyplot(fig)

# monthly profit by category
st.header('Monthly Profit by Category')
fig, ax = plt.subplots(figsize=(12, 5))
monthly_profit = df.groupby(['Category','Month'])['Profit'].sum().unstack(level=0)
monthly_profit.plot(ax=ax)
ax.set_xlabel('Month')
ax.set_ylabel('Sales ($)')
ax.set_xticks(range(1,13))
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ============================================
# SECTION 4: DISCOUNT VS PROFIT
# ============================================
discount = df.groupby('Discount')['Profit'].mean()

st.header('Discount vs Profit')
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df['Discount'], df['Profit'], alpha=0.3)
ax.set_xlabel('Discount')
ax.set_ylabel('Profit ($)')
ax.axhline(y=0, color='red', linestyle='--')
plt.tight_layout()
st.pyplot(fig)

# ============================================
# SECTION 5: TOP & BOTTOM PRODUCTS
# ============================================
st.header('Top 10 vs Bottom 10 Products')
top = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
bottom = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=True).head(10)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Most Profitable')
    st.dataframe(top)
with col2:
    st.subheader('Least Profitable')
    st.dataframe(bottom)

# ============================================
# SECTION 6: BRAND PERFORMANCE
# ============================================
df['Brand'] = df['Product Name'].str.split().str[0]
print(df['Brand'].value_counts().head(20))

brand_perf = df.groupby(['Brand','Category'])[['Sales', 'Profit']].sum()
brand_perf['Margin'] = (brand_perf['Profit'] / brand_perf['Sales'] * 100).round(2)
brand_perf = brand_perf[brand_perf['Sales'] > 10000]  # filter out tiny brands
brand_perf_margin = brand_perf.sort_values('Margin', ascending=False).head(10)
brand_perf_profit = brand_perf.sort_values('Profit', ascending=False).head(10)
print(brand_perf_margin)
print(brand_perf_profit)

brand_heat = brand_perf_profit
print("Averages:")
print(brand_heat.mean())
print("\nStandard Deviations:")
print(brand_heat.std())

# Normalize — show how far each brand is from average
brand_normalized = (brand_heat - brand_heat.mean()) / brand_heat.std()

st.header('Brand Performance vs Averages')
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(brand_normalized, annot=True, fmt='.1f', cmap='RdYlGn', center=0, ax=ax)
ax.set_title('Brand Performance vs Average')
plt.tight_layout()
st.pyplot(fig)
