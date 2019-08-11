import unittest
from phones_parser import parse


class ParserSanityCheck(unittest.TestCase):
    def test_run_parser(self):
        self.assertEqual(next(parse(['89091234567']), None), '89091234567', 'plain phones should pass')

        self.assertEqual(next(parse(['abcd']), None), None, 'alpha sequences should not pass')
        self.assertEqual(next(parse(['12345']), None), None, 'too short numeric sequences should not pass')
        self.assertEqual(next(parse(['926123456789']), None), None, 'too long sequences of digits should not pass')
        self.assertEqual(
            next(parse(['Get as much as possible (but not too much!)']), None), None,
            'at least some digits has to present'
        )
        self.assertEqual(
            next(parse(['(926) 123-45-67']), None),
            '89261234567',
            'brackets, spaces, dashes should vanish'
        )

        self.assertEqual(
            next(parse(['(926) 123-45-67']), None),
            '89261234567',
            'brackets, spaces, dashes should vanish'
        )

        self.assertEqual(
            next(parse([
                '<img src="/pfiles/asdasdasd/d3e2f0656731524f6ccd7a3a4a193569-a34-90.jpg" width="60" height="80">'
            ]), None),
            None,
            'random hashes should not pass'
        )

        self.assertEqual(next(parse(['tel:+74951370720']), None), '84951370720', 'real line from hands.ru should pass')
        self.assertEqual(next(parse(['54.5913 293212.83']), None), None, 'some points should not pass')
