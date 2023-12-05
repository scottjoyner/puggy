import csv
import pandas as pd

data = pd.read_csv("tx.csv")

accounts = set(data['Account'])
descriptions = set(data['Description'])
categories = set(data["Category"])
category_counts = {}
for x in categories:
    category_counts[x] = 0
#print(category_counts)
inflow_category_counts = {}
outflow_category_counts = {}

inflow_category_counts = {x: 0 for x in categories}
outflow_category_counts = {x: 0 for x in categories}
account_flows = {x: [0, 0] for x in accounts} # [Inflows, Outflows]

#print(account_flows)
print(account_flows.keys())
for index, row in data.iterrows():
    if row['Amount'] > 0:
        account_flows[row["Account"]] = [account_flows[row["Account"]][0] + float(row["Amount"]), account_flows[row["Account"]][1]]
    if row['Amount'] < 0:
        account_flows[row["Account"]] = [account_flows[row["Account"]][0], account_flows[row["Account"]][1] + float(row["Amount"])]
print(account_flows)
for account in account_flows:
    print(f"Income [{int(account_flows[account][0])}] {account}")
#, account_flows[row["Account"]][2][row["Category"]] + float(row["Amount"]), account_flows[row["Account"]][3][row["Category"]]
# , account_flows[row["Account"]][2][row["Category"]], account_flows[row["Account"]][3][row["Category"]] + float(row["Amount"])
# print(f"{a} [{value} {b}]")