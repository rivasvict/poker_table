#!/usr/bin/env python

from .crews.poker_table import PokerTable
from crewai.flow.flow import start, Flow

class PokerTableFlow(Flow):
  
  @start()
  def initiate_game(self):
    return PokerTable().crew().kickoff()

def kickoff():
  poker_flow = PokerTableFlow()
  poker_flow.kickoff()

if __name__ == "__main__":
  kickoff()