inputs = [1.2, 5.7, 9.2] # Ouput from each neuron in previous layer
# Every unique input has a unique weight associated with it
n1weights = [2.2, 4.1, 3.3]
n2weights = [1.2, 3.2, 4.7]
n3weights = [5.1, 4.6, 7.3]

# every unique neuron has a unique bias too
n1bias = 3
n2bias = 0.2
n3bias = 1.5

# Step 1: Neuron to add up all the inputs times the weights + bias
output = [inputs[0] * n1weights[0] + inputs[1] * n1weights[1] + inputs[2] * n1weights[2] + n1bias,
          inputs[0] * n2weights[0] + inputs[1] * n2weights[1] + inputs[2] * n2weights[2] + n2bias,
          inputs[0] * n3weights[0] + inputs[1] * n3weights[1] + inputs[2] * n3weights[2] + n3bias
        ]
print(output)