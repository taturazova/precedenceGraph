import networkx as nx
import matplotlib.pyplot as plt

def getGraph(question):

    ops=getOperations(question)
    G = nx.MultiDiGraph()
    edge_labels = dict()
    # Check if there is a conflict
    for i,op in enumerate(ops):
        for j in range(i+1,len(ops)):
            if(ops[i].get("data_item")==ops[j].get("data_item")) and (ops[i].get("num")!=ops[j].get("num")):
                if(ops[i].get("type")=='w') or (ops[i].get("type")=='r' and ops[j].get("type")=='w'):
                # conflict
                    G.add_edge(ops[i].get("num"), ops[j].get("num"), label=ops[j].get("data_item"))
                    edge_labels[(ops[i].get("num"),ops[j].get("num"))] = ops[j].get("data_item")
    pos = nx.spring_layout(G)
    nx.draw_networkx(G,with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
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
        op=op+dict.get('data_item')
    return op

# Get Precedence Graph
getGraph("r1(A);w2(A);r1(C);c1;r2(B);w2(B);c2;r3(B);r3(A);w3(B);w3(C);c3;r4(A);r4(B);r4(C);w4(D);c4")
