class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            graph[b].append(a)

        state = [0] * numCourses  # 0=не видел, 1=в пути, 2=готово

        def dfs(v: int) -> bool:
            if state[v] == 1:
                return False  # цикл
            if state[v] == 2:
                return True  # уже проверен

            state[v] = 1
            for nei in graph[v]:
                if not dfs(nei):
                    return False
            state[v] = 2
            return True

        for course in range(numCourses):
            if state[course] == 0:
                if not dfs(course):
                    return False

        return True