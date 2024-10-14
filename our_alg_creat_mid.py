import json

'''
The output indicates the fraction of traffic measured through switch.
'''

with open("our_alg_mid.py", 'w') as f:
    f.write("import gurobipy, json\n")
    f.write("\n")
    with open('topology.json', 'r') as fp:
        data = json.load(fp)
        d = data["d"]
        switch_list = data["switches"]
        paths_list = data["paths"]
    fp.close()
    
    f.write("model = gurobipy.Model()\n")
    f.write("\n")
    
    for switch in switch_list:
        f.write(switch + " = model.addVar(lb=0, ub=" + str(d) + ", vtype=gurobipy.GRB.CONTINUOUS, name=\'" + switch + "\')\n")
    f.write("obj1 = model.addVar(lb=0,vtype=gurobipy.GRB.CONTINUOUS, name=\'obj1_v\')\n")
    f.write("obj2 = model.addVar(lb=0,vtype=gurobipy.GRB.CONTINUOUS, name=\'obj2_v\')\n")
    f.write("obj3 = model.addVar(lb=0,vtype=gurobipy.GRB.CONTINUOUS, name=\'obj3_v\')\n")
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
            f.write(tmp[:-1] + ">=" + str(d) + ",\"c" + str(num) + "\")\n")

    objective1 = ""
    objective2 = ""
    for paths in paths_list:
        str_switch_sum = ""
        varianc = ""
        for switch in paths_list[paths][1]:
            str_switch_sum += switch + "+"
            varianc += switch + "**2+"
        str_switch_sum = str_switch_sum[:-1]
        varianc = varianc[:-1]
        objective1 += str_switch_sum + "+"
        objective2 += "(" + varianc + ")/" + str(len(paths_list[paths][1])) + "-((" + str_switch_sum + ")/" + str(len(paths_list[paths][1])) + ")**2+"
        
    objective3 = ""
    str_switch_sum = ""
    varianc = ""
    for switch in switch_list:
        temp = ""
        for paths in paths_list:
            if switch in paths_list[paths][1]:
                temp += switch + "*" + str(paths_list[paths][0]) + "+"
        temp = temp[:-1]
        str_switch_sum += temp + "+"
        varianc += "(" + temp + ")**2+"
    str_switch_sum = str_switch_sum[:-1]
    varianc = varianc[:-1]
    objective3 = "(" + varianc + ")/" + str(len(switch_list)) + "-((" + str_switch_sum + ")/" + str(len(switch_list)) + ")**2"    
     
    f.write("model.addConstr("+objective1[:-1]+"==obj1,\"c"+str(num+1)+"\")\n")
    f.write("model.addConstr("+objective2[:-1]+"==obj2,\"c"+str(num+2)+"\")\n")
    f.write("model.addConstr("+objective3+"==obj3,\"c"+str(num+3)+"\")\n")
    f.write("\n")

    f.write("model.setObjectiveN(obj1, index=0, priority=3, name='obj1')\n")
    f.write("model.setObjectiveN(obj2, index=1, priority=1, name='obj2')\n")
    f.write("model.setObjectiveN(obj3, index=2, priority=2, name='obj3')\n")
    f.write("model.optimize()\n")
    f.write("print(\"Obj:\", model.objVal)\n")
    f.write("for v in model.getVars():\n")
    f.write("\tprint(f\"{v.varName}:{round(v.x,6)}\")\n")
    f.write("\n")
        
    f.write("paths_switch = {}\n")
    f.write("for v in model.getVars():\n")
    f.write("\tpaths_switch[v.varName] = v.x\n")
    f.write("\n")
    f.write("with open(\"result_mid.json\",\"w\") as f:\n")
    f.write("\tjson.dump(paths_switch,f)\n")
f.close()
