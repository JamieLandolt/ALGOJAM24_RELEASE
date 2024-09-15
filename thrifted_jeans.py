from matplotlib import pyplot as plt

bx = []
by = []
with open("data/Thrifted Jeans_price_history.csv") as csv:
    for i, line in enumerate(csv):
        line = line.split(",")
        if i != 0:
            bx.append(float(line[0]))  # Assuming bx is a label (string)
            by.append(float(line[1].strip()))  # Convert y-values to float
    plt.plot(bx, by, color="green", label="Goober")

half_by = len(by)//2
avg1 = sum(by[:half_by])/half_by
avg2 = sum(by[half_by:])/len(by[half_by:])
print(avg1, avg2)

m = (avg2 - avg1)/(365 * 3/4 - 365 * 1/4)
c = avg2 - m * 365 * 3/4

avg_growth = m * 365

percentage_growth = 100 * avg_growth / c

print(f"Equation: val = {round(m, 2)}(day) + {round(c, 2)}")

# Eqn 1
# val = 0.06121634425160155(day) + 47.4611514441842
# c2
start_val = 0.06121634425160155 * 365 + 47.4611514441842

# day 365 * 2
end_val = (percentage_growth/100 + 1) * start_val

m2 = (end_val - start_val)/365

#Eqn 2
print(f"Prediction Equation: val = {m2}(day) + {start_val}")

print(f"{percentage_growth=}")
print(f"{c=}, {c + avg_growth=}")

plt.show()
