class ArrayProductSelf:

    def product_except_self(self,nums):
        n = len(nums)
        answer = [1] * n  # Initialize the result array with 1s
        
        # Left pass
        left_product = 1
        for i in range(n):
            answer[i] = left_product
            left_product *= nums[i]
        
        # Right pass
        right_product = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= right_product
            right_product *= nums[i]
        
        return answer


    
    def main(self):
        result = self.product_except_self([1,2,3,4])
        print(result)
    
if __name__=="__main__":
    apd = ArrayProductSelf()
    apd.main()