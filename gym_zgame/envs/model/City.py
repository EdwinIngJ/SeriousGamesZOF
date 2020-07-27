import json
import numpy as np
import random
import pyfiglet as pf
import statistics as stat
from gym_zgame.envs.Print_Colors.PColor import PBack, PFore, PFont, PControl
from gym_zgame.envs.model.Neighborhood import Neighborhood
from gym_zgame.envs.model.NPC import NPC
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS
from gym_zgame.envs.enums.LEVELS import LEVELS
from gym_zgame.envs.enums.NPC_STATES import NPC_STATES_DEAD, NPC_STATES_ZOMBIE, NPC_STATES_FLU
from gym_zgame.envs.enums.NPC_ACTIONS import NPC_ACTIONS

class City:

    def __init__(self, loc_npc_range=(9, 15),developer_mode=False):
        # Main parameters
        self.developer_mode = developer_mode
        self.neighborhoods = []
        self._init_neighborhoods(loc_npc_range)
        self._init_neighborhood_threats()
        self.fear = 5
        self.resources = 10
        self.delta_resources = 0
        self.nbh_delta_local_fear_values = None
        self.score = 0
        self.total_score = 0
        self.turn = 0
        self.max_turns = 14  # each turn represents one day
        # Computed
        self.orig_alive, self.orig_dead = self._get_original_state_metrics()
        # CONSTANTS
        self.UPKEEP_DEPS = [DEPLOYMENTS.Z_CURE_CENTER_EXP, DEPLOYMENTS.Z_CURE_CENTER_FDA,
                            DEPLOYMENTS.FLU_VACCINE_MAN, DEPLOYMENTS.PHEROMONES_MEAT,
                            DEPLOYMENTS.FIREBOMB_BARRAGE, DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY]
        # Keep summary stats up to date for ease
        self.num_npcs = 0
        self.num_alive = 0
        self.num_dead = 0
        self.num_ashen = 0
        self.num_human = 0
        self.num_zombie_bitten = 0
        self.num_zombie = 0
        self.num_healthy = 0
        self.num_incubating = 0
        self.num_flu = 0
        self.num_immune = 0
        self.num_moving = 0
        self.num_active = 0
        self.num_sickly = 0
        self.update_summary_stats()

    def _init_neighborhoods(self, loc_npc_range):
        center = Neighborhood('CENTER', LOCATIONS.CENTER,
                              {LOCATIONS.N: NPC_ACTIONS.N,
                               LOCATIONS.S: NPC_ACTIONS.S,
                               LOCATIONS.E: NPC_ACTIONS.E,
                               LOCATIONS.W: NPC_ACTIONS.W},
                              random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        north = Neighborhood('N', LOCATIONS.N,
                             {LOCATIONS.CENTER: NPC_ACTIONS.S,
                              LOCATIONS.NE: NPC_ACTIONS.E,
                             LOCATIONS.NW: NPC_ACTIONS.W},
                             random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        south = Neighborhood('S', LOCATIONS.S,
                             {LOCATIONS.CENTER: NPC_ACTIONS.N,
                              LOCATIONS.SE: NPC_ACTIONS.E,
                              LOCATIONS.SW: NPC_ACTIONS.W},
                             random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        east = Neighborhood('E', LOCATIONS.E,
                            {LOCATIONS.CENTER: NPC_ACTIONS.W,
                             LOCATIONS.NE: NPC_ACTIONS.N,
                             LOCATIONS.SE: NPC_ACTIONS.S},
                            random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        west = Neighborhood('W', LOCATIONS.W,
                            {LOCATIONS.CENTER: NPC_ACTIONS.E,
                             LOCATIONS.NW: NPC_ACTIONS.N,
                             LOCATIONS.SW: NPC_ACTIONS.S},
                            random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        north_east = Neighborhood('NE', LOCATIONS.NE,
                                  {LOCATIONS.N: NPC_ACTIONS.W,
                                   LOCATIONS.E: NPC_ACTIONS.S},
                                  random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        north_west = Neighborhood('NW', LOCATIONS.NW,
                                  {LOCATIONS.N: NPC_ACTIONS.E,
                                   LOCATIONS.W: NPC_ACTIONS.S},
                                  random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        south_east = Neighborhood('SE', LOCATIONS.SE,
                                  {LOCATIONS.S: NPC_ACTIONS.W,
                                   LOCATIONS.E: NPC_ACTIONS.N},
                                  random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        south_west = Neighborhood('SW', LOCATIONS.SW,
                                  {LOCATIONS.S: NPC_ACTIONS.E,
                                   LOCATIONS.W: NPC_ACTIONS.N},
                                  random.randrange(loc_npc_range[0], loc_npc_range[1], 1), developer_mode=self.developer_mode)
        self.neighborhoods = [north_west, north, north_east, west, center, east, south_west, south, south_east]

    def _init_neighborhood_threats(self):
        # Add 10 dead in a random location
        dead_loc_index = random.choice(range(len(self.neighborhoods)))
        dead_loc = self.neighborhoods[dead_loc_index]
        dead_npcs = []
        for _ in range(10):
            dead_npc = NPC()
            dead_npc.change_dead_state(NPC_STATES_DEAD.DEAD)
            dead_npcs.append(dead_npc)
        dead_loc.add_NPCs(dead_npcs)
        dead_loc.orig_dead += 10

        # Add 1 zombie in a random location
        zombie_loc = random.choice(self.neighborhoods)
        zombie_npc = NPC()
        zombie_npc.change_zombie_state(NPC_STATES_ZOMBIE.ZOMBIE)
        zombie_loc.add_NPC(zombie_npc)
        zombie_loc.orig_alive += 1
        # Add 1 flue incubating at each location
        for nbh in self.neighborhoods:
            flu_npc = NPC()
            flu_npc.change_flu_state(NPC_STATES_FLU.INCUBATING)
            nbh.add_NPC(flu_npc)
            nbh.orig_alive += 1

    def _get_original_state_metrics(self):
        og_alive = 0
        og_dead = 0
        for nbh in self.neighborhoods:
            nbh_stats = nbh.get_data()
            og_alive += nbh_stats.get('original_alive', 0)
            og_dead += nbh_stats.get('original_dead', 0)
        return og_alive, og_dead

    def update_summary_stats(self):
        num_npcs = 0
        num_alive = 0
        num_dead = 0
        num_ashen = 0
        num_human = 0
        num_zombie_bitten = 0
        num_zombie = 0
        num_healthy = 0
        num_incubating = 0
        num_flu = 0
        num_immune = 0
        num_moving = 0
        num_active = 0
        num_sickly = 0

        for nbh in self.neighborhoods:
            nbh_stats = nbh.get_data()
            num_npcs += nbh_stats.get('num_npcs', 0)
            num_alive += nbh_stats.get('num_alive', 0)
            num_dead += nbh_stats.get('num_dead', 0)
            num_ashen += nbh_stats.get('num_ashen', 0)
            num_human += nbh_stats.get('num_human', 0)
            num_zombie_bitten += nbh_stats.get('num_zombie_bitten', 0)
            num_zombie += nbh_stats.get('num_zombie', 0)
            num_healthy += nbh_stats.get('num_healthy', 0)
            num_incubating += nbh_stats.get('num_incubating', 0)
            num_flu += nbh_stats.get('num_flu', 0)
            num_immune += nbh_stats.get('num_immune', 0)
            num_moving += nbh_stats.get('num_moving', 0)
            num_active += nbh_stats.get('num_active', 0)
            num_sickly += nbh_stats.get('num_sickly', 0)

        self.num_npcs = num_npcs
        self.num_alive = num_alive
        self.num_dead = num_dead
        self.num_ashen = num_ashen
        self.num_human = num_human
        self.num_zombie_bitten = num_zombie_bitten
        self.num_zombie = num_zombie
        self.num_healthy = num_healthy
        self.num_incubating = num_incubating
        self.num_flu = num_flu
        self.num_immune = num_immune
        self.num_moving = num_moving
        self.num_active = num_active
        self.num_sickly = num_sickly

    def do_turn(self, actions):
        loc_1 = actions[0][0]  # Unpack for readability
        dep_1 = actions[0][1]  # Unpack for readability
        loc_2 = actions[1][0]  # Unpack for readability
        dep_2 = actions[1][1]  # Unpack for readability
        nbh_1_index = 0  # Get location indexes for easier handling
        nbh_2_index = 0  # Get location indexes for easier handling
        for i in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[i]
            if loc_1 is nbh.location:
                nbh_1_index = i
            if loc_2 is nbh.location:
                nbh_2_index = i
        # Process turn
        self._add_buildings_to_locations(nbh_1_index, dep_1, nbh_2_index, dep_2)
        self.update_states()
        self.reset_bags()
        self.adjust_bags_for_deployments()
        self.adjust_bags_for_events()
        self.process_moves()
        # Update state info
        done = self.check_done()
        self.update_summary_stats()
        score = self.get_score()
        self.score = score
        self.total_score += score
        self.resources += 1
        for nbh_index in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[nbh_index]
            nbh.local_fear -= 1 if nbh.local_fear > 0 else 0
        self.fear -= 1 if self.fear > 0 else 0
        self.turn += 1

        return score, done

    def _add_buildings_to_locations(self, nbh_1_index, dep_1, nbh_2_index, dep_2):
        # Update the list of deployments at that location
        self.neighborhoods[nbh_1_index].add_deployment(dep_1)
        self.neighborhoods[nbh_2_index].add_deployment(dep_2)

    def update_states(self):
        self._update_trackers()
        self._update_global_states()
        self._update_artificial_states()
        self._update_event_states()
        self._update_natural_states()
        self._update_deployment_states()

    def _update_deployment_states(self):
        for nbh in self.neighborhoods:
            for dep_index in range(len(nbh.deployments)):
                dep = nbh.deployments[dep_index]
                if dep is DEPLOYMENTS.FIREBOMB_BARRAGE: #Firebombs deactivate after 1 turn
                    nbh.deployments[dep_index] = DEPLOYMENTS.FIREBOMB_PRIMED
            if nbh.swarm_enabled: #If there's a swarm, there's a 1% chance * the number of zombies for a deployment to be destroyed
                if len(nbh.deployments) > 0 and random.random() < 0.01 * nbh.num_zombie:
                    nbh.deployments.remove(random.choice(nbh.deployments))
                

    def _update_trackers(self):
        # Update fear and resources increments
        resource_cost_per_turn = 0
        deployments_fear_resource_costs = {
            DEPLOYMENTS.QUARANTINE_FENCED : [1,0],
            DEPLOYMENTS.BITE_CENTER_AMPUTATE : [1,0],
            DEPLOYMENTS.Z_CURE_CENTER_FDA : [1,0],
            DEPLOYMENTS.Z_CURE_CENTER_EXP : [1,1],
            DEPLOYMENTS.FLU_VACCINE_MAN : [1,1],
            DEPLOYMENTS.BROADCAST_DONT_PANIC : [-1,0],
            DEPLOYMENTS.BROADCAST_CALL_TO_ARMS : [1,0],
            DEPLOYMENTS.SNIPER_TOWER_FREE : [1,0],
            DEPLOYMENTS.PHEROMONES_MEAT : [-1,1],
            DEPLOYMENTS.BSL4LAB_SAFETY_OFF : [0,-2],
            DEPLOYMENTS.RALLY_POINT_FULL : [1,0],
            DEPLOYMENTS.FIREBOMB_PRIMED : [1,0],
            DEPLOYMENTS.FIREBOMB_BARRAGE : [10,1],
            DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY : [1,1]
        }
        local_fear_cost_per_turn = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0}
        for nbh_index in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[nbh_index]
            for dep in nbh.deployments:
                # deployments not included do not have fear or resources costs
                if dep is DEPLOYMENTS.BSL4LAB_SAFETY_ON:
                    if nbh.num_active >= 5:
                        resource_cost_per_turn -= 1
                elif dep in deployments_fear_resource_costs:
                    resource_cost_per_turn += deployments_fear_resource_costs[dep][1]
                    for local_fear_change_nbh_index in range(len(self.neighborhoods)):
                        if local_fear_change_nbh_index == nbh_index:
                            local_fear_cost_per_turn[nbh_index] += deployments_fear_resource_costs[dep][0]
                        else:
                            local_fear_cost_per_turn[local_fear_change_nbh_index] += deployments_fear_resource_costs[dep][0] * 0.50 #deployments outside the neighborhood only affect fear by 50% than if they were in that neighborhood
        self.nbh_delta_local_fear_values = local_fear_cost_per_turn.copy()
        self.delta_resources = resource_cost_per_turn

    def _update_global_states(self):
        self.resources -= self.delta_resources  # remove upkeep resources (includes new deployments)
        local_fears = [] #List of local fears in each neighborhood
        for nbh_index in range(len(self.neighborhoods)): # increase local fear for each neighborhood from deployments (includes new deployments)
            nbh = self.neighborhoods[nbh_index]
            nbh.local_fear += int(self.nbh_delta_local_fear_values[nbh_index] + .9)
            if nbh.local_fear < 0:
                nbh.local_fear = 0
            local_fears.append(nbh.local_fear)
            
        average_local_fear = stat.mean(local_fears) #Average of local_fears found with statistics module
        self.fear = average_local_fear #Global Fear temporarily set to average of all local fears
        for local_fear in local_fears: #Global Fear influenced by how far each local fear is from average local fear
            if local_fear < average_local_fear: #If local fear is below average, global fear lowered by .5 * the difference
                self.fear -= (average_local_fear - local_fear) * .5
            else: #Otherwise, global fear increased by the difference
                self.fear += local_fear - average_local_fear 
        self.fear = int(self.fear+.9)
        
        if self.fear < 0:
            self.fear = 0
        if self.resources < 0:
            self.resources = 0
            self._destroy_upkeep_deployments()
        
    def _destroy_upkeep_deployments(self):
        for nbh in self.neighborhoods:
            nbh.destroy_deployments_by_type(self.UPKEEP_DEPS)

    def _update_artificial_states(self,):
        # Some deployments (z cure station, flu vaccine, sniper tower, kiln, and firebomb)
        # Have immediate state changes (aka artificial ones) that happen before the natural ones
        self.update_summary_stats()
        for nbh_index in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[nbh_index]
            state_change_deployments = [DEPLOYMENTS.Z_CURE_CENTER_FDA, DEPLOYMENTS.Z_CURE_CENTER_EXP, DEPLOYMENTS.FLU_VACCINE_OPT, DEPLOYMENTS.FLU_VACCINE_MAN, DEPLOYMENTS.KILN_NO_QUESTIONS, DEPLOYMENTS.SNIPER_TOWER_CONFIRM, DEPLOYMENTS.SNIPER_TOWER_FREE, DEPLOYMENTS.FIREBOMB_BARRAGE] 
            for dep in nbh.deployments:
                if dep in state_change_deployments:
                    self._art_trans(dep, nbh_index)            
        self.update_summary_stats()
        
    def _art_trans(self, dep, nbh_index):
        #Editable variables for deployment probabilities
        nbh = self.neighborhoods[nbh_index]
        bite_cure_prob_z_cure_center_fda = 0.25
        zombie_cure_prob_z_cure_center_fda = 0.01
        bite_cure_prob_z_cure_center_exp = 0.33
        bite_cure_fail_prob_z_cure_center_exp = 0.5
        zombie_cure_prob_z_cure_center_exp = 0.33
        vaccine_success_flu_vaccine_free = max(0, 0.2 - (0.01 * self.fear))
        vaccine_success_flu_vaccine_man = 0.5
        zombie_burn_prob_kiln_no_questions = 0.1
        sick_burn_prob_kiln_no_questions = 0.05
        active_burn_prob_kiln_no_questions = 0.01
        zombie_shot_prob_sniper_tower_confirm = 1 / nbh.num_zombie if nbh.num_zombie > 0 else 0
        zombie_shot_prob_sniper_tower_free = 1 / nbh.num_moving if nbh.num_moving > 0 else 0
        zombie_bitten_shot_prob_sniper_tower_free = 0.5 * (nbh.num_zombie_bitten / nbh.num_moving) if nbh.num_moving > 0 else 0
        flu_shot_prob_sniper_tower_free = 0.5 * (nbh.num_flu / nbh.num_moving) if nbh.num_moving > 0 else 0
        dead_dead_prob_firebomb_barrage = 0.5
        death_prob_firebomb_barrage = 0.1
        vaporize_prob_firebomb_barrage = 0.9
        for npc in nbh.NPCs:
            #Dictionary of all [conditions, probability of state change, state change type, state change to] for each deployment
            states_changes_for_deployments = {
                DEPLOYMENTS.Z_CURE_CENTER_FDA : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, bite_cure_prob_z_cure_center_fda, "zombie", NPC_STATES_ZOMBIE.HUMAN],
                                                 [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, zombie_cure_prob_z_cure_center_fda, "zombie", NPC_STATES_ZOMBIE.ZOMBIE_BITTEN]],
                DEPLOYMENTS.Z_CURE_CENTER_EXP : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, bite_cure_prob_z_cure_center_exp, "zombie", NPC_STATES_ZOMBIE.HUMAN],
                                                 [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, bite_cure_fail_prob_z_cure_center_exp, "dead", NPC_STATES_DEAD.DEAD],
                                                 [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, zombie_cure_prob_z_cure_center_exp, "zombie", NPC_STATES_ZOMBIE.ZOMBIE_BITTEN]],
                DEPLOYMENTS.FLU_VACCINE_OPT : [[(npc.state_flu is not NPC_STATES_FLU.IMMUNE) and (npc.state_zombie is not NPC_STATES_ZOMBIE.ZOMBIE), vaccine_success_flu_vaccine_free, "flu", NPC_STATES_FLU.IMMUNE]],
                DEPLOYMENTS.FLU_VACCINE_MAN : [[(npc.state_flu is not NPC_STATES_FLU.IMMUNE) and (npc.state_zombie is not NPC_STATES_ZOMBIE.ZOMBIE), vaccine_success_flu_vaccine_man, "flu", NPC_STATES_FLU.IMMUNE]],
                DEPLOYMENTS.KILN_NO_QUESTIONS : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, zombie_burn_prob_kiln_no_questions, "dead", NPC_STATES_DEAD.ASHEN],
                                                 [npc.sickly, sick_burn_prob_kiln_no_questions, "dead", NPC_STATES_DEAD.ASHEN],
                                                 [npc.active, active_burn_prob_kiln_no_questions, "dead", NPC_STATES_DEAD.ASHEN]],
                DEPLOYMENTS.SNIPER_TOWER_CONFIRM : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, zombie_shot_prob_sniper_tower_confirm, "dead", NPC_STATES_DEAD.DEAD]],
                DEPLOYMENTS.SNIPER_TOWER_FREE : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, zombie_shot_prob_sniper_tower_free, "dead", NPC_STATES_DEAD.DEAD],
                                                 [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, zombie_bitten_shot_prob_sniper_tower_free, "dead", NPC_STATES_DEAD.DEAD],
                                                 [npc.state_flu is NPC_STATES_FLU.FLU, flu_shot_prob_sniper_tower_free, "dead", NPC_STATES_DEAD.DEAD]], 
                DEPLOYMENTS.FIREBOMB_BARRAGE : [[npc.state_dead is NPC_STATES_DEAD.DEAD, dead_dead_prob_firebomb_barrage, "dead", NPC_STATES_DEAD.ASHEN],
                                                [npc.moving, death_prob_firebomb_barrage, "dead", NPC_STATES_DEAD.DEAD],
                                                [npc.moving, vaporize_prob_firebomb_barrage, "dead", NPC_STATES_DEAD.ASHEN]]
            }
            for possible_change in states_changes_for_deployments[dep]:
                if possible_change[0] and random.random() <= possible_change[1]:
                    if possible_change[2] == "zombie":
                        npc.change_zombie_state(possible_change[3])
                    elif possible_change[2] == "dead":
                        npc.change_dead_state(possible_change[3])
                    elif possible_change[2] == "flu":
                        npc.change_flu_state(possible_change[3])
                        
    def _update_event_states(self):
        for nbh in self.neighborhoods:
            nbh.checkForEvents()
            
    def _update_natural_states(self):
        self._society_transitions()
        self._flu_transitions()
        self._zombie_transitions()

    def _society_transitions(self):
        for nbh_index in range(len(self.neighborhoods)):
            # Get baselines
            nbh = self.neighborhoods[nbh_index]
            trans_probs = nbh.compute_baseline_trans_probs()

            # Get society based transitions probabilities
            burial_prob = trans_probs.get('burial')

            # Update based on deployments
            if DEPLOYMENTS.KILN_OVERSIGHT in nbh.deployments:
                burial_prob = min(1.0, burial_prob * 1.5)
            if DEPLOYMENTS.KILN_NO_QUESTIONS in nbh.deployments:
                burial_prob = min(1.0, burial_prob * 5.0)

            # Universal Law: Burial
            for npc in nbh.NPCs:
                if npc.state_dead is NPC_STATES_DEAD.DEAD:
                    if random.random() <= burial_prob:
                        npc.change_dead_state(NPC_STATES_DEAD.ASHEN)

    def _flu_transitions(self):
        for nbh_index in range(len(self.neighborhoods)):
            # Get baselines
            nbh = self.neighborhoods[nbh_index]
            trans_probs = nbh.compute_baseline_trans_probs()

            # Get flu based transitions probabilities
            recover_prob = trans_probs.get('recover')
            pneumonia_prob = trans_probs.get('pneumonia')
            incubate_prob = trans_probs.get('incubate')
            fumes_prob = trans_probs.get('fumes')
            cough_prob = trans_probs.get('cough')
            mutate_prob = trans_probs.get('mutate')

            # Update based on deployments
            if DEPLOYMENTS.BSL4LAB_SAFETY_OFF in nbh.deployments:
                fumes_prob = min(1.0, fumes_prob * 10.0)
            if DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS in nbh.deployments:
                cough_prob = min(1.0, fumes_prob * 0.75)
                fumes_prob = min(1.0, fumes_prob * 0.75)
            if DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY in nbh.deployments:
                cough_prob = min(1.0, fumes_prob * 0.25)
                fumes_prob = min(1.0, fumes_prob * 0.25)

            # Flu Laws
            for npc in nbh.NPCs:
                # Recover
                if npc.state_flu is NPC_STATES_FLU.FLU:
                    if random.random() <= recover_prob:
                        npc.change_flu_state(NPC_STATES_FLU.IMMUNE)
                # Pneumonia
                if npc.state_flu is NPC_STATES_FLU.FLU:
                    if random.random() <= pneumonia_prob:
                        npc.change_dead_state(NPC_STATES_DEAD.DEAD)
                # Incubate
                if npc.state_flu is NPC_STATES_FLU.INCUBATING:
                    if random.random() <= incubate_prob:
                        npc.change_flu_state(NPC_STATES_FLU.FLU)
                # Fumes
                if npc.state_flu is NPC_STATES_FLU.HEALTHY:
                    if random.random() <= fumes_prob:
                        npc.change_flu_state(NPC_STATES_FLU.INCUBATING)
                # Cough
                if npc.state_flu is NPC_STATES_FLU.HEALTHY:
                    if random.random() <= cough_prob:
                        npc.change_flu_state(NPC_STATES_FLU.INCUBATING)
                # Mutate
                if npc.state_flu is NPC_STATES_FLU.IMMUNE:
                    if random.random() <= mutate_prob:
                        npc.change_flu_state(NPC_STATES_FLU.HEALTHY)

    def _zombie_transitions(self):
        for nbh_index in range(len(self.neighborhoods)):
            # Get baselines
            nbh = self.neighborhoods[nbh_index]
            trans_probs = nbh.compute_baseline_trans_probs()

            # Get zombie based transitions probabilities
            turn_prob = trans_probs.get('turn')
            devour_prob = trans_probs.get('devour')
            bite_prob = trans_probs.get('bite')
            fight_back_prob = trans_probs.get('fight_back')
            collapse_prob = trans_probs.get('collapse')
            rise_prob = trans_probs.get('rise')

            # Update based on deployments
            if DEPLOYMENTS.BITE_CENTER_DISINFECT in nbh.deployments:
                turn_prob = min(1.0, turn_prob * 0.5)
            if DEPLOYMENTS.BITE_CENTER_AMPUTATE in nbh.deployments:
                turn_prob = min(1.0, turn_prob * 0.05)
            if DEPLOYMENTS.BROADCAST_CALL_TO_ARMS in nbh.deployments:
                fight_back_prob = min(1.0, fight_back_prob * 5.0)
                devour_prob = min(1.0, devour_prob * 1.25)
            if DEPLOYMENTS.BSL4LAB_SAFETY_OFF in nbh.deployments:
                rise_prob = min(1.0, rise_prob * 10.0)
            if DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS in nbh.deployments:
                bite_prob = min(1.0, bite_prob * 0.75)
                fight_back_prob = min(1.0, fight_back_prob * 0.75)
            if DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS in nbh.deployments:
                bite_prob = min(1.0, bite_prob * 0.25)
                fight_back_prob = min(1.0, fight_back_prob * 0.25)

            # Zombie Laws
            for npc in nbh.NPCs:
                # Turn
                if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN:
                    if random.random() <= turn_prob:
                        npc.change_zombie_state(NPC_STATES_ZOMBIE.ZOMBIE)
                # Devour
                if npc.state_zombie is NPC_STATES_ZOMBIE.HUMAN:
                    if random.random() <= devour_prob:
                        npc.change_dead_state(NPC_STATES_DEAD.DEAD)
                # Bite
                if npc.state_zombie is NPC_STATES_ZOMBIE.HUMAN:
                    if random.random() <= bite_prob:
                        npc.change_zombie_state(NPC_STATES_ZOMBIE.ZOMBIE_BITTEN)
                # Fight Back
                if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE:
                    if random.random() <= fight_back_prob:
                        npc.change_dead_state(NPC_STATES_DEAD.DEAD)
                        npc.change_zombie_state(NPC_STATES_ZOMBIE.HUMAN)
                        
                # Collapse
                if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE:
                    if random.random() <= collapse_prob:
                        npc.change_dead_state(NPC_STATES_DEAD.DEAD)
                        npc.change_zombie_state(NPC_STATES_ZOMBIE.HUMAN)
                # Rise
                if npc.state_dead is NPC_STATES_DEAD.DEAD:
                    if random.random() <= rise_prob:
                        npc.change_zombie_state(NPC_STATES_ZOMBIE.ZOMBIE)
                        npc.change_dead_state(NPC_STATES_DEAD.ALIVE)

    def reset_bags(self):
        for nbh in self.neighborhoods:
            for npc in nbh.NPCs:
                npc.empty_bag()  # empty everyone's bag
                if npc.state_dead is NPC_STATES_DEAD.ALIVE:
                    npc.set_init_bag_alive()  # if alive, give default 
                # Zombie want to move toward the active people around them
                # Find number active in adj neighborhood
                actions_to_add_bags = {}
                for loc, npc_action in nbh.adj_locations.items():
                    for temp_nbh in self.neighborhoods:
                        if temp_nbh.location is loc:
                            actions_to_add_bags[npc_action] = temp_nbh.num_active
                if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE:
                    # Add a STAY to the bag for each person in the current nbh
                    for _ in range(nbh.num_active):
                        npc.add_to_bag(NPC_ACTIONS.STAY)
                # Add number active from adj nbhs with actions that would move the npc there
                for npc_action, num_active in actions_to_add_bags.items():
                    for _ in range(num_active):
                        npc.add_to_bag(npc_action)

    def adjust_bags_for_deployments(self):
        for nbh_index in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[nbh_index]
            for dep in nbh.deployments:
                self._push_specific_bag_adjust(dep, nbh_index)
                self._pull_bag_adjust(dep, nbh_index)

    def _specific_action_bag_add(self, npc, action, number_to_add): #A bag editor for adding a number of any of the following actions: NPC_ACTIONS.STAY, NPC_ACTIONS.N, NPC_ACTIONS.S, NPC_ACTIONS.E, NPC_ACTIONS.W
        for _ in range(number_to_add):
            npc.add_to_bag(action)
            
    def _push_action_bag_add(self, npc, nbh, number_to_add): #A bag editor for adding a number of actions to move an NPC away from their current location
        for npc_action in nbh.adj_locations.values():
            for _ in range(number_to_add):
                npc.add_to_bag(npc_action)
                             
    def _push_specific_bag_adjust(self, dep, nbh_index): #Method to adjust bags to incorporate pushing NPCs away from a certain location or moving them in a certain direction as a result of deployments
        nbh = self.neighborhoods[nbh_index]
        deps_that_belong_here = {DEPLOYMENTS.QUARANTINE_OPEN : 1, DEPLOYMENTS.QUARANTINE_FENCED : 1, DEPLOYMENTS.PHEROMONES_BRAINS : 1, DEPLOYMENTS.PHEROMONES_MEAT : 1, DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS : 1, DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY : 1}
        if deps_that_belong_here.get(dep, 0) == 0:
            return -1
        for npc in nbh.NPCs:
            bag_changes_for_deployments = { #format for each possible change is [condition, push npc away from neighborhood or specific action, number of actions to addof each]
                DEPLOYMENTS.QUARANTINE_OPEN : [[npc.active, "push", 3],
                                               [npc.sickly, NPC_ACTIONS.STAY, 10]], 
                DEPLOYMENTS.QUARANTINE_FENCED : [[npc.active, "push", 3],
                                                 [npc.sickly, NPC_ACTIONS.STAY, 10]],
                DEPLOYMENTS.PHEROMONES_BRAINS : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, NPC_ACTIONS.STAY, 10],
                                                 [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, NPC_ACTIONS.STAY, 1]],
                DEPLOYMENTS.PHEROMONES_MEAT : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, NPC_ACTIONS.STAY, 10],
                                               [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, NPC_ACTIONS.STAY, 9],
                                               [npc.active or npc.state_flu is NPC_STATES_FLU.INCUBATING, NPC_ACTIONS.STAY, 1]],
                DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS : [[npc.sickly or npc.active, NPC_ACTIONS.STAY, 2]],
                DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY : [[npc.sickly or npc.active, NPC_ACTIONS.STAY, 9]]
            }
            for possible_changes in bag_changes_for_deployments[dep]:
                if possible_changes[0]:
                    if possible_changes[1] == "push":
                        self._push_action_bag_add(npc, nbh, possible_changes[2])
                    else:
                        self._specific_action_bag_add(npc, possible_changes[1], possible_changes[2])
                        
    def _pull_bag_adjust(self, dep, nbh_index):
        nbh = self.neighborhoods[nbh_index]
        deps_that_belong_here = {DEPLOYMENTS.QUARANTINE_OPEN : 1, DEPLOYMENTS.QUARANTINE_FENCED : 1, DEPLOYMENTS.PHEROMONES_BRAINS : 1, DEPLOYMENTS.PHEROMONES_MEAT : 1, DEPLOYMENTS.RALLY_POINT_OPT : 1, DEPLOYMENTS.RALLY_POINT_FULL : 1}
        if deps_that_belong_here.get(dep, 0) == 0:
            return -1
        for loc, npc_action in nbh.adj_locations.items():
            inward_npc_action = NPC_ACTIONS.reverse_action(npc_action)
            for temp_nbh in self.neighborhoods:
                if temp_nbh.location is loc:
                    for npc in temp_nbh.NPCs:
                        bag_changes_for_deployments = { #format for each possible change is [condition, push npc away from neighborhood or specific action, number of actions to addof each]
                            DEPLOYMENTS.QUARANTINE_OPEN : [[npc.sickly, 10]],
                            DEPLOYMENTS.QUARANTINE_FENCED : [[npc.sickly, 10]],
                            DEPLOYMENTS.PHEROMONES_BRAINS : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, 10],
                                                             [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, 1]],
                            DEPLOYMENTS.PHEROMONES_MEAT : [[npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE, 10],
                                                           [npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN, 9],
                                                           [npc.active or npc.state_flu is NPC_STATES_FLU.INCUBATING, 1]],
                            DEPLOYMENTS.RALLY_POINT_OPT : [[npc.active, 3]],
                            DEPLOYMENTS.RALLY_POINT_FULL : [[(npc.state_zombie is not NPC_STATES_ZOMBIE.ZOMBIE) or (npc.state_dead is not NPC_STATES_DEAD.DEAD), 10]]
                        }
                        for possible_changes in bag_changes_for_deployments[dep]:
                            if possible_changes[0]:
                                self._specific_action_bag_add(npc, inward_npc_action, possible_changes[1])

    def adjust_bags_for_events(self):
        for nbh in self.neighborhoods:
            if nbh.gathering_enabled:
                nbh.add_to_all_human_bags(NPC_ACTIONS.STAY, 5)
            if nbh.panic_enabled:
                for npc in nbh.NPCs:
                    if npc.state_zombie is not NPC_STATES_ZOMBIE.ZOMBIE and npc.state_dead is not NPC_STATES_DEAD.DEAD:
                        self._push_action_bag_add(npc, nbh, 3)
                
    def process_moves(self):
        # Non-dead, non-zombie people
        self._normal_moves()
        # Zombies move differently
        self._zombie_moves()

    def _normal_moves(self):
        # For each person that's not dead and not a zombie, pick an action from their bag and do it
        for nbh_index in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[nbh_index]
            nbh.clean_all_bags()
            for npc in nbh.NPCs:
                if npc.state_dead is NPC_STATES_DEAD.ALIVE and npc.state_zombie is not NPC_STATES_ZOMBIE.ZOMBIE:
                    action = npc.selection()  # Selects a random action from the npc bag of actions
                    new_location = self._get_new_location(nbh.location, action)
                    if new_location is None:  # handles movement out of the city
                        new_location = nbh.location  # if movement out of the city, stay in place
                    # Find index of new neighborhood
                    new_nbh_index = nbh_index  # default is to just leave things where they are
                    for temp_index in range(len(self.neighborhoods)):
                        temp_nbh = self.neighborhoods[temp_index]
                        if temp_nbh.location is new_location:
                            new_nbh_index = temp_index
                    # Execute the move
                    self._execute_movement(old_nbh_index=nbh_index, new_nbh_index=new_nbh_index, NPC=npc)

    def _zombie_moves(self):
        # For each person that's not dead and not a zombie, pick an action from their bag and do it
        for nbh_index in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[nbh_index]
            nbh.clean_all_bags()
            zombies_to_move = []
            for npc in nbh.NPCs:
                if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE and npc.state_dead is NPC_STATES_DEAD.ALIVE:
                    zombies_to_move.append(npc)
            # If there aren't zombies, finish
            if len(zombies_to_move) == 0:
                continue
            # Pick a random zombie, this zombie will control the movement of all zombies!
            rand_zombie = random.choice(zombies_to_move)
            action = rand_zombie.selection()  # Selects a random action from the npc bag of actions
            new_location = self._get_new_location(nbh.location, action)
            if new_location is None:  # handles movement out of the city
                new_location = nbh.location  # if movement out of the city, stay in place
            # Find index of new neighborhood
            new_nbh_index = nbh_index  # default is to just leave things where they are
            for temp_index in range(len(self.neighborhoods)):
                temp_nbh = self.neighborhoods[temp_index]
                if temp_nbh.location is new_location:
                    new_nbh_index = temp_index
            # Execute the move for all zombies in the neighborhood
            for zombie in zombies_to_move:
                self._execute_movement(old_nbh_index=nbh_index, new_nbh_index=new_nbh_index, NPC=zombie)

    def _execute_movement(self, old_nbh_index, new_nbh_index, NPC):
        nbh_old = self.neighborhoods[old_nbh_index]
        nbh_new = self.neighborhoods[new_nbh_index]
        # Get chance of move succeeding based on deployments at new neighborhood
        prob_of_move = 1.0
        if DEPLOYMENTS.QUARANTINE_FENCED in nbh_new.deployments:
            prob_of_move *= 0.05  # 95% chance of staying (move failing)
        if DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS in nbh_new.deployments:
            prob_of_move *= 0.75  # 25% chance of staying (move failing)
        if DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY in nbh_new.deployments:
            prob_of_move *= 0.25  # 75% chance of staying (move failing)
        # If the move is successful, add and remove the NPC from the neighborhoods
        if random.random() <= prob_of_move:
            nbh_old.remove_NPC(NPC)
            nbh_new.add_NPC(NPC)

    def check_done(self):
        return self.turn >= self.max_turns

    def get_score(self):
        self.update_summary_stats()
        active_weight = 1.0
        sickly_weight = 0.5
        fear_weight = 1.0
        zombie_weight = 2.0
        score = (self.num_active * active_weight) + \
                (self.num_sickly * sickly_weight) - \
                (self.fear * fear_weight) - \
                (self.num_zombie * zombie_weight)
        scaled_score = np.floor((score + 800) / 100)  # scaled to fit env state space range
        return scaled_score

    def get_data(self):
        self.update_summary_stats()
        city_data = {'total_score': self.total_score,
                     'fear': self.fear,
                     'resources': self.resources,
                     'num_npcs': self.num_npcs,
                     'num_alive': self.num_alive,
                     'num_dead': self.num_dead,
                     'num_ashen': self.num_ashen,
                     'num_human': self.num_human,
                     'num_zombie_bitten': self.num_zombie_bitten,
                     'num_zombie': self.num_zombie,
                     'num_healthy': self.num_healthy,
                     'num_incubating': self.num_incubating,
                     'num_flu': self.num_flu,
                     'num_immune': self.num_immune,
                     'num_moving': self.num_moving,
                     'num_active': self.num_active,
                     'num_sickly': self.num_sickly,
                     'original_alive': self.orig_alive,
                     'original_dead': self.orig_dead}
        return city_data

    def return_events(self):
        events_currently_going_on = {
            "NW"     : [],
            "N"      : [],
            "NE"     : [],
            "W"      : [],
            "CENTER" : [],
            "E"      : [],
            "SW"     : [],
            "S"      : [],
            "SE"     : []   
            }
        nbhs = list(events_currently_going_on.keys())
        for i in range(len(self.neighborhoods)):
            if self.neighborhoods[i].gathering_enabled:
                events_currently_going_on[nbhs[i]].append("Gatherings")
            if self.neighborhoods[i].panic_enabled:
                events_currently_going_on[nbhs[i]].append("Panic")
            if self.neighborhoods[i].swarm_enabled:
                events_currently_going_on[nbhs[i]].append("Swarm")
        return events_currently_going_on
    
    def _mask_visible_data(self, nbh_fear, value):
            offset_amount = min(int(.85 * value), int(nbh_fear / 75 * value)) #The offset value
            return random.randint(value - offset_amount, value + offset_amount)
            
        
    def show_data(self, nbh_fear, value):
        #Decides which data to show
        if self.developer_mode:
            return value
        else:
            return self._mask_visible_data(nbh_fear, value)

    def rl_encode(self):
        # Set up data structure for the state space, must match the ZGameEnv!
        state = np.zeros(shape=(10, 7 + (self.max_turns * 2)), dtype='uint8')

        # Set the state information for the global state
        state[0, 0] = int(self.fear)  # Global Fear
        state[0, 1] = int(self.resources)  # Global Resources
        state[0, 2] = int(self.turn)  # Turn number
        state[0, 3] = int(self.orig_alive)  # Original number alive
        state[0, 4] = int(self.orig_dead)  # Original number dead
        state[0, 5] = int(self.score)  # Score on a given turn (trying to maximize)

        # Set the state information for the different neighborhoods
        # Don't need to worry about order here as neighborhoods are stored in a list
        # Remember the state should not have the raw values, but the masked values (none, few, many)
        for i in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[i]
            nbh_data = nbh.get_data()
            state[i + 1, 0] = nbh_data.get('original_alive', 0)  # i + 1 since i starts at 0 and 0 is already filled
            state[i + 1, 1] = nbh_data.get('original_dead', 0)
            state[i + 1, 2] = self._mask_visible_data(nbh.local_fear, nbh_data.get('num_active', 0))
            state[i + 1, 3] = self._mask_visible_data(nbh.local_fear, nbh_data.get('num_sickly', 0))
            state[i + 1, 4] = self._mask_visible_data(nbh.local_fear, nbh_data.get('num_zombie', 0))
            state[i + 1, 5] = self._mask_visible_data(nbh.local_fear, nbh_data.get('num_dead', 0))
            state[i + 1, 6] = nbh_data.get('local_fear', 0)
            for j in range(len(nbh.deployments)):
                state[i + 1, j + 7] = nbh.deployments[j].value

        return state

    def human_encode(self):
        city_data = self.get_data()
        nbhs_data = []
        for nbh in self.neighborhoods:
            nbh_data = nbh.get_data()
            nbhs_data.append(nbh_data)
        state_data = {'city': city_data, 'neighborhoods': nbhs_data}
        state_json = json.dumps(state_data)
        return state_json

    def rl_render(self):
        minimal_report = 'Turn {0} of {1}. Turn Score: {2}. Total Score: {3}'.format(self.turn, self.max_turns,
                                                                                     self.score, self.total_score)
        print(minimal_report)
        return minimal_report

    def human_render(self):
        return self.neighborhoods, self.score, self.total_score, self.fear, self.resources, self.orig_alive, self.orig_dead, self.return_events()

    @staticmethod
    def _get_new_location(old_location, npc_action):
        if old_location is LOCATIONS.CENTER:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.CENTER
            if npc_action is NPC_ACTIONS.N:
                return LOCATIONS.N
            if npc_action is NPC_ACTIONS.S:
                return LOCATIONS.S
            if npc_action is NPC_ACTIONS.E:
                return LOCATIONS.E
            if npc_action is NPC_ACTIONS.W:
                return LOCATIONS.W
        elif old_location is LOCATIONS.N:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.N
            if npc_action is NPC_ACTIONS.N:
                return None
            if npc_action is NPC_ACTIONS.S:
                return LOCATIONS.CENTER
            if npc_action is NPC_ACTIONS.E:
                return LOCATIONS.NE
            if npc_action is NPC_ACTIONS.W:
                return LOCATIONS.NW
        elif old_location is LOCATIONS.S:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.S
            if npc_action is NPC_ACTIONS.N:
                return LOCATIONS.CENTER
            if npc_action is NPC_ACTIONS.S:
                return None
            if npc_action is NPC_ACTIONS.E:
                return LOCATIONS.SE
            if npc_action is NPC_ACTIONS.W:
                return LOCATIONS.SW
        elif old_location is LOCATIONS.E:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.E
            if npc_action is NPC_ACTIONS.N:
                return LOCATIONS.NE
            if npc_action is NPC_ACTIONS.S:
                return LOCATIONS.SE
            if npc_action is NPC_ACTIONS.E:
                return None
            if npc_action is NPC_ACTIONS.W:
                return LOCATIONS.CENTER
        elif old_location is LOCATIONS.W:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.W
            if npc_action is NPC_ACTIONS.N:
                return LOCATIONS.NW
            if npc_action is NPC_ACTIONS.S:
                return LOCATIONS.SW
            if npc_action is NPC_ACTIONS.E:
                return LOCATIONS.CENTER
            if npc_action is NPC_ACTIONS.W:
                return None
        elif old_location is LOCATIONS.NE:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.NE
            if npc_action is NPC_ACTIONS.N:
                return None
            if npc_action is NPC_ACTIONS.S:
                return LOCATIONS.E
            if npc_action is NPC_ACTIONS.E:
                return None
            if npc_action is NPC_ACTIONS.W:
                return LOCATIONS.N
        elif old_location is LOCATIONS.NW:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.NW
            if npc_action is NPC_ACTIONS.N:
                return None
            if npc_action is NPC_ACTIONS.S:
                return LOCATIONS.W
            if npc_action is NPC_ACTIONS.E:
                return LOCATIONS.N
            if npc_action is NPC_ACTIONS.W:
                return None
        elif old_location is LOCATIONS.SE:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.SE
            if npc_action is NPC_ACTIONS.N:
                return LOCATIONS.E
            if npc_action is NPC_ACTIONS.S:
                return None
            if npc_action is NPC_ACTIONS.E:
                return None
            if npc_action is NPC_ACTIONS.W:
                return LOCATIONS.S
        elif old_location is LOCATIONS.SW:
            if npc_action is NPC_ACTIONS.STAY:
                return LOCATIONS.SW
            if npc_action is NPC_ACTIONS.N:
                return LOCATIONS.W
            if npc_action is NPC_ACTIONS.S:
                return None
            if npc_action is NPC_ACTIONS.E:
                return LOCATIONS.S
            if npc_action is NPC_ACTIONS.W:
                return None
        else:
            raise ValueError('Bad location passed into new location mapping.')


if __name__ == '__main__':
    city = City()
    print(city.get_data())


