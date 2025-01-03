from typing import List, Literal, Optional
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
