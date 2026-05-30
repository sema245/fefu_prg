class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None

        old_to_new = {}

        def dfs(cur: 'Node') -> 'Node':
            if cur in old_to_new:
                return old_to_new[cur]

            copy = Node(cur.val)
            old_to_new[cur] = copy
            for nei in cur.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy

        return dfs(node)