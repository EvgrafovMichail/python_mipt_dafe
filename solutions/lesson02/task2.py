


def get_doubled_factorial(num: int) -> int:
        
    factorial = 1
    
    for n in range(1, num + 1):
        if n % 2 != num % 2: continue
        factorial *= n
        
    
    return factorial
