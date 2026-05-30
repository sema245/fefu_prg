from collections import deque


class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])

        def bfs(starts: list[tuple[int, int]]) -> list[list[bool]]:
            visited = [[False] * n for _ in range(m)]
            q = deque(starts)
            for r, c in starts:
                visited[r][c] = True

            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            while q:
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                        # идём только если вверх или ровно (обратное направление потока)
                        if heights[nr][nc] >= heights[r][c]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
            return visited

        pacific_starts = [(0, j) for j in range(n)] + [(i, 0) for i in range(m)]
        atlantic_starts = [(m - 1, j) for j in range(n)] + [(i, n - 1) for i in range(m)]

        pac = bfs(pacific_starts)
        atl = bfs(atlantic_starts)

        res = []
        for i in range(m):
            for j in range(n):
                if pac[i][j] and atl[i][j]:
                    res.append([i, j])

        return res