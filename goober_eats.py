from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

bx = []
by = []
with open("data/Goober Eats_price_history.csv") as csv:
    for i, line in enumerate(csv):
        line = line.split(",")
        if i != 0:
            bx.append(float(line[0]))  # Assuming bx is a label (string)
            by.append(float(line[1].strip()))  # Convert y-values to float
    plt.plot(bx, by, color="green", label="Goober")

with open("data/Coffee_price_history.csv") as csv:
    for i, line in enumerate(csv):
        line = line.split(",")
        if i != 0:
            bx.append(float(line[0]))  # Assuming bx is a label (string)
            by.append(float(line[1].strip()) * 0.4)  # Convert y-values to float
    plt.plot(bx, by, color="red", label="Coffee")

plt.show()