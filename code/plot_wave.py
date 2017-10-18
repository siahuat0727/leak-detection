import numpy as np
import matplotlib.pyplot as plt
import itertools
import os.path

def plot(location, file_name):
    path = location + file_name
    if os.path.exists(path):
        with open(path) as f:
            data = [int(x) for x in next(f).split()]
            data = data[1000:1500]
            # plt.figure(file_name)
            plt.title(location[3:-1] + "  " + file_name[:-4])
            plt.ylim(280, 420)
            plt.plot(data)
            # plt.show()
            graph_path = path[:-3] + "png"
            plt.savefig(graph_path)
            plt.clf()
            print(graph_path + " is plotted")

def plot2(location, x, y):
    file_type = ".log"
    file_name = str(x) + "-" + str(y) + "_new"  + file_type
    plot(location, file_name)

def plotAll():
    folder_name = ["no_leak", "leak"]
    for location in ["../" + str(x) + "/" for x in folder_name]:
        for x, y in itertools.product(range(1,8), range(0, 100, 20)):
            plot2(location, x, y)
        plot(location, "open_close_new.log");

plotAll()
# plot("../no_leak_new/", "open_close.txt")
