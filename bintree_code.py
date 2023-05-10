nodes_list = []
leaf_list = []

AL = 0
AR = 0
C0 = 0
CL = 0
CR = 0
D = 0     # Depth
M = 0     # Mod Value
RK = 0    # Root Key
RSR = 0   # Root Structure Regulator Value


total_cost_nodes = 0
total_disbalances = 0
total_2balanced = 0
total_local_min = 0
weakly_dominant_counter = 0
parity_siblings_counter = 0
total_l1_tress = 0
increasing_paths = []

class Stack:
  def __init__(self):
    self.storage = []
  def isEmpty(self):
    return len(self.storage) == 0
  def push(self, node):
    self.storage.append(node)
  def pop(self):
    return self.storage.pop()

class Node():
    def __init__(self, id, key, SR, depth, parent):
        self.id = id
        self.key = key
        self.SR = SR
        self.parent = parent
        self.left = None
        self.right = None
        self.depth = depth
        self.visited = False
        self.is_leaf = False

        self.par_sibling = False
        self.l1_node = False
        self.is_loc_min = False
        self.loc_min = -1

        # Disbalance
        self.disbalance = 0
        self.subtree_sum = 0

        self.is_2node = False
        self.two_nodes_counter = 0
        self.is_2balanced = False
        self.leafs = []
        self.roc = 0 # right only counter
        self.loc = 0 # left only counter
        self.increasing = 0
        self.max_value = -1

def get_inputs():
    global AL
    global AR
    global C0
    global CL
    global CR
    global D
    global M
    global RK
    global RSR
    AL, AR, C0, CL, CR, D, M, RK, RSR = input().split()
    AL = int(AL)
    AR = int(AR)
    C0 = int(C0)
    CL = int(CL)
    CR = int(CR)
    D = int(D)
    M = int(M)
    RK = int(RK)
    RSR = int(RSR)

def get_inputs_from_file(dir):
    global AL
    global AR
    global C0
    global CL
    global CR
    global D
    global M
    global RK
    global RSR

    file = open(dir)

    for line in file:
        temp_line = line.strip("\n")
        AL, AR, C0, CL, CR, D, M, RK, RSR = temp_line.split()
        AL = int(AL)
        AR = int(AR)
        C0 = int(C0)
        CL = int(CL)
        CR = int(CR)
        D = int(D)
        M = int(M)
        RK = int(RK)
        RSR = int(RSR)

    file.close()

def generate_tree(RK, RSR):
    global nodes_list
    global total_cost_nodes

    # Create Root Node
    id = len(nodes_list)
    root = Node(id, RK, RSR, 0, None)
    nodes_list.append(root)
    root_cost = RK
    total_cost_nodes += root_cost
    create_child(RSR,root)

def create_child(SR,upper_node):
    global nodes_list
    global leaf_list
    global total_cost_nodes


    if SR < C0 or upper_node.depth == D:
        upper_node.is_leaf = True
        leaf_list.append(upper_node)
        return

    if C0 <= SR and SR < CL:
        #Only LEFT child exist

        # Given the values and formulas we calculate the SR and key of the new node
        new_left_SR = (SR*AL) % M
        new_left_key = (AL*(upper_node.key+1)) % M

        id = len(nodes_list) # we get the id for the new node
        # We create new left node
        # Remember that the node has the following properties: Node(id, key, SR, depth, parent)

        new_left_node = Node(id, new_left_key, new_left_SR, upper_node.depth+1, upper_node)

        # we sum up the total cost of the node
        total_cost_nodes += new_left_key * (new_left_node.depth+1)

        # we append the new node to the node_list (where we store all our nodes)
        nodes_list.append(new_left_node)

        # As we have created the new node we link it as a child of its parent node(upper_node)
        upper_node.left = new_left_node # we link the whole node as a child
        upper_node.left_key = new_left_key #  we link the key of the child

        # We call the function recursively on the newly created node
        create_child(new_left_SR,new_left_node)


    elif CL <= SR and SR < CR:
        #Only RIGHT child exist

        # Given the values and formulas we calculate the SR and key of the new node
        new_right_SR = (SR*AR) % M
        new_right_key = (AR * (upper_node.key + 2)) % M

        id = len(nodes_list) # we get the id for the new node
        # We create new right node
        # Remember that the node has the following properties: Node(id, key, SR, depth, parent)
        new_right_node = Node(id, new_right_key, new_right_SR, upper_node.depth + 1, upper_node)

        # we sum up the total cost of the node
        total_cost_nodes += new_right_key * (new_right_node.depth + 1)

        # we append the new node to the node_list (where we store all our nodes)
        nodes_list.append(new_right_node)

        # As we have created the new node we link it as a child of its parent node(upper_node)
        upper_node.right_key = new_right_key
        upper_node.right = new_right_node

        # We call the function recursively on the newly created node
        create_child(new_right_SR, new_right_node)


    elif CR <= SR and SR < M:
        #Both RIGHT and LEFT children exist

        # Given the values and formulas we calculate the SR and key of the new nodes
        # values for left node
        new_left_SR = (SR*AL) % M
        new_left_key = (AL * (upper_node.key + 1)) % M
        # values for right node
        new_right_SR = (SR*AR) % M
        new_right_key = (AR * (upper_node.key + 2)) % M

        # ---------Creating LEFT child---------
        id = len(nodes_list) #we get the id for the new node
        # We create new left node
        # Remember that the node has the following properties: Node(id, key, SR, depth, parent)
        new_left_node = Node(id, new_left_key, new_left_SR, upper_node.depth + 1, upper_node)

        # we sum up the total cost of the node
        total_cost_nodes += new_left_key * (new_left_node.depth + 1)

        # we append the new node to the node_list (where we store all our nodes)
        nodes_list.append(new_left_node)

        # As we have created the new node we link it as a child of its parent node(upper_node)
        upper_node.left = new_left_node
        upper_node.left_key = new_left_key

        # We call the function recursively on the newly created node
        create_child(new_left_SR, new_left_node)

        # ---------Creating RIGHT child--------
        id = len(nodes_list) #we get the id for the new node
        # We create new right node
        # Remember that the node has the following properties: Node(id, key, SR, depth, parent)
        new_right_node = Node(id,new_right_key, new_right_SR, upper_node.depth + 1, upper_node)

        # we sum up the total cost of the node
        total_cost_nodes += new_right_key * (new_right_node.depth + 1)

        # we append the new node to the node_list (where we store all our nodes)
        nodes_list.append(new_right_node)

        # As we have created the new node we link it as a child of its parent node(upper_node)
        upper_node.right_key = new_right_key
        upper_node.right = new_right_node

        # We call the function recursively on the newly created node
        create_child(new_right_SR, new_right_node)


def printPostorder(node):
    global total_disbalances
    global parity_siblings_counter
    global total_2balanced
    global total_local_min
    global weakly_dominant_counter
    global total_l1_tress
    global increasing_paths

    if node:

        if node.parent:
            if node.key < node.parent.key:
                # increasing_paths.append(node.parent.increasing)
                node.increasing = node.key
            elif node.key >= node.parent.key:
                node.increasing = node.parent.increasing + node.key
                increasing_paths.append(node.increasing)

        # First recur on left child
        printPostorder(node.left)
        # the recur on right child
        printPostorder(node.right)

        # now print the data of node
        # print("Processing the node --->", node.key, "- /", node.SR, "/")
        # print("Node depth", node.depth)

        if not node.right and not node.left: # NODE IS A LEAF
            # LEAF
            node.is_leaf = True
        # Local MIN
            node.is_loc_min = True
            node.loc_min = node.key
            total_local_min += node.key
            # print("Loc min now is ", node.loc_min)

        # 2-balanced
            node.is_2balanced = True
            node.two_nodes_counter = 0
            total_2balanced += node.key
            print("adding two balanced node", node.key)

            # DISBALANCE
            node.subtree_sum += node.key
            # print("node subtree sum is", node.subtree_sum)
            node.disbalance = 0
            # print("Node disbalance is", node.disbalance)

            # if node.parent.key <= node.key:
            #     node.parent.increasing = node.key + node.parent.key
            #     increasing_paths.append(node.parent.increasing)
            #     # print("parent node", node.parent.key, "parent node incresing path", node.parent.increasing)
            # else:
            #     node.parent.increasing = node.parent.key

        elif node.left and not node.right:  # ONLY LEFT CHILD

        # l 1
            node.loc = 1
            if node.left.roc == 0:
                node.roc = 0
                total_l1_tress += 1
                # print("ADDING 1")
            elif node.left.roc != 0:
                node.roc = node.left.roc
            # print("l 1 counter ", node.roc)

        # weakly dominant
            if node.left.is_leaf:
                node.leafs.append(node.left.key)
                # print("Nodes leafs", node.leafs)
            else:
                node.leafs = node.left.leafs
                # print("Nodes leafs", node.leafs)

            # print("+++++++++++++++++++++++++++++++++++++type", type(node.key))
            if node.key >= max(node.leafs):
                # print("node leafs", node.leafs)
                weakly_dominant_counter += 1

        # local min
            if node.key <= node.left.loc_min:
                node.loc_min = node.key
                total_local_min += node.key
                # print("Loc min now is ", node.loc_min)
            else:
                node.loc_min = node.left.loc_min
                # print("Loc min now is ", node.loc_min)

        # 2-balanced
            node.two_nodes_counter = node.left.two_nodes_counter
            if node.two_nodes_counter == 0:
                total_2balanced += node.key
                print("adding two balanced node", node.key)


        # DISBALANCE
            node.subtree_sum += node.left.subtree_sum + node.key
            # print("node subtree sum is", node.subtree_sum)
            node.disbalance = node.left.subtree_sum
            # print("Node disbalance is", node.disbalance)
            total_disbalances += node.disbalance
            # ----------------------------------

            # if node.parent:
            #     if node.parent.key <= node.key:
            #         node.parent.increasing = node.increasing + node.parent.key
            #         increasing_paths.append(node.parent.increasing)
            #         # print("parent node", node.parent.key, "parent node increasing path", node.parent.increasing)
            #     else:
            #         node.parent.increasing = node.parent.key

        elif node.right and not node.left:  # ONLY RIGHT CHILD


            # ----------------------------------
        # l 1
            if node.right.roc == 0:
                node.roc = 1
            elif node.right.roc != 0:
                node.roc = node.right.roc + 1
            # print("l 1 counter ", node.roc)

        # weakly dominant
            if node.right.is_leaf:
                node.leafs.append(node.right.key)
                # print("Nodes leafs", node.leafs)
            else:
                node.leafs = node.right.leafs
                # print("node leafs", node.leafs)

            if node.key >= max(node.leafs):
                # print("node leafs", node.leafs)
                weakly_dominant_counter += 1

        # local min
            if node.key <= node.right.loc_min:
                node.loc_min = node.key
                total_local_min += node.key
                # print("Loc min now is ", node.loc_min)
            else:
                node.loc_min = node.right.loc_min
                # print("Loc min now is ", node.loc_min)

        # 2balanced
            node.two_nodes_counter = node.right.two_nodes_counter
            if node.two_nodes_counter == 0:
                total_2balanced += node.key
                print("adding two balanced node", node.key)


        # DISBALANCE
            node.subtree_sum += node.right.subtree_sum + node.key
            # print("node subtree sum is", node.subtree_sum)
            node.disbalance = node.right.subtree_sum
            # print("Node disbalance is", node.disbalance)
            total_disbalances += node.disbalance

            # INCREASING
            # if node.parent:
            #     if node.parent.key <= node.key:
            #         node.parent.increasing = node.increasing + node.parent.key
            #         increasing_paths.append(node.parent.increasing)
            #         # print("parent node", node.parent.key, "parent node increasing path", node.parent.increasing)
            #     else:
            #         node.parent.increasing = node.parent.key


        elif node.right and node.left: # BOTH CHILDREN

        # l 1

            if node.left.roc == 0 and node.right.roc == 0:
                if node.left.loc > 0 or node.right.loc > 0:
                    node.roc = 0
                    node.loc = node.left.loc + node.right.loc # new
                    total_l1_tress += 1
                    # print("ADDING 1")
            else:
                node.roc = node.left.roc+node.right.roc
            # print("l 1 counter ", node.roc)

        # weakly dominant
            if node.right.is_leaf and node.left.is_leaf:
                node.leafs.append(node.left.key)
                node.leafs.append(node.right.key)
                # print("Nodes leafs", node.leafs)
            elif node.right.is_leaf and not node.left.is_leaf:
                node.leafs = node.left.leafs
                node.leafs.append(node.right.key)
                # print("Nodes leafs", node.leafs)
            elif node.left.is_leaf and not node.right.is_leaf:
                node.leafs = node.right.leafs
                node.leafs.append(node.left.key)
                # print("Nodes leafs", node.leafs)
            else:
                node.leafs = node.right.leafs + node.left.leafs
                # print("Nodes leafs", node.leafs)


            if node.key >= max(node.leafs):
                # print("node leafs", node.leafs)
                weakly_dominant_counter += 1

        # local min
            if node.key <= min(node.left.loc_min, node.right.loc_min):
                node.loc_min = node.key
                total_local_min += node.key
                # print("Loc min now is ", node.loc_min)
            else:
                node.loc_min = min(node.left.loc_min, node.right.loc_min)
                # print("Loc min now is ", node.loc_min)

        # 2-balanced
            node.is_2node = True

            if node.left.two_nodes_counter == node.right.two_nodes_counter:
                node.two_nodes_counter = node.left.two_nodes_counter + node.right.two_nodes_counter + 1
                node.is_2balanced = True
                print("adding two balanced node", node.key)
                total_2balanced += node.key
            else:
                node.two_nodes_counter = max(node.left.two_nodes_counter,node.right.two_nodes_counter)

        # DISBALANCE
            node.subtree_sum += node.left.subtree_sum + node.right.subtree_sum + node.key
            # print("node subtree sum  is", node.subtree_sum)
            node.disbalance = abs((node.left.subtree_sum) - (node.right.subtree_sum))
            # print("Node disbalance is", node.disbalance)
            total_disbalances += node.disbalance

        # Parity siblings
            if node.right.key % 2 == node.left.key % 2:
                node.right.par_sibling = True
                node.left.par_sibling = True
                parity_siblings_counter += 1
            # ----------------------------------

            # INCREASING
            # if node.parent:
            #     if node.parent.key <= node.key:
            #         node.parent.increasing = node.increasing + node.parent.key
            #         increasing_paths.append(node.parent.increasing)
            #         # print("parent node", node.parent.key, "parent node increasing path", node.parent.increasing)
            #     else:
            #         node.parent.increasing = node.parent.key

        # print("---")



# ----------------------MAIN------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

get_inputs_from_file("./pubdata2_bintree/pub01.in")
generate_tree(RK,RSR)

printPostorder(nodes_list[0])

# print("+++++++++++++++++++")
print(total_cost_nodes)
print(total_disbalances)
print(total_2balanced)
print(parity_siblings_counter)
print(total_local_min)
print(weakly_dominant_counter)
print(total_l1_tress )
# print("8. max value of increasing path", increasing_paths)
print(max(increasing_paths))
