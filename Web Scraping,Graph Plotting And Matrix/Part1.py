#1
import matplotlib.pyplot as plt  
import pandas as pd
df = pd.read_csv('dailyActivity_merged.csv')  
print(df.dtypes) 

df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])

lis1 = df['ActivityDate'].values.tolist()  
lis2 = df['TotalSteps'].values.tolist()  

plt.figure(figsize=(12, 6))
plt.plot(lis1, lis2, marker='o', linewidth=2, markersize=4, color='blue')
plt.title('Total Number of Steps on Daily Basis', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Steps', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#3
df = pd.read_csv('dailyActivity_merged.csv')  
print(df.dtypes) 

df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])

dates = df['ActivityDate'].values.tolist()  
distances = df['TotalDistance'].values.tolist()  

plt.figure(figsize=(14, 7))
plt.bar(dates, distances, color='skyblue', edgecolor='navy', alpha=1)
plt.title('Daily Distance Covered', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Distance (miles/km)', fontsize=12)
plt.grid(True, linestyle='--', alpha=1, axis='y' )
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#4
df = pd.read_csv('sleepDay_merged.csv')  
print(df.dtypes) 

df['SleepDay'] = pd.to_datetime(df['SleepDay'])

dates = df['SleepDay'].values.tolist()  
total_time_in_bed = df['TotalTimeInBed'].values.tolist()  

plt.figure(figsize=(14, 7))
plt.scatter(dates, total_time_in_bed, color='red', alpha=0.7, s=50)  # s=50 controls point size
plt.title('Total Time in Bed - Scatter Chart', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Time in Bed (minutes)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#5

df = pd.read_csv('hourlySteps_merged.csv')
print(df.dtypes)

df['ActivityHour'] = pd.to_datetime(df['ActivityHour'])
april_12 = pd.to_datetime('2016-04-12').date() in df['ActivityHour'].dt.date.values

print(df['ActivityHour'].dt.date.unique())
print("does exite {april_12}")

filtered_df = df[df['ActivityHour'].dt.date == pd.to_datetime('2016-04-12').date()]

hours = filtered_df['ActivityHour'].dt.hour.values
step_total = filtered_df['StepTotal'].values

plt.pie(hours , labels = step_total , autopct='%1.0f%%')
plt.title(' pie chart')
plt.show()

