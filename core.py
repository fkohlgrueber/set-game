from itertools import product, combinations
from random import shuffle

from typing import Optional, List, Iterable


class Card(tuple):
    pass


class Deck(object):
    def __init__(self, num_features: int, num_options_per_feature: int):
        self.num_features = num_features
        self.num_options_per_feature = num_options_per_feature
        self._card_stack = []

        self.initialize()

    def __len__(self):
        return len(self._card_stack)

    def initialize(self) -> None:
        self._card_stack = [Card(i) for i in product(range(self.num_options_per_feature), repeat=self.num_features)]
        shuffle(self._card_stack)

    def next_card(self) -> Optional[Card]:
        try:
            return self._card_stack.pop(0)
        except IndexError:
            return None


class CardSet(object):
    def __init__(self, cards: Iterable[Card]):
        self.cards = tuple(cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __repr__(self):
        return "CardSet: " + self.cards.__repr__()

    def is_valid(self) -> bool:

        # check for empty CardSet
        if not len(self.cards):
            return False

        for feature_idx in range(len(self.cards[0])):
            num_different_options = len(set(c[feature_idx] for c in self.cards))

            # check if all cards in set either have the same or unique values
            if num_different_options not in (1, len(self.cards)):
                return False

        return True


class BasePlayer(object):
    def __init__(self, num_options_per_feature: int):
        self.num_options_per_feature = num_options_per_feature

    def show_cards(self, cards: Iterable[Card]):
        raise NotImplementedError()

    def remove_cards(self, cards: Iterable[Card]):
        raise NotImplementedError()

    def calc_sets(self) -> List[CardSet]:
        raise NotImplementedError()


class BruteForcePlayer(BasePlayer):
    def __init__(self, num_options_per_feature: int):
        super().__init__(num_options_per_feature)

        self.open_cards = []

    def show_cards(self, cards: Iterable[Card]):
        self.open_cards.extend(cards)

    def remove_cards(self, cards: Iterable[Card]):
        for c in cards:
            self.open_cards.remove(c)

    def calc_sets(self):
        possible_sets = filter(lambda x: x.is_valid(),
                               map(CardSet, combinations(self.open_cards,
                                                         self.num_options_per_feature)))
        return list(possible_sets)


class Game(object):
    def __init__(self, num_features: int, num_options_per_feature: int):
        self.num_features = num_features
        self.num_options_per_feature = num_options_per_feature

        self.deck = Deck(num_features, num_options_per_feature)

    def play(self, player: BasePlayer) -> List[CardSet]:
        found_sets = []
        print(f"Game started with a deck of {len(self.deck)} cards.")
        while True:
            next_card = self.deck.next_card()
            if next_card is None:
                break
            print(f"Showing new card {next_card}.")
            player.show_cards([next_card])
            sets = player.calc_sets()
            if not len(sets):
                continue
            if len(sets) == 1:
                print(f"Player found set {sets[0]}.")
            else:
                print(f"Player found sets {sets}. Removing first found set.")
            found_sets.append(sets[0])
            player.remove_cards(sets[0].cards)

        print("Game finished!")
        return found_sets


if __name__ == '__main__':
    g = Game(num_features=4, num_options_per_feature=3)
    g.play(BruteForcePlayer(num_options_per_feature=3))
