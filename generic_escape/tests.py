
from . import GenericEscape
import unittest

class GenericEscapeTest(unittest.TestCase):
    def test_escape(self):
        def back_and_forth_check(instance, s):
            v = instance.unescape(instance.escape(s))[1]
            self.assertEqual(s,v)
        inst = GenericEscape()
        for s in ["asdf","a'b","a'\'b",'b\\\' a','a\\n\nb']:
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
