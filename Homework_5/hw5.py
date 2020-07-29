import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max.columns', 100)
pd.set_option('display.max.rows', 20530)

data = pd.read_table('HiSeqV2', index_col=0)
data = 2 ** data  # log->normal
data_normal = data.loc[:, [True if int(i[-2]) else False for i in data.columns]]
data_tumor = data.loc[:, [False if int(i[-2]) else True for i in data.columns]]

data_normal_mean = data_normal.mean(axis=1)
data_tumor_mean = data_tumor.mean(axis=1)
logfc = np.log2(data_tumor_mean) - np.log2(data_normal_mean)
pvals = [ttest_ind(data_normal.values[i], data_tumor.values[i])[1] for i in range(data_normal.values.shape[0])]
logfc_pvals = pd.DataFrame([logfc], index=['logFC']).T
logfc_pvals['-log10 pval'] = -np.log10(pvals)

print(logfc_pvals)

ax = sns.scatterplot(x='logFC', y='-log10 pval', data=logfc_pvals)
plt.show()
