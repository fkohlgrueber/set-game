import unittest
from copy import deepcopy

from core import CardSet, Card, Deck, BasePlayer, BruteForcePlayer, Game


class SetTestCase(unittest.TestCase):
    def test_empty_set(self):
        card_set = CardSet([])
        self.assertEqual(card_set.is_valid(), False)

    def test_valid_identical(self):
        card_set = CardSet([Card([1]), Card([1]), Card([1])])
        self.assertEqual(card_set.is_valid(), True)

    def test_valid_different(self):
        card_set = CardSet([Card([1]), Card([2]), Card([3])])
        self.assertEqual(card_set.is_valid(), True)

    def test_invalid(self):
        card_set = CardSet([Card([1]), Card([2]), Card([2])])
        self.assertEqual(card_set.is_valid(), False)

    def test_valid_multiple_features(self):
        card_set = CardSet([Card([1, 1]), Card([2, 1]), Card([3, 1])])
        self.assertEqual(card_set.is_valid(), True)


class DeckTestCase(unittest.TestCase):
    def test_num_cards(self):
        deck = Deck(num_features=4, num_options_per_feature=3)
        self.assertEqual(len(deck._card_stack), 81)

    def test_cards_2_2(self):
        deck = Deck(num_features=2, num_options_per_feature=2)
        self.assertEqual(sorted(deck._card_stack), [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_cards_1_3(self):
        deck = Deck(num_features=1, num_options_per_feature=3)
        self.assertEqual(sorted(deck._card_stack), [(0,), (1,), (2,)])

    def test_cards_3_1(self):
        deck = Deck(num_features=3, num_options_per_feature=1)
        self.assertEqual(sorted(deck._card_stack), [(0, 0, 0)])

    def test_cards_3_2(self):
        deck = Deck(num_features=3, num_options_per_feature=2)
        exp = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
               (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
        self.assertEqual(sorted(deck._card_stack), exp)

    def test_get_cards(self):
        deck = Deck(num_features=3, num_options_per_feature=2)
        exp = deepcopy(deck._card_stack)

        for i in range(len(exp)):
            self.assertEqual(deck.next_card(), exp[i])

        self.assertIsNone(deck.next_card())


class BasePlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = BasePlayer(0)

    def test_show_cards(self):
        self.assertRaises(NotImplementedError, self.player.show_cards, [])

    def test_remove_cards(self):
        self.assertRaises(NotImplementedError, self.player.remove_cards, [])

    def test_calc_sets(self):
        self.assertRaises(NotImplementedError, self.player.calc_sets)


class BruteForcePlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player_class = BruteForcePlayer

    def test_no_cards(self):
        player = self.player_class(num_options_per_feature=3)
        self.assertEqual(player.calc_sets(), [])

    def test_not_enough_cards(self):
        player = self.player_class(num_options_per_feature=3)
        player.show_cards([Card([1]), Card([1])])
        self.assertEqual(player.calc_sets(), [])

    def test_no_matching_set(self):
        player = self.player_class(num_options_per_feature=3)
        player.show_cards([Card([0]), Card([1]), Card([1])])
        self.assertEqual(player.calc_sets(), [])

    def test_matching_set(self):
        player = self.player_class(num_options_per_feature=3)
        player.show_cards([Card([0]), Card([1]), Card([2])])
        exp = [CardSet([Card([0]), Card([1]), Card([2])])]
        self.assertEqual(player.calc_sets(), exp)

    def test_multiple_matching_sets(self):
        player = self.player_class(num_options_per_feature=3)
        player.show_cards([Card([0, 0]), Card([1, 0]), Card([0, 1]), Card([2, 0]), Card([0, 2])])
        exp = [CardSet([Card([0, 0]), Card([1, 0]), Card([2, 0])]),
               CardSet([Card([0, 0]), Card([0, 1]), Card([0, 2])])]
        self.assertEqual(player.calc_sets(), exp)

    def test_remove_cards(self):
        player = self.player_class(num_options_per_feature=3)
        card_a = Card([1, 0])
        player.show_cards([Card([0, 0]), card_a, Card([0, 1]), Card([2, 0]), Card([0, 2])])
        player.remove_cards([card_a])
        exp = [CardSet([Card([0, 0]), Card([0, 1]), Card([0, 2])])]
        self.assertEqual(player.calc_sets(), exp)

    def test_remove_card_error(self):
        player = self.player_class(num_options_per_feature=3)
        self.assertRaises(ValueError, player.remove_cards, [Card([0, 0])])


class GameTestCase(unittest.TestCase):
    def test_game(self):
        game = Game(num_features=2, num_options_per_feature=3)
        game.deck._card_stack.sort()
        sets = game.play(BruteForcePlayer(3))

        exp = [CardSet([Card([0, 0]), Card([0, 1]), Card([0, 2])]),
               CardSet([Card([1, 0]), Card([1, 1]), Card([1, 2])]),
               CardSet([Card([2, 0]), Card([2, 1]), Card([2, 2])])]
        self.assertEqual(sets, exp)

    def test_game_multiple_matches(self):
        game = Game(num_features=2, num_options_per_feature=3)
        game.deck._card_stack = [Card([2, 0]), Card([1, 0]), Card([0, 1]), Card([0, 2]), Card([0, 0])]
        sets = game.play(BruteForcePlayer(3))

        exp = [CardSet([Card([2, 0]), Card([1, 0]), Card([0, 0])])]
        self.assertEqual(sets, exp)


if __name__ == '__main__':
    unittest.main()
