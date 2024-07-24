import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = '202406_202406_연령별인구현황_월간 (2).csv'
data = pd.read_csv(file_path, encoding='cp949')

# Preprocess the data
data = data.rename(columns={data.columns[0]: "지역"})
data = data.replace(',', '', regex=True)
for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Function to calculate the middle school population ratio
def calculate_middle_school_ratio(df, region):
    total_population = df.loc[df['지역'] == region, '2024년06월_계_총인구수'].values[0]
    middle_school_population = df.loc[df['지역'] == region, ['2024년06월_계_13세', '2024년06월_계_14세', '2024년06월_계_15세']].sum(axis=1).values[0]
    return middle_school_population / total_population * 100

# Streamlit app
st.title('중학생 인구 비율 분석')

# Select region
regions = data['지역'].unique()
selected_region = st.selectbox('지역을 선택하세요:', regions)

# Calculate the ratio
ratio = calculate_middle_school_ratio(data, selected_region)

# Plot the pie chart
labels = ['중학생 인구 비율', '기타 인구 비율']
sizes = [ratio, 100 - ratio]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')

st.pyplot(fig1)
