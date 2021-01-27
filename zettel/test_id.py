import unittest
from unittest import TestCase

from zettel.id import Id


class TestIdParse(TestCase):
    def test_single_letter(self):
        a = Id("a")
        self.assertEqual(1, len(a.parts))
        self.assertEqual("a", repr(a.parts[0]))

    def test_single_digit(self):
        a = Id("0")
        self.assertEqual(1, len(a.parts))
        self.assertEqual("0", repr(a.parts[0]))

    def test_two_letters(self):
        a = Id("aa")
        self.assertEqual(1, len(a.parts))
        self.assertEqual("aa", repr(a.parts[0]))

    def test_two_digits(self):
        a = Id("00")
        self.assertEqual(1, len(a.parts))
        self.assertEqual("00", repr(a.parts[0]))

    def test_two_letters_with_separator(self):
        a = Id("a.b")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("a", repr(a.parts[0]))
        self.assertEqual("b", repr(a.parts[1]))

    def test_two_digits_with_separator(self):
        a = Id("0.1")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("0", repr(a.parts[0]))
        self.assertEqual("1", repr(a.parts[1]))

    def test_letter_then_digit(self):
        a = Id("a0")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("a", repr(a.parts[0]))
        self.assertEqual("0", repr(a.parts[1]))

    def test_digit_then_letter(self):
        a = Id("0a")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("0", repr(a.parts[0]))
        self.assertEqual("a", repr(a.parts[1]))

    def test_letter_then_digit_with_separator(self):
        a = Id("a.0")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("a", repr(a.parts[0]))
        self.assertEqual("0", repr(a.parts[1]))

    def test_digit_then_letter_with_separator(self):
        a = Id("0.a")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("0", repr(a.parts[0]))
        self.assertEqual("a", repr(a.parts[1]))

    def test_letter_then_digit_with_two_separators(self):
        a = Id("a..0")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("a", repr(a.parts[0]))
        self.assertEqual("0", repr(a.parts[1]))

    def test_digit_then_letter_with_two_separators(self):
        a = Id("0..a")
        self.assertEqual(2, len(a.parts))
        self.assertEqual("0", repr(a.parts[0]))
        self.assertEqual("a", repr(a.parts[1]))


class TestIdNext(TestCase):
    def test_single_letter(self):
        a = Id("a")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("b", repr(n.parts[0]))
        self.assertEqual("b", n.value)

    def test_two_letters(self):
        a = Id("aa")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("ab", repr(n.parts[0]))
        self.assertEqual("ab", n.value)

    def test_single_digit(self):
        a = Id("0")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("1", repr(n.parts[0]))
        self.assertEqual("1", n.value)

    def test_two_digits(self):
        a = Id("00")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("01", repr(n.parts[0]))
        self.assertEqual("01", n.value)

    def test_single_rollover_letter(self):
        a = Id("Z")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("aa", repr(n.parts[0]))
        self.assertEqual("aa", n.value)

    def test_two_with_single_rollover_letter(self):
        a = Id("aZ")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("ba", repr(n.parts[0]))
        self.assertEqual("ba", n.value)

    def test_single_rollover_digit(self):
        a = Id("9")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("00", repr(n.parts[0]))
        self.assertEqual("00", n.value)

    def test_two_with_single_rollover_digit(self):
        a = Id("09")
        n = a.next()
        self.assertEqual(1, len(n.parts))
        self.assertEqual("10", repr(n.parts[0]))
        self.assertEqual("10", n.value)

    def test_two_parts_single_digit_single_letter(self):
        a = Id("0a")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("b", repr(n.parts[1]))
        self.assertEqual("0b", n.value)

    def test_two_parts_single_letter_single_digit(self):
        a = Id("a0")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("1", repr(n.parts[1]))
        self.assertEqual("a1", n.value)

    def test_two_parts_single_letter_single_digit_with_rollover(self):
        a = Id("a9")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("00", repr(n.parts[1]))
        self.assertEqual("a00", n.value)

    def test_two_parts_single_digit_single_letter_with_rollover(self):
        a = Id("0Z")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("aa", repr(n.parts[1]))
        self.assertEqual("0aa", n.value)

    def test_two_parts_single_letter_single_digit_single_separator(self):
        a = Id("a.0")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("1", repr(n.parts[1]))
        self.assertEqual("a.1", n.value)

    def test_two_parts_single_digit_single_letter_single_separator(self):
        a = Id("0.a")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("b", repr(n.parts[1]))
        self.assertEqual("0.b", n.value)

    def test_two_parts_two_letters_single_separator(self):
        a = Id("a.a")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("b", repr(n.parts[1]))
        self.assertEqual("a.b", n.value)

    def test_two_parts_two_digits_single_separator(self):
        a = Id("0.0")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("1", repr(n.parts[1]))
        self.assertEqual("0.1", n.value)

    def test_two_parts_single_letter_single_digit_single_separator_with_rollover(self):
        a = Id("a.9")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("00", repr(n.parts[1]))
        self.assertEqual("a.00", n.value)

    def test_two_parts_single_digit_single_letter_single_separator_with_rollover(self):
        a = Id("0.Z")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("aa", repr(n.parts[1]))
        self.assertEqual("0.aa", n.value)

    def test_two_parts_two_letters_single_separator_with_rollover(self):
        a = Id("a.Z")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("aa", repr(n.parts[1]))
        self.assertEqual("a.aa", n.value)

    def test_two_parts_two_digits_single_separator_with_rollover(self):
        a = Id("0.9")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("00", repr(n.parts[1]))
        self.assertEqual("0.00", n.value)

    def test_two_parts_single_letter_single_digit_two_separators(self):
        a = Id("a..0")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("a", repr(n.parts[0]))
        self.assertEqual("1", repr(n.parts[1]))
        self.assertEqual("a..1", n.value)

    def test_two_parts_single_digit_single_letter_two_separators(self):
        a = Id("0..a")
        n = a.next()
        self.assertEqual(2, len(n.parts))
        self.assertEqual("0", repr(n.parts[0]))
        self.assertEqual("b", repr(n.parts[1]))
        self.assertEqual("0..b", n.value)

    def test_next_structure(self):
        a = Id("200010111223")
        n = a.next()
        self.assertEqual("200010111224", n.value)

    def test_next_structure_with_last_9(self):
        a = Id("200010111229")
        n = a.next()
        self.assertEqual("200010111230", n.value)


class TestIdParent(TestCase):
    def test_single_letter(self):
        a = Id("a")
        self.assertRaises(ValueError, a.parent)

    def test_two_letters(self):
        a = Id("aa")
        self.assertRaises(ValueError, a.parent)

    def test_single_digit(self):
        a = Id("0")
        self.assertRaises(ValueError, a.parent)

    def test_two_digits(self):
        a = Id("00")
        self.assertRaises(ValueError, a.parent)

    def test_single_rollover_letter(self):
        a = Id("Z")
        self.assertRaises(ValueError, a.parent)

    def test_two_letters_with_rollover(self):
        a = Id("aZ")
        self.assertRaises(ValueError, a.parent)

    def test_single_rollover_digit(self):
        a = Id("9")
        self.assertRaises(ValueError, a.parent)

    def test_two_digits_with_rollover(self):
        a = Id("09")
        self.assertRaises(ValueError, a.parent)

    def test_letter_then_digit(self):
        a = Id("a0")
        p = a.parent()
        self.assertEqual("a", p.value)
        self.assertEqual(1, len(p.parts))
        self.assertEqual("a", repr(p.parts[0]))

    def test_digit_then_letter(self):
        a = Id("0a")
        p = a.parent()
        self.assertEqual("0", p.value)
        self.assertEqual(1, len(p.parts))
        self.assertEqual("0", repr(p.parts[0]))


class TestIdCompare(TestCase):
    def test_single_equal_letters(self):
        l = Id("a")
        r = Id("a")
        self.assertEqual(0, l.compare(r))

    def test_single_equal_numbers(self):
        l = Id("0")
        r = Id("0")
        self.assertEqual(0, l.compare(r))

    def test_single_equal_letter_and_number(self):
        l = Id("a")
        r = Id("0")
        self.assertEqual(0, l.compare(r))

    def test_single_different_letters(self):
        l = Id("a")
        r = Id("b")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_single_different_numbers(self):
        l = Id("0")
        r = Id("1")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_single_different_letter_and_number(self):
        l = Id("a")
        r = Id("1")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_single_to_double_different_letters(self):
        l = Id("a")
        r = Id("aa")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_single_to_double_different_numbers(self):
        l = Id("0")
        r = Id("01")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_double_to_double_different_letters(self):
        l = Id("aa")
        r = Id("ab")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_double_to_double_different_numbers(self):
        l = Id("00")
        r = Id("01")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_double_to_double_different_letter_and_numbers(self):
        l = Id("aa")
        r = Id("01")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_same_letters_with_separator(self):
        l = Id("a.a")
        r = Id("a.a")
        self.assertEqual(0, l.compare(r))

    def test_different_letters_with_separator(self):
        l = Id("a.a")
        r = Id("a.b")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_single_letter_and_letters_with_separator(self):
        l = Id("a")
        r = Id("a.b")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_two_lower_a_greater_than_lower_z(self):
        l = Id("z")
        r = Id("aa")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_capital_a_greater_than_lower_a(self):
        l = Id("a")
        r = Id("A")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_capital_a_greater_than_lower_z(self):
        l = Id("z")
        r = Id("A")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_capital_last_greater_than_lower_last(self):
        l = Id("aa")
        r = Id("aA")
        self.assertEqual(-1, l.compare(r))
        self.assertEqual(1, r.compare(l))

    def test_equality(self):
        a = Id('a')
        b = Id('a')
        c = Id('a')
        d = Id('0')
        e = Id('0')
        f = Id('0')

        # Reflexive
        self.assertEqual(a, a)
        self.assertEqual(d, d)
        # Consistent
        self.assertEqual(a, a)
        self.assertEqual(d, d)

        # Symmetric
        self.assertEqual(a, b)
        self.assertEqual(b, a)
        self.assertEqual(d, e)
        self.assertEqual(e, d)
        self.assertEqual(a, d)
        self.assertEqual(d, a)

        # Transitive
        self.assertEqual(b, c)
        self.assertEqual(a, c)
        self.assertEqual(e, f)
        self.assertEqual(d, f)
        self.assertEqual(b, f)
        self.assertEqual(a, f)


if __name__ == '__main__':
    unittest.main()