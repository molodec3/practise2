class Rule:

    def __init__(self, first_arg, second_arg=None):
        if second_arg is None:
            rule_list = first_arg.split(' ')
            self.first = rule_list[0]
            if rule_list[1] != '1':
                self.second = rule_list[1:]
            else:
                self.second = ['']
        else:
            self.first = first_arg
            self.second = second_arg

    def __hash__(self):  # implemented own hashes to have properly working set
        return hash((self.first, tuple(self.second)))

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second


class Grammar:

    def __init__(self):
        self.rules = dict()

    def add_rule(self, rule):
        if self.rules.get(rule.first) is None:
            self.rules[rule.first] = list()

        self.rules[rule.first].append(rule.second)

    def __hash__(self):
        return hash(frozenset(self.rules.items()))

    def __eq__(self, other):
        return self.rules == other.rules


class EarleySituation:

    grammar = None  # grammar -- given by user
    helpers = None  # helpers -- symbols which are not from the alphabet but name the rules given

    def __init__(self, rule, position, dot, grammar=None, helpers=None):
        self.rule = rule  # name from helpers as first and list of symbols as second
        self.position = position  # prev position
        self.dot = dot  # dot position
        if grammar is not None:
            EarleySituation.grammar = grammar
        if helpers is not None:
            EarleySituation.helpers = helpers

    def __hash__(self):
        return hash((self.rule, self.position, self.dot))

    def __eq__(self, other):
        return self.rule == other.rule and self.position == other.position and self.dot == other.dot


def process_earley(g, w):
    helpers = {key for key in g.rules.keys()}
    D = [set() for i in range(len(w) + 1)]
    D[0].add(EarleySituation(Rule('S\' S'), 0, 0, g, helpers))
    flag_change = True
    while flag_change:
        flag_change = predict(D, 0) or complete(D, 0)

    for i in range(1, len(w) + 1):
        scan(D, i, w)
        flag_change = True
        while flag_change:
            flag_change = predict(D, i) or complete(D, i)

    if EarleySituation(Rule('S\'', ['S']), 0, 1) in D[len(w)]:
        return True
    return False


def scan(D, j, w):
    if j == 0:
        return
    for situation in D[j - 1]:
        if situation.dot < len(situation.rule.second) and \
                situation.rule.second[situation.dot] not in EarleySituation.helpers:
            if situation.rule.second[situation.dot] == w[j - 1]:
                D[j].add(EarleySituation(situation.rule, situation.position, situation.dot + 1))


def predict(D, j):
    addition = set()
    origin_len = len(D[j])
    for situation in D[j]:
        if situation.dot < len(situation.rule.second) and \
                situation.rule.second[situation.dot] in EarleySituation.helpers:
            for rule in EarleySituation.grammar.rules[situation.rule.second[situation.dot]]:
                next_situation = EarleySituation(Rule(situation.rule.second[situation.dot], rule), j, 0)
                addition.add(next_situation)

    D[j].update(addition)
    if len(D[j]) > origin_len:
        return True
    return False


def complete(D, j):
    addition = set()
    origin_len = len(D[j])
    for situation in D[j]:
        if situation.rule.second == [''] or situation.dot == len(situation.rule.second):
            for prev_situation in D[situation.position]:
                if prev_situation.dot < len(prev_situation.rule.second) and \
                        prev_situation.rule.second[prev_situation.dot] == situation.rule.first:
                    addition.add(EarleySituation(prev_situation.rule, prev_situation.position, prev_situation.dot + 1))

    D[j].update(addition)
    if len(D[j]) > origin_len:
        return True
    return False


def main():
    w = input()
    rules_count = int(input())
    grammar = Grammar()
    for i in range(rules_count):
        rule_str = input()
        rule = Rule(rule_str)
        grammar.add_rule(rule)

    result = process_earley(grammar, w)
    print(result)


if __name__ == '__main__':
    main()
