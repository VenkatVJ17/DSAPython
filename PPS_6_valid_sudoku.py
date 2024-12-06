import numpy as np

def extract_digits(input_arr):
    return [item for item in input_arr if isinstance(item,str) and item.isdigit()]

def has_duplicates(input_arr):
    input_arr = extract_digits(input_arr)
    return len(input_arr)!=len(set(input_arr))

def valid_sudoku(digs):
    #validate row
    for i in range(0,9):
        row_arr = digs[i]
        if(has_duplicates(row_arr)):
            return False
        
        col_arr = [row[i] for row in digs]
        if(has_duplicates(col_arr)):
            return False
    #validate column
    

    #validate 3x3 matrix
    for i in range(0,9,3):
        for j in range(0,9,3):
            r,c=i,j
            elements = [digs[k][l] for k in range(r,r+3) for l in range(c,c+3)]
            if(has_duplicates(elements)):
                return False
    return True

    
    
    pass
def main():
    result = valid_sudoku([["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]])
    print(result)

if __name__=="__main__":
    main()