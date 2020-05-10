# Nofar Bar-Zakai, 205643638, Noa Dagan, 311302137
import hashlib

class Node():
    def __init__(self, hash_value):
        self.hash_value = hash_value
        self.right_node = None
        self.left_node = None
        self.right_list = []
        self.left_list = []

class Merkle_Tree:
    def __init__(self, list_of_transactions):
        self.list_of_transactions = self.list_of_node(list_of_transactions)
        self.tree = Node("")

    # The function convert the list to list of nodes
    def list_of_node(self,list_of_transactions):
        nodes_list = []
        # run over all the list, create new node and append to the list of nodes
        for i in range(len(list_of_transactions)):
            new_node = Node(list_of_transactions[i])
            nodes_list.append(new_node)
        # return list of nodes
        return nodes_list

    # The function create the Merkle tree
    def create_merkle_tree(self):
        # initalize the list of list_of_transactions
        list_of_transactions = self.list_of_transactions
        merkle_tree = self.tree
        prev_transaction = []
        len_of_list = len(list_of_transactions)
        # run over the nodes
        for i in range(0,len_of_list,2):
            if len_of_list == 1:
                left_node = list_of_transactions[i]
                self.tree = left_node
            else:
                # find left node and right node
                left_node = list_of_transactions[i]
                right_node = list_of_transactions[i + 1]
                # calculate hash of the nodes
                prev_node = str(left_node.hash_value) + str(right_node.hash_value)
                prev_hash = hashlib.sha256(prev_node.encode('utf-8'))
                prev_hash = prev_hash.hexdigest()
                #create new node and update left and right nodes and lists
                new_node = Node(prev_hash)
                new_node.right_node = right_node
                new_node.left_node = left_node
                new_node.right_list = new_node.right_list + right_node.right_list + right_node.left_list
                new_node.right_list.append(right_node.hash_value)
                new_node.left_list = new_node.left_list + left_node.right_list + left_node.left_list
                new_node.left_list.append(left_node.hash_value)
                # append the new node to the list
                prev_transaction.append(new_node)
        # if its not the root continue in recursive and initialize the members
        if len_of_list != 1:
            self.list_of_transactions = prev_transaction
            self.merkle_tree = merkle_tree
            self.create_merkle_tree()

    # The function create the proof of inclusion to a given leaf
    def create_proof_of_inclusion(self, leaf_node):
        result_list = ""
        root_node = self.tree
        is_root = False
        # while didnt reach the leaf
        while root_node.hash_value != leaf_node:
            # if the node in left side add the right node to the result
            if root_node.left_list.__contains__(leaf_node):
                if is_root == False:
                    result_list = "r " + root_node.right_node.hash_value
                    is_root = True
                else:
                    result_list = "r " + root_node.right_node.hash_value + " " + result_list
                root_node = root_node.left_node
            else:
                # if the node in Right side add the right node to the result
                if is_root == False:
                    result_list = "l " + root_node.left_node.hash_value
                    is_root = True
                else:
                    result_list = "l " + root_node.left_node.hash_value + " " + result_list
                root_node = root_node.right_node
        return result_list

    #The funrion find the nonce that with a root will give the difficulty
    def find_nonce(self, level_number):
        index = 0
        root = self.tree.hash_value
        # run over the root until find the nonce number
        while True:
            # calculate the hash value
            root_value = str(index) + root
            root_value = hashlib.sha256(root_value.encode('utf-8'))
            root_value = root_value.hexdigest()
            # find the level_number first digit of the number
            number = str(str(root_value)[:level_number])
            # check all the digit are zero
            if all(v == '0' for v in number):
                return index, root_value
            index += 1

# The function check proof of inclusion
def check_proof(path):
    leaf = path[1]
    root = path[2]
    # run over all the proof
    for i in range(3,len(path),2):
        # if its left add from the left side
        if path[i] == "l":
            leaf = hashlib.sha256(path[i + 1].encode('utf-8') + leaf.encode('utf-8'))
            leaf = leaf.hexdigest()
        # if its right add from the right side
        elif path[i] == "r":
            leaf = hashlib.sha256(leaf.encode('utf-8') + path[i + 1].encode('utf-8'))
            leaf = leaf.hexdigest()
        # if invalid value
        else:
            return False
    # compare the result to the root
    if leaf == root:
        return True
    else:
        return False

# The main function
if __name__ == '__main__':
    leafs = []
    merkle_root = ""
    if_tree_created = False
    while True:
        # get input from the user
        input_string = input()
        input_string = input_string.split(" ")
        task_number = input_string[0]
        # case task 1
        if task_number == '1':
            # flag tree created
            if_tree_created = True
            len_of_leafs = len(input_string)
            # run over all the string and add to list of leafs
            for i in range(1,len_of_leafs):
                 leafs.append(input_string[i])
            # create merkle tree and print the root hash value
            new_merkle_tree = Merkle_Tree(leafs)
            new_merkle_tree.create_merkle_tree()
            merkle_root = new_merkle_tree.tree.hash_value
            print(merkle_root)
        # case task 2
        elif task_number == '2':
            # check that tree was created else terminate the program
            if if_tree_created == True:
                leaf_index = input_string[1]
                # ckeck the index not out of range
                if int(leaf_index) < len(leafs):
                    find_leaf = leafs[int(leaf_index)]
                    # create proof of inclusion and print the result
                    proof_of_inclusion = new_merkle_tree.create_proof_of_inclusion(find_leaf)
                    print(proof_of_inclusion)
            else:
                break
        # case task 3
        elif task_number == '3':
            # check the index not out of range
            if len(input_string) > 3:
                # check proof of inclusion and print the result
                result = check_proof(input_string)
                if result:
                    print("True")
                else:
                    print("False")
            else:
                print("False")
        # case task 4
        elif task_number == '4':
            # check that tree was created else terminate the program
            if if_tree_created:
                # level number check is digit
                level_number = input_string[1]
                if level_number.isdigit():
                    # find nonce and print the index and root value
                    index, root_value = new_merkle_tree.find_nonce(int(level_number))
                    result = str(index) + " " + str(root_value)
                    print(result)
            else:
                break
        # case task 5 terminate the program
        elif task_number == '5':
            break
        # invalid task terminate the program
        else:
            break