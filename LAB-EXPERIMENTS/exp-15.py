# Experiment 15: Simple Decision Tree Classifier (Standard Python)

# Sample Dataset: [Outlook, Humidity] -> PlayTennis
# Outlook: 0 = Sunny, 1 = Overcast, 2 = Rain
# Humidity: 0 = High, 1 = Normal
# PlayTennis: 0 = No, 1 = Yes

class SimpleDecisionTree:
    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict_one(self, sample):
        outlook, humidity = sample[0], sample[1]
        
        # Simple Decision Logic (Root: Outlook)
        if outlook == 1: # Overcast
            return 1 # Yes
        elif outlook == 0: # Sunny
            if humidity == 0: # High
                return 0 # No
            else:
                return 1 # Yes
        else: # Rain
            if humidity == 0: # High
                return 0 # No
            else:
                return 1 # Yes

    def predict(self, X_test):
        return [self.predict_one(x) for x in X_test]

if __name__ == "__main__":
    print("--- Experiment 15: Decision Tree ---")
    
    # Training samples
    X_train = [
        [0, 0], # Sunny, High -> No
        [0, 1], # Sunny, Normal -> Yes
        [1, 0], # Overcast, High -> Yes
        [2, 0], # Rain, High -> No
        [2, 1]  # Rain, Normal -> Yes
    ]
    y_train = [0, 1, 1, 0, 1]
    
    dt = SimpleDecisionTree()
    dt.fit(X_train, y_train)

    test_samples = [
        [0, 1], # Sunny, Normal
        [2, 0], # Rain, High
        [1, 0]  # Overcast, High
    ]
    
    predictions = dt.predict(test_samples)
    
    outlook_map = {0: 'Sunny', 1: 'Overcast', 2: 'Rain'}
    humidity_map = {0: 'High', 1: 'Normal'}
    play_map = {0: 'No', 1: 'Yes'}
    
    print("Predictions on Test Data:")
    for sample, pred in zip(test_samples, predictions):
        print(f"  Outlook: {outlook_map[sample[0]]:<8} | Humidity: {humidity_map[sample[1]]:<6} -> Play Tennis: {play_map[pred]}")
