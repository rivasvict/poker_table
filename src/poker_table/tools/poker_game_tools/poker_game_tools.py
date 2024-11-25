import json
from typing import Dict, List, Any, Literal, Optional, Tuple
import random
from pydantic import BaseModel

# Game state type definitions
class Card(BaseModel):
    suit: Literal["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
    value: Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

class Action(BaseModel):
    playerId: str
    action: Literal["RAISE", "CALL", "FOLD"]
    amount: int
class Player(BaseModel):
    playerId: str
    name: str 
    chips: int
    currentBet: int
    facialExpression: str
    cards: List[Card]
    action: Optional[Literal["RAISE", "CALL", "FOLD"]]

class RoundHistory(BaseModel):
    round: Literal["FLOP", "TURN", "RIVER"]
    actions: List[Action]

class GameState(BaseModel):
    gameId: str
    timestamp: str
    potAmount: int
    currentFullDeckOfCards: List[Card] = random.sample(
        [
            Card(suit=suit, value=value)
            for suit in ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]
            for value in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        ],
        k=52
    )
    communityCards: List[Card]
    currentBet: int
    players: List[Player] = [
        Player(
            playerId="player_1",
            name="PLayer 1",
            chips=1000,
            currentBet=0,
            facialExpression="neutral",
            cards=[],
            action=None
        ),
        Player(
            playerId="player_2", 
            name="Player 2",
            chips=1000,
            currentBet=0,
            facialExpression="neutral",
            cards=[],
            action=None
        ),
        Player(
            playerId="player_3",
            name="Player 3",
            chips=1000,
            currentBet=0,
            facialExpression="neutral", 
            cards=[],
            action=None
        )
    ]
    roundHistory: List[RoundHistory]
    gameStatus: Literal["IN_PROGRESS", "COMPLETED"]
    currentRound: Literal["FLOP", "TURN", "RIVER"]

FLOP_NUMBER_OF_CARDS = 3
TURN_NUMBER_OF_CARDS = 1
RIVER_NUMBER_OF_CARDS = 1
class PokerGameFunctions:

    @staticmethod
    def set_game(game_state: GameState) -> GameState:
        """
        Deals cards to players and sets community cards.
        """
        # Create a deck
        deck = game_state.currentFullDeckOfCards
        
        # Deal 2 cards to each active player
        card_index = 0
        for player in game_state.players:
            player.cards = [game_state.currentFullDeckOfCards[card_index], game_state.currentFullDeckOfCards[card_index + 1]]
            card_index += 2
        # Remove the cards that were dealt to the players
        game_state.currentFullDeckOfCards = game_state.currentFullDeckOfCards[card_index + 1:]
        
        # Set community cards based on current round
        game_state.communityCards = game_state.currentFullDeckOfCards[:FLOP_NUMBER_OF_CARDS]

        # Remove the cards that were used for the community cards
        game_state.currentFullDeckOfCards = game_state.currentFullDeckOfCards[FLOP_NUMBER_OF_CARDS:]
        
        # Save the game state to a json file
        print('Saving game state to json file')
        PokerGameFunctions.update_game_state(game_state)
        
        return game_state

    @staticmethod
    def set_turn_round() -> Tuple[List[Card], Literal["TURN"]]:
        game_state = PokerGameFunctions.get_game_state()
        return PokerGameFunctions.set_round(game_state, "TURN")

    @staticmethod
    def set_river_round() -> Tuple[List[Card], Literal["RIVER"]]:
        game_state = PokerGameFunctions.get_game_state()
        return PokerGameFunctions.set_round(game_state, "RIVER")

    @staticmethod
    def set_round(game_state: GameState, round: Literal["FLOP", "TURN", "RIVER"]) -> Tuple[List[Card], Literal["TURN", "RIVER"]]:
        # Get the number of cards to add based on the round
        cards_to_add = TURN_NUMBER_OF_CARDS if round == "TURN" else RIVER_NUMBER_OF_CARDS
        
        # Add new cards to existing community cards
        new_cards = game_state.currentFullDeckOfCards[:cards_to_add]
        game_state.communityCards.extend(new_cards)

        # Remove the cards that were used for the community cards
        game_state.currentFullDeckOfCards = game_state.currentFullDeckOfCards[cards_to_add:]

        # Set the current round
        game_state.currentRound = round

        return game_state.communityCards, game_state.currentRound

    @staticmethod
    def get_current_round() -> Literal["FLOP", "TURN", "RIVER"]:
        game_state = PokerGameFunctions.get_game_state()
        return game_state.currentRound

    @staticmethod
    def get_game_state() -> GameState:
        # Read the game state from the json file
        with open('game_state.json', 'r') as f:
            game_state = json.load(f)
        return GameState(**game_state)

    @staticmethod
    def get_cards_by_player(player_id: str) -> str:
        game_state = PokerGameFunctions.get_game_state()
        for player in game_state.players:
            if player.playerId == player_id:
                return str(player.cards)
        return []

    @staticmethod
    def get_community_cards() -> str:
        game_state = PokerGameFunctions.get_game_state()
        return str(game_state.communityCards)

    @staticmethod
    def set_bet(player_id: str, amount: int, facial_expression: str) -> str:
        game_state = PokerGameFunctions.get_game_state()
        for player in game_state.players:
            if player.playerId == player_id:
                # Raise case
                if game_state.currentBet < amount:
                    game_state.currentBet = amount
                    player.facialExpression = facial_expression
                    player.chips -= amount
                    game_state.potAmount += amount
                    player.action = "RAISE"
                # Call case
                elif game_state.currentBet == amount:
                    player.facialExpression = facial_expression
                    player.chips -= amount
                    game_state.potAmount += amount
                    player.action = "CALL"
                # Fold case
                else:
                    player.cards = []
                    player.action = "FOLD"
                    return f"Bet not set successfully for player {player_id}. folded."
            
        # Update the game state file
        PokerGameFunctions.update_game_state(game_state)
        return f"Bet set successfully for player {player_id}: '{amount}' chips with facial expression '{facial_expression}'."

    @staticmethod
    def update_game_state(game_state: GameState) -> GameState:
        with open('game_state.json', 'w') as f:
            json.dump(game_state.model_dump(), f)
        return game_state

    @staticmethod
    def get_players_and_community_cards() -> str:
        game_state = PokerGameFunctions.get_game_state()
        return f"Players: {game_state.players}\nCommunity Cards: {game_state.communityCards}"
# game_state = GameState(gameId='123456', timestamp='2024-03-20T15:30:00Z', potAmount=1500, communityCards=[], currentBet=200, roundHistory=[], gameStatus='IN_PROGRESS')
# print(PokerGameFunctions.get_cards_by_player('player_1'))
# print(game_state.model_dump_json(indent=2))
# PokerGameFunctions.set_game(game_state)
# print("------------------------")
# print("Community Cards:")
# print(game_state.currentFullDeckOfCards)
# print("------------------------")
# print(game_state.communityCards)
# print("------------------------")
# print(PokerGameFunctions.get_cards_by_player(game_state, 'player_2'))
# print("------------------------")
# print(game_state.model_dump_json(indent=2))
