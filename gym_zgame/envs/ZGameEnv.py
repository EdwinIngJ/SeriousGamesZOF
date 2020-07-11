import gym
from gym import spaces
import math
from gym_zgame.envs.enums import PLAY_TYPE
from gym_zgame.envs.model.City import City
from gym_zgame.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, LOCATIONS
from gym_zgame.envs.Print_Colors.PColor import PBack, PFore, PFont


class ZGame(gym.Env):

    def __init__(self):
        # Tunable parameters
        self.developer_mode = False # Defaults only, set in main classes
        self.play_type = PLAY_TYPE.MACHINE  
        self.render_mode = 'machine'
        # CONSTANTS
        self.MAX_TURNS = 14
        # Main parameters
        self.city = City(developer_mode=self.developer_mode)
        self.total_score = 0
        self.turn = 0
        self.done = False
        # Defining spaces
        self._num_locations = len(LOCATIONS)
        self._num_deployments = len(DEPLOYMENTS)
        self._num_actions = self._num_locations * self._num_deployments
        self.action_space = spaces.MultiDiscrete([self._num_actions, self._num_actions])
        self.observation_space = spaces.Box(low=0, high=200, shape=(10, 6 + (self.MAX_TURNS * 2)), dtype='uint8')
        self.reset()

    def reset(self):
        self.city = City(developer_mode=self.developer_mode)
        self.total_score = 0
        self.turn = 0
        self.done = False
        self._num_locations = len(LOCATIONS)
        self._num_deployments = len(DEPLOYMENTS)
        self._num_actions = self._num_locations * self._num_deployments
        self.action_space = spaces.MultiDiscrete([self._num_actions, self._num_actions])
        self.observation_space = spaces.Box(low=0, high=200, shape=(10, 6 + (self.MAX_TURNS * 2)), dtype='uint8')
        obs = self.get_obs()
        return obs

    def step(self, actions):
        # Convert actions
        formatted_actions = self.decode_raw_action(actions=actions)
        # Adjudicate turn
        score, done = self._do_turn(formatted_actions)
        # Update score and turn counters
        self.total_score += score
        self.turn += 1
        # Check if done
        if done or (self.turn >= self.MAX_TURNS):
            self.done = True
        # Report out basic information for step
        obs = self.get_obs()
        info = {'turn': self.turn, 'step_reward': score, 'total_reward': self.total_score}
        return obs, self.total_score, self.done, info

    def _do_turn(self, actions):
        score, done = self.city.do_turn(actions=actions)
        return score, done

    def get_obs(self):
        if self.play_type == PLAY_TYPE.HUMAN:
            return self.city.human_encode()
        elif self.play_type == PLAY_TYPE.MACHINE:
            return self.city.rl_encode()
        else:
            raise ValueError('Failed to find acceptable play type.')

    def render(self, mode='human'):
        if self.render_mode == 'human' or mode == 'human':
            return self.city.human_render()
        elif self.render_mode == 'machine' or mode == 'machine':
            return self.city.rl_render()
        else:
            raise ValueError('Failed to find acceptable play type.')

    @staticmethod
    def encode_raw_action(location_1, deployment_1, location_2=None, deployment_2=None):
        # Takes in locations and deployments and converts it to a pair of ints that matches the action space def
        # Think of it as a 2d array where rows are locations and columns are deployments
        # Then, the 2d array is unwrapped into a 1d array where the 2nd row starts right after the first
        action_1 = location_1.value * len(DEPLOYMENTS) + deployment_1.value
        action_2 = location_2.value * len(DEPLOYMENTS) + deployment_2.value
        return [action_1, action_2]

    @staticmethod
    def decode_raw_action(actions):
        # Reverse process of the encoding, takes in a list of raw actions and returns a list of model ready actions
        # Modular arithmetic to the rescue
        readable_actions = []
        for action in actions:
            location_int = action // len(DEPLOYMENTS)  # gets the quotient
            deployment_int = action % len(DEPLOYMENTS)  # gets the remainder
            readable_actions.append([LOCATIONS(location_int), DEPLOYMENTS(deployment_int)])
        return readable_actions

    @staticmethod
    def print_player_action_selections():
        # Build up console output
        fbuffer = '********************************************************************************************'
        ebuffer = '********************************************************************************************'
        player_action_string = PBack.green + fbuffer + PBack.reset + '\n'
        player_action_string += PBack.green + '**||' + PBack.reset + \
                                PBack.orange + ' LOCATIONS'.ljust(13) + PBack.reset + \
                                PBack.green + '||' + PBack.reset + \
                                PBack.orange + ' DEPLOYEMENTS'.ljust(69) + PBack.reset + \
                                PBack.green + '||**' + PBack.reset + '\n'

        num_locations = len(LOCATIONS)
        num_deployments = len(DEPLOYMENTS)
        num_rows = math.ceil(num_deployments / 2)
        col_width = 13
        for i in range(num_rows):
            loc_val = LOCATIONS(i).value if i < num_locations else '--'
            loc_name = LOCATIONS(i).name if i < num_locations else '--'
            dep1_val = DEPLOYMENTS(i).value if i < num_deployments else '--'
            dep1_name = DEPLOYMENTS(i).name if i < num_deployments else '--'
            dep2_val = DEPLOYMENTS(i + num_rows).value if (i + num_rows) < num_deployments else '--'
            dep2_name = DEPLOYMENTS(i + num_rows).name if (i + num_rows) < num_deployments else '--'
            pair_1 = ' {0} - {1}'.format(loc_val, loc_name)
            pair_2 = ' {0} - {1}'.format(dep1_val, dep1_name)
            pair_3 = ' {0} - {1}'.format(dep2_val, dep2_name)
            player_action_string += PBack.green + '**||' + PBack.reset + \
                                    pair_1.ljust(col_width) + \
                                    PBack.green + '||' + PBack.reset + \
                                    pair_2.ljust(col_width + 18) + \
                                    PBack.green + '||' + PBack.reset + \
                                    pair_3.ljust(col_width + 23) + \
                                    PBack.green + '||**' + PBack.reset + '\n'

        player_action_string += PBack.green + ebuffer + PBack.reset
        print(player_action_string)
        return player_action_string
