import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

rmse_df = pd.DataFrame({"model": ["collaborative: item-based KNN", "collaborative: NMF", "neural net"],
                        "rmse": [1.2855, 1.306, 0.4325]})

fig, ax = plt.subplots(figsize = (10,6))
sns.barplot(data = rmse_df, x = "model", y = "rmse")
plt.xlabel("model")
plt.ylabel("RMSE")
#plt.xticks(rotation = 45)
plt.title("Model RMSE Comparison")
plt.subplots_adjust(left = 0.06, right = 0.99, bottom = 0.08, top = 0.95)
plt.savefig("rmse_plot.png")
plt.show()
