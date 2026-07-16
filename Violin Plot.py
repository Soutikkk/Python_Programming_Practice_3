import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(100)

plt.violinplot(data)

plt.title("Violin Plot")
plt.show()