import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# datayı load et
file_path = r"C:\Users\faruk\OneDrive\Masaüstü\veriler\deneme.xlsx"
df = pd.read_excel(file_path, header=None)

# non numeric bir şey olma ihtimaline karsi kontrol et
data = df.values.flatten()
data = pd.Series(data)  
data = pd.to_numeric(data, errors='coerce').dropna()

# sample sayısı belirle
n_samples = 1000
sample_size = len(data)

# bootstrap yap
samples = np.random.choice(data, (n_samples, sample_size), replace=True)

# output için
samples_df = pd.DataFrame(samples)

# excele kaydet
output_file_path = r"C:\Users\faruk\OneDrive\Masaüstü\veriler\bootstrap_samples.xlsx"
samples_df.to_excel(output_file_path, index=False)

# visualizasyon
plt.figure(figsize=(12, 6))

# data histogrami orjinal
plt.subplot(1, 2, 1)
plt.hist(data, bins=30, color='blue', alpha=0.7)
plt.title('Original Data Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')

# bootstrap histogramı
sample_means = np.mean(samples, axis=1)
plt.subplot(1, 2, 2)
plt.hist(sample_means, bins=30, color='green', alpha=0.7)
plt.title('Bootstrap Sample Means Histogram')
plt.xlabel('Mean Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
