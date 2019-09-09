def decrease(target_num, compare_num):
    return int(target_num) == (int(compare_num) - 1)
    
def increase(target_num, compare_num):
    return int(target_num) == (int(compare_num) + 1)
    
def float_greater_than(target_num, compare_num):
    return float(target_num) > float(compare_num)
 
COMPARATORS = {'dec': decrease, 'inc': increase, 'flo-gt': float_greater_than}
