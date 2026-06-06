from bisect import bisect_left


class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails = []  # tails[i] — наименьший возможный хвост возр. подпоследовательности длины i+1
        for num in nums:
            pos = bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)  # удлиняем последовательность
            else:
                tails[pos] = num  # улучшаем хвост
        return len(tails)
