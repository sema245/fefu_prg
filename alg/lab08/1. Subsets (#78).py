class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []

        def backtrack(start: int, path: list[int]) -> None:
            res.append(path[:])  # каждый узел рекурсии — отдельное подмножество
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()  # откат

        backtrack(0, [])
        return res
