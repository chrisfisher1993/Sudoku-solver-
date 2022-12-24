"""We the undersigned promise that we have in good faith attempted to follow the
principles of pair programming. Although we were free to discuss ideas with others, the implementation is our own. We
have shared a common workspace (possibly virtually) and taken turns at the keyboard for the majority of the work that we
are submitting. Furthermore, any non programming portions of the assignment were
done independently. We recognize that should this not be the case, we will be subject to penalties as outlined in the
course syllabus. [Christopher Fisher & Jesus Chavez]"""

import backtrack
from csp_lib.sudoku import (Sudoku, easy1, harder1)
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv, mac
from backtrack import backtracking_search, unordered_domain_values
i = 0

for puzzle in [easy1, harder1]:
    # backtracking_search(s, select_unassigned_variable=mrv, inference=forward_checking) is not None
    # solve as much as possible by AC3 then backtrack search if needed using MRV and MAC.
    "i indicates which puzzle it is"
    i += 1
    s = Sudoku(puzzle)  # construct a Sudoku problem
    print("This is puzzle", i)
    "show the puzzle in initial state"
    s.display(s.infer_assignment())
    print("**********************")

    "AC3 search the puzzle"
    AC3(s)
    "if it meets the goal test print it out"
    if (s.goal_test(s.curr_domains)):
        s.display(s.infer_assignment())
        print("**********************")
    else:
        print("could not be solved with just AC3")
        s.display(s.infer_assignment())
        print("**********************")
        print("Now try backtrack search")
        "solved will check that backtrack search has a solution and display the puzzle if so"
        solved = backtracking_search(s, mrv) is not None
        if solved:
            s.display(s.infer_assignment())