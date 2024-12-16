from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .tools.set_game_tool import GetCurrentRoundTool, SetBetForPlayer1Tool, SetGameTool, GetPlayer1CardsTool, SetBetForPlayer2Tool, GetPlayer2CardsTool, SetBetForPlayer3Tool, GetPlayer3CardsTool, GetCommunityCardsTool, GetPlayersAndCommunityCardsTool, SetRiverRoundTool, SetTurnRoundTool
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

	# Poker engine
	@agent
	def poker_engine_vision_system(self) -> Agent:
		return Agent(
			config=self.agents_config['poker_engine_vision_system'],
			verbose=True
		)

	@agent
	def poker_engine_prefrontal_cortex_system(self) -> Agent:
		return Agent(
			config=self.agents_config['poker_engine_prefrontal_cortex_system'],
			verbose=True
		)

	@agent
	def poker_engine_limbic_system(self) -> Agent:
		return Agent(
			config=self.agents_config['poker_engine_limbic_system'],
			verbose=True
		)

	# End of poker engine

	@task
	def set_game_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_game_task'],
			tools=[SetGameTool()]
		)

	def check_cards(self, player_id, task_config_key) -> Task:
		get_player_card_tools = {
			"player_1": GetPlayer1CardsTool,
			"player_2": GetPlayer2CardsTool,
			"player_3": GetPlayer3CardsTool,
		}

		GetPlayerCardsTool = get_player_card_tools[player_id]
		return Task(
			config=self.tasks_config[task_config_key],
			tools=[GetPlayerCardsTool(), GetCommunityCardsTool()]
		)

	@task
	def player_1_check_cards_task(self) -> Task:
		return self.check_cards(player_id='player_1', task_config_key='player_1_check_cards_task')

	def bet(self, player_id, task_config_key) -> Task:
		bet_tools = {
			'player_1': SetBetForPlayer1Tool,
			'player_2': SetBetForPlayer2Tool, 
			'player_3': SetBetForPlayer3Tool
		}
		SetBetForPlayerTool = bet_tools[player_id]
		return Task(
			config=self.tasks_config[task_config_key],
			# TODO: Add a tool for player to be able to see the players' facial expressions
			tools=[SetBetForPlayerTool()]
		)

	@task
	def player_1_bet_task(self) -> Task:
		return self.bet(player_id='player_1', task_config_key='player_1_bet_task')

	# Poker engine tasks
	@task
	def poker_engine_vision_system_gather_information_task(self) -> Task:
		return Task(
			config=self.tasks_config['poker_engine_vision_system_gather_information_task'],
			# TODO: Add a tool for player to be able to see the players' facial expressions
			tools=[GetPlayer2CardsTool(), GetCommunityCardsTool()]
		)

	@task
	def poker_engine_prefrontal_cortex_system_decide_best_objective_bet_task(self) -> Task:
		return Task(
			config=self.tasks_config['poker_engine_prefrontal_cortex_system_decide_best_objective_bet_task'],
			tools=[]
		)

	@task
	def poker_engine_limbic_system_bet_task(self) -> Task:
		return self.bet(player_id='player_2', task_config_key='poker_engine_limbic_system_bet_task')

	# End of poker engine tasks

	# @task
	# def player_2_check_cards_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['player_2_check_cards_task'],
	# 		tools=[GetPlayer2CardsTool(), GetCommunityCardsTool()]
	# 	)

	# @task
	# def player_2_bet_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['player_2_bet_task'],
	# 		# TODO: Add a tool for player to be able to see the players' facial expressions
	# 		tools=[SetBetForPlayer2Tool()]
	# 	)

	@task
	def player_3_check_cards_task(self) -> Task:
		return Task(
			config=self.tasks_config['player_3_check_cards_task'],
			tools=[GetPlayer3CardsTool(), GetCommunityCardsTool()]
		)

	@task
	def player_3_bet_task(self) -> Task:
		return self.bet(player_id='player_3', task_config_key='player_3_bet_task')

	@task
	def set_turn_round_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_turn_round_task'],
			tools=[SetTurnRoundTool()]
		)

	@task
	def player_1_bet_task_on_turn_round(self) -> Task:
		return self.bet(player_id='player_1', task_config_key='player_1_bet_task')

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
