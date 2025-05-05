inputs = [1.2, 5.7, 9.2] # Ouput from each neuron in previous layer
# Every unique input has a unique weight associated with it
weights = [2.2, 4.1, 3.3]
# every unique neuron has a unique bias too
bias = 3

# Step 1: Neuron to add up all the inputs times the weights + bias
output = inputs[0] * weights[0] + inputs[1] * weights[1] + inputs[2] * weights[2] + bias
print(output)