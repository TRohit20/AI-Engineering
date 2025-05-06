import numpy as np 

np.random.seed(0)

weights = [
    [2.2, 4.1, 3.3],
    [1.2, 3.2, 4.7],
    [5.1, 4.6, 7.3]
]


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

layer1 = Layer_Dense(4,5)
layer2 = Layer_Dense(5,2)

layer1.forward(weights)
#print(layer1.output)
layer2.forward(layer1.output)
print(layer2.output)