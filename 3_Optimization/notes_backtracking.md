# Backtracking Algorithm

if assignment complete:
    return assignment
var = Select-Unassigned-Var(assignment, csp)
for value in Domain-Values(var, assignment, csp):
    if value consistent with assignment:
        add {var = value} to assignment
        result = Backtrack(assignment, csp)
        if result ≠ failure:
            return result
        remove {var = value} from assignment
    return failure
