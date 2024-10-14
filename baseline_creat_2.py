import json

'''
NSPA
The output result represents the proportion of unmeasured flows measured by the switch. 
Replace the "switch_p" in topology.json with the output proportion, and iterate until the value stabilizes.
'''

with open("baseline_2.py", 'w') as f:
    f.write("import gurobipy, json\n")
    f.write("\n")
    f.write("model = gurobipy.Model()\n")
    f.write("\n")
    
    with open('topology.json', 'r') as fp:
        data = json.load(fp)
        switch_list = data["switches"]
        paths_list = data["paths"]
        switch_p = data["switch_p"]
    fp.close()    
    
    for switch in switch_list:
        f.write(switch + " = model.addVar(lb=0, ub=1, vtype=gurobipy.GRB.CONTINUOUS, name='" + switch + "')\n")
    for switch in switch_list:
        f.write(switch + "_l = model.addVar(vtype=gurobipy.GRB.CONTINUOUS, name='" + switch + "_l')\n")
    f.write("obj = model.addVar(vtype=gurobipy.GRB.CONTINUOUS, name='obj')\n")
    f.write("\n")
    
    switch_l = {}
    egress_switch = {}
    for paths in paths_list:
        pre_num = 0
        egress_str = str(paths_list[paths][0]) + "-"
        for switch in paths_list[paths][1][:-1]:
            if switch not in switch_l:
                switch_l[switch] = 0
            egress_str += switch + "*" + str(paths_list[paths][0] - pre_num) + "-"
            switch_l[switch] += paths_list[paths][0] - pre_num
            
            # During the first run, please comment out the following two lines of code.
            temp = switch_p[switch] * (paths_list[paths][0] - pre_num)
            pre_num += temp
            
        egress_str = egress_str[:-1]
        if paths_list[paths][1][-1] not in egress_switch:
            egress_switch[paths_list[paths][1][-1]] = egress_str
        else:
            egress_switch[paths_list[paths][1][-1]] += "+" + egress_str
        
    num = 0
    for switch in switch_l:
        num += 1
        temp = str(switch_l[switch])
        flag = 0
        if switch in egress_switch:
            temp += "+" + egress_switch[switch]
            flag = 1
        f.write("model.addConstr(" + switch + "*" + temp + "==" +switch + "_l,\"c" + str(num) + "\")\n")
        if flag:
            num += 1
            f.write("model.addConstr(" + switch + "*" + temp + ">=0,\"c" + str(num) + "\")\n")
    
    for switch in egress_switch:
        if switch not in switch_l:
            num += 1
            f.write("model.addConstr(" + egress_switch[switch] + "==" +switch + "_l,\"c" + str(num) + "\")\n")
    num += 1
    f.write("model.addConstr(obj == gurobipy.max_(")
    temp = ""
    for switch in switch_list:
        temp += switch + "_l,"
    temp = temp[:-1]
    f.write(temp + "),\"c" + str(num) + "\")\n")
    f.write("\n")
    
    f.write("model.setObjective(obj)\n")
    f.write("model.optimize()\n")
    f.write("print(\"Obj:\", model.objVal)\n")
    f.write("for v in model.getVars():\n")
    f.write("\tprint(f\"{v.varName}:{round(v.x,6)}\")\n")
    f.write("\n")
    
f.close()
                