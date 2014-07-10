import re

class Literal:
    def __init__(self, info, num):
        self.info = info
        self.num = num

class Formula:
    def __init__(self, leftFormula=None, operator=None, rightFormula=None, literal=None):
        self.leftFormula = leftFormula
        self.operator = operator
        self.rightFormula = rightFormula
        self.literal = literal

class Connective:
    def __init__(self, val):
        self.val = val

def tokenize(boolean_expr, selector):
    boolean_expr = boolean_expr.replace('(', ' ( ')
    boolean_expr = boolean_expr.replace(')', ' ) ')
    split_words = boolean_expr.split()
    if selector is True:
        char = 'r'
        tier = 'region'
    else:
        char = 'z'
        tier = 'zone'
    tier_regexp = re.compile (char+'[0-9]+')
    replica_regexp = re.compile ('replica-[0-9]+:'+tier)
    and_regexp = re.compile ('and')
    or_regexp = re.compile ('or')
    not_regexp = re.compile ('not')

    for i in range (0, len(split_words)):
        word = split_words[i]
        if tier_regexp.match(word):
            num = int (word[1:])
            split_words[i] = Literal(char, num)
        elif replica_regexp.match(word):
            num = int (word[len('replica-'):-len(':'+tier)])
            split_words[i] = Literal('replica:'+tier, num)
        elif and_regexp.match(word):
            split_words[i] = Connective('and')
        elif or_regexp.match(word):
            split_words[i] = Connective('or')
        elif not_regexp.match(word):
            split_words[i] = Connective('not')
    return split_words
            
def throw_exception ():
    print 'Cannot parse the policy file'
    exit()

def parse(boolean_expr):
    S = []

    for char in boolean_expr:
        if char is ' ':
            continue
        elif char is '(':
            S.append('(')
            continue
        elif char is ')':
            right = S.pop()
            C = S.pop()
            left = S.pop()
            S.pop()
            F = Formula (left, C, right)
            if not S:
                S.append(F)
                continue
            if isinstance(S[-1:][0], Connective):
                Con = S[-1:][0]
                if Con.val is 'not':
                    S.pop()
                    G=Formula(F,Con)
                    S.append(G)
                else:
                    S.append(F)
            else:
                S.append(F)
            continue
        elif isinstance(char, Connective):
            S.append(char)
            continue
        elif isinstance(char, Literal):
            if not S:
                S.append(Formula(literal=char))
            else:
                if isinstance(S[-1:][0], Connective):
                    if S[-1:][0].val == 'not':
                        S.pop()
                        S.append(Formula(Formula(literal=char), Connective('not')))
                    else:
                        S.append(Formula(literal=char))
                else:
                    S.append(Formula(literal=char))
        else:
            throw_exception()
    # print S
    F = S.pop()
    if S != []:
        throw_exception()
    return F

def evaluate (boolean_formula, val, assigned_replicas):
    if boolean_formula is None:
        return 1
    elif boolean_formula.literal is not None:
        if 'replica' in  boolean_formula.literal.info:
            if boolean_formula.literal.num-1 in assigned_replicas:
                return 2 * (assigned_replicas[boolean_formula.literal.num-1] == val)
            return 1
        else:
            return 2 * (boolean_formula.literal.num == val)
    else:
        if boolean_formula.operator.val == 'not':
            return three_valued_not (evaluate (boolean_formula.leftFormula, val, assigned_replicas))
        elif boolean_formula.operator.val == 'or':
            return three_valued_or (evaluate (boolean_formula.leftFormula, val, assigned_replicas), evaluate (boolean_formula.rightFormula, val, assigned_replicas))
        elif boolean_formula.operator.val == 'and':
            return three_valued_and (evaluate (boolean_formula.leftFormula, val, assigned_replicas), evaluate (boolean_formula.rightFormula, val, assigned_replicas))

def print_formula (boolean_formula):
    if boolean_formula is None:
        return None
    elif boolean_formula.literal is not None:
        return str (boolean_formula.literal.info) + ' ' + str (boolean_formula.literal.num)
    else:
        if boolean_formula.operator.val == 'not':
            return '(' + 'not' + ' ' + str (print_formula(boolean_formula.leftFormula)) + ')'
        return '(' + str (print_formula(boolean_formula.leftFormula)) + ' ' + str(boolean_formula.operator.val) + ' ' + str (print_formula(boolean_formula.rightFormula)) + ')'

def three_valued_not (a):
    return 2-a

def three_valued_or (a, b):
    if a is 2 or b is 2:
        return 1
    if a is 0:
        return b
    return a

def three_valued_and (a, b):
    if a is 0 or b is 0:
        return 0
    if a is 1:
        return b
    return a

def change_literal_to_formula (policy_info, num_replica):
    def substitute (boolean_formula, i, tier):
        if boolean_formula is None:
            return None
        elif boolean_formula.literal is not None:
            if 'replica' in  boolean_formula.literal.info:
                if boolean_formula.literal.num-1 >= i:
                    throw_exception()
                if policy_info[boolean_formula.literal.num-1][tier] is not None:
                    return policy_info[boolean_formula.literal.num-1][tier]
                else:
                    return boolean_formula
            else:
                return boolean_formula
        else:
            if boolean_formula.operator.val == 'not':
                return Formula (substitute(boolean_formula.leftFormula, i,tier), boolean_formula.operator)
            else:
                return Formula (substitute(boolean_formula.leftFormula, i, tier), boolean_formula.operator, substitute(boolean_formula.rightFormula, i, tier))

    for i in range (0, num_replica):
        policy_info[i]['region'] = substitute (policy_info[i]['region'], i, 'region')
        policy_info[i]['zone'] = substitute (policy_info[i]['zone'], i, 'zone')
    return policy_info
