"""

Homework 2

"""

def moving_average(prices, n):
    """
    Calculates n-period moving average of a list of floats/integers.

    Parameters:
        prices: list of values (ordered in time),
        n: integer moving-average parameter

    Returns:
        list with None for the first n-1 values in prices and the appropriate moving average for the rest

    Example use:
    >>> ma = moving_average([2,3,4,5,8,5,4,3,2,1], 3)
    >>> [round(m, 2) if m is not None else None for m in ma]
    [None, None, 3.0, 4.0, 5.67, 6.0, 5.67, 4.0, 3.0, 2.0]
    >>> moving_average([2,3,4,5,8,5,4,3,2,1], 2)
    [None, 2.5, 3.5, 4.5, 6.5, 6.5, 4.5, 3.5, 2.5, 1.5]
    """
    # Your code here. Don't change anything above.

    i = 0
    ma = [None] * (n-1)

    while i < len(prices) - n + 1:
        window = prices[i: i + n]
        window_average = sum(window) / n
        ma.append(round(window_average, 2))
        i += 1
    return ma


def cross_overs(prices1, prices2):
    """ 
    Identify cross-over indices for two equal-length lists of prices (here: moving averages)

    Parameters:
        prices1, prices2: lists of prices (ordered by time)

    Returns:
        list of crossover points

    Each item in the returned list is a list [time_index, higher_index], where:
        - time_index is the crossover time index (when it happends
        - higher_index indicates which price becomes higher at timeIndex: either 1 for first list or 2 for second list
    
    There are no crossovers before both price lists have values that are not None.
    You can start making comparisons from the point at which both have number values.
    
    Example use:
    >>> p1 = [1, 2, 4, 5]
    >>> p2 = [0, 2.5, 5, 3]
    >>> cross_overs(p1, p2)
    [[1, 2], [3, 1]]
    >>> p1 = [None, 2.5, 3.5, 4.5, 4.5, 3.5, 2.5, 1.5, 3.5, 3.5]
    >>> p2 = [None, None, 3.0, 4.0, 4.333333333333333, 4.0, 3.0, 2.0, 3.0, 2.6666666666666665]
    >>> cross_overs(p1, p2)
    [[5, 2], [8, 1]]
    >>> l3 = [1,22,5,14,8,20,4]
    >>> l4 = [38,21,4,15,10,17,6]
    >>> cross_overs(l3, l4)
    [[1, 1], [3, 2], [5, 1], [6, 2]]
    """
    # Your code here. Don't change anything above.
    crossovers = []
    time_index = -1
    higher_index = 0

    for i1, i2 in zip(prices1,prices2):
        if i1 == None or i2 == None:
            time_index += 1
            continue
        elif i1 > i2:
            if higher_index == 2:
                crossovers.append([time_index+1, higher_index-1])
            higher_index = 1
            time_index += 1
            continue
        elif i2 > i1:
            if higher_index == 1:
                crossovers.append([time_index+1, higher_index+1])
            higher_index = 2
            time_index += 1
            continue

    return crossovers

    

def make_trades(starting_cash, prices, crossovers):
    """
    Given an initial cash position, use a list of crossovers to make trades

    Parameters:
        starting_cash: initial cash position
        prices: list of prices (ordered by time)
        crossovers: list of crossover points on the prices

    Returns:
        list containing current value of trading position (either in stock value or cash) at each time index
    
    Assume each item crossovers[i] is a list [time_index, buy_index]
    Assume that buy_index = 1 means "buy"
    Assume that buy_index = 2 means "sell"

    We buy stock at any time_index where crossover's buy_index indicates 1, and sell at 2.
    In more detail:
        - We want to buy at time_index whenever buy_index = 1 and we currently hold a cash position
            - We buy at the stock price at time_index. We buy with the entire cash position we have and only hold stock
        - We want to sell at time_index when buy_index = 2 and we hold a stock position
            - We sell at the stock price at time_index. We sell our entire stock position and will only hold cash

    Whenever we trade, we buy with our entire cash position, or sell our entire stock position.
    We will therefore always hold either stock or cash, but never both.
    
    Assume we can hold fractional stock quantities, and there are no transaction fees.

    Example use:
    # In the first example, We start with cash 1.0.
    # We hold cash until we buy at index 1 at the price 4. We then hold 0.25 shares. 
    # After that, our portfolio is in stock, so its value fluctuates with the stock price.
    # As the stock price goes from 4 to 6, our portfolio value goes from 1.0 to 1.5.
    # This goes on until we sell at index 3 at the price 5. 
    # Then we hold cash again and the value of the portfolio does not change as it is in cash.
    >>> starting_cash = 1.0
    >>> prices = [2,4,6,5,1]
    >>> cos = [[1, 1], [3, 2]] # not real crossovers, just to illustrate portfolio value when trading
    >>> values = make_trades(starting_cash, prices, cos)
    >>> values 
    [1.0, 1.0, 1.5, 1.25, 1.25]
    >>> starting_cash = 1000.0
    >>> prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
    >>> cos = [[5, 2], [8, 1], [10, 2], [11, 1], [15, 2]]
    >>> values = make_trades(starting_cash, prices, cos)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 166.67, 833.33, 833.33, 952.38, 1190.48, 833.33, 1071.43]
    >>> prices =[38,21,20,13,7,14,22,23,27,23,44,26,48,32,48,60,70,40,34,35,33]
    >>> crossovers = [[7, 1], [19, 2]]
    >>> money = 100.0
    >>> values = make_trades(money, prices, crossovers)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 117.39, 100.0, 191.3, 113.04, 208.7, 139.13, 208.7, 260.87, 304.35, 173.91, 147.83, 152.17, 152.17]
    >>> l2 = [39,22,5,14,8,15,23,27,23,44,26,48,32,48,13,34,15,34,35]
    >>> c2 = [[4, 1], [5, 2], [6, 1], [11, 2], [12, 1], [13, 2], [16, 1], [17, 2], [18, 1]]
    >>> values = make_trades(10.0, l2, c2)
    >>> [round(v, 3) for v in values] # round every value of the returned list using list comprehension
    [10.0, 10.0, 10.0, 10.0, 10.0, 18.75, 18.75, 22.011, 18.75, 35.87, 21.196, 39.13, 39.13, 58.696, 58.696, 58.696, 58.696, 133.043, 133.043]
    """
    # Your code here. Don't change anything above.
    # Note: the rounding in the examples happens *after* the function call. Your function should not round the results.
    current_value = []  # value of portfolio
    current_stock = 0
    current_cash = starting_cash
    for i in range(len(prices)):
        current_price = prices[i]
        for c in crossovers:
            # Check if we are holding stock already
            if current_stock != 0:
                # Check if action is required at this time step
                if c[0] == i:
                    # Check if we are asked to sell, since we can only sell
                    if c[1] == 2:
                        current_cash = current_stock * current_price
                        current_stock = 0
                        crossovers.remove(c)
            else:
                # Check if action is required at this time setp
                if c[0] == i:
                    # Check if we are asked to buy, since we can only buy
                    if c[1] == 1:
                        current_stock = current_cash/current_price
                        current_cash = 0
                        crossovers.remove(c)
        if current_cash != 0:
            current_value.append(current_cash)
        else:
            current_value.append(current_stock * current_price)
    return current_value





    # for i in range(len(prices)):
    #     if i != crossovers[start_index][0]:
    #         x = (prices[start_index-1]/prices[start_index]) * current_value[start_index-1]
    #         current_value.append(x)
    #     elif i == crossovers[start_index][0]:
    #         if crossovers[start_index][1] == 1:
    #             y = current_value[start_index] / prices[i]
    #             current_value.append(y)
    #         elif crossovers[start_index][1] == 2:
    #             current_value.append(current_value[start_index-1])
    #         start_index += 1

# starting_cash = 1000.0
# prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
# cos = [[5, 2], [8, 1], [10, 2], [11, 1], [15, 2]] # not real crossovers, just to illustrate portfolio value when trading
# values = make_trades(starting_cash, prices, cos)
# print([round(v, 2) for v in values])


def is_pldrm(s):
    assert type(s) is str, "Type non-string not supported"
    for i in range(len(s)):
        if s[i] != s[::-1][i]:
            return False
    return True

def palindrome(s, k):
    """
    Find highest-value palindrome from s with max k digit changes.
    
    Parameters:
        s - an integer in string format
        k - number of changes
        
    Returns:
        highest-value palindrome number in string format; 
        if creating a palindrome is not possible, returns the string 'Not possible.'
    
    Example use:
    >>> palindrome('1921', 2)
    '1991'
    >>> palindrome('1921', 3)
    '9999'
    >>> palindrome('11122', 1)
    'Not possible.'
    >>> palindrome('11119111', 4)
    '91199119'
    """
    # Your code here.
    # Define helper function that checks if the str is a PLDRM
    
    if k == 0:
        if is_pldrm(s):
            return int(s)
        return -1
    curr_max = -float("inf")
    values = set("9")
    visited = set()
    for i in s:
        values.add(i)

    # Search through potential palindrome layers
    for v in values:
        for j in range(len(s)):
            temp = s[:j] + v + s[j + 1:]
            if temp in visited:
                continue
            else:
                visited.add(temp)
                if is_pldrm(temp):
                    if int(temp) >= curr_max:
                        curr_max = max(int(temp), palindrome(temp, k - 1))
                else:
                    check_next = palindrome(temp, k - 1)
                    if type(check_next) is str:
                        continue
                    elif check_next >= curr_max:
                        curr_max = check_next
    if curr_max == -1:
        return "Not possible."
    return curr_max

print("Testing Palindrome")
print("Test case 1921 and 2, expect 1991.", palindrome('1921', 2))
print("Test case 1921 and 2, expect 9999.", palindrome('1921', 3))
print("Test case 11122 and 2, expect NP.", palindrome('11122', 1))
print("Test case 11119111 and 4, expect 91199119.", palindrome('11119111', 4))
print("Test case 1234666 and 4, expect 9664669.", palindrome("1234666", 4))
print("Test case 0 and 4, expect 9.", palindrome("0", 4))
print("Test case 0 and 0, expect 0.", palindrome("0", 0))


def reverse_engineer(seq):
    """
    Reverse engineer an input sequence
    
    Parameters:
        seq - list of strings
    
    Returns:
        list of values corresponding to each letter present in the sequences (smallest possible values)
        (in alphabetical order)
    
    Example use
    >>> reverse_engineer(["a", "ab", "c", "a", "ab", "ac"])
    [2, 4, 5]
    >>> reverse_engineer(["b", "bc", "ab", "bc", "b", "abc", "b"])
    [3, 1, 2]
    >>> reverse_engineer(["a", "b", "d", "c", "a", "ab"])
    [6, 9, 11, 10]
    """
    # Your code here.
    pass