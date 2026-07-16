import numpy as np
import matplotlib.pyplot as plt

data = np.random.rand(10, 10)

plt.imshow(data)
plt.colorbar()

plt.title("Heatmap")
plt.show()