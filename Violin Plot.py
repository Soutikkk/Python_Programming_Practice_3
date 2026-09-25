import matplotlib.pyplot as plt
import numpy as np

# Generate random data
np.random.seed(10)
data = np.random.randn(100)

# Create a violin plot
plt.figure(figsize=(7, 5))

plt.violinplot(
    data,
    showmeans=True,
    showmedians=True,
    showextrema=True
)

# Add title and labels
plt.title("Violin Plot of Random Data")
plt.xlabel("Data")
plt.ylabel("Values")

# Add grid for better readability
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Display the plot
plt.show()
