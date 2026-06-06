class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        if sum(gas) < sum(cost):
            return -1  # суммарно бензина не хватает — объехать нельзя

        total = 0  # бак на текущем участке
        start = 0
        for i in range(len(gas)):
            total += gas[i] - cost[i]
            if total < 0:
                # с этого старта не доедем — пробуем следующую станцию
                start = i + 1
                total = 0

        return start
