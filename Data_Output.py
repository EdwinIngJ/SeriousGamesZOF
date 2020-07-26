import json
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from gym_zgame.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, LOCATIONS


class Data_Output:
    def __init__(self, data_log):
        self.data_to_output = pd.DataFrame(pd.read_json(data_log, lines=True))[-1400:]
        self.data_npc_count_to_score = {
            'total_score' : [],
            'fear' : [],
            'num_alive' : [],
            'num_dead' : [],
            'num_ashen' : [],
            'num_human' : [],
            'num_zombie_bitten' : [],
            'num_zombie' : [],
            'num_healthy' : [],
            'num_incubating' : [],
            'num_flu' : [],
            'num_immune' : [],
            'num_moving' : [],
            'num_moving' : [],
            'num_active' : [],
            'num_sickly' : [],
            'original_alive' : [],
            'original_dead' : []
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
            'total_score' : None
        }
        self.game_count = 0
        self.parseRawState()
        
    def decode_raw_action(self, actions):
        # Reverse process of the encoding, takes in a list of raw actions and returns a list of model ready actions
        # Modular arithmetic to the rescue
        readable_actions = []
        for action in actions:
            location_int = action // len(DEPLOYMENTS)  # gets the quotient
            deployment_int = action % len(DEPLOYMENTS)  # gets the remainder
            readable_actions.append([LOCATIONS(location_int), DEPLOYMENTS(deployment_int)])
        return readable_actions

    def cut(self, string, what_to_find):
        index = string.index(what_to_find) + len(what_to_find)
        return string[index:]

    def readNumber(self, string):
        output = ""
        for i in string:
            if i.isdigit():
                output += i
            else:
                break
        return int(output)

    def cutRead(self, string, cuts1, keys1, cuts2, keys2):
        for i in range(len(cuts1)):
            string = self.cut(string, cuts1[i])
            self.data_npc_count_to_score[keys1[i]].append(self.readNumber(string))
        for i in range(len(cuts2)):
            string = self.cut(string, cuts2[i])
            self.data_local_fear_to_score[keys2[i]].append(self.readNumber(string))
            
    def parseRawState(self):
        for index in self.data_to_output['step'].keys():
            if self.data_to_output['step'][index] == 13:
                self.game_count += 1
                string = self.data_to_output['raw_state'][index]
                keys1 = list(self.data_npc_count_to_score.keys())
                cuts1 = [x + '\": ' for x in keys1]
                keys2 = list(self.data_local_fear_to_score.keys())
                cuts2 = ['local_fear\": ' for _ in range(9)]
                self.cutRead(string, cuts1, keys1, cuts2, keys2)
        self.data_local_fear_to_score['total_score'] = self.data_npc_count_to_score['total_score'][:]
        
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
        plt.plot(x_axis, self.data_npc_count_to_score['num_alive'], color = "cyan", label = "Number of Alive (Includes Zombies)")
        plt.plot(x_axis, self.data_npc_count_to_score['num_dead'], color = "yellow", label = "Number of Dead")
        plt.plot(x_axis, self.data_npc_count_to_score['num_ashen'], color = "green", label = "Number of Dead Ashen")
        plt.plot(x_axis, self.data_npc_count_to_score['num_zombie_bitten'], color = "blue", label = "Number of Zombie Bitten")
        plt.plot(x_axis, self.data_npc_count_to_score['num_zombie'], color = "magenta", label = "Number of Zombies")
        plt.plot(x_axis, self.data_npc_count_to_score['num_healthy'], color = "orange", label = "Number of Healthy")
        plt.plot(x_axis, self.data_npc_count_to_score['num_incubating'], color = "olive", label = "Number of Incubating")
        plt.plot(x_axis, self.data_npc_count_to_score['num_flu'], color = "pink", label = "Number of Flu")
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
    data = Data_Output(data_log)
    data.deployment_usage_graph()
    data.npc_count_to_score_graph()
    data.local_fear_std_to_score_graph()
