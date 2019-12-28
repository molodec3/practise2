import pytest

from main import process_earley, Grammar, Rule


def get_result(rules, word):
    grammar = Grammar()
    for rule in rules:
        grammar.add_rule(Rule(rule))
    return process_earley(grammar, word)


@pytest.mark.parametrize('rules, word, result', [
    (['S S C', 'S C', 'C c D', 'D a D b', 'D 1'], 'ccabccaabb', True),
    (['S S C', 'S C', 'C c D', 'D a D b', 'D 1'], 'ccccccccccc', True),
    (['S S C', 'S C', 'C c D', 'D a D b', 'D 1'], 'cccccccccca', False),
    (['S S C', 'S C', 'C c D', 'D a D b', 'D 1'], 'bbaacccccab', False),
    (['S C', 'S S a', 'C D d', 'D c D', 'D 1', 'S S S b'], 'cccdcdb', True),
    (['S C', 'S S a', 'C D d', 'D c D', 'D 1', 'S S S b'], 'ccccccdaaacdaaaab', True),
    (['S C', 'S S a', 'C D d', 'D c D', 'D 1', 'S S S b'], 'aab', False),
    (['S C', 'S S a', 'C D d', 'D c D', 'D 1', 'S S S b'], 'bcccddacccda', False)
])
def test_basic(rules, word, result):
    assert get_result(rules, word) == result


@pytest.mark.parametrize('word, result', [
    ('aaaaaaaaa', True),
    ('', True),
    ('ab', False),
    ('abccba', True),
    ('abcba', True),
    ('abcabc', False)
])
def test_palindrome(word, result):
    rules = ['S 1', 'S a', 'S b', 'S c', 'S a S a', 'S b S b', 'S c S c']
    assert get_result(rules, word) == result


@pytest.mark.parametrize('word, result', [
    ('a', True),
    ('ddcabaababacbaba', True),
    ('baa', False),
    ('d', False),
    ('', False)
])
def test_polish_notation(word, result):
    rules = ['S a', 'S b S', 'S c S S', 'S d S S S']
    assert get_result(rules, word) == result


@pytest.mark.parametrize('word, result', [
    ('()()()(()(()))', True),
    ('', True),
    (')(', False),
    ('()(()(()))()()())', False)
])
def test_cbs(word, result):
    rules = ['S 1', 'S ( S ) S']
    assert get_result(rules, word) == result
