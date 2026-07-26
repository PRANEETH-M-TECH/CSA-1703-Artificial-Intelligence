# Experiment 6: Vacuum Cleaner Problem

class VacuumCleaner:
    def __init__(self, location='A', status_a='DIRTY', status_b='DIRTY'):
        self.location = location
        self.status = {'A': status_a, 'B': status_b}

    def clean(self):
        print(f"Initial State: Vacuum at Room {self.location}, Status: {self.status}")
        cost = 0

        while self.status['A'] == 'DIRTY' or self.status['B'] == 'DIRTY':
            current = self.location
            if self.status[current] == 'DIRTY':
                print(f"Room {current} is DIRTY -> Action: SUCK")
                self.status[current] = 'CLEAN'
                cost += 1
            else:
                print(f"Room {current} is CLEAN.")

            # Move to the other room if dirty
            if current == 'A' and self.status['B'] == 'DIRTY':
                print("Moving to Room B -> Action: RIGHT")
                self.location = 'B'
                cost += 1
            elif current == 'B' and self.status['A'] == 'DIRTY':
                print("Moving to Room A -> Action: LEFT")
                self.location = 'A'
                cost += 1

        print(f"\nFinal State: Vacuum at Room {self.location}, Status: {self.status}")
        print(f"Total Performance Cost: {cost} actions")

if __name__ == "__main__":
    print("--- Experiment 6: Vacuum Cleaner Agent ---")
    agent = VacuumCleaner(location='A', status_a='DIRTY', status_b='DIRTY')
    agent.clean()
