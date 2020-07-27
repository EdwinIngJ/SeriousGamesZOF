import uuid
import json
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAY_TYPE import PLAY_TYPE
from stable_baselines import A2C


class ZGame:
    """
    RL Algorithm: A2C, pretrained in RUN_RL_Training.py
    Original paper: https://arxiv.org/abs/1602.01783
    OpenAI blog post: https://openai.com/blog/baselines-acktr-a2c/
    https://stable-baselines.readthedocs.io/en/master/modules/a2c.html
    """
    def __init__(self, model_filename, data_log_file='data_log.json'):
        self.ENV_NAME = 'ZGame-v0'
        self.DATA_LOG_FILE_NAME = data_log_file
        self.MODEL_FILENAME = model_filename
        self.GAME_ID = uuid.uuid4()
        self.env = None
        self.current_actions = []
        self.turn = 0
        self.max_turns = 14
        # Learning Parameters
        self._verbosity = 1
        self.model = None
        # Always do these actions upon start
        self._setup()

    def _setup(self):
        # Game parameters
        self.env = gym.make(self.ENV_NAME)
        self.env.play_type = PLAY_TYPE.MACHINE
        self.env.render_mode = 'human-nogui'
        self.env.MAX_TURNS = self.max_turns
        self.model = A2C.load(self.MODEL_FILENAME)
        self.env.reset()
        # Report success
        print('Created new environment {0} with GameID: {1}'.format(self.ENV_NAME, self.GAME_ID))

    def done(self):
        print("Episode finished after {} turns".format(self.turn))
        self._cleanup()

    def _cleanup(self):
        self.env.close()

    def _print_actions(self, actions):
        decoded_actions = self.env.decode_raw_action(actions)
        action_1 = decoded_actions[0]
        action_2 = decoded_actions[1]
        print('Action 1: Location - {0}, Deployment - {1}'.format(action_1[0].name, action_1[1].name))
        print('Action 2: Location - {0}, Deployment - {1}'.format(action_2[0].name, action_2[1].name))

    def run(self):
        print('Starting new game with machine play!')
        observation = self.env.reset()
        self.env.render(mode='human-nogui')
        for turn in range(self.max_turns):
            actions, _states = self.model.predict(observation)
            observation, reward, done, info = self.env.step(actions)
            self.env.render(mode='human-nogui')
            self._print_actions(actions)
            print(info)
            # Write action and stuff out to disk.
            data_to_log = {
                'game_id': str(self.GAME_ID),
                'step': self.turn,
                'actions': actions.tolist(),
                'reward': int(reward),
                'game_done': done,
                'game_info': {k.replace('.', '_'): v for (k, v) in info.items()},
                'raw_state': observation.tolist()
            }
            with open(self.DATA_LOG_FILE_NAME, 'a') as f_:
                f_.write(json.dumps(data_to_log) + '\n')

            # Update counter
            self.turn += 1

            print('Continue? y/n')
            is_continue = input()
            if is_continue is not 'y':
                done = True

            if done:
                self.done()
                break
