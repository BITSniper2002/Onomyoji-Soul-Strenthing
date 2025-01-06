import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = []
with open('./soul_data.txt','r') as f:
    lines = f.readlines()
    for l in lines:
        data.append(float(l.rstrip('\n')))


# Calculate statistics
max_value = np.max(data)
mean_value = np.mean(data)
median_value = np.median(data)

# Print statistics
print(f"Max Value: {max_value:.2f}")
print(f"Mean Value: {mean_value:.2f}")
print(f"Median Value: {median_value:.2f}")

# Plot histogram
plt.figure(figsize=(10, 6))
sns.histplot(data, bins=100, kde=True)
plt.title('Histogram of Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.savefig('Histogram.png')
plt.show()

# Divide data into 8 ranges
range_labels = [f'Range {i+1}' for i in range(8)]
data_ranges = np.linspace(np.min(data), np.max(data), 9)
data_range_counts = np.histogram(data, bins=data_ranges)[0]

# Plot frequency of each range
plt.figure(figsize=(10, 6))
sns.barplot(x=range_labels, y=data_range_counts)
plt.title('Frequency of Each Range')
plt.xlabel('Range')
plt.ylabel('Frequency')
plt.xticks(range(len(data_ranges)-1), [f'{data_ranges[i]:.2f} - {data_ranges[i+1]:.2f}' for i in range(len(data_ranges)-1)])
plt.savefig('Frequency of Each Range.png')
plt.show()
