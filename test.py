import pickle


pickle_in = open("nn_w.pickle","r")
example_dict = pickle.load(pickle_in)

print(example_dict)
