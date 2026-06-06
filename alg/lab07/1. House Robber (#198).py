class Solution:
    def rob(self, nums: list[int]) -> int:
        prev, cur = 0, 0  # prev = dp[i-2], cur = dp[i-1]
        for num in nums:
            # либо пропускаем дом, либо грабим его и берём сумму до i-2
            prev, cur = cur, max(cur, prev + num)
        return cur
