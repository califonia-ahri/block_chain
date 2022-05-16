# it doesn't work due to site's remodeling
import requests
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("read created blocks today")
url = "https://www.blockchain.com/btc/blocks?format=json"
resp = requests.get(url=url)
data = resp.json
print(data)

header = []
block = data["blocks"]
for n in range(len(block)):
    height = block[n]["height"]
    btime = block[n]["time"]
    bhash = block[n]["hash"]
    header.append([height, btime, bhash])

# read created block yesterday
stime = btime - 24 * 60 * 60

# read created block in the last 10 days
for nDay in range(0, 10):
    ts = time.gmtime(stime)
    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    print("%s read created blocks.." % date)

    url = "https://www.blockchain.com/btc/blocks/" + str(stime) + "000?format=json"
    resp = requests.get(url=url)
    data = resp.json()

    block = data["blocks"]
    for n in range(len(block)):
        height = block[n]["height"]
        btime = block[n]["time"]
        bhash = block[n]["hash"]
        header.append([height, btime, bhash])

    stime = block[0]["time"] - 24 * 60 * 60

df = pd.DataFrame(header, columns=["Height", "Time", "Hash"])
sdf = df.sort_values("Time")
sdf = sdf.rest_index()
print("%d blocks readed." % len(df))

# observe consuming time of creating a block distribution
mtime = sdf["Time"].diff().values
mtime = mtime[np.logical_not(np.isnan(mtime))]
print("average mining time = %d (s)" % np.mean(mtime))
print("standard deviation = %d (s)" % np.std(mtime))

plt.figure(figsize=(8, 4))
n, bins, patches = plt.hist(
    mtime, 30, facecolor="red", edgecolor="black", linewidth=0.5, alpha=0.5
)
plt.title("Mining time distribution")
plt.show()

# percentage of mining a block in 5 minutes
s = 60 * 5
p = 1 - np.exp(-s / np.mean(mtime))
print("percentage of mining a block in 5 minutes = %.2f (%s)" % (p * 100, "%"))
