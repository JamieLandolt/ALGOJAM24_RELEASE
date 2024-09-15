from matplotlib import pyplot as plt

csv = "data/Coffee Beans_price_history.csv"
csv2 = "data/Milk_price_history.csv"
csv3 = "data/Coffee_price_history.csv"
last_c = 0
last_r1 = 0
d = {}
l = []
l2 = []


def test(ratio, milk_mult, bean_mult, csv, csv2, csv3):
    global last_c
    global last_r1
    global d
    global l
    global l2
    by = []
    cy = []
    with open(csv) as csv:
        for i, line in enumerate(csv):
            line = line.split(",")
            if i != 0:
                by.append(float(line[1].strip()) * float(ratio.split(":")[0]) * bean_mult)
    with open(csv2) as csv2:
        for i, line in enumerate(csv2):
            line = line.split(",")
            if i != 0:
                by[i-1] += float(line[1].strip()) * float(ratio.split(":")[1]) * milk_mult
        by = [by[i + 1] - by[i] for i in range(len(by) - 1)]
    with open(csv3) as csv3:
        for i, line in enumerate(csv3):
            line = line.split(",")
            if i != 0:
                cy.append(float(line[1].strip()))
        cy = [cy[i+1] - cy[i] for i in range(len(cy)-1)]

    c = 0
    diffs = []
    for i in range(len(cy) - 1):
        diff = abs(cy[i + 1] - by[i])
        diffs.append(diff)

        if (cy[i + 1] < 0 and by[i] < 0) or cy[i + 1] > 0 and by[i] > 0:
            c += 1
    l.append(c)
    l2.append([ratio, milk_mult, bean_mult])
    if c not in d:
        d[c] = [[ratio, milk_mult, bean_mult]]
    else:
        d[c].append([ratio, milk_mult, bean_mult])
    """if c != last_c or r1 != last_r1:
        print(f"{c=}. For {ratio=}, {milk_mult=}, {bean_mult=}")"""
    last_c = c
    last_r1 = r1

for r1 in range(1, 3):
    for r2 in range(4, 14):
        for milk_mult in range(150, 250):
            milk_mult = milk_mult / 2000
            for bean_mult in range(250, 350):
                bean_mult = bean_mult/2000
                test(f"{r1}:{r2}", milk_mult, bean_mult, csv, csv2, csv3)

print(d)
m = max(d)
print(m, d[m])

x = l
r = []
m = []
b = []
for val in l2:
    r.append(val[0])
    m.append(val[1])
    b.append(val[2])

#plt.plot(x, r, label="ratio", color="green")
x.sort()
m.sort()
b.sort()
plt.plot(m, x, label="milk", color="red")
plt.show()
plt.clf()
plt.plot(b, x, label="beans", color="blue")
plt.show()

#print(m, b, x)

with open("c_vals.txt", "w") as cs:
    for c, params in d.items():
        cs.write(f"{c},{params}")
