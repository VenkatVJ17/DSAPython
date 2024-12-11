class BestTimeBuySellStock:
    def maxProfit(self,prices):
        if not prices or len(prices) < 2:
            return 0
        
        # Initialize variables for minimum price and maximum profit
        min_price = float('inf')
        max_profit = 0
        
        # Iterate over the prices
        for price in prices:
            # Update the minimum price seen so far
            min_price = min(min_price, price)
            # Calculate the potential profit and update the maximum profit
            max_profit = max(max_profit, price - min_price)
        
        return max_profit
    
    def main(self):
        result = self.maxProfit([7, 1, 5, 3, 6, 4])
        print(result)

if __name__=="__main__":
    btbss = BestTimeBuySellStock()
    btbss.main()        