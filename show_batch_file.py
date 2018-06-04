import pickle
pickle_in = open("nn_w.pickle","r")
example_dict = pickle.load(pickle_in)
print "Nearest Neighbor with weight"
print(example_dict[0])
for i in range(0,20):
    print example_dict[2][i]
pickle_in = open("nn.pickle","r")
example_dict = pickle.load(pickle_in)
print "Nearest Neighbor without weight"
print(example_dict[0])
for i in range(0,20):
    print example_dict[2][i]
pickle_in = open("bb_w.pickle","r")
example_dict = pickle.load(pickle_in)
print "BnB with weight"
print(example_dict[0])
for i in range(0,20):
    print example_dict[2][i]
pickle_in = open("bb.pickle","r")
example_dict = pickle.load(pickle_in)
print "BNB without weight"
print(example_dict[0])
for i in range(0,20):
    print example_dict[2][i]
