# Experiment 11: Map Coloring using Constraint Satisfaction Problem (CSP)

def is_valid_color(node, color, assignment, neighbors):
    for neighbor in neighbors.get(node, []):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def map_coloring(variables, colors, neighbors, assignment={}):
    if len(assignment) == len(variables):
        return assignment # All variables assigned

    # Pick unassigned variable
    unassigned = [v for v in variables if v not in assignment]
    var = unassigned[0]

    for color in colors:
        if is_valid_color(var, color, assignment, neighbors):
            assignment[var] = color
            result = map_coloring(variables, colors, neighbors, assignment)
            if result is not None:
                return result
            del assignment[var] # Backtrack

    return None

if __name__ == "__main__":
    print("--- Experiment 11: Map Coloring (CSP) ---")
    
    # Regions/Variables
    regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    # Available Colors
    colors = ['Red', 'Green', 'Blue']
    
    # Adjacency Constraints
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }

    solution = map_coloring(regions, colors, neighbors)
    if solution:
        print("Color Assignment for Map Regions:")
        for region, color in solution.items():
            print(f"  {region}: {color}")
    else:
        print("No valid coloring solution found.")
