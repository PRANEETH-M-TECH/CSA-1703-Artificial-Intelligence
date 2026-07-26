# Experiment 4: Crypt-Arithmetic Problem (SEND + MORE = MONEY)
import itertools

def solve_cryptarithmetic():
    # SEND + MORE = MONEY
    letters = 'SENDMOREMONEY'
    unique_letters = list(set(letters)) # S, E, N, D, M, O, R, Y (8 unique letters)
    
    if len(unique_letters) > 10:
        print("Invalid crypt-arithmetic problem: More than 10 unique letters.")
        return

    # Generate permutations of digits (0-9) for unique letters
    for perm in itertools.permutations(range(10), len(unique_letters)):
        mapping = dict(zip(unique_letters, perm))
        
        # Leading letters S and M cannot be 0
        if mapping['S'] == 0 or mapping['M'] == 0:
            continue
            
        send = mapping['S']*1000 + mapping['E']*100 + mapping['N']*10 + mapping['D']
        more = mapping['M']*1000 + mapping['O']*100 + mapping['R']*10 + mapping['E']
        money = mapping['M']*10000 + mapping['O']*1000 + mapping['N']*100 + mapping['E']*10 + mapping['Y']
        
        if send + more == money:
            print("Solution Found!")
            print(f"  SEND  -> {send}")
            print(f"+ MORE  -> {more}")
            print(f"------     -----")
            print(f" MONEY  -> {money}")
            print("\nDigit Mapping:", mapping)
            return

    print("No solution found.")

if __name__ == "__main__":
    print("--- Experiment 4: Crypt-Arithmetic (SEND + MORE = MONEY) ---")
    solve_cryptarithmetic()
