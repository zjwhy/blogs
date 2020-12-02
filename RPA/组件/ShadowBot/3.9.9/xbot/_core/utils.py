import re


def pattern_from_str_or_re(value):
    if isinstance(value, str):
        chars = [c for c in value]
        regex_tokens = {'*', '.', '?', '+', '$', '^',
                        '[', ']', '(', ')', '{', '}', '|', '\\', '/'}
        for i in range(len(chars)-1, -1, -1):
            if chars[i] in regex_tokens:
                chars.insert(i, '\\')
        return ''.join(chars)
    elif isinstance(value, re.Pattern):
        return value.pattern
    else:
        return None
