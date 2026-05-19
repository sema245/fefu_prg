class Solution:
    def romanToInt(self, s: str) -> int:
        roman_int = {
            'I':1,
            'V':5,
            'X':10,
            'L':50,
            'C':100,
            'D':500,
            'M':1000
        }
        sum = 0
        for i in range(1,len(s),2):
            if roman_int[s[i]] < roman_int[s[i-1]]:
                sum += roman_int[s[i]] - roman_int[s[i-1]]
            else:
                sum += roman_int[s[i-1]] + roman_int[s[i]]
        return sum
print(Solution().romanToInt("XIV"))