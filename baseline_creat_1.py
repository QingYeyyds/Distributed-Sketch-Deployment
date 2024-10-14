import json

'''
The output indicates the switches where the complete sketch is deployed.
'''

with open("baseline_1.py", 'w') as f:
    f.write("import gurobipy\n")
    f.write("\n")
    f.write("model = gurobipy.Model()\n")
    f.write("\n")
    
    with open('topology.json', 'r') as fp:
        data = json.load(fp)
        switch_list = data["switches"]
        paths_list = data["paths"]
        
        for i in switch_list:
            f.write(i + " = model.addVar(lb=0, ub=1, vtype=gurobipy.GRB.INTEGER, name='" + i + "')\n")
        f.write("\n")
        
        num = 0
        for paths in paths_list:
            path = paths_list[paths][1]
            if paths_list[paths][0] != 0:
                num += 1
                f.write("model.addConstr(")
                tmp = ""
                for switch in path:
                    tmp += switch + "+"
                f.write(tmp[:-1] + ">=1,\"c" + str(num) + "\")\n")
        f.write("\n")

        str_switch_sum = ""
        for switch in switch_list:
            str_switch_sum += switch + "+"
        str_switch_sum = str_switch_sum[:-1]
        f.write("model.setObjective(" + str_switch_sum + ")\n")
        f.write("model.optimize()\n")
        f.write("print(\"Obj:\", model.objVal)\n")
        f.write("for v in model.getVars():\n")
        f.write("\tprint(f\"{v.varName}:{round(v.x,6)}\")\n")
    fp.close()
f.close()
                