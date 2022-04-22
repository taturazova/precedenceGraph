import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def getGraph(question):

    ops=getOperations(question)
    G = nx.MultiDiGraph()
    edge_labels = dict()
    # Check if there is a conflict
    edge_list=defaultdict(dict)
    numEdges=0
    for i,op in enumerate(ops):
        for j in range(i+1,len(ops)):
            if(ops[i].get("data_item")==ops[j].get("data_item")) and (ops[i].get("num")!=ops[j].get("num")):
                if(ops[i].get("type")=='w') or (ops[i].get("type")=='r' and ops[j].get("type")=='w'):
                # conflict
                    if (ops[i].get("num"),ops[j].get("num"),ops[j].get("data_item")) not in edge_list:
                        numEdges+=1
                        edge_list[(ops[i].get("num"),ops[j].get("num"),ops[j].get("data_item"))]=1
                        print(str(ops[i].get("num"))+" -> "+str(ops[j].get("num"))+" "+ops[j].get("data_item"))
                    G.add_edge(ops[i].get("num"), ops[j].get("num"), label=ops[j].get("data_item"))
                    edge_labels[(ops[i].get("num"),ops[j].get("num"))] = ops[j].get("data_item")
    pos = nx.spring_layout(G)
    nx.draw(G,pos,with_labels=True,connectionstyle='arc3, rad = 0.1')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    # nx.draw_networkx_edge_labels(G,pos=pos_labels,edge_labels=edge_labels)
    print("Num Edges: "+str(numEdges))
    plt.show()

# Get list of operations from question string
def getOperations(question):
    s_ops = question.split(';');
    ops=[];
    for op in s_ops:
        if(len(op)>0):
            ops.append(opToDict(op))
    return ops

# Operation to dictionary (read/write/commit, transaction number, data item)
def opToDict(operation):
    op={}
    op["type"]=operation[0]
    op["num"]=int(operation[1])
    if op.get("type")!='c':
        op["data_item"]=operation[3]

    return op

# Debug method
def dictToOp(dict):
    op=""
    op=op+dict.get('type')+str(dict.get('num'))
    if dict.get('type')!='c':
        op=op+"("+dict.get('data_item')+")"
    return op

# Print schedule in columns
def toColumnsSchedule(question):
    ops=getOperations(question)
    for op in ops:
        print("\t"*(op["num"]-1)+dictToOp(op))

question="r2(A);w2(A);r1(B);r2(B);r1(A);w1(B);w2(B);c1;r3(B);c2;w3(C);c3;"
# Get Precedence Graph
toColumnsSchedule(question)
getGraph(question)
