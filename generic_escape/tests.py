
from . import GenericEscape, GenericQuote
import unittest

class GenericEscapeTest(unittest.TestCase):
    def test_escape(self):
        def back_and_forth_check(instance, s):
            v = instance.unescape(instance.escape(s))[1]
            self.assertEqual(s,v)
        for escaped in [GenericEscape.escaped,
                        {'a':'aa'},
                        {'~':'~tilde', 'b':'~bee', '\\':'~backslash', 'Z':'~Z'}]:
            inst = GenericEscape()
            inst.escaped = escaped
            inst.unescape_whitelist = {'Z'}
            inst.update()
            for s in ["asdf","a'~bZ","a'\'Z~~b",'~b\\\'ZZ a','a~Z~\\n\nb']:
                back_and_forth_check(inst,s)
    def test_unescape(self):
        inst = GenericEscape()
        for original,unescape_r in [
                ('a@','a@'),
                ('abc@\nd','abc@'),
                ('a\\n\\\\x@','a\n\\x@'),
                ('a@\\Xyz','a@'),
                ('abc@"yz','abc@')]:
            length, ue = inst.unescape(original)
            self.assertEqual(original.index('@'), length-1)
            self.assertEqual(ue, unescape_r)

class GenericQuoteTest(unittest.TestCase):
    def test_quote(self):
        class MyEscapeClass(GenericEscape):
            escaped = {'~':'~tilde',
                       'b':'~bee'}
        inst = GenericQuote()
        inst.quoting_delimiters = {'[[':(']]','~doubleleftbracket'),
                                   '[!':('>','~leftanglebracket'),
                                   'X':('Y','~capitaly'),
                                   'Z':('Z','~capitalz')}
        inst.escape_class = MyEscapeClass
        inst.update()
        for startq in inst.quoting_delimiters.keys():
            for s in ['[[!Xa~>]]~ [[~[',
                      '[<[[[!> aa XZ~',
                      '[[X>]]>aY~capitaly~~[[']:
                quoted = inst.quote(startq, s)
                self.assertEqual(s, inst.unquote(quoted)[2])
    def test_unescape(self):
        class MyEscapeClass(GenericEscape):
            escaped = {'~':'~tilde',
                       'b':'~bee',
                       '[':'~[', ']':'~]',
                       'Z':'~Z'}
            unescape_whitelist = {'Z'}
        inst = GenericQuote()
        inst.quoting_delimiters = {'[':(']',None),
                                   'aaa':('aaa','~3a'),
                                   'a':('a','~a')}
        inst.escape_class = MyEscapeClass
        inst.update()
        for original,unquote_r in [
                ('[@x]@','x'),
                ('aaa@x~beeaaa@','xb'),
                ('a@~a~a~beea@aa','aab'),
                ('[@a~]Z~Z~tilde~beexZ]@]', 'a]ZZ~bxZ')]:
            expected_sq = original[:original.index('@')]
            original = original.replace('@','',1)
            sq, length, uq = inst.unquote(original)
            self.assertEqual(original.index('@'), length)
            self.assertEqual(uq, unquote_r)

