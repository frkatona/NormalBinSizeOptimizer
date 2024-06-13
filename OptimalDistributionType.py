import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# # Generating a sample dataset
# np.random.seed(42)
# data = np.random.normal(loc=0, scale=1, size=1000)

# Using actual dataset
data = pd.read_csv('data/spruce.csv')['logsize']

# Define candidate distributions
distributions = {
    "norm": stats.norm,
    "lognorm": stats.lognorm,
    "expon": stats.expon,
    "gamma": stats.gamma,
    "weibull_min": stats.weibull_min
}

# Fit data to each distribution and calculate goodness-of-fit measures
results = []

for dist_name, dist in distributions.items():
    params = dist.fit(data)
    
    # Perform K-S test
    ks_stat, ks_p_value = stats.kstest(data, dist_name, args=params)
    
    # Calculate AIC and BIC
    log_likelihood = np.sum(dist.logpdf(data, *params))
    k = len(params)
    aic = 2 * k - 2 * log_likelihood
    bic = k * np.log(len(data)) - 2 * log_likelihood
    
    results.append({
        "Distribution": dist_name,
        "KS Statistic": ks_stat,
        "KS p-value": ks_p_value,
        "AIC": aic,
        "BIC": bic
    })

# Convert results to DataFrame and sort by AIC
results_df = pd.DataFrame(results).sort_values(by="AIC")
print(results_df)

# Plot histograms and Q-Q plots for each distribution
fig, axes = plt.subplots(len(distributions), 2, figsize=(12, 20))

for i, (dist_name, dist) in enumerate(distributions.items()):
    params = dist.fit(data)
    
    # Histogram
    sns.histplot(data, bins=30, kde=False, stat="density", ax=axes[i, 0])
    x = np.linspace(np.min(data), np.max(data), 100)
    axes[i, 0].plot(x, dist.pdf(x, *params), label=dist_name)
    axes[i, 0].set_title(f"{dist_name} - Histogram")
    axes[i, 0].legend()
    
    # Q-Q plot
    stats.probplot(data, dist=dist, sparams=params, plot=axes[i, 1])
    axes[i, 1].set_title(f"{dist_name} - Q-Q Plot")

plt.tight_layout()
plt.show()
