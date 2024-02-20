def replace_chars(string, k):
    n = len(string)
    seen = []
    result = []
    
    for i, char in enumerate(string):
        if char not in seen:
            result.append(char)
        else:
            result.append("-")
        
        # If i > k, remove char start from string[0]
        if i >= k:
            seen.remove(string[i - k])
        
        #if not already in seen, add
        if char not in seen:
            seen.append(char)
            
    return ''.join(result)
            
            
# sample test
print(replace_chars("abcdefaxc", 10))  # Output: abcdef-x-
print(replace_chars("abcdefaxcqwertba", 10))  # Output: abcdef-x-qw-rtb-
