import random
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS
from gym_zgame.envs.enums.NPC_STATES import NPC_STATES_DEAD, NPC_STATES_ZOMBIE, NPC_STATES_FLU
from gym_zgame.envs.model.NPC import NPC

class Neighborhood:

    def __init__(self, id, location, adj_locations, num_init_npcs,developer_mode=False):
        self.developer_mode = developer_mode
        self.id = id
        self.location = location
        self.NPCs = []
        self.adj_locations = adj_locations
        self._npc_init(num_init_npcs)
        self.deployments = []
        self.local_fear = 5
        # Transition probabilities
        self.swarm_enabled = False
        self.gathering_enabled = False
        self.panic_enabled = False
        self.checkForEvents()
        self.event_probs = None
        self.compute_event_probs()
        self.trans_probs = self.compute_baseline_trans_probs()
        # Keep summary stats up to date for ease
        self.num_npcs = len(self.NPCs)
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
        self.orig_alive, self.orig_dead = self._get_original_state_metrics()

    def _npc_init(self, num_npcs):
        init_npcs = []
        #There is a 10% chance for the NPC to be a zombie and/or have the flu
        for _ in range(num_npcs):
            npc = NPC()
            zombie_chance = random.uniform(0, 1)
            flu_chance = random.uniform(0, 1)
            if zombie_chance >= 0.9:
                npc.change_zombie_state(NPC_STATES_ZOMBIE.ZOMBIE)
            if flu_chance >= 0.9:
                npc.change_flu_state(NPC_STATES_FLU.FLU)
            init_npcs.append(npc)
        self.add_NPCs(init_npcs)

    def _get_original_state_metrics(self):
        og_alive = 0
        og_dead = 0
        og_alive += self.num_alive
        og_dead += self.num_dead
        return og_alive, og_dead
    
    def compute_event_probs(self):
        self.event_probs = {
            'burial': 0,
            'recover': 0,
            'pneumonia': 0,
            'incubate': 0,
            'fumes': 0,
            'cough': 0,
            'mutate': 0,
            'turn': 0,
            'devour': 0,
            'bite': 0,
            'fight_back': 0,
            'collapse': 0,
            'rise': 0
        }
        if self.gathering_enabled:
            changes = [#changes to be made to event_multipliers
                ['cough', .25],
                ['incubate', .1],
                ['fight_back', .15],
                ['devour', -.1],
                ['bite', .15]
            ]
            for change in changes:
                self.event_probs[change[0]] += change[1]

        if self.panic_enabled:
            changes = [
                ['incubate', .15],
                ['fight_back', .2],
                ['bite', .25],
                ['turn', .25],
                ['pneumonia', .1]
            ]
            for change in changes:
                self.event_probs[change[0]] += change[1]

        if self.swarm_enabled:
            changes = [
                ['turn', .2],
                ['devour', (self.num_zombie / self.num_moving) * 0.5 if self.num_moving > 0 else 0],
                ['bite', (self.num_zombie / self.num_moving) * 0.5 if self.num_moving > 0 else 0],
                ['fight_back', self.num_zombie * -0.01],
                ['collapse', .05],
                ['rise', .1],
                ['fumes', self.num_dead * .01],
                ['pneumonia', .01]
            ]
                
    def compute_baseline_trans_probs(self):
        self.compute_event_probs()
        self.update_summary_stats()
        trans_probs = {
            'burial': (self.num_active / self.num_dead) * 0.1 if self.num_dead > 0 else 0,  # dead -> ashen
            'recover': 0.25,  # flu -> flu immune
            'pneumonia': 0.01,  # flu -> dead
            'incubate': 0.25,  # incubating -> flu
            'fumes': self.num_dead * 0.01,  # healthy -> incubating
            'cough': self.num_flu / self.num_moving if self.num_moving > 0 else 0,  # healthy -> incubating
            'mutate': 0.01,  # immune -> healthy
            'turn': 0.2,  # zombie bitten -> zombie
            'devour': (self.num_zombie / self.num_moving) * 0.5 if self.num_moving > 0 else 0,  # human -> dead
            'bite': (self.num_zombie / self.num_moving) * 0.5 if self.num_moving > 0 else 0,  # human -> zombie bitten
            'fight_back': self.num_active * 0.01,  # zombie -> dead
            'collapse': 0.1,  # zombie -> dead
            'rise': 0.1  # dead -> zombie
        }
        
        for prob in self.event_probs:
            trans_probs[prob] = max(min(1, trans_probs[prob] + self.event_probs[prob]), 0)
            
        return trans_probs

    def add_NPC(self, NPC):
        self.NPCs.append(NPC)
        self.update_summary_stats()

    def add_NPCs(self, NPCs):
        self.NPCs.extend(NPCs)
        self.update_summary_stats()

    def remove_NPC(self, NPC):
        if NPC in self.NPCs:
            self.NPCs.remove(NPC)
            self.update_summary_stats()
        else:
            print('WARNING: Attempted to remove NPC that did not exist in neighborhood')

    def remove_NPCs(self, NPCs):
        for NPC in NPCs:
            self.remove_NPC(NPC)

    def clean_all_bags(self):
        for npc in self.NPCs:
            npc.clean_bag(self.location)
            
    def add_to_all_human_bags(self, action, amount_to_add): #human is misleading as its just non-zombie
        for npc in self.NPCs:
            if npc.state_zombie is not NPC_STATES_ZOMBIE.ZOMBIE:
                for _ in range(amount_to_add): 
                    npc.add_to_bag(action)
                
    def add_deployment(self, deployment):
        self.deployments.append(deployment)
        
    def add_deployments(self, deployments):
        self.deployments.extend(deployments)

    def destroy_deployments_by_type(self, dep_types):
        self.deployments = [dep for dep in self.deployments if dep not in dep_types]

    def update_summary_stats(self):
        self.num_npcs = len(self.NPCs)
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
        for npc in self.NPCs:
            if npc.state_dead is NPC_STATES_DEAD.ALIVE:
                num_alive += 1
            if npc.state_dead is NPC_STATES_DEAD.DEAD:
                num_dead += 1
            if npc.state_dead is NPC_STATES_DEAD.ASHEN:
                num_ashen += 1
            if npc.state_zombie is NPC_STATES_ZOMBIE.HUMAN:
                num_human += 1
            if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE_BITTEN:
                num_zombie_bitten += 1
            if npc.state_zombie is NPC_STATES_ZOMBIE.ZOMBIE:
                num_zombie += 1
            if npc.state_flu is NPC_STATES_FLU.HEALTHY:
                num_healthy += 1
            if npc.state_flu is NPC_STATES_FLU.INCUBATING:
                num_incubating += 1
            if npc.state_flu is NPC_STATES_FLU.FLU:
                num_flu += 1
            if npc.state_flu is NPC_STATES_FLU.IMMUNE:
                num_immune += 1
            if npc.moving:
                num_moving += 1
            if npc.active:
                num_active += 1
            if npc.sickly:
                num_sickly += 1

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

        total_count_dead = self.num_alive + self.num_dead + self.num_ashen
        total_count_zombie = self.num_human + self.num_zombie_bitten + self.num_zombie
        total_count_flu = self.num_healthy + self.num_incubating + self.num_flu + self.num_immune
        assert (self.num_npcs == total_count_dead)
        assert (self.num_npcs == total_count_zombie)
        assert (self.num_npcs == total_count_flu)

    def getPopulation(self): #Alive Humans (Active and Sickly)
        return self.num_active + self.num_sickly
    
    def get_data(self):
        self.update_summary_stats()
        neighborhood_data = {'id': self.id,
                             'location': self.location,
                             'local_fear': self.local_fear,
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
                             'original_dead': self.orig_dead,
                             'deployments': self.deployments}
        return neighborhood_data

    def checkForEvents(self):
        population = self.getPopulation() #Number of Alive Humans (Both Active and Sickly) as Zombies are also Alive
        if (9 <= population and population > self.num_zombie and 20 >= self.local_fear): #Conditions for gatherings if more alive humans than zombies, there are atleast 9 alive humans, and fear is below 20
            self.gathering_enabled = True
        else:
            self.gathering_enabled = False
        if (population >= 6 and 20 < self.local_fear): #Conditions for panic if fear above 20 and there's enough people to start a panic
            self.panic_enabled = True
        else:
            self.panic_enabled = False
        if (self.num_zombie > 2 * population): #If there's atleast 100% more zombies than alive humans, it can be considered a swarm
            self.swarm_enabled = True
        else:
            self.swarm_enabled = False

if __name__ == '__main__':
    nb = Neighborhood('CENTER', LOCATIONS.CENTER, (LOCATIONS.N, LOCATIONS.S, LOCATIONS.W, LOCATIONS.E), 10)
    print(nb.num_npcs)
