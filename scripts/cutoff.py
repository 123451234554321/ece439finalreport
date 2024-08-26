import pandas as pd
import matplotlib.pyplot as plt

# bootstrap excelini yukle
file_path = r'C:\Users\faruk\OneDrive\Masaüstü\odev\veriler\boostrap.xlsx'
bootstrap_df = pd.read_excel(file_path)

# cutoff icin ayri histogram ciz
plt.figure(figsize=(10, 6))
plt.hist(bootstrap_df[0], bins=30, edgecolor='black')  # Assuming the column has no header
plt.title('Histogram of Bootstrapped Means')
plt.xlabel('Bootstrapped Mean')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# bir boxplot grafigi
plt.figure(figsize=(8, 5))
plt.boxplot(bootstrap_df[0], vert=False)  
plt.title('Boxplot of Bootstrapped Means')
plt.xlabel('Bootstrapped Mean')
plt.grid(True)
plt.show()

# percentileleri hesapla
percentiles = bootstrap_df[0].quantile([0.10, 0.25, 0.35, 0.50, 0.65, 0.75, 0.90])
print("Percentiles:\n", percentiles)

# percentilelere gore cutoff belirle
very_low_cutoff = percentiles[0.10]
low_cutoff = percentiles[0.25]
moderate_low_cutoff = percentiles[0.35]
moderate_cutoff = percentiles[0.50]
moderate_high_cutoff = percentiles[0.65]
high_cutoff = percentiles[0.75]
very_high_cutoff = percentiles[0.90]

print(f"Very Low Cutoff: {very_low_cutoff}")
print(f"Low Cutoff: {low_cutoff}")
print(f"Moderate Low Cutoff: {moderate_low_cutoff}")
print(f"Moderate Cutoff: {moderate_cutoff}")
print(f"Moderate High Cutoff: {moderate_high_cutoff}")
print(f"High Cutoff: {high_cutoff}")
print(f"Very High Cutoff: {very_high_cutoff}")
