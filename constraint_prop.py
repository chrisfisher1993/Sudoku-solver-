"""Constraint propagation"""

def AC3(csp, queue=None, removals=None):
    """AC3 constraint propagation
    AC3(variables csp, domains queue, constraints removals)
    csp - constraint satisfaction problem
    queue - list of constraints (might be None in which case they are
        populated from csp's variable list (len m) and neighbors (len k1...km):
        [(v1, n1), (v1, n2), ..., (v1, nk1), (v2, n1), (v2, n3), ... (v2, nk2),
         (vm, n1), (vk, n2), ..., (vk, nkm) ]

    removals - List of variables and values that have been pruned.  This is only
        useful for backtracking search which will enable us to restore things
        to a former point

    returns
        True - All constraints have been propagated and hold
        False - A variables domain has been reduced to the empty set through
            constraint propagation.  The problem cannot be solved from the
            current configuration of the csp.
    """

    # Hints:
    # Remember that:
    #    csp.variables is a list of variables of fixed length
    #    csp.neighbors[x] is the neighbors of variable x of varying lengths

    "queue by default is assigned None so we use that as the base case"
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    """After we've assigned the queue with pairs of variables and their neighbors, we'll call support_pruning to make sure
    "we can prune values"""
    csp.support_pruning()

    "while loop that pops a pair out of the queue"
    while queue:
        (Xi, Xj) = queue.pop()
        "if we have to remove a value since there's a violation in the constraints"
        if revise(csp, Xi, Xj, removals):
            "return false if not in the csp current domains of our csp variable"
            if not csp.curr_domains[Xi]:
                return False
            "otherwise we iterate through the neighbors and so long as the two values are not the" \
            "same we can add them to the queue"
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True


def revise(csp, Xi, Xj, removals):
    """Return true if we remove a value.
    Given a pair of variables Xi, Xj, check for each value i in Xi's domain
    if there is some value j in Xj's domain that does not violate the
    constraints.

    csp - constraint satisfaction problem
    Xi, Xj - Variable pair to check
    removals - list of removed (variable, value) pairs.  When value i is
        pruned from Xi, the constraint satisfaction problem needs to know
        about it and possibly updated the removed list (if we are maintaining
        one)
    """
    #Restrict domain Xi such that it is consistent with Xj ”
    revised = False
    # x in current domains from Xi's original list
    for x in csp.curr_domains[Xi][:]:
        #If Xi=x conflicts with Xj=y for every possible y then eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):  # constraint holds between x & y:
            csp.prune(Xi, x, removals)
            revised = True
    return revised