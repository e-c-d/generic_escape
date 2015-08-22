
import re
from itertools import chain as ichain

class GenericEscape(object):
    """You should most definitely subclass this."""
    
    simple_escaped = ["'",'"','\\']
    simple_escaped_character = '\\'
    escaped = {'\n': r'\n'}
    
    def __init__(self):
        self.update()
    
    def update(self):
        e = self.escaped.copy()
        esc_char = self.simple_escaped_character
        e.update((x,esc_char+x) for x in self.simple_escaped)
        
        def re_one_of(xs):
            # the "a^" thing matches nothing on purpose.
            # it is necessary in the case where `xs` is empty
            # because then the regex is "()" which matches the
            # empty string. oops.
            return '|'.join(ichain(
                (re.escape(x) for x in xs), ["a^"]))
        
        self._escape_re = re.compile(re_one_of(e.keys()), re.DOTALL)
        
        self._unescape_re = re.compile(
            '({})|({})'.format(*[
                re_one_of(X)
                for X in [e.values(), e.keys()]]), re.DOTALL)
        self._escape_dict = e
        self._unescape_dict = {v:k for k,v in e.items()}
    
    def unescape(self, string, start_position=0):
        """returns (end_position, unescaped_string)"""
        unescape_re   = self._unescape_re
        unescape_dict = self._unescape_dict
        r = []
        i = start_position
        len_string = len(string)
        while True:
            m = unescape_re.search(string, i)
            if m:
                r.append(string[i:m.start()])
                good, bad = m.groups()
                if good is not None:
                    i = m.end()
                    r.append(unescape_dict[good])
                else: # bad is not None
                    i = m.start()
                    break
            else: # rest of string is kosher, use it as-is
                r.append(string[i:])
                i = len(string)
                break
        
        return (i, ''.join(r))
    
    def escape(self, string):
        """returns escaped string"""
        escape_dict = self._escape_dict
        return self._escape_re.sub(lambda m:escape_dict[m.group()], string)

