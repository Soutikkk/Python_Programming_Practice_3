import matplotlib.pyplot as plt

products = ["A", "B", "C"]
sales = [100, 150, 120]

plt.bar(products, sales)
plt.title("Sales")
plt.xlabel("Products")
plt.ylabel("Sales")
plt.show()