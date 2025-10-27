# menuTitle: Round Metrics to Base 5

f = CurrentFont()
base = 5

for g in f:
    # print(g.name)
    # print(g.width, g.leftMargin, g.rightMargin)
    if g.leftMargin:
        g.leftMargin = base * round(g.leftMargin / base)
    if g.rightMargin:
        g.rightMargin = base * round(g.rightMargin / base)
