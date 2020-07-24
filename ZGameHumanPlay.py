import json
import uuid
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAY_TYPE import PLAY_TYPE
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS
from GUI import *

class ZGame:

    def __init__(self, data_log_file='data_log.json', developer_mode = False):
        self.ENV_NAME = 'ZGame-v0'
        self.DATA_LOG_FILE_NAME = data_log_file
        self.DEVELOPER_MODE = developer_mode
        self.GAME_ID = uuid.uuid4()
        self.env = None
        self.current_actions = []
        self.turn = 0
        self.max_turns = 14
        # Always do these actions upon start
        self._setup()

    def _setup(self):
        # Game parameters
        self.env = gym.make(self.ENV_NAME)
        self.env.developer_mode = self.DEVELOPER_MODE
        self.env.play_type = PLAY_TYPE.HUMAN
        self.env.render_mode = 'human'
        self.env.MAX_TURNS = 14
        self.env.reset()
        # Report success
        print('Created new environment {0} with GameID: {1}'.format(self.ENV_NAME, self.GAME_ID))

    def done(self):
        print("Episode finished after {} turns".format(self.turn))
        self._cleanup()

    def _cleanup(self):
        self.env.close()

    def _read_action(self, location_or_deployment, input_number):
        print('Input Action - ' + location_or_deployment.title() + ' ' + input_number + ':')
        user_input = input()
        number_of_locations_or_deployments = len(LOCATIONS) if location_or_deployment == "location" else len(DEPLOYMENTS)
        while not(user_input.isdigit()) or int(user_input) not in range(0, number_of_locations_or_deployments):
            print(location_or_deployment.title() + " must be a value between 0 and " + str(number_of_locations_or_deployments - 1) + ". Please enter a valid " + location_or_deployment + ".")
            user_input = input()
        return int(user_input)
    
    def run(self):
        #Instantiating GUI
        root = Tk()
        user_interface = GUI(root,self)
        root.mainloop()
        
