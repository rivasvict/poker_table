from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from poker_table.tools.set_game_tool import SetBetForPlayer1Tool, SetGameTool, GetPlayer1CardsTool, GetPlayer1CardsInput
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

	@task
	def set_game_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_game_task'],
			tools=[SetGameTool()]
		)

	@task
	def player_1_bet_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_1_bet_task'],
			# TODO: Add a tool for player to be able to see the community cards
			tools=[GetPlayer1CardsTool(), SetBetForPlayer1Tool()]
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
