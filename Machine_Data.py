import json
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from gym_zgame.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, LOCATIONS


class Machine_Data_Output:
    def __init__(self, data_log):
        self.data_to_output = pd.DataFrame(pd.read_json(data_log, lines=True))[-1400:]
        self.data_npc_count_to_score = {
            'total_score' : [],
            'fear': [],
            'num_active' : [],
            'num_sickly' : [],
            'num_zombie' : [],
            'num_dead' : [],
            'orig_alive' : [],
            'orig_dead' : []
        }
        self.data_local_fear_to_score = {
            #Local Fears
            'NW' : [],
            'N' : [],
            'NE' : [],
            'W' : [],
            'CENTER' : [],
            'E' : [],
            'SW' : [],
            'S' : [],
            'SE' : [],
            #Score
            'total_score' : []
        }
        self.game_count = 0
        self.parseRawState()

    def nbhDataSum(self, state, state_index):
        return sum([state[i][state_index] for i in range(1,10)])
    
    def addToNPCData(self,keys,values):
        for i in range(len(keys)):
            self.data_npc_count_to_score[keys[i]].append(values[i])

    def addToFearData(self,keys,values):
        for i in range(len(keys)):
            self.data_local_fear_to_score[keys[i]].append(values[i])
            
    def parseRawState(self):
        for state in self.data_to_output['raw_state']:
            if state[0][2] == 14:
                self.game_count += 1
                values = [state[0][5],state[0][0],self.nbhDataSum(state,2),self.nbhDataSum(state,3),self.nbhDataSum(state,4),self.nbhDataSum(state,5),state[0][3],state[0][4]]
                self.addToNPCData(list(self.data_npc_count_to_score.keys()), values)
                values = [state[i][6] for i in range(1,10)] + [state[0][5]]
                self.addToFearData(list(self.data_local_fear_to_score.keys()),values)
                             
    def decode_raw_action(self, actions):
        # Reverse process of the encoding, takes in a list of raw actions and returns a list of model ready actions
        # Modular arithmetic to the rescue
        readable_actions = []
        for action in actions:
            location_int = action // len(DEPLOYMENTS)  # gets the quotient
            deployment_int = action % len(DEPLOYMENTS)  # gets the remainder
            readable_actions.append([LOCATIONS(location_int), DEPLOYMENTS(deployment_int)])
        return readable_actions

    def deployment_usage_graph(self):
        all_actions = self.data_to_output['actions']
        num_deps_used = {}
        for dep in DEPLOYMENTS:
            num_deps_used[dep.name] = 0
        for action_set in all_actions:
            readable_actions = self.decode_raw_action(action_set)
            num_deps_used[readable_actions[0][1].name] += 1
            num_deps_used[readable_actions[1][1].name] += 1
        plt.bar(list(num_deps_used.keys()), list(num_deps_used.values()))
        plt.xlabel("Deployment Name")
        plt.ylabel("Usage")
        plt.title("Deployment Usage")
        plt.xticks(rotation = 90)
        plt.tight_layout()
        plt.show()

    def npc_count_to_score_graph(self):
        x_axis = list(range(1,self.game_count+1))
        plt.plot(x_axis, self.data_npc_count_to_score['total_score'], color = "black", label = "Final Score")
        plt.plot(x_axis, self.data_npc_count_to_score['fear'], color = "red", label = "Global Fear")
        plt.plot(x_axis, self.data_npc_count_to_score['num_active'], color = "cyan", label = "Number of Active")
        plt.plot(x_axis, self.data_npc_count_to_score['num_sickly'], color = "yellow", label = "Number of Sickly")
        plt.plot(x_axis, self.data_npc_count_to_score['num_zombie'], color = "green", label = "Number of Zombies")
        plt.plot(x_axis, self.data_npc_count_to_score['num_dead'], color = "blue", label = "Number of Dead")
        plt.xlabel("Game Number")
        plt.ylabel("Amount")
        plt.title("NPC Counts and Global Fear Compared to Score")
        plt.xticks(rotation = 90)
        plt.tight_layout()
        plt.legend()
        plt.show()

    def local_fear_std_to_score_graph(self):
        keys = list(self.data_local_fear_to_score.keys())
        x_axis = [stat.stdev([self.data_local_fear_to_score[key][i] for key in keys]) for i in range(len(self.data_local_fear_to_score["NW"]))]
        plt.scatter(x_axis, self.data_local_fear_to_score['total_score'])
        plt.xlabel("Standard Deviation between Local Fears")
        plt.ylabel("Final Score")
        plt.title("Effect of Local Fear STD on Final Score")
        plt.xticks(rotation = 90)
        plt.tight_layout()
        plt.show()
        
        
if __name__ == '__main__':
    data_log = "data_log.json"
    data = Machine_Data_Output(data_log)
    data.deployment_usage_graph()
    data.npc_count_to_score_graph()
    data.local_fear_std_to_score_graph()
