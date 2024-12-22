from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .tools.set_game_tool import GetCurrentRoundTool, GetOtherPlayersFacialExpressionForPlayer1Tool, GetOtherPlayersFacialExpressionForPlayer2Tool, GetOtherPlayersFacialExpressionForPlayer3Tool, SetBetForPlayer1Tool, SetGameTool, GetPlayer1CardsTool, SetBetForPlayer2Tool, GetPlayer2CardsTool, SetBetForPlayer3Tool, GetPlayer3CardsTool, GetCommunityCardsTool, GetPlayersAndCommunityCardsTool, SetRiverRoundTool, SetTurnRoundTool
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
			verbose=False
		)

	@agent
	def player_2(self) -> Agent:
		return Agent(
			config=self.agents_config['player_2'],
			verbose=False
		)

	@agent
	def player_3(self) -> Agent:
		return Agent(
			config=self.agents_config['player_3'],
			verbose=False
		)

	# Poker engine
	@agent
	def brain_vision_system(self) -> Agent:
		return Agent(
			config=self.agents_config['brain_vision_system'],
			verbose=True
		)

	@agent
	def brain_pref_cortex(self) -> Agent:
		return Agent(
			config=self.agents_config['brain_pref_cortex'],
			verbose=True
		)

	@agent
	def lymbic_system(self) -> Agent:
		return Agent(
			config=self.agents_config['lymbic_system'],
			verbose=True
		)

	# End of poker engine

	def check_cards_task(self, player_id, task_config_key) -> Task:
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

	def bet_task(self, player_id, task_config_key) -> Task:
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

	def get_other_players_facial_expression(self, player_id, task_config_key) -> Task:
		get_facial_expression_tools = {
			'player_1': GetOtherPlayersFacialExpressionForPlayer1Tool,
			'player_2': GetOtherPlayersFacialExpressionForPlayer2Tool,
			'player_3': GetOtherPlayersFacialExpressionForPlayer3Tool,
		}
		GetOtherPlayersFacialExpressionForPlayerTool = get_facial_expression_tools[player_id]	
		return Task(
			config=self.tasks_config[task_config_key],
			tools=[GetOtherPlayersFacialExpressionForPlayerTool()]
		)

	@task
	def set_game_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_game_task'],
			tools=[SetGameTool()]
		)

	# The '0' at the end of 'player_1_check_cards_task_0' means this is the first turn
	@task
	def player_1_check_cards_task_0(self) -> Task:
		return self.check_cards_task(player_id='player_1', task_config_key='player_1_check_cards_task')

	# The '0' at the end of 'player_1_get_other_players_facial_expression_task_0' means this is the first turn
	@task
	def player_1_get_other_players_facial_expression_task_0(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_1', task_config_key='player_1_get_players_scene')

	# The '0' at the end of 'player_1_bet_task_0' means this is the first turn
	@task
	def player_1_bet_task_0(self) -> Task:
		return self.bet_task(player_id='player_1', task_config_key='player_1_bet_task')

	# Poker engine tasks
	# The '0' at the end of 'gather_visual_information_0' means this is the first turn
	@task
	def gather_visual_information_0(self) -> Task:
		return self.check_cards_task(player_id='player_2', task_config_key='gather_visual_information')

	# The '0' at the end of 'get_players_scene_0' means this is the first turn
	@task
	def get_players_scene_0(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_2', task_config_key='get_players_scene')

	# The '0' at the end of 'analyze_best_play_0' means this is the first turn
	@task
	def analyze_best_play_0(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_best_play'],
			tools=[]
		)

	# The '0' at the end of 'lymbic_system_bet_task_0' means this is the first turn
	@task
	def lymbic_system_bet_task_0(self) -> Task:
		return self.bet_task(player_id='player_2', task_config_key='lymbic_system_bet_task')

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
	def player_3_check_cards_task_0(self) -> Task:
		return self.check_cards_task(player_id='player_3', task_config_key='player_3_check_cards_task')

	# The '0' at the end of 'player_3_get_other_players_facial_expression_task_0' means this is the first turn
	@task
	def player_3_get_other_players_facial_expression_task_0(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_3', task_config_key='player_3_get_players_scene')

	@task
	def player_3_bet_task_0(self) -> Task:
		return self.bet_task(player_id='player_3', task_config_key='player_3_bet_task')

	@task
	def set_turn_round_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_turn_round_task'],
			tools=[SetTurnRoundTool()]
		)

	# The '1' at the end of 'player_1_check_cards_task_1' means this is the first turn
	@task
	def player_1_check_cards_task_1(self) -> Task:
		return self.check_cards_task(player_id='player_1', task_config_key='player_1_check_cards_task')

	# The '1' at the end of 'player_1_get_other_players_facial_expression_task_1' means this is the first turn
	@task
	def player_1_get_other_players_facial_expression_task_1(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_1', task_config_key='player_1_get_players_scene')

	# The '1' at the end of 'player_1_bet_task_1' means this is the first turn
	@task
	def player_1_bet_task_1(self) -> Task:
		return self.bet_task(player_id='player_1', task_config_key='player_1_bet_task')

	# The '1' at the end of 'gather_visual_information_1' means this is the first turn
	@task
	def gather_visual_information_1(self) -> Task:
		return self.check_cards_task(player_id='player_2', task_config_key='gather_visual_information')

	# The '1' at the end of 'get_players_scene_1' means this is the first turn
	@task
	def get_players_scene_1(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_2', task_config_key='get_players_scene')

	# The '1' at the end of 'analyze_best_play_1' means this is the first turn
	@task
	def analyze_best_play_1(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_best_play'],
			tools=[]
		)

	# The '1' at the end of 'lymbic_system_bet_task_1' means this is the first turn
	@task
	def lymbic_system_bet_task_1(self) -> Task:
		return self.bet_task(player_id='player_2', task_config_key='lymbic_system_bet_task')

	# The '1' at the end of 'player_3_check_cards_task_1' means this is the first turn
	@task
	def player_3_check_cards_task_1(self) -> Task:
		return self.check_cards_task(player_id='player_3', task_config_key='player_3_check_cards_task')

	# The '1' at the end of 'player_3_get_other_players_facial_expression_task_1' means this is the first turn
	@task
	def player_3_get_other_players_facial_expression_task_1(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_3', task_config_key='player_3_get_players_scene')

	# The '1' at the end of 'player_3_bet_task_1' means this is the first turn
	@task
	def player_3_bet_task_1(self) -> Task:
		return self.bet_task(player_id='player_3', task_config_key='player_3_bet_task')

	@task
	def set_river_round_task(self) -> Task:
		return Task(
			config=self.tasks_config['set_river_round_task'],
			tools=[SetRiverRoundTool()]
		)

	# The '2' at the end of 'player_1_check_cards_task_2' means this is the first turn
	@task
	def player_1_check_cards_task_2(self) -> Task:
		return self.check_cards_task(player_id='player_1', task_config_key='player_1_check_cards_task')

	# The '2' at the end of 'player_1_get_other_players_facial_expression_task_2' means this is the first turn
	@task
	def player_1_get_other_players_facial_expression_task_2(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_1', task_config_key='player_1_get_players_scene')

	# The '2' at the end of 'player_1_bet_task_2' means this is the first turn
	@task
	def player_1_bet_task_2(self) -> Task:
		return self.bet_task(player_id='player_1', task_config_key='player_1_bet_task')

	# The '2' at the end of 'gather_visual_information_1' means this is the first turn
	@task
	def gather_visual_information_2(self) -> Task:
		return self.check_cards_task(player_id='player_2', task_config_key='gather_visual_information')

	# The '2' at the end of 'get_players_scene_2' means this is the first turn
	@task
	def get_players_scene_2(self) -> Task:
		return self.get_other_players_facial_expression(player_id='player_2', task_config_key='get_players_scene')

	# The '2' at the end of 'analyze_best_play_1' means this is the first turn
	@task
	def analyze_best_play_2(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_best_play'],
			tools=[]
		)

	# The '2' at the end of 'lymbic_system_bet_task_1' means this is the first turn
	@task
	def lymbic_system_bet_task_2(self) -> Task:
		return self.bet_task(player_id='player_2', task_config_key='lymbic_system_bet_task')

	# The '2' at the end of 'player_3_check_cards_task_2' means this is the first turn
	@task
	def player_3_check_cards_task_2(self) -> Task:
		return self.check_cards_task(player_id='player_3', task_config_key='player_3_check_cards_task')

	# The '2' at the end of 'player_3_bet_task_2' means this is the first turn
	@task
	def player_3_bet_task_2(self) -> Task:
		return self.bet_task(player_id='player_3', task_config_key='player_3_bet_task')

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
			verbose=False,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
