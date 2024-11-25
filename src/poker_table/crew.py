from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from poker_table.tools.set_game_tool import GetCurrentRoundTool, SetBetForPlayer1Tool, SetGameTool, GetPlayer1CardsTool, SetBetForPlayer2Tool, GetPlayer2CardsTool, SetBetForPlayer3Tool, GetPlayer3CardsTool, GetCommunityCardsTool, GetPlayersAndCommunityCardsTool, SetRiverRoundTool, SetTurnRoundTool
# Uncomment the following line to use an example of a custom tool
# from poker_table.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class PokerTable():
	"""PokerTable crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def game_master(self) -> Agent:
		return Agent(
			config=self.agents_config['game_master'],
			verbose=True
		)

	@agent
	def player_1(self) -> Agent:
		return Agent(
			config=self.agents_config['player_1'],
			verbose=True
		)

	@agent
	def player_2(self) -> Agent:
		return Agent(
			config=self.agents_config['player_2'],
			verbose=True
		)

	@agent
	def player_3(self) -> Agent:
		return Agent(
			config=self.agents_config['player_3'],
			verbose=True
		)

	@task
	def set_game_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_game_task'],
			tools=[SetGameTool()]
		)

	@task
	def player_1_check_cards_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_1_check_cards_task'],
			tools=[GetPlayer1CardsTool(), GetCommunityCardsTool()]
		)

	@task
	def player_1_bet_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_1_bet_task'],
			# TODO: Add a tool for player to be able to see the players' facial expressions
			tools=[SetBetForPlayer1Tool()]
		)
	
	@task
	def player_2_check_cards_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_2_check_cards_task'],
			tools=[GetPlayer2CardsTool(), GetCommunityCardsTool()]
		)

	@task
	def player_2_bet_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_2_bet_task'],
			# TODO: Add a tool for player to be able to see the players' facial expressions
			tools=[SetBetForPlayer2Tool()]
		)

	@task
	def player_3_check_cards_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_3_check_cards_task'],
			tools=[GetPlayer3CardsTool(), GetCommunityCardsTool()]
		)

	@task
	def player_3_bet_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_3_bet_task'],
			# TODO: Add a tool for player to be able to see the players' facial expressions
			tools=[SetBetForPlayer3Tool(), GetCurrentRoundTool()]
		)

	@task
	def set_turn_round_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_turn_round_task'],
			tools=[SetTurnRoundTool()]
		)

	@task
	def set_river_round_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_river_round_task'],
			tools=[SetRiverRoundTool()]
		)

	@task
	def decide_game_winner_task(self) -> Task:
		return Task(
			config=self.tasks_config['decide_game_winner_task'],
			tools=[GetPlayersAndCommunityCardsTool()]
		)

	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the PokerTable crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
