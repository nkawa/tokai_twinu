import csv
import matplotlib.animation as anm
import matplotlib.pyplot as plt
from matplotlib import cm
import datetime

def update(i, data):
    if i != 0:
        plt.cla()
    x = []
    y = []
    label = ""
    print(str(i) + " / " + str(len(data)))
    for (i, item) in enumerate(data[i]):
        pos = item.split()
        if len(pos) == 1:
            dt_utc_naive = datetime.datetime.utcfromtimestamp(int(float(pos[0]) / 1000000000 + 3600 * 9))
            break
        x.append(float(pos[0]))
        y.append(-float(pos[1]))
    plt.xlim([-7.5, 7.5])
    plt.ylim([0, 12.5])
    plt.title(dt_utc_naive, fontsize=52)
    plt.scatter(y, x, s=800, c="blue")


with open('poses.csv') as f:
    reader = csv.reader(f)
    rows = []
    row_count = 0
    for i, row in enumerate(reader):
        if i % 10 == 0:
            rows.append(row)
            row_count += 1
    print(len(rows), "data len")
    fig = plt.figure(figsize=(30, 30))

    frame = 0
    
    ani = anm.FuncAnimation(fig, update, fargs = (rows,), interval=10, frames=row_count)
    dpi = 100
    ani.save('cardbox_locs6.mp4', writer="ffmpeg",dpi=dpi, savefig_kwargs={'transparent': True, 'facecolor' : 'none'})