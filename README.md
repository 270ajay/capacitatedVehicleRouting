# Optimization of Capacitated Vehicle Routing Problem using PuLP iteratively

**Description**

-	Optimizing Capacitated Vehicle Routing Problem (CVRP) using Mixed Integer Programming, iteratively.  
-   Each iteration, if order `demand > minDeliveryAmount`, then `max(minDeliveryAmount, orderDemand * minDeliveryPercentage)` is used as demand for that order.
-   Program ends when every order has 0 demand. 
-   Mixed Integer Model used is in page3,4 of `https://arxiv.org/pdf/1606.01935.pdf`.



## Prerequisites

To run this **Python** program, please install **pulp**, **csv**, **logging** libraries/packages. 



## Structure Of The Project

All the code is in src folder. 
Input data (demands and travel matrix csv files) used is in input folder.
Output (csv and log file) from Optimizer is in output folder.

To run the code, please run **routeOptimization.py** (to run from cmd, please enter python.exe routeOptimization.py).


## Sample Lp file

```shell
\* Assign_fromOrder_toOrder *\
Minimize
OBJ: 350 Assign_Order5_Order6 + 350 Assign_Order5_Order7
 + 430 Assign_Order5_Warehouse + 490 Assign_Order6_Order5
 + 320 Assign_Order6_Order7 + 200 Assign_Order6_Warehouse
 + 470 Assign_Order7_Order5 + 230 Assign_Order7_Order6
 + 320 Assign_Order7_Warehouse + 300 Assign_Warehouse_Order5
 + 240 Assign_Warehouse_Order6 + 350 Assign_Warehouse_Order7
Subject To
CorrectFlowCt_Order5: - Assign_Order5_Order6 - Assign_Order5_Order7
 - Assign_Order5_Warehouse + Assign_Order6_Order5 + Assign_Order7_Order5
 + Assign_Warehouse_Order5 = 0
CorrectFlowCt_Order6: Assign_Order5_Order6 - Assign_Order6_Order5
 - Assign_Order6_Order7 - Assign_Order6_Warehouse + Assign_Order7_Order6
 + Assign_Warehouse_Order6 = 0
CorrectFlowCt_Order7: Assign_Order5_Order7 + Assign_Order6_Order7
 - Assign_Order7_Order5 - Assign_Order7_Order6 - Assign_Order7_Warehouse
 + Assign_Warehouse_Order7 = 0
EachOrderOnceCt_Order5: Assign_Order5_Order6 + Assign_Order5_Order7
 + Assign_Order5_Warehouse = 1
EachOrderOnceCt_Order6: Assign_Order6_Order5 + Assign_Order6_Order7
 + Assign_Order6_Warehouse = 1
EachOrderOnceCt_Order7: Assign_Order7_Order5 + Assign_Order7_Order6
 + Assign_Order7_Warehouse = 1
MaxNumOfRoutesCt_Warehouse: Assign_Warehouse_Order5 + Assign_Warehouse_Order6
 + Assign_Warehouse_Order7 <= 10
CapacityAndSubtourElimCt_Order5_Order6: 110 Assign_Order5_Order6 + CurrentLoad_Order5
 - CurrentLoad_Order6 <= 100
CapacityAndSubtourElimCt_Order5_Order7: 120 Assign_Order5_Order7 + CurrentLoad_Order5
 - CurrentLoad_Order7 <= 100
CapacityAndSubtourElimCt_Order6_Order5: 130 Assign_Order6_Order5 - CurrentLoad_Order5
 + CurrentLoad_Order6 <= 100
CapacityAndSubtourElimCt_Order6_Order7: 120 Assign_Order6_Order7 + CurrentLoad_Order6
 - CurrentLoad_Order7 <= 100
CapacityAndSubtourElimCt_Order7_Order5: 130 Assign_Order7_Order5 - CurrentLoad_Order5
 + CurrentLoad_Order7 <= 100
CapacityAndSubtourElimCt_Order7_Order6: 110 Assign_Order7_Order6 - CurrentLoad_Order6
 + CurrentLoad_Order7 <= 100
CapacityAndSubtourElimCt_Warehouse_Order5: 130 Assign_Warehouse_Order5
 - CurrentLoad_Order5 + CurrentLoad_Warehouse <= 100
CapacityAndSubtourElimCt_Warehouse_Order6: 110 Assign_Warehouse_Order6
 - CurrentLoad_Order6 + CurrentLoad_Warehouse <= 100
CapacityAndSubtourElimCt_Warehouse_Order7: 120 Assign_Warehouse_Order7
 - CurrentLoad_Order7 + CurrentLoad_Warehouse <= 100
Bounds
30 <= CurrentLoad_Order5 <= 100
10 <= CurrentLoad_Order6 <= 100
20 <= CurrentLoad_Order7 <= 100
CurrentLoad_Warehouse <= 100
Binaries
Assign_Order5_Order6
Assign_Order5_Order7
Assign_Order5_Warehouse
Assign_Order6_Order5
Assign_Order6_Order7
Assign_Order6_Warehouse
Assign_Order7_Order5
Assign_Order7_Order6
Assign_Order7_Warehouse
Assign_Warehouse_Order5
Assign_Warehouse_Order6
Assign_Warehouse_Order7
End
```