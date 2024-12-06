from collections import Counter

def top_k_elements(nums,k):
    freq_cnt = Counter(nums)
    top_k = [key for key, value in sorted(freq_cnt.items(),key=lambda item: item[1], reverse=True)[:k]]
    return top_k

def main():
    result = top_k_elements([1,1,1,2,2,3],2)
    print(result)

if __name__=="__main__":
    main()