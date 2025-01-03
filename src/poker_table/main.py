#!/usr/bin/env python

from .crews.poker_table import PokerTable
from crewai.flow.flow import start, Flow
from poker_table.crews.poker_table.tools.poker_game_tools.model import GameState

class PokerTableFlow(Flow):
  
  @start()
  def initiate_game(self):
    inputs = {
      'game_state': GameState(
        gameId='123456',
        timestamp='2024-03-20T15:30:00Z',
        potAmount=0,
        communityCards=[],
        currentBet=0,
        roundHistory=[],
        gameStatus='IN_PROGRESS',
        currentRound='FLOP'
      )
    }
    return PokerTable(inputs=inputs).crew().kickoff(inputs=inputs)

def kickoff():
  poker_flow = PokerTableFlow()
  poker_flow.kickoff()

if __name__ == "__main__":
  kickoff()