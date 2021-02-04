import pandas as pd

'''
    B Tree 구현

    개발 환경 :
        Window System
        Anaconda
    
    개발 Tool :
        VS code 2019
    
    개발 버전 :
        Python : 3.8.5
        pandas : 1.2.1

    프로그램 특징 :
        1.  원래대로라면 leaf에서 삽입을 하고 Maximum을 초과했을 때 split을 통해
            가운데 key 값이 올라가 recursive하게 split하지만 Back-up의 overhead를 줄이기 위해
            삽입을 하러 tree를 탐색하 때 거쳐가는 노드의 key 개수가 maximum이라면 즉시 split
'''

MAXIMUM = 11 # 한 node에서 가질 수 있는 최대 key 개수 split의 편의를 위해 홀수만 가능

class Node:
    """
        B-Tree의 Node Class
    """    
    def __init__(self, leaf):
        self.datas = [] # [key, value] 쌍으로 append
        self.child = [] # B-Tree 구조에서 다음 노드의 정보를 담는 child
        self.leaf = leaf # 해당 노드가 leaf 인지 아닌지 판별

class B_Tree:
    """
        B-Tree에서의 삭제, 삽입, 검색이 구현된 B-Tree Class
    """    
    def __init__(self):
        self.tree = Node(True)

    def search(self, key, node=None):
        if node is None:
            return self.search(key, self.tree)
        
        idx = 0
        while idx < len(node.datas) and node.datas[idx][0] < key:
            idx += 1               # 정렬된 data 안에서 key보다 큰 첫 data key index - 1 반환
        
        if idx < len(node.datas) and node.datas[idx][0] == key:
            return node.datas[idx]         # key를 찾았을 경우 [key, value] 배열 반환
        elif node.leaf:
            return None                   # leaf여서 더 이상의 child가 없으며 key도 찾지 못한 경우
        else :
            return self.search(key, node.child[idx]) # nonleaf이므로 다음 child에서 search 실행

    def split_child(self, parent, idx):
        minimum = MAXIMUM // 2 # 한 node에서 최소 key 개수 

        left_child = parent.child[idx]
        right_child = Node(left_child.leaf)

        middle_key = left_child.datas[minimum]

        right_child.datas = left_child.datas[minimum+1:]
        left_child.datas = left_child.datas[:minimum]

        if not left_child.leaf:
            right_child.child = left_child.child[minimum+1:]
            left_child.child = left_child.child[:minimum+1]
        
        parent.datas.insert(idx, middle_key)
        parent.child.insert(idx+1, right_child)

    def insert(self, data):
        root = self.tree

        if len(root.datas) == MAXIMUM:
            # B Tree root에 MAXIMUM의 key 값이 있는 경우
            new_root = Node(False)
            self.tree = new_root
            new_root.child.append(root)
            self.split_child(new_root, 0)
            self.insert_available_node(new_root, data)
        else :
            self.insert_available_node(root, data)

    def insert_available_node(self, node, data):
        # 주어진 data의 key값에 해당하는 위치에 insert 수행
        idx = len(node.datas) - 1 # 뒤에서부터 탐색
        if not node.leaf:
            # nonleaf라면 node key를 비교하다가 처음으로 작은 node key의 index 값에 + 1 이용해 subtree 접근 
            while idx >= 0 and node.datas[idx][0] > data[0]:
                idx -= 1
            idx += 1

            if len(node.child[idx].datas) == MAXIMUM:
                # 찾은 index에 해당하는 subtree의 key 개수가 maximum이면 split을 미리 한다
                self.split_child(node, idx)
                if node.datas[idx][0] < data[0]:
                    # subtree의 split으로 인해 올라온 key값과 넣으줄 data의 key값 비교 통해 index 조정
                    idx += 1
            self.insert_available_node(node.child[idx], data)     
        else :
            # leaf라면 data insert
            node.datas.append([None, None])
            while idx >= 0 and node.datas[idx][0] > data[0]:
                # data를 삽입할 idx 찾기 & key 순 정렬 유지
                node.datas[idx + 1] = node.datas[idx]
                idx -= 1

            node.datas[idx + 1] = data

    # Print the tree
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.datas), end=":")
        for data in x.datas:
            print(data[0], end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)

def main():
    global MAXIMUM
    
    input_df = pd.read_csv("../data/input.csv", sep='\s+', header=None)
    
    btree = B_Tree()

    for key, value in input_df.iterrows():
        btree.insert([value[0], value[1]])
        print(f"{value[0]} key's insertion complete")

    # for idx in range(100):
    #     btree.insert([idx, idx])
    #     print(f"{idx} complete")

    btree.print_tree(btree.tree)

if __name__ == "__main__":
    main()