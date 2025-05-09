import numpy as np 

inputs = [1.2, 5.7, 9.2] # Ouput from each neuron in previous layer
# Every unique input has a unique weight associated with it
weights = [
    [2.2, 4.1, 3.3],
    [1.2, 3.2, 4.7],
    [5.1, 4.6, 7.3]
]

# every unique neuron has a unique bias too
biases = [ 3, 0.2, 1.5]


# Step 1: Neuron to add up all the inputs times the weights + bias
layer_outputs = [] # Output of current layer
for neuron_weights, neuron_bias in zip(weights, biases):
    neuron_output = 0 # output of current neuron
    for n_input, weight in zip(inputs, neuron_weights):
        neuron_output += n_input + weight
    neuron_output += neuron_bias
    layer_outputs.append(neuron_output)

print(layer_outputs)

'''
Doing dot product with a layer of neurons and multiple inputs
a = [1, 2, 3]
b = [4, 5, 6]
dot product = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
'''

# Weights always has to be first as that is what determines how the returning array should be indexed
# Simply said, it is the weights that differentiate how many neurons are there
output = np.dot(weights, inputs) + biases
print(output)

# Shapes = Size at each dimension of that dimension - Always homologus
# Eg: a = [1, 2, 3, 4 ] -> Shape = 4 i.e 1D Array / Vector
# b = [
#       [1, 2, 3],      -> Shape = (2, 4) i.e 2D Array, Matrix
#       [4, 5, 6]
#   ]