import unittest
from alethiometer.instrument import Alethiometer, InstrumentError


class TestR1(unittest.TestCase):

    def setUp(self):
        self._al = Alethiometer()

    def test_add_symbol_exception(self):
        self._al.add_symbol("a")
        self._al.add_symbol("b", prev_name="a")
        self.assertRaises(InstrumentError, self._al.add_symbol, "d", "c")

    def test_add_symbols_len(self):
        self.assertEqual(0, len(self._al))
        self._al.add_symbol("a")
        self.assertEqual(1, len(self._al))
        self._al.add_symbol("b", prev_name="a")
        self.assertEqual(2, len(self._al))
        self._al.add_symbol("c", prev_name="b")
        self.assertEqual(3, len(self._al))        

    def test_add_symbol_append(self):
        self._al.add_symbol("a")
        self._al.add_symbol("b", prev_name="a")
        self._al.add_symbol("c", prev_name="b")
        self._al.add_symbol("d", prev_name="c")
        self.assertEqual("b", self._al.get_next_symbol("a", 1))
        self.assertEqual("c", self._al.get_next_symbol("a", 2))
        self.assertEqual("d", self._al.get_next_symbol("b", 2))

    def test_add_symbol_middle(self):
        self._al.add_symbol("a")
        self._al.add_symbol("d", prev_name="a")
        self._al.add_symbol("b", prev_name="a")
        self._al.add_symbol("c", prev_name="b")
        self.assertEqual("b", self._al.get_next_symbol("a", 1))
        self.assertEqual("c", self._al.get_next_symbol("a", 2))
        self.assertEqual("d", self._al.get_next_symbol("b", 2))

    def test_symbol_rotation(self):
        self._al.add_symbol("a")
        self._al.add_symbol("b", prev_name="a")
        self._al.add_symbol("c", prev_name="b")
        self.assertEqual("a", self._al.get_next_symbol("b", 2))
        self.assertEqual("c", self._al.get_next_symbol("b", 4))
        self.assertEqual("c", self._al.get_next_symbol("c", 3))
        self.assertEqual("c", self._al.get_next_symbol("b", 7))

    def test_rotation_single(self):
        self._al.add_symbol("b")
        self.assertEqual("b", self._al.get_next_symbol("b", 1))
        self.assertEqual("b", self._al.get_next_symbol("b", 2))
        self.assertEqual("b", self._al.get_next_symbol("b", 3))
        

class TestR2(unittest.TestCase):

    def setUp(self):
        self._al = Alethiometer()
    
    def test_add_concepts(self):
        self.assertEqual(1, self._al.add_concepts("c1"))
        self.assertEqual(3, self._al.add_concepts("c2", "c3", "c4"))
        self.assertEqual(1, self._al.add_concepts("c1", "c4", "c5"))

    def test_chain_concepts_single_next(self):
        self._al.add_concepts("c1", "c2", "c3", "c4", "c5")
        self._al.chain_concepts("c2", "c3", "c4", "c1")
        self.assertEqual({"c3", "c4", "c1"}, self._al.get_next_concepts("c2"))

    def test_chain_concepts_single_previous(self):
        self._al.add_concepts("c1", "c2", "c3", "c4", "c5")
        self._al.chain_concepts("c2", "c3", "c4", "c1")
        for c in {"c3", "c4", "c1"}:
            self.assertEqual({"c2"}, self._al.get_previous_concepts(c))

    def test_chain_concepts_multiple_next(self):
        self._al.add_concepts("c1", "c2", "c3", "c4", "c5", "c6", "c7")
        self._al.chain_concepts("c1", "c3", "c4")
        self._al.chain_concepts("c1", "c4", "c5", "c6")
        self.assertEqual({"c3", "c4", "c5", "c6"}, self._al.get_next_concepts("c1"))

    def test_chain_concepts_multiple_previous(self):
        self._al.add_concepts("c1", "c2", "c3", "c4", "c5", "c6", "c7")
        self._al.chain_concepts("c1", "c3", "c4")
        self._al.chain_concepts("c2", "c3", "c4", "c5")
        self._al.chain_concepts("c7", "c4")
        self._al.chain_concepts("c1", "c4", "c5")
        self.assertEqual({"c1", "c2"}, self._al.get_previous_concepts("c3"))
        self.assertEqual({"c1", "c2", "c7"}, self._al.get_previous_concepts("c4"))
        self.assertEqual({"c1", "c2"}, self._al.get_previous_concepts("c5"))


class TestR3(unittest.TestCase):

    def setUp(self):
        self._al = Alethiometer()
        self._al.add_symbol("a")
        self._al.add_symbol("b", prev_name="a")
        self._al.add_symbol("c", prev_name="b")
        self._al.add_symbol("d", prev_name="c")
        self._al.add_concepts("c1", "c2", "c3", "c4", "c5", "c6", "c7")

    def test_get_concepts_of_symbol_no_filter(self):
        self._al.link_symbol_to_concept("a", "c3")
        self._al.link_symbol_to_concept("a", "c2")
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("a", "c7")
        self.assertEqual({"c3", "c2", "c1", "c7"}, self._al.get_concepts_of_symbol("a"))

    def test_get_concepts_of_symbol_filter(self):
        self._al.link_symbol_to_concept("a", "c3")
        self._al.link_symbol_to_concept("a", "c2")
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("a", "c7")
        self.assertEqual({"c3", "c7"}, self._al.get_concepts_of_symbol("a", lambda x: int(x[1:]) > 2))

    def test_get_symbol_of_concepts_simple(self):
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("b", "c1")
        self._al.link_symbol_to_concept("c", "c1")
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("a", "c2")
        self.assertEqual(["a", "b", "c"], sorted([t[0] for t in self._al.get_symbols_of_concept("c1")]))

    def test_get_symbol_of_concepts_full(self):
        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("b", "c1")
        self._al.link_symbol_to_concept("c", "c1")
        self._al.link_symbol_to_concept("a", "c1")
    
        self._al.link_symbol_to_concept("a", "c3")
        self._al.link_symbol_to_concept("a", "c4")
        self._al.link_symbol_to_concept("a", "c5")

        self._al.link_symbol_to_concept("b", "c2")

        self._al.link_symbol_to_concept("c", "c7")
        self._al.link_symbol_to_concept("c", "c6")

        self.assertEqual([("a", 4), ("c", 3), ("b", 2)], self._al.get_symbols_of_concept("c1"))


class TestR4(unittest.TestCase):

    def setUp(self):
        self._al = Alethiometer()
        self._al.add_symbol("a")
        self._al.add_symbol("b", prev_name="a")
        self._al.add_symbol("c", prev_name="b")
        self._al.add_concepts("c1", "c2", "c3", "c4", "c5", "c6", "c7")

        self._al.link_symbol_to_concept("a", "c1")
        self._al.link_symbol_to_concept("a", "c2")
        self._al.link_symbol_to_concept("a", "c3")

        self._al.link_symbol_to_concept("b", "c3")
        self._al.link_symbol_to_concept("b", "c4")
        self._al.link_symbol_to_concept("b", "c5")

        self._al.link_symbol_to_concept("c", "c5")
        self._al.link_symbol_to_concept("c", "c6")
        self._al.link_symbol_to_concept("c", "c7")

        self._al.chain_concepts("c2", "c6", "c7")
        self._al.chain_concepts("c4", "c5")
        self._al.chain_concepts("c6", "c3")
    
    def test_translate_one(self):
        res = self._al.translation(["b"])
        self.assertIn(res, {"c3", "c4", "c5"})

    def test_translate_fail(self):
        res1 = self._al.translation(["b"])
        res2 = self._al.translation(["a", "b"])
        self.assertIsNotNone(res1)
        self.assertIsNone(res2)

    def test_translate_multiple_1(self):
        self.assertEqual("c2 c6 c3", self._al.translation(["a", "c", "b"]))

    def test_translate_multiple_2(self):
        self.assertEqual("c2 c6 c3", self._al.translation(["a", "c", "a"]))
