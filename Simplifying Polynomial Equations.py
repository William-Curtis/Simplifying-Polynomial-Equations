def break_sec_add(equation):
    """
    Breaks a string into a list of strings where each even index (e.g. 0,2) is
    a section of terms and each odd index (e.g. 1) is either '+' or '-'
    
    Example
     Input: '(2x^2+x-3)^3(x^2+x)+(-x^3+x+1)(x^2-2x+4)(x^2)'
     Output: ['(2x^2+x-3)^3(x^2+x)', '+', '(-x^3+x+1)(x^2-2x+4)(x^2)']
    """
    do_check = True
    sign_idx = []
    result = []
    # Goes through every index of the equation to get the index of every
    # operation sign not in brackets and adds it to the list sign_idx
    for i in range(len(equation)):
        if equation[i] == "(":
            do_check = False
        elif equation[i] == ")":
            do_check = True
        elif do_check and (equation[i] == "+" or equation[i] == "-"):
            sign_idx.append(i)
    sign_idx_len = len(sign_idx)
    # Uses the sign_idx to add the sections before/between/after operators and the
    # opperators themselves to the list result
    for i in range(sign_idx_len*2 + 1):
        if i % 2 != 0:
            result.append(equation[sign_idx[0]])
            equation = equation[sign_idx.pop(0)+1:]
        else:
            if i == sign_idx_len*2:
                result.append(equation) 
            else:
                result.append(equation[:sign_idx[0]])
    return result
        
def break_sec_mult(equation):
    """
    Breaks a string into a list of lists where each term gets rewritten in the 
    form: ['term', exponent]
    
    Example
     Input: '(2x^2+x-3)^3(x^2+x)'
     Output: [['2x^2+x-3', 3], ['x^2+x', 1]]
    """
    result = []
    sec_start = 0
    for i in range(len(equation)):
        # Uses brackets to identify different terms
        if equation[i] == "(":
            sec_start = i + 1
        elif equation[i] == ")":
            result.append([equation[sec_start:i], None])
            # Checks if there is an exponent on the term
            try:
                if equation[i+1] == "^": # If so, adds the value
                    result[-1][1] = int(equation[i+2:equation[i+2:].index("(") + i + 2])
                    #equation = equation[equation[1:].index("("):]
                else:
                    result[-1][1] = 1
            except IndexError: # If no exponent assumes 1
                result[-1][1] = 1
            except ValueError: # If there is only one term and it has an exponent
                result[-1][1] = int(equation[i+2:])
    return result
        
def exp_expansion(equation):
    """
    Takes a list in the form: ['term', exponent] and evaluates it, returning 
    the result in the form:
    [['coefficent', ('x', 'power')], '+/-'. ['coefficent', ('x', 'power')], ...,
     '+/-', 'coefficent x', '+/-', 'coefficent']
    
    Example
     Input: ['2x^2+x-3', 3]
     Output: [['8', ('x', '6')], '+', ['12', ('x', '5')], '-', ['30', ('x', '4')], '-',
              ['35', ('x', '3')],  '+', ['45', ('x', '2')], '+', '27x', '-', '27']
    """
    result = equation[0]
    # Still does operation even if it has an exponent of 1, 
    # this is to get it to have the right format
    if equation[1] == 1:
        result = mult_expansion(equation[0], '1')
    else:
        for n in range(int(equation[1]) - 1):
            result = mult_expansion(result, equation[0])
    return result
        
def add_expansion(equation, equation2, subtract):
    """
    Takes two lists of terms in the form:
    [['coefficent', ('x', 'power')], '+/-'. ['coefficent', ('x', 'power')], ...]
    if the variable subtract is True, it does the subtraction of the two lists,
    if the variable subtract is False, it does the addition of the two lists
    
    Example
     Input: [['2', ('x', '2')], '+', 'x', '-', '3'],
            [['-3', ('x', '3')], '-', ['4', ('x', '2')], '+', '5'],
            False
     Output: [['-3', ('x', '3')], '-', ['2', ('x', '2')], '+',
              ['1', ('x', '1')], '+', ['2', ('x', '0')]]
    """
    result = []
    result_terms = {}
    # Adds equation into the dictonary result_terms
    for i in range(0, len(equation), 2):
        # prevents errors of referencing previous index by having an unique
        # case if it is the first index in the list
        if i == 0:
            # If statement checks if the term is a list (exponent >= 2),
            # has an x in it (exponent = 1), or is a number (exponent = 0)
            if type(equation[i]) == list:
                if equation[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms[equation[i][1][1]] = 0
                result_terms[equation[i][1][1]] += int(equation[i][0])
            elif equation[i].isdigit():
                if '0' not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms['0'] = 0
                result_terms['0'] += int(equation[i])
            else:
                if '1' not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms['1'] = 0
                result_terms['1'] += int(equation[i][:-1])
        else:
            # If statement checks if the term is a list (exponent >= 2),
            # has an x in it (exponent = 1), or is a number (exponent = 0)
            if type(equation[i]) == list:
                if equation[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms[equation[i][1][1]] = 0
                if equation[i-1] == '-': # Deals with the case where the previous index is '-'
                    result_terms[equation[i][1][1]] -= int(equation[i][0])
                else:
                    result_terms[equation[i][1][1]] += int(equation[i][0])
            elif equation[i].isdigit():
                if '0' not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms['0'] = 0
                if equation[i-1] == '-': # Deals with the case where the previous index is '-'
                    result_terms['0'] -= int(equation[i])
                else:
                    result_terms['0'] += int(equation[i])
            else:
                if '1' not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms['1'] = 0
                if equation[i-1] == '-': # Deals with the case where the previous index is '-'
                    result_terms['1'] -= int(equation[i][:-1])
                elif equation[i] == 'x':
                    result_terms['1'] += 1
                else:
                    result_terms['1'] += int(equation[i][:-1])
    
    if subtract:
        # Subtracts equation2 into the dictonary result_terms
        for i in range(0, len(equation2), 2):
            # prevents errors of referencing previous index by having an unique
            # case if it is the first index in the list
            if i == 0:
                # If statement checks if the term is a list (exponent >= 2),
                # has an x in it (exponent = 1), or is a number (exponent = 0)
                if type(equation2[i]) == list:
                    if equation2[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[equation2[i][1][1]] = 0
                    result_terms[equation2[i][1][1]] -= int(equation2[i][0])
                elif equation2[i].isdigit():
                    if '0' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['0'] = 0
                    result_terms['0'] -= int(equation2[i])
                else:
                    if '1' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['1'] = 0
                    result_terms['1'] -= int(equation2[i][:-1])
            else:
                # If statement checks if the term is a list (exponent >= 2),
                # has an x in it (exponent = 1), or is a number (exponent = 0)
                if type(equation2[i]) == list:
                    if equation2[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[equation2[i][1][1]] = 0
                    if equation2[i-1] == '-': # Deals with the case where the previous index is '-'
                        result_terms[equation2[i][1][1]] += int(equation2[i][0])
                    else:
                        result_terms[equation2[i][1][1]] -= int(equation2[i][0])
                elif equation2[i].isdigit():
                    if '0' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['0'] = 0
                    if equation2[i-1] == '-': # Deals with the case where the previous index is '-'
                        result_terms['0'] += int(equation2[i])
                    else:
                        result_terms['0'] -= int(equation2[i])
                else:
                    if '1' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['1'] = 0
                    if equation2[i-1] == '-': # Deals with the case where the previous index is '-'
                        result_terms['1'] += int(equation2[i][:-1])
                    elif equation2[i] == 'x':
                        result_terms['1'] -= 1
                    else:
                        result_terms['1'] -= int(equation2[i][:-1])
    else:
        for i in range(0, len(equation2), 2): # Adds equation2 into the dictonary result_terms
            # prevents errors of referencing previous index by having an unique
            # case if it is the first index in the list
            if i == 0:
                # If statement checks if the term is a list (exponent >= 2),
                # has an x in it (exponent = 1), or is a number (exponent = 0)
                if type(equation2[i]) == list:
                    if equation2[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[equation2[i][1][1]] = 0
                    result_terms[equation2[i][1][1]] += int(equation2[i][0])
                elif equation2[i].isdigit():
                    if '0' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['0'] = 0
                    result_terms['0'] += int(equation2[i])
                else:
                    if '1' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['1'] = 0
                    result_terms['1'] += int(equation2[i][:-1])
            else:
                # If statement checks if the term is a list (exponent >= 2),
                # has an x in it (exponent = 1), or is a number (exponent = 0)
                if type(equation2[i]) == list:
                    if equation2[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[equation2[i][1][1]] = 0
                    if equation2[i-1] == '-': # Deals with the case where the previous index is '-'
                        result_terms[equation2[i][1][1]] -= int(equation2[i][0])
                    else:
                        result_terms[equation2[i][1][1]] += int(equation2[i][0])
                elif equation2[i].isdigit():
                    if '0' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['0'] = 0
                    if equation2[i-1] == '-': # Deals with the case where the previous index is '-'
                        result_terms['0'] -= int(equation2[i])
                    else:
                        result_terms['0'] += int(equation2[i])
                else:
                    if '1' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['1'] = 0
                    if equation2[i-1] == '-': # Deals with the case where the previous index is '-'
                        result_terms['1'] -= int(equation2[i][:-1])
                    elif equation2[i] == 'x':
                        result_terms['1'] += 1
                    else:
                        result_terms['1'] += int(equation2[i][:-1])
    # Converts dictionary result_terms into a list result
    # creates and iterable of all exponents from greatest to least to be used in the for loop
    for key in sorted(iter(list(result_terms)), key=lambda x: int(x), reverse=True):
        # to prevent having an operator in front there is 
        # an unique case if it is the first index in the list 
        if result == []:
            if key == 0 or key == 1:
                result.append(str(result_terms[key]))
            else:
                result.append([str(result_terms[key]), ('x', key)])
        else:
            if key == 0: # specilized case if term is of exponent 0
                if '-' in str(result_terms[key]): # Deals with the case where the value is negative
                    result.append('-')
                    result.append(str(abs(result_terms[key])))
                else:
                    result.append('+')
                    result.append(str(result_terms[key]))
            elif key == 1: # specilized case if term is of exponent 1
                if '-' in str(result_terms[key]): # Deals with the case where the value is negative
                    result.append('-')
                    result.append(str(abs(result_terms[key]))+'x')
                else:
                    result.append('+')
                    result.append(str(result_terms[key])+'x')
            else:
                if '-' in str(result_terms[key]): # Deals with the case where the value is negative
                    result.append('-')
                    result.append([str(abs(result_terms[key])), ('x', key)])
                else:
                    result.append('+')
                    result.append([str(result_terms[key]), ('x', key)])
    
    return result

def mult_expansion(equation, equation2):
    """
    Takes either two strings or lists in the form as shown in the example bellow, 
    and evaluates and return the product
    
    Example
     Input: '2x^2+x-3', '4x^4+4x^3-11x^2-6x+9'
     Alt Input: [['2', ('x', '2')], '+', 'x', '-', '3'],
                 [['4', ('x', '4')], '+', ['4', ('x', '3')], '-', ['11', ('x', '2')],
                  '-', '6x', '+', 9]
     Output: [['8', ('x', '6')], '+', ['12', ('x', '5')], '-', ['30', ('x', '4')], '-'
              ['35', ('x', '3')], '+' ['45', ('x', '2')], '+', '27x', '-', '27']
    """
    result = []
    result_terms = {}
    # Converts equation to correct format if it is in the form of a string
    if type(equation) != list:
        terms = break_sec_terms(equation)
    else:
        terms = equation
    # Converts equation2 to correct format if it is in the form of a string
    if type(equation2) != list:
        terms2 = break_sec_terms(equation2)
    else:
        terms2 = equation2
    # Multiplies each term from variable terms with each term variable from terms2
    # Adds the result to dictonary result_terms
    for i in range(0, len(terms2), 2):
        for j in range(0, len(terms), 2):
            if type(terms2[i]) == type(terms[j]) == list:
                if str(int(terms2[i][1][1]) + int(terms[j][1][1])) not in result_terms: # Adds dictionary value if doesn't exist
                    result_terms[str(int(terms2[i][1][1]) + int(terms[j][1][1]))] = 0
                try:
                    if terms2[i-1] == '-' == terms[j-1]: # Deals with the case where both terms are negative
                        result_terms[str(int(terms2[i][1][1]) + int(terms[j][1][1]))] += int(terms2[i][0]) * int(terms[j][0])
                    elif terms2[i-1] == '-' or terms[j-1] == '-': # Deals with the case where one term is negative
                        result_terms[str(int(terms2[i][1][1]) + int(terms[j][1][1]))] -= int(terms2[i][0]) * int(terms[j][0])
                    else:
                        result_terms[str(int(terms2[i][1][1]) + int(terms[j][1][1]))] += int(terms2[i][0]) * int(terms[j][0])
                except IndexError: # Deals with the case where there is no preceeding operator
                    result_terms[str(int(terms2[i][1][1]) + int(terms[j][1][1]))] += int(terms2[i][0]) * int(terms[j][0])
            elif type(terms2[i]) == list:
                if terms[j].isdigit():
                    if terms2[i][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[terms2[i][1][1]] = 0
                    try:
                        if terms2[i-1] == '-' == terms[j-1]: # Deals with the case where both terms are negative
                            result_terms[terms2[i][1][1]] += int(terms2[i][0]) * int(terms[j])
                        elif terms2[i-1] == '-' or terms[j-1] == '-': # Deals with the case where one term is negative
                            result_terms[terms2[i][1][1]] -= int(terms2[i][0]) * int(terms[j])
                        else:
                            result_terms[terms2[i][1][1]] += int(terms2[i][0]) * int(terms[j])
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms[terms2[i][1][1]] += int(terms2[i][0]) * int(terms[j])
                else:
                    if str(int(terms2[i][1][1]) + 1) not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[str(int(terms2[i][1][1]) + 1)] = 0
                    if terms[j][:-1].isdigit():
                        coefficent = int(terms[j][:-1])
                    else:
                        coefficent = 1
                    try:
                        if terms2[i-1] == '-' == terms[j-1]: # Deals with the case where both terms are negative
                            result_terms[str(int(terms2[i][1][1]) + 1)] += int(terms2[i][0]) * coefficent
                        elif terms2[i-1] == '-' or terms[j-1] == '-': # Deals with the case where one term is negative
                            result_terms[str(int(terms2[i][1][1]) + 1)] -= int(terms2[i][0]) * coefficent
                        else:
                            result_terms[str(int(terms2[i][1][1]) + 1)] += int(terms2[i][0]) * coefficent
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms[str(int(terms2[i][1][1]) + 1)] += int(terms2[i][0]) * coefficent
            elif type(terms[j]) == list:
                if terms2[i].isdigit():
                    if terms[j][1][1] not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[terms[j][1][1]] = 0
                    try:
                        if terms[j-1] == '-' == terms2[i-1]: # Deals with the case where both terms are negative
                            result_terms[terms[j][1][1]] += int(terms[j][0]) * int(terms2[i])
                        elif terms[j-1] == '-' or terms2[i-1] == '-': # Deals with the case where one term is negative
                            result_terms[terms[j][1][1]] -= int(terms[j][0]) * int(terms2[i])
                        else:
                            result_terms[terms[j][1][1]] += int(terms[j][0]) * int(terms2[i])
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms[terms[j][1][1]] += int(terms[j][0]) * int(terms2[i])
                else:
                    if str(int(terms[j][1][1]) + 1) not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms[str(int(terms[j][1][1]) + 1)] = 0
                    if terms2[i][:-1].isdigit():
                        coefficent = int(terms2[i][:-1])
                    else:
                        coefficent = 1
                    try:
                        if terms[j-1] == '-' == terms2[i-1]: # Deals with the case where both terms are negative
                            result_terms[str(int(terms[j][1][1]) + 1)] += int(terms[j][0]) * coefficent
                        elif terms[j-1] == '-' or terms2[i-1] == '-': # Deals with the case where one term is negative
                            result_terms[str(int(terms[j][1][1]) + 1)] -= int(terms[j][0]) * coefficent
                        else:
                            result_terms[str(int(terms[j][1][1]) + 1)] += int(terms[j][0]) * coefficent
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms[str(int(terms[j][1][1]) + 1)] += int(terms[j][0]) * coefficent
            else:
                if terms2[i].isdigit() and terms[j].isdigit():
                    if '0' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['0'] = 0
                    try:
                        if terms[j-1] == '-' == terms2[i-1]: # Deals with the case where both terms are negative
                            result_terms['0'] += int(terms[j]) * int(terms2[i])
                        elif terms[j-1] == '-' or terms2[i-1] == '-': # Deals with the case where one term is negative
                            result_terms['0'] -= int(terms[j]) * int(terms2[i])
                        else:
                            result_terms['0'] += int(terms[j]) * int(terms2[i])
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms['0'] += int(terms[j]) * int(terms2[i])
                elif terms2[i].isdigit():
                    if '1' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['1'] = 0
                    if terms[j][:-1].isdigit():
                        coefficent = int(terms[j][:-1])
                    else:
                        coefficent = 1
                    try:
                        if terms[j-1] == '-' == terms2[i-1]: # Deals with the case where both terms are negative
                            result_terms['1'] += int(terms2[i]) * coefficent
                        elif terms[j-1] == '-' or terms2[i-1] == '-': # Deals with the case where one term is negative
                            result_terms['1'] -= int(terms2[i]) * coefficent
                        else:
                            result_terms['1'] += int(terms2[i]) * coefficent
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms['1'] += int(terms2[i]) * coefficent
                elif terms[j].isdigit():
                    if '1' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['1'] = 0
                    if terms2[i][:-1].isdigit():
                        coefficent = int(terms2[i][:-1])
                    else:
                        coefficent = 1
                    try:
                        if terms[j-1] == '-' == terms2[i-1]: # Deals with the case where both terms are negative
                            result_terms['1'] += int(terms[j]) * coefficent
                        elif terms[j-1] == '-' or terms2[i-1] == '-': # Deals with the case where one term is negative
                            result_terms['1'] -= int(terms[j]) * coefficent
                        else:
                            result_terms['1'] += int(terms[j]) * coefficent
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms['1'] += int(terms[j]) * coefficent
                else:
                    if '2' not in result_terms: # Adds dictionary value if doesn't exist
                        result_terms['2'] = 0
                    if terms[j][:-1].isdigit():
                        coefficent1 = int(terms[j][:-1])
                    else:
                        coefficent1 = 1
                    if terms2[i][:-1].isdigit():
                        coefficent2 = int(terms2[i][:-1])
                    else:
                        coefficent2 = 1
                    try:
                        if terms[j-1] == '-' == terms2[i-1]: # Deals with the case where both terms are negative
                            result_terms['2'] += coefficent1 * coefficent2
                        elif terms[j-1] == '-' or terms2[i-1] == '-': # Deals with the case where one term is negative
                            result_terms['2'] -= coefficent1 * coefficent2
                        else:
                            result_terms['2'] += coefficent1 * coefficent2
                    except IndexError: # Deals with the case where there is no preceeding operator
                        result_terms['2'] += coefficent1 * coefficent2
    # Converts dictionary result_terms into a list result
    # creates and iterable of all exponents from greatest to least to be used in the for loop
    for key in sorted(iter(list(result_terms)), key=lambda x: int(x), reverse=True):
        # to prevent having an operator in front there is 
        # an unique case if it is the first index in the list 
        if result == []:
            if key == '0' or key == '1':
                result.append(str(result_terms[key]))
            else:
                result.append([str(result_terms[key]), ('x', key)])
        else:
            if key == '0': # specilized case if term is of exponent 0
                if '-' in str(result_terms[key]): # Deals with the case where the value is negative
                    result.append('-')
                    result.append(str(abs(result_terms[key])))
                else:
                    result.append('+')
                    result.append(str(result_terms[key]))
            elif key == '1': # specilized case if term is of exponent 1
                if '-' in str(result_terms[key]): # Deals with the case where the value is negative
                    result.append('-')
                    result.append(str(abs(result_terms[key]))+'x')
                else:
                    result.append('+')
                    result.append(str(result_terms[key])+'x')
            else:
                if '-' in str(result_terms[key]): # Deals with the case where the value is negative
                    result.append('-')
                    result.append([str(abs(result_terms[key])), ('x', key)])
                else:
                    result.append('+')
                    result.append([str(result_terms[key]), ('x', key)])
    return result

def break_sec_terms(equation):
    """
    Takes a string as input and returns it in the form:
    [['coefficent', ('x', 'power')], '+/-'. ['coefficent', ('x', 'power')], ...,
     '+/-', 'coefficent x', '+/-', 'coefficent']
    
    Example
     Input: '2x^2+x-3'
     Output: [['2', ('x', '2')], '+', 'x', '-', '3']
    """
    result = []
    try:
        while True:
            # Identifies if/where the first instance of '+' is
            try:
                plus_idx = equation.index('+')
            except ValueError:
                plus_idx = None
            # Identifies if/where the first instance of '-' is
            try:
                minus_idx = equation[1:].index('-') + 1
            except ValueError:
                minus_idx = None
            # "Example String"[:None] == "Example String"
            # For the last term where both plus_idx and minus_idx is None
            # Will still properly append to list result, however be met with a
            # TypeError at substringing the variable equation (None + 1 == TypeError)
            if plus_idx == None: # Indicates minus is likely first
                result.append(equation[:minus_idx]) # Adds everything before the minus to list result
                result.append(equation[minus_idx]) # Adds the minus to list result
                equation = equation[minus_idx + 1:] # removes everything before/including the minus
            elif minus_idx == None: # Indicates plus is first
                result.append(equation[:plus_idx]) # Adds everything before the plus to list result
                result.append(equation[plus_idx]) # Adds the plus to list result
                equation = equation[plus_idx + 1:] # removes everything before/including the plus
            elif plus_idx < minus_idx: # Indicates plus is first
                result.append(equation[:plus_idx]) # Adds everything before the plus to list result
                result.append(equation[plus_idx]) # Adds the plus to list result
                equation = equation[plus_idx + 1:] # removes everything before/including the plus
            else: # Indicates minus is first
                result.append(equation[:minus_idx]) # Adds everything before the minus to list result
                result.append(equation[minus_idx]) # Adds the minus to list result
                equation = equation[minus_idx + 1:] # removes everything before/including the minus
    except TypeError: # TypeError is caused by after the last term is appended to list
        pass # So, nothing needs to be done when the error occurs
    finally: # replace all terms with '^' with proper format using break_exp_term()
        try:
            for i in range(len(result)):
                if '^' in result[i]:
                    result[i] = break_exp_term(result[i])
        except IndexError:
            pass
    return result
    
def break_exp_term(term):
    """
    Takes a string as input in the form ax^b and returns it in the form ['a', ('x', 'b')]
    
    Example
     Input: '2x^2'
     Output: ['2', ('x', '2')]
    """
    result = [term[:term.index('x')]] # Adds coefficent
    if result[0] == '-': # Deals with the case where it is -1
        result[0] = '-1'
    elif result[0] == '': # Deals with the case where it is 1
        result[0] = '1'
    result.append(('x', term[term.index('^')+1:])) # adds the 'x' and exponent value
    return result
        
def equation_to_string(equation):
    """
    Takes a list of terms and operators as input and returns it as a string in
    the form: 'ax^n +/- bx^n-1 +/- ... +/- cx +/- d'
    
    Example
     Input: [['-3', ('x', '3')], '-', ['2', ('x', '2')], '+',
              ['1', ('x', '1')], '+', ['2', ('x', '0')]]
     Output: '-3x^3 - 2x^2 + x + 2'
    """
    result = ''
    if len(equation) == 1:
        equation = equation[0]
    for term in equation:
        if type(term) == list:
            if term[1][1] == '0': # Deals with the case where exponent is 0
                result += term[0]
            elif term[1][1] == '1': # Deals with the case where exponent is 1
                if term[0] == "1": # Deals with the case where it is 1
                    result += term[1][0]
                elif term[0] == "-1": # Deals with the case where it is -1
                    result += "-x"
                else:
                    result += term[0] + term[1][0]
            else:
                result += term[0] + term[1][0] + "^" + term[1][1]
        else:
            result += term
        result += ' ' # Adds a space between terms and operators for visual clarity
    return result

if __name__ == "__main__":
    # Get the equation from the input file
    file_input = open("input.txt", "r")
    equation_full = file_input.readline()
    file_input.close()
    equation_full = equation_full.replace(" ", "") # remove spaces
    
    # Break equation into ["", "+/-", "", ...] (for addition/subtraction)
    equation_full = break_sec_add(equation_full)
    
    # Break further into [["", exp], ["", exp]] (for multiplication)
    temp = []
    for i in range(len(equation_full)):
        if equation_full[i] == '-':
            temp.append('-')
        elif equation_full[i] == '+':
            temp.append('+')
        else:
            temp.append(break_sec_mult(equation_full[i]))
    equation_full = temp
    del temp
    
    # Expand Terms (ax^n +/- bx^n-1 +/- ... +/- cx +/- d)^n
    for i in range(len(equation_full)):
        if type(equation_full[i]) == list:
            for j in range(len(equation_full[i])):
                equation_full[i][j] = exp_expansion(equation_full[i][j])
        else:
            pass
    
    # Multiply Terms (ax^n +/- bx^n-1 +/- ... +/- cx +/- d) (ax^n +/- bx^n-1 +/- ... +/- cx +/- d)
    result_temp = []
    for i in range(len(equation_full)):
        if type(equation_full[i]) == list:
            if len(equation_full[i]) == 1:
                result_temp.append(equation_full[i])
            elif len(equation_full[i]) == 2:
                result_temp.append(mult_expansion(equation_full[i][0], equation_full[i][1]))
            else:
                temp = equation_full[i][0]
                for j in range(1, len(equation_full[i])):
                    temp = mult_expansion(temp, equation_full[i][j])
                result_temp.append(temp)
                del temp
        else:
            result_temp.append(equation_full[i])
    equation_full = result_temp
    del result_temp
    
    # Add Terms (ax^n +/- bx^n-1 +/- ... +/- cx +/- d) + (ax^n +/- bx^n-1 +/- ... +/- cx +/- d)
    if len(equation_full) != 1:
        for i in range(0, len(equation_full), 2):
            if i == 0:
                temp = equation_full[0]
            else:
                if equation_full[i-1] == '-':
                    temp = add_expansion(temp, equation_full[i], True)
                else:
                    temp = add_expansion(temp, equation_full[i], False)
        equation_full = temp
        del temp
    
    # Convert into a string for standard polynomial apperence
    equation_full = equation_to_string(equation_full)
    print()
    print(equation_full) # ... and print the result
    
    # Output result into an output file
    file_output = open("output.txt", "w")
    file_output.write(equation_full)
    file_output.close()