# item-dimensions-tabbed.txt
import csv
dict={}
dict_w={}

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
with open('warehouse-grid.csv', 'r') as file:
    read = csv.DictReader(file)
    for row in read:
        pos = [0,0]
        item=row['itemnum']
        pos[0]=int(float(row['x']))
        pos[1]=int(float(row['y']))
        dict[item]=pos
file.close()

with open('item-dimensions-tabbed.txt', 'r') as file:
    read = file.readline()
    while not (read==""):
        if not read:
            break
        numbers = read.split()
        n=str(numbers[0])
        n1= int(n)
        m=numbers[4]
        m_1=num(m)
        dict_w[n1]=m_1
        read = file.readline()
file.close()

print dict_w[138302]
print dict_w[138417]
'''
    for row in read:
        pos = [0,0]
        item=row['itemnum']
        pos[0]=int(float(row['x']))
        pos[1]=int(float(row['y']))
        dict[item]=pos
'''
