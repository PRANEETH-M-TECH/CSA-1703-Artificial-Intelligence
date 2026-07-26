# Experiment 16: Feed Forward Neural Network (Pure Python)
import math
import random

# Sigmoid Activation Function
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Random Weights Initialization
        random.seed(42)
        self.w_input_hidden = [[random.uniform(-1, 1) for _ in range(hidden_nodes)] for _ in range(input_nodes)]
        self.w_hidden_output = [[random.uniform(-1, 1) for _ in range(output_nodes)] for _ in range(hidden_nodes)]

    def feedforward(self, inputs):
        # Hidden layer activation
        hidden = []
        for j in range(self.hidden_nodes):
            activation = sum(inputs[i] * self.w_input_hidden[i][j] for i in range(self.input_nodes))
            hidden.append(sigmoid(activation))

        # Output layer activation
        outputs = []
        for k in range(self.output_nodes):
            activation = sum(hidden[j] * self.w_hidden_output[j][k] for j in range(self.hidden_nodes))
            outputs.append(sigmoid(activation))

        return hidden, outputs

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            for inputs, target in zip(X, y):
                # Forward Pass
                hidden, outputs = self.feedforward(inputs)

                # Backpropagation
                # Output layer error
                output_errors = [target[k] - outputs[k] for k in range(self.output_nodes)]
                output_deltas = [output_errors[k] * sigmoid_derivative(outputs[k]) for k in range(self.output_nodes)]

                # Hidden layer error
                hidden_errors = []
                for j in range(self.hidden_nodes):
                    error = sum(output_deltas[k] * self.w_hidden_output[j][k] for k in range(self.output_nodes))
                    hidden_errors.append(error)
                hidden_deltas = [hidden_errors[j] * sigmoid_derivative(hidden[j]) for j in range(self.hidden_nodes)]

                # Update Hidden-to-Output Weights
                for j in range(self.hidden_nodes):
                    for k in range(self.output_nodes):
                        self.w_hidden_output[j][k] += learning_rate * output_deltas[k] * hidden[j]

                # Update Input-to-Hidden Weights
                for i in range(self.input_nodes):
                    for j in range(self.hidden_nodes):
                        self.w_input_hidden[i][j] += learning_rate * hidden_deltas[j] * inputs[i]

if __name__ == "__main__":
    print("--- Experiment 16: Feed Forward Neural Network (XOR Problem) ---")
    
    # XOR Input/Output
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [[0], [1], [1], [0]]

    nn = NeuralNetwork(input_nodes=2, hidden_nodes=4, output_nodes=1)
    
    print("Training Neural Network...")
    nn.train(X, y, epochs=10000, learning_rate=0.5)

    print("\nResults after training:")
    for inputs in X:
        _, output = nn.feedforward(inputs)
        print(f"Input: {inputs} -> Predicted Output: {output[0]:.4f} (Target: {int(output[0] > 0.5)})")
