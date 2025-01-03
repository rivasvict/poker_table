from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from .poker_game_tools import PokerGameFunctions, GameState

game = PokerGameFunctions()

class SetGameInput(BaseModel):
    """Input schema for SetGame."""
    game_state: GameState = Field(..., description="The game state to be set.")
    # game_state: dict = Field(..., description="The game state to set.")
    # game_state: GameState = Field(..., description="The game state to set.")

class SetGameTool(BaseTool):
    name: str = "setGame"
    description: str = (
        "Set the game state to the given game state."
    )
    args_schema: Type[BaseModel] = SetGameInput

    # def _run(self, game_state: GameState) -> str:
    def _run(self, game_state=GameState) -> str:
        print('---------------------------------')
        print(str(game_state))
        game_state = game.set_game(game_state=game_state)
        print(game_state.model_dump_json(indent=2))
        return "Game state set successfully."

set_game_tool = SetGameTool()

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
        cards = game.get_cards_by_player(player_id='player_1')
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
        return game.set_bet(player_id="player_1", amount=amount, facial_expression=facial_expression)

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
        cards = game.get_cards_by_player(player_id='player_2')
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
        return game.set_bet(player_id="player_2", amount=amount, facial_expression=facial_expression)

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
        cards = game.get_cards_by_player(player_id='player_3')
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
        return game.set_bet(player_id="player_3", amount=amount, facial_expression=facial_expression)

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
        return game.get_community_cards()

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
        return game.get_players_and_community_cards()

class GetCurrentRoundInput(BaseModel):
    """Input schema for GetCurrentRound."""
    # player_id: str = Field(..., description="The id of the player.")

class GetCurrentRoundTool(BaseTool):
    name: str = "getCurrentRound"
    description: str = (
        "Get the current round of the game."
    )
    args_schema: Type[BaseModel] = GetCurrentRoundInput

    def _run(self) -> str:
        return game.get_current_round()

class SetTurnRoundInput(BaseModel):
    """Input schema for SetTurnRound."""
    # player_id: str = Field(..., description="The id of the player.")

class SetTurnRoundTool(BaseTool):
    name: str = "setTurnRound"
    description: str = (
        "Set the turn round of the game."
    )
    args_schema: Type[BaseModel] = SetTurnRoundInput

    def _run(self) -> str:
        return game.set_turn_round()

class SetRiverRoundInput(BaseModel):
    """Input schema for SetRiverRound."""
    # player_id: str = Field(..., description="The id of the player.")

class SetRiverRoundTool(BaseTool):
    name: str = "setRiverRound"
    description: str = (
        "Set the river round of the game."
    )
    args_schema: Type[BaseModel] = SetRiverRoundInput

    def _run(self) -> str:
        return game.set_river_round()

class GetOtherPlayersFacialExpressionForPlayer1Input(BaseModel):
    """Input schema for GetOtherPlayersFacialExpressionForPlayer1"""

class GetOtherPlayersFacialExpressionForPlayer1Tool(BaseTool):
    name: str = "getOtherPLayersFacialExpressionForPlayer1Tool"
    description: str = (
        "Get other players facial expression for player 1"
    )
    args_schema: Type[BaseModel] = GetOtherPlayersFacialExpressionForPlayer1Input

    def _run(self) -> str:
        return game.get_other_players_facial_expressions(player_id="player_1")

class GetOtherPlayersFacialExpressionForPlayer2Input(BaseModel):
    """Input schema for GetOtherPlayersFacialExpressionForPlayer2"""

class GetOtherPlayersFacialExpressionForPlayer2Tool(BaseTool):
    name: str = "getOtherPLayersFacialExpressionForPlayer2Tool"
    description: str = (
        "Get other players facial expression for player 2"
    )
    args_schema: Type[BaseModel] = GetOtherPlayersFacialExpressionForPlayer2Input

    def _run(self) -> str:
        return game.get_other_players_facial_expressions(player_id="player_2")

class GetOtherPlayersFacialExpressionForPlayer3Input(BaseModel):
    """Input schema for GetOtherPlayersFacialExpressionForPlayer3"""

class GetOtherPlayersFacialExpressionForPlayer3Tool(BaseTool):
    name: str = "getOtherPLayersFacialExpressionForPlayer3Tool"
    description: str = (
        "Get other players facial expression for player 3"
    )
    args_schema: Type[BaseModel] = GetOtherPlayersFacialExpressionForPlayer3Input

    def _run(self) -> str:
        return game.get_other_players_facial_expressions(player_id="player_3")