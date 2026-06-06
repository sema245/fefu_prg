class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []

        def backtrack(start: int, remain: int, path: list[int]) -> None:
            if remain == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:
                    continue
                path.append(candidates[i])
                # i, а не i+1 — один и тот же элемент можно брать несколько раз
                backtrack(i, remain - candidates[i], path)
                path.pop()  # откат

        backtrack(0, target, [])
        return res
