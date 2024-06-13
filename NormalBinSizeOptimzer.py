import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, chisquare

# # Using generated normally distributed dataset
# np.random.seed(42)  # For reproducibility
# data = np.random.normal(loc=100, scale=3, size=1000)

# Using actual dataset
data = pd.read_csv('data/spruce.csv')['logsize']

def sturges_formula(n):
    return int(np.ceil(np.log2(n) + 1))

def rice_rule(n):
    return int(np.ceil(2 * n**(1/3)))

def scotts_rule(data):
    n = len(data)
    sigma = np.std(data)
    bin_width = 3.5 * sigma / n**(1/3)
    return int(np.ceil((np.max(data) - np.min(data)) / bin_width))

def freedman_diaconis_rule(data):
    n = len(data)
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    bin_width = 2 * iqr / n**(1/3)
    return int(np.ceil((np.max(data) - np.min(data)) / bin_width))

def doanes_formula(data):
    n = len(data)
    g1 = pd.Series(data).skew()
    sigma_g1 = np.sqrt((6 * (n - 2)) / ((n + 1) * (n + 3)))
    return int(np.ceil(1 + np.log2(n) + np.log2(1 + np.abs(g1) / sigma_g1)))

# Calculate the optimal number of bins using each method
n = len(data)
bins_sturges = sturges_formula(n)
bins_rice = rice_rule(n)
bins_scott = scotts_rule(data)
bins_fd = freedman_diaconis_rule(data)
bins_doane = doanes_formula(data)

# Fit a Gaussian distribution to the data
mu, std = norm.fit(data)

# Create x values for the Gaussian fit line
x = np.linspace(np.min(data), np.max(data), 100)

# Calculate the Gaussian fit line
p = norm.pdf(x, mu, std)

# Plot histograms and Gaussian fit lines
def plot_hist_with_fit(ax, data, bins, method_name):
    # Calculate the observed frequencies (histogram)
    observed_freq, bin_edges = np.histogram(data, bins=bins, density=True)
    
    # Calculate the expected frequencies based on the Gaussian fit
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    expected_freq = norm.pdf(bin_centers, mu, std)
    
    # Scale expected frequencies to match the histogram's total area
    expected_freq_scaled = expected_freq * np.sum(observed_freq) / np.sum(expected_freq)
    
    # Chi-square statistic
    chi2_stat, p_value = chisquare(observed_freq, f_exp=expected_freq_scaled)
    
    # R-squared value
    ss_res = np.sum((observed_freq - expected_freq_scaled)**2)
    ss_tot = np.sum((observed_freq - np.mean(observed_freq))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    ax.hist(data, bins=bins, density=True, edgecolor='k', alpha=0.6)
    ax.plot(x, p, 'k', linewidth=2)
    title = f"{method_name}: {bins} bins\n"
    title += f"Chi2 = {chi2_stat:.2f}, R2 = {r_squared:.2f}"
    ax.set_title(title)

# Plot histograms using the calculated bin sizes
fig, axes = plt.subplots(3, 2, figsize=(15, 15))

plot_hist_with_fit(axes[0, 0], data, bins_sturges, "Sturges' Formula")
plot_hist_with_fit(axes[0, 1], data, bins_rice, "Rice Rule")
plot_hist_with_fit(axes[1, 0], data, bins_scott, "Scott's Rule")
plot_hist_with_fit(axes[1, 1], data, bins_fd, "Freedman-Diaconis Rule")
plot_hist_with_fit(axes[2, 0], data, bins_doane, "Doane’s Formula")

# Hide the unused subplot
axes[2, 1].axis('off')

plt.tight_layout()
plt.show()