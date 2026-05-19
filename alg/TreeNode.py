import math
class Solution:
    def isPalindrome(self, x: int) -> bool:
        isPal = True
        rev = 0
        n = math.ceil(lent/2)
        for i in range(0,n):
            if pal[i] != pal[lent-i-1]:
                isPal = False
        return isPal

print(Solution().isPalindrome(-121))