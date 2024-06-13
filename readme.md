# Histogram Bin Size Optimizer

Here are some Python scripts to help analyze histogram data to determine model of fit and optimal bin size.  The following rules are implemented and their fit and the basic statistics are output for a given dataset input.

- Sturges' Formula
- Rice Rule
- Scott's Rule
- Freedman-Diaconis Rule
- Doane’s Formula

## example output
For an example CSV from the Vincent Arel-Bundock's [histogram data](https://vincentarelbundock.github.io/Rdatasets/datasets.html) (log size of trees), the following output was generated:

### Distribution optimizer with fits and QQ plots

![Distribution Optimizer](misc/ResultsDemo_DistributionOptimizer.png)

### Distribution stats (terminal output)

![Distribution Stats](misc/ResultsDemo_DistributionStats.png)


### Bin size optimizer for normally distributed data
![Bin Size Optimizer](misc/ResultsDemo_BinSizeOptimizer.png)