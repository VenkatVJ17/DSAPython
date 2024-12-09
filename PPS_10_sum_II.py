class Solution:
    def sum_2(self,nums,target):
        nbr_dct=dict()
        for i in range(len(nums)):
            complement = target-nums[i]
            if (complement) in nbr_dct:
                return [nbr_dct.get(complement),i+1]
            else:
                nbr_dct[nums[i]] = i+1
        return []
    
    def main(self):
        result = self.sum_2([2,7,11,15],9)
        print(result)

if __name__=="__main__":
    sol = Solution()
    sol.main()    