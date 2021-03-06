# -*- coding: utf-8 -*-
"""OPTIMA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dXMtiLiCRDsXzbBVTrqQ4i2eSrg4xq_G
"""

pip install requests

pip install python-firebase

from firebase import firebase

database=firebase.FirebaseApplication("https://optima-55043.firebaseio.com/",None)

results=database.get("https://optima-55043.firebaseio.com/",'orders')

print(results)

answers=[]
for i in results:
  answers.append(results[i])

final=[]
for i in answers:
  for item in i:
    final.append(i[item])

print(final)

amount=[]
for i in final:
  for items in i:
    if(items=='amount'):
      amount.append(i[items])

date_time=[]
for i in final:
  for items in i:
    if(items=='dateTime'):
      amount.append(i[items])

indi_products=[]
for i in final:
  for items in i:
    if(items=='products'):
      fin=[]
      for j in i[items]:
        fin.append(j)
      indi_products.append(fin)

print(indi_products)

count=0
pid=[]
price=[]
qt=[]
item=[]
customer=[]
for i in indi_products:
  count+=1
  for j in i:
    customer.append(count)
    for items in j:
        if(items=='id'):
          pid.append(j[items])
        if(items=='price'):
          price.append(j[items])
        if(items=='quantity'):
          qt.append(j[items])
        if(items=='title'):
          item.append(j[items])

import pandas as pd

column_names=["customer_number","product_id","price","quantity","item_name"]
df=pd.DataFrame(columns=column_names)

df['customer_number']=customer

df['product_id']=pid

df['price']=price

df['quantity']=qt

df['item_name']=item

print(df.head(2))

x=(df.groupby("item_name").sum().reset_index())

x.sort_values('quantity',ascending=False,inplace=True)

import matplotlib.pyplot as plt

names=x['item_name'].tolist()

values=x['quantity'].tolist()

my_circle=plt.Circle( (0,0), 0.8, color='white')
my_circle1=plt.Circle( (0,0), 0.8, color='white')

from palettable.colorbrewer.qualitative import Pastel1_7

plt.pie(values, labels=names, colors=Pastel1_7.hex_colors)
m1=plt.gcf()
m1.gca().add_artist(my_circle1)
plt.savefig('1.png',format='png')
plt.title("Sales of all items")
plt.show()

from PIL import Image

x['total_value']=x['price']*x['quantity']

order_preference=x['item_name'].tolist()

x.sort_values('total_value',ascending=False,inplace=True)

max_profit=x["item_name"].tolist()

paisa_generated=x["total_value"].tolist()

plt.hlines(y=max_profit, xmin=0, xmax=paisa_generated, color='red')
plt.plot(paisa_generated, max_profit,"D")
plt.yticks(max_profit)
plt.savefig('2.png',format='png')
plt.title("Total revenue generated from each product")
plt.show()

print(x)

results2=database.get("https://optima-55043.firebaseio.com/",'requestedItems')

requested_items=[]
for i,j in results2.items():
  requested_items.append(j)
print(requested_items)

for i in range(len(requested_items)):
  if(type(requested_items[i])==dict):
    for j in requested_items[i].values():
      requested_items.append(j)
    requested_items[i]=0
for i in requested_items:
  if(i==0):
    del i
req_items=pd.DataFrame(columns=["Items"])
print(req_items)

req_items["Items"]=requested_items
req_items["Count"]=[1 for i in range(len(requested_items))]

req_items['Quantity'] = req_items['Count'].groupby(req_items['Items']).transform('sum')

req_items.drop(['Count'],axis=1)

req_items.drop_duplicates(subset ="Items", 
                     keep = "first", inplace = True)

req_items.drop(["Count"],axis=1,inplace=True)

req_items

import numpy as np
plt.rcdefaults()
fig, ax = plt.subplots()
x=req_items["Items"].tolist()
y=req_items['Quantity'].to_numpy()  

y_pos = np.arange(len(x))
print(y_pos)
ax.barh(y_pos, y, align='center',ec='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(x)
ax.invert_yaxis()
plt.savefig('3.png',format='png')
ax.title("Requested Items")
plt.show()
