import random

COLORS = ["Red", "Green", "Blue", "Yellow"]
VALUES = [str(n) for n in range(0, 10)] + ["Skip", "Reverse", "Draw Two"]
WILD_CARDS = ["Wild", "Wild Draw Four"]

def create_deck():
    deck = []
    for color in COLORS:
        deck += [{"color": color, "value": value} for value in VALUES for _ in (0,1)]
    deck += [{"color": None, "value": wc} for wc in WILD_CARDS for _ in range(4)]
    random.shuffle(deck)
    return deck

def draw_card(deck, hand, num=1):
    for _ in range(num):
        if deck:
            hand.append(deck.pop())
        else:
            print("Deck is empty!")

def can_play(card, top_card):
    return (card["color"] == top_card["color"] or
            card["value"] == top_card["value"] or
            card["color"] is None)

def display_hand(hand):
    for idx, card in enumerate(hand):
        color = card["color"] if card["color"] else "Any"
        print(f"{idx}: {color} {card['value']}")

def uno_game(num_players=2):
    deck = create_deck()
    hands = [[] for _ in range(num_players)]
    for hand in hands:
        draw_card(deck, hand, 7)

    discard = [deck.pop()]
    direction = 1
    current = 0
    skip = 0

    while True:
        if skip:
            skip -= 1
            print(f"Player {current+1} is skipped!")
        else:
            print(f"\nPlayer {current+1}'s turn. Top card: {discard[-1]['color']} {discard[-1]['value']}")
            display_hand(hands[current])

            playable = [can_play(card, discard[-1]) for card in hands[current]]
            if any(playable):
                idx = int(input("Choose a card to play (index): "))
                if not playable[idx]:
                    print("You can't play that card!")
                    continue
                card = hands[current].pop(idx)
                discard.append(card)

                # Handle special cards
                if card["value"] == "Skip":
                    skip = 1
                elif card["value"] == "Reverse":
                    direction *= -1
                elif card["value"] == "Draw Two":
                    next_player = (current + direction) % num_players
                    draw_card(deck, hands[next_player], 2)
                    skip = 1
                elif card["value"] == "Wild":
                    color = input("Choose color (Red/Green/Blue/Yellow): ")
                    discard[-1]["color"] = color
                elif card["value"] == "Wild Draw Four":
                    color = input("Choose color (Red/Green/Blue/Yellow): ")
                    discard[-1]["color"] = color
                    next_player = (current + direction) % num_players
                    draw_card(deck, hands[next_player], 4)
                    skip = 1

                if len(hands[current]) == 1:
                    print("UNO!")
                if len(hands[current]) == 0:
                    print(f"Player {current+1} wins!")
                    break
            else:
                print("No playable card, drawing...")
                draw_card(deck, hands[current])

        current = (current + direction) % num_players

if __name__ == "__main__":
    num = int(input("Enter number of players (2+): "))
    uno_game(num)