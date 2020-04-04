import pulp, varsAndCts, utilities, logging


def buildAndSolveOptimizationModel(inputData, solution):

    logging.info("\nBuilding model. Iteration: "+str(inputData.iteration))
    model = pulp.LpProblem("Assign_fromOrder_toOrder", pulp.LpMinimize)

    assignVars = varsAndCts.createAssignVehicleVars(model, inputData)
    subtourElimVars = varsAndCts.createSubtourElimVars(model, inputData)

    varsAndCts.createObjectiveFunction(model, assignVars, inputData)

    varsAndCts.createEachOrderOnceCt(model, assignVars, inputData)
    varsAndCts.createCtForCorrectFlow(model, assignVars, inputData)
    varsAndCts.createUpperBoundOnMaxNumberOfRoutesCt(model, assignVars, inputData)
    varsAndCts.createSubtourElimCt(model, assignVars, subtourElimVars, inputData)


    if inputData.writeLpFile:
        utilities.writeLpFile(model, inputData.iteration)


    pulp.LpSolverDefault.msg = 1
    logging.info("Calling solve")
    model.solve(pulp.PULP_CBC_CMD(maxSeconds = inputData.timeLimitForSolver))
    logging.info(str(pulp.LpStatus[model.status]))
    logging.info("Objective value: " + str(pulp.value(model.objective)))

    utilities.printOutputFromSolver(assignVars)
    solution = utilities.storeSolution(assignVars, solution, inputData)

    return solution

