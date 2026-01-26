def is_prime(n):
  
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_palindrome(n):
  
    str_n = str(n)
    return str_n == str_n[::-1]


def find_prime_palindromes(start, end):
    
    prime_palindromes = []
    
    for num in range(start, end + 1):
        if is_prime(num) and is_palindrome(num):
            prime_palindromes.append(num)
    
    return prime_palindromes


def main():
    
    start = 1
    end = 20000
    
    print(f"Finding prime palindrome numbers between {start} and {end}...\n")
    
    prime_palindromes = find_prime_palindromes(start, end)
    
    print(f"Prime Palindrome Numbers: {prime_palindromes}")
    print(f"\nTotal count: {len(prime_palindromes)}")
    print("\nDetails:")
    for num in prime_palindromes:
        print(f"  {num}" end='')


if __name__ == "__main__":
    main()
