import json
import uuid
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAY_TYPE import PLAY_TYPE
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS


class ZGame:

    def __init__(self, data_log_file='data_log.json'):
        self.ENV_NAME = 'ZGame-v0'
        self.DATA_LOG_FILE_NAME = data_log_file
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

    def run(self):
        print('Starting new game with human play!')
        self.env.reset()
        self.env.render(mode='human')
        for turn in range(self.max_turns):
            self.env.print_player_action_selections()
                                                       
            print('Input Action - Location 1:')
            location_1 = input()
            while not(location_1.isdigit()) or int(location_1) not in range(0,len(LOCATIONS)):
                print('Location must be a value between 0-'+str(len(LOCATIONS)-1)+'. Please enter a valid location.')
                location_1 = input()
            location_1 = int(location_1)
            
            print('Input Action - Deployment 1:')
            deployment_1 = input()
            while not(deployment_1.isdigit()) or int(deployment_1) not in range(0,len(DEPLOYMENTS)):
                print('Deployment must be a value between 0-'+str(len(DEPLOYMENTS)-1)+'. Please enter a valid deployment number:')
                deployment_1 = input()
            deployment_1 = int(deployment_1)
            
            print('Input Action - Location 2:')
            location_2 = input()
            while not(location_2.isdigit()) or int(location_2) not in range(0,len(LOCATIONS)):
                print('Location must be a value between 0-'+str(len(LOCATIONS)-1)+'. Please enter a valid location:')
                location_2 = input()
            location_2 = int(location_2)
            
            print('Input Action - Deployment 2:')
            deployment_2 = input()
            while not(deployment_2.isdigit()) or int(deployment_2) not in range(0,len(DEPLOYMENTS)):
                print('Deployment must be a value between 0-'+str(len(DEPLOYMENTS)-1)+'. Please enter a valid deployment number:')
                deployment_2 = input()
            deployment_2 = int(deployment_2)
                
            actions = self.env.encode_raw_action(location_1=LOCATIONS(location_1),
                                                 deployment_1=DEPLOYMENTS(deployment_1),
                                                 location_2=LOCATIONS(location_2),
                                                 deployment_2=DEPLOYMENTS(deployment_2))
            observation, reward, done, info = self.env.step(actions)
            print(info)
            self.env.render(mode='human')

            # Write action and stuff out to disk.
            data_to_log = {
                'game_id': str(self.GAME_ID),
                'step': self.turn,
                'actions': actions,
                'reward': reward,
                'game_done': done,
                'game_info': {k.replace('.', '_'): v for (k, v) in info.items()},
                'raw_state': observation
            }
            with open(self.DATA_LOG_FILE_NAME, 'a') as f_:
                f_.write(json.dumps(data_to_log) + '\n')

            # Update counter
            self.turn += 1
            if done:
                self.done()
                break
