from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from poker_table.tools.poker_game_tools.poker_game_tools import PokerGameFunctions, GameState


class SetGameInput(BaseModel):
    """Input schema for SetGame."""
    # game_state: GameState = Field(..., description="The game state to set.")

class SetGameTool(BaseTool):
    name: str = "setGame"
    description: str = (
        "Set the game state to the given game state."
    )
    args_schema: Type[BaseModel] = SetGameInput

    def _run(self) -> str:
        # Implementation goes here
        game_state = GameState(gameId='123456', timestamp='2024-03-20T15:30:00Z', potAmount=0, communityCards=[], currentBet=0, roundHistory=[], gameStatus='IN_PROGRESS')
        print(game_state.model_dump_json(indent=2))
        PokerGameFunctions.set_game(game_state)
        return "Game state set successfully."

# set_game_tool = SetGameTool()

class GetPlayer1CardsInput(BaseModel):
    """Input schema for GetPlayerCards."""
    # player_id: str = Field(..., description="The id of the player.")

class GetPlayer1CardsTool(BaseTool):
    name: str = "getPlayer1Cards"
    description: str = (
        "Get the cards of the player 1."
    )
    args_schema: Type[BaseModel] = GetPlayer1CardsInput

    def _run(self) -> str:
        cards = PokerGameFunctions.get_cards_by_player(player_id='player_1')
        return cards;

class SetBetForPlayer1Input(BaseModel):
    """Input schema for SetBetForPlayer1."""
    amount: int = Field(..., description="The amount of the bet.")
    facial_expression: str = Field(..., description="The facial expression of the player.")

class SetBetForPlayer1Tool(BaseTool):
    name: str = "setBetForPlayer1"
    description: str = (
        "Set the bet of the player_1."
    )
    args_schema: Type[BaseModel] = SetBetForPlayer1Input

    def _run(self, amount: int, facial_expression: str) -> str:
        return PokerGameFunctions.set_bet(player_id="player_1", amount=amount, facial_expression=facial_expression)

class GetPlayer2CardsInput(BaseModel):
    """Input schema for GetPlayerCards."""
    # player_id: str = Field(..., description="The id of the player.")

class GetPlayer2CardsTool(BaseTool):
    name: str = "getPlayer2Cards"
    description: str = (
        "Get the cards of the player 2."
    )
    args_schema: Type[BaseModel] = GetPlayer2CardsInput

    def _run(self) -> str:
        cards = PokerGameFunctions.get_cards_by_player(player_id='player_2')
        return cards;

class SetBetForPlayer2Input(BaseModel):
    """Input schema for SetBetForPlayer2."""
    amount: int = Field(..., description="The amount of the bet.")
    facial_expression: str = Field(..., description="The facial expression of the player.")

class SetBetForPlayer2Tool(BaseTool):
    name: str = "setBetForPlayer2"
    description: str = (
        "Set the bet of the player_2."
    )
    args_schema: Type[BaseModel] = SetBetForPlayer2Input

    def _run(self, amount: int, facial_expression: str) -> str:
        return PokerGameFunctions.set_bet(player_id="player_2", amount=amount, facial_expression=facial_expression)

class GetPlayer3CardsInput(BaseModel):
    """Input schema for GetPlayerCards."""
    # player_id: str = Field(..., description="The id of the player.")

class GetPlayer3CardsTool(BaseTool):
    name: str = "getPlayer3Cards"
    description: str = (
        "Get the cards of the player 3."
    )
    args_schema: Type[BaseModel] = GetPlayer3CardsInput

    def _run(self) -> str:
        cards = PokerGameFunctions.get_cards_by_player(player_id='player_3')
        return cards;

class SetBetForPlayer3Input(BaseModel):
    """Input schema for SetBetForPlayer3."""
    amount: int = Field(..., description="The amount of the bet.")
    facial_expression: str = Field(..., description="The facial expression of the player.")

class SetBetForPlayer3Tool(BaseTool):
    name: str = "setBetForPlayer3"
    description: str = (
        "Set the bet of the player_3."
    )
    args_schema: Type[BaseModel] = SetBetForPlayer3Input

    def _run(self, amount: int, facial_expression: str) -> str:
        return PokerGameFunctions.set_bet(player_id="player_3", amount=amount, facial_expression=facial_expression)

class GetCommunityCardsInput(BaseModel):
    """Input schema for GetCommunityCards."""
    # player_id: str = Field(..., description="The id of the player.")

class GetCommunityCardsTool(BaseTool):
    name: str = "getCommunityCards"
    description: str = (
        "Get the community cards."
    )
    args_schema: Type[BaseModel] = GetCommunityCardsInput

    def _run(self) -> str:
        return PokerGameFunctions.get_community_cards()

class GetPlayersAndCommunityCardsInput(BaseModel):
    """Input schema for GetPlayersAndCommunityCards."""
    # player_id: str = Field(..., description="The id of the player.")

class GetPlayersAndCommunityCardsTool(BaseTool):
    name: str = "getPlayersAndCommunityCards"
    description: str = (
        "Get the players and the community cards."
    )
    args_schema: Type[BaseModel] = GetPlayersAndCommunityCardsInput

    def _run(self) -> str:
        return PokerGameFunctions.get_players_and_community_cards()