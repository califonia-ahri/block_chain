# Collecting coinbase transaction from third party API server
# refer few block's minor wallet
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

# refer last number of block
resp = requests.get(url="https://blockchain.info/latestblock")
data = resp.json()
nHeight = data["height"]

# read few blocks from last, collect wallet address of coinbase transaction

mining = []

for n in range(nHeight, nHeight - 100, -1):
    url = "https://blockchain.info/block-height/" + str(n) + "?format=json"
    resp = requests.get(url=url)
    data = resp.json()
    block = data["blocks"][0]

    stime = block["time"]
    addr = block["tx"][0]["out"][0]["addr"]
    value = block["tx"][0]["out"][0]["value"]

    ts = time.gmtime(stime)
    data = time.strftime("%Y-%m-%d %H:%M:%S", ts)

    # store result in list
    mining.append([data, addr, value])

    # print result
    print("#%d : %s\t%s\t%f" % (n, data, addr, value * 1e-8))

# store results in dataframe
df = pd.DataFrame(mining, columns=["Data", "Address", "Reward"])

# binding same wallet
grp = df.groupby("Address").Address.count()
print()
print(grp)

# Histogram
plt.figure(figsize=(6, 3))
plt.title("Miner's Address")
x = list(range(1, len(grp.values) + 1))
plt.bar(
    x, grp.values, width=1, color="red", edgecolor="black", linewidth=0.5, alpha=0.5
)
plt.show()
