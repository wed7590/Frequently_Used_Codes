import matplotlib as mpl
import matplotlib.pyplot as plt
import csv

ch0 = []
ch1 = []
ch2 = []
i = 0
f = open("data.csv")
for row in csv.reader(f):
    ch0.append(int(row[0]))
    ch1.append(int(row[1]))
    ch2.append(int(row[2]))
    i+=1
x = range(i)
plt.plot(x, ch0)
plt.plot(x, ch1)
plt.plot(x, ch2)
plt.show()

