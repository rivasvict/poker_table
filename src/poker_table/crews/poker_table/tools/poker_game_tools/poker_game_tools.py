import json
from typing import List, Literal, Tuple
from pydantic import BaseModel

from poker_table.crews.poker_table.tools.poker_game_tools.model import Card, GameState

FLOP_NUMBER_OF_CARDS = 3
TURN_NUMBER_OF_CARDS = 1
RIVER_NUMBER_OF_CARDS = 1

default_game_state: GameState = GameState(
    gameId='123456',
    timestamp='2024-03-20T15:30:00Z',
    potAmount=0,
    communityCards=[],
    currentBet=0,
    roundHistory=[],
    gameStatus='IN_PROGRESS',
    currentRound='FLOP'
)

class PokerGameFunctions(BaseModel):
    game_state: GameState = None

    def set_game(self, game_state) -> GameState:
        """Initialize PokemonGameFunctions with a new GameState"""
        # self.game_state = game_state if game_state is not None else default_game_state
        self.game_state = game_state

        """
        Deals cards to players and sets community cards.
        """

        # Deal 2 cards to each active player
        card_index = 0
        for player in self.game_state.players:
            player.cards = [self.game_state.currentFullDeckOfCards[card_index], self.game_state.currentFullDeckOfCards[card_index + 1]]
            card_index += 2
        # Remove the cards that were dealt to the players
        self.game_state.currentFullDeckOfCards = self.game_state.currentFullDeckOfCards[card_index + 1:]
        
        # Set community cards based on current round
        self.game_state.communityCards = self.game_state.currentFullDeckOfCards[:FLOP_NUMBER_OF_CARDS]

        # Remove the cards that were used for the community cards
        self.game_state.currentFullDeckOfCards = self.game_state.currentFullDeckOfCards[FLOP_NUMBER_OF_CARDS:]
        
        # Save the game state to a json file
        print('Saving game state to json file')
        self.update_game_state(self.game_state, storage_type='local')
        
        return self.game_state

    def set_turn_round(self) -> Tuple[List[Card], Literal["TURN"]]:
        game_state = self.get_game_state(storage_type='local')
        return self.set_round(game_state, "TURN")

    def set_river_round(self) -> Tuple[List[Card], Literal["RIVER"]]:
        game_state = self.get_game_state()
        return self.set_round(game_state, "RIVER")

    def set_round(self, game_state: GameState, round: Literal["FLOP", "TURN", "RIVER"]) -> Tuple[List[Card], Literal["TURN", "RIVER"]]:
        # Get the number of cards to add based on the round
        cards_to_add = TURN_NUMBER_OF_CARDS if round == "TURN" else RIVER_NUMBER_OF_CARDS
        
        # Add new cards to existing community cards
        new_cards = game_state.currentFullDeckOfCards[:cards_to_add]
        game_state.communityCards.extend(new_cards)

        # Remove the cards that were used for the community cards
        game_state.currentFullDeckOfCards = game_state.currentFullDeckOfCards[cards_to_add:]

        # Set the current round
        game_state.currentRound = round

        # Save the game state to a json file
        print('Saving game state to json file')
        self.update_game_state(game_state)

        return game_state.communityCards, game_state.currentRound

    def get_current_round(self) -> Literal["FLOP", "TURN", "RIVER"]:
        game_state = self.get_game_state()
        return game_state.currentRound

    def get_game_state(self, storage_type: Literal['file', 'local'] = 'local') -> GameState:
        if storage_type == 'local':
            return self.game_state
        else:
            # Read the game state from the json file
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)
                return GameState(**game_state)

    def get_cards_by_player(self, player_id: str) -> str:
        game_state = self.get_game_state()
        for player in game_state.players:
            if player.playerId == player_id:
                return str(player.cards)
        return []

    def get_community_cards(self) -> str:
        game_state = self.get_game_state()
        return str(game_state.communityCards)

    def set_bet(self, player_id: str, amount: int, facial_expression: str) -> str:
        game_state = self.get_game_state()
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
        self.update_game_state(game_state)
        return f"Bet set successfully for player {player_id}: '{amount}' chips with facial expression '{facial_expression}'."

    def update_game_state(self, game_state: GameState, storage_type: Literal['local', 'file'] = 'local') -> GameState:
        if storage_type == 'local':
            self.game_state = game_state
        else:
            with open('game_state.json', 'w') as f:
                json.dump(game_state.model_dump(), f)
        return game_state

    def get_players_and_community_cards(self) -> str:
        game_state = self.get_game_state()
        return f"Players: {game_state.players}\nCommunity Cards: {game_state.communityCards}"

    def get_other_players_facial_expressions(self, player_id: str) -> str:
        game_state = self.get_game_state()
        other_players_expressions = []
        
        for player in game_state.players:
            if player.playerId != player_id:
                other_players_expressions.append(f"{player.playerId}: {player.facialExpression}")
                
        return ", ".join(other_players_expressions)

# test = PokerGameFunctions()
# test.set_game(game_state=default_game_state)
# test.set_turn_round()
# test.set_river_round()
# print(test.model_dump_json(indent=2))
