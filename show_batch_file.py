import pickle

pickle_in = open("nn_w.pickle","r")
example_dict = pickle.load(pickle_in)

print(example_dict[0])
print example_dict[1]
pickle_in = open("nn.pickle","r")
example_dict = pickle.load(pickle_in)

print(example_dict[0])
print example_dict[1]
pickle_in = open("bb_w.pickle","r")
example_dict = pickle.load(pickle_in)

print(example_dict[0])
print example_dict[1]
pickle_in = open("bb.pickle","r")
example_dict = pickle.load(pickle_in)

print(example_dict[0])
print example_dict[1]
