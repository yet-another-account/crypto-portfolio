import json
import urllib2
import matplotlib.pyplot as plt

assetlist = []

with open('portfolio.json') as fh:
    pf = json.load(fh)
    assets = pf['assets']
    for asset in assets:
        name = asset['name']
        price_api = urllib2.urlopen(
            "https://api.coinmarketcap.com/v1/ticker/{}".format(name)).read()

        price = json.loads(price_api)[0]
        usdprice = float(price['price_usd'])
        quantity = asset['amount']
        assetlist.append((name, usdprice * quantity, quantity, usdprice))

assetlist = sorted(assetlist, key=lambda a: a[1], reverse=True)
assettxt = [(name.ljust(15), str(am).ljust(14), str(q).ljust(8), str(upr).ljust(10))
             for name, am, q, upr in assetlist]

for asset in assettxt:
    print("{} ${} ({} @ ${} each)".format(*asset))

total = sum([k[1] for k in assetlist])
print("Total:".ljust(16) + "$" + str(total))

# make plot

labels = [k[0] for k in assetlist]
values = [k[1] for k in assetlist]

with open('portfoliotemplate.html') as pft:
    template = pft.read()
    template = template % (json.dumps(values), json.dumps(labels))
    with open('myportfolio.html', 'w') as pfout:
        pfout.write(template)

print("Portfolio pie chart generated at myportfolio.html!")
