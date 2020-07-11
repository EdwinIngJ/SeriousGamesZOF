from enum import IntEnum
import random
import warnings


class DEPLOYMENTS(IntEnum):
    NONE = 0
    QUARANTINE_OPEN = 1
    QUARANTINE_FENCED = 2
    BITE_CENTER_DISINFECT = 3
    BITE_CENTER_AMPUTATE = 4
    Z_CURE_CENTER_FDA = 5
    Z_CURE_CENTER_EXP = 6
    FLU_VACCINE_OPT = 7
    FLU_VACCINE_MAN = 8
    KILN_OVERSIGHT = 9
    KILN_NO_QUESTIONS = 10
    BROADCAST_DONT_PANIC = 11
    BROADCAST_CALL_TO_ARMS = 12
    SNIPER_TOWER_CONFIRM = 13
    SNIPER_TOWER_FREE = 14
    PHEROMONES_BRAINS = 15
    PHEROMONES_MEAT = 16
    BSL4LAB_SAFETY_ON = 17
    BSL4LAB_SAFETY_OFF = 18
    RALLY_POINT_OPT = 19
    RALLY_POINT_FULL = 20
    FIREBOMB_PRIMED = 21
    FIREBOMB_BARRAGE = 22
    SOCIAL_DISTANCING_SIGNS = 23
    SOCIAL_DISTANCING_CELEBRITY = 24

    @staticmethod
    def print():
        for deployment in DEPLOYMENTS:
            print('{0} -> {1}'.format(deployment.value, deployment.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(DEPLOYMENTS))

    @staticmethod
    def get_value_from_string(deployment):
        if deployment.upper() == 'NONE':
            return DEPLOYMENTS.NONE.value
        elif deployment.upper() == 'QUARANTINE_OPEN':
            return DEPLOYMENTS.QUARANTINE_OPEN.value
        elif deployment.upper() == 'QUARANTINE_FENCED':
            return DEPLOYMENTS.QUARANTINE_FENCED.value
        elif deployment.upper() == 'BITE_CENTER_DISINFECT':
            return DEPLOYMENTS.BITE_CENTER_DISINFECT.value
        elif deployment.upper() == 'BITE_CENTER_AMPUTATE':
            return DEPLOYMENTS.BITE_CENTER_AMPUTATE.value
        elif deployment.upper() == 'Z_CURE_CENTER_FDA':
            return DEPLOYMENTS.Z_CURE_CENTER_FDA.value
        elif deployment.upper() == 'Z_CURE_CENTER_EXP':
            return DEPLOYMENTS.Z_CURE_CENTER_EXP.value
        elif deployment.upper() == 'FLU_VACCINE_OPT':
            return DEPLOYMENTS.FLU_VACCINE_OPT.value
        elif deployment.upper() == 'FLU_VACCINE_MAN':
            return DEPLOYMENTS.FLU_VACCINE_MAN.value
        elif deployment.upper() == 'KILN_OVERSIGHT':
            return DEPLOYMENTS.KILN_OVERSIGHT.value
        elif deployment.upper() == 'KILN_NO_QUESTIONS':
            return DEPLOYMENTS.KILN_NO_QUESTIONS.value
        elif deployment.upper() == 'BROADCAST_DONT_PANIC':
            return DEPLOYMENTS.BROADCAST_DONT_PANIC.value
        elif deployment.upper() == 'BROADCAST_CALL_TO_ARMS':
            return DEPLOYMENTS.BROADCAST_CALL_TO_ARMS.value
        elif deployment.upper() == 'SNIPER_TOWER_CONFIRM':
            return DEPLOYMENTS.SNIPER_TOWER_CONFIRM.value
        elif deployment.upper() == 'SNIPER_TOWER_FREE':
            return DEPLOYMENTS.SNIPER_TOWER_FREE.value
        elif deployment.upper() == 'PHEROMONES_BRAINS':
            return DEPLOYMENTS.PHEROMONES_BRAINS.value
        elif deployment.upper() == 'PHEROMONES_MEAT':
            return DEPLOYMENTS.PHEROMONES_MEAT.value 
        elif deployment.upper() == 'BSL4LAB_SAFETY_ON':
            return DEPLOYMENTS.BSL4LAB_SAFETY_ON.value
        elif deployment.upper() == 'BSL4LAB_SAFETY_OFF':
            return DEPLOYMENTS.BSL4LAB_SAFETY_OFF.value
        elif deployment.upper() == 'RALLY_POINT_OPT':
            return DEPLOYMENTS.RALLY_POINT_OPT.value
        elif deployment.upper() == 'RALLY_POINT_FULL':
            return DEPLOYMENTS.RALLY_POINT_FULL.value
        elif deployment.upper() == 'FIREBOMB_PRIMED':
            return DEPLOYMENTS.FIREBOMB_PRIMED.value
        elif deployment.upper() == 'FIREBOMB_BARRAGE':
            return DEPLOYMENTS.FIREBOMB_BARRAGE.value
        elif deployment.upper() == 'SOCIAL_DISTANCING_SIGNS':
            return DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS.value
        elif deployment.upper() == 'SOCIAL_DISTANCING_CELEBRITY':
            return DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY.value       
        else:
            warnings.warn('Tried to convert string ({}) to DEPLOYMENTS enum and failed; returned NONE'.format(deployment))
            return DEPLOYMENTS.NONE.value

    @staticmethod
    def get_name_from_string(deployment):
        if deployment.upper() == 'NONE':
            return DEPLOYMENTS.NONE.name
        elif deployment.upper() == 'QUARANTINE_OPEN':
            return DEPLOYMENTS.QUARANTINE_OPEN.name
        elif deployment.upper() == 'QUARANTINE_FENCED':
            return DEPLOYMENTS.QUARANTINE_FENCED.name
        elif deployment.upper() == 'BITE_CENTER_DISINFECT':
            return DEPLOYMENTS.BITE_CENTER_DISINFECT.name
        elif deployment.upper() == 'BITE_CENTER_AMPUTATE':
            return DEPLOYMENTS.BITE_CENTER_AMPUTATE.name
        elif deployment.upper() == 'Z_CURE_CENTER_FDA':
            return DEPLOYMENTS.Z_CURE_CENTER_FDA.name
        elif deployment.upper() == 'Z_CURE_CENTER_EXP':
            return DEPLOYMENTS.Z_CURE_CENTER_EXP.name
        elif deployment.upper() == 'FLU_VACCINE_OPT':
            return DEPLOYMENTS.FLU_VACCINE_OPT.name
        elif deployment.upper() == 'FLU_VACCINE_MAN':
            return DEPLOYMENTS.FLU_VACCINE_MAN.name
        elif deployment.upper() == 'KILN_OVERSIGHT':
            return DEPLOYMENTS.KILN_OVERSIGHT.name
        elif deployment.upper() == 'KILN_NO_QUESTIONS':
            return DEPLOYMENTS.KILN_NO_QUESTIONS.name
        elif deployment.upper() == 'BROADCAST_DONT_PANIC':
            return DEPLOYMENTS.BROADCAST_DONT_PANIC.name
        elif deployment.upper() == 'BROADCAST_CALL_TO_ARMS':
            return DEPLOYMENTS.BROADCAST_CALL_TO_ARMS.name
        elif deployment.upper() == 'SNIPER_TOWER_CONFIRM':
            return DEPLOYMENTS.SNIPER_TOWER_CONFIRM.name
        elif deployment.upper() == 'SNIPER_TOWER_FREE':
            return DEPLOYMENTS.SNIPER_TOWER_FREE.name
        elif deployment.upper() == 'PHEROMONES_BRAINS':
            return DEPLOYMENTS.PHEROMONES_BRAINS.name
        elif deployment.upper() == 'PHEROMONES_MEAT':
            return DEPLOYMENTS.PHEROMONES_MEAT.name
        elif deployment.upper() == 'BSL4LAB_SAFETY_ON':
            return DEPLOYMENTS.BSL4LAB_SAFETY_ON.name
        elif deployment.upper() == 'BSL4LAB_SAFETY_OFF':
            return DEPLOYMENTS.BSL4LAB_SAFETY_OFF.name
        elif deployment.upper() == 'RALLY_POINT_OPT':
            return DEPLOYMENTS.RALLY_POINT_OPT.name
        elif deployment.upper() == 'RALLY_POINT_FULL':
            return DEPLOYMENTS.RALLY_POINT_FULL.name
        elif deployment.upper() == 'FIREBOMB_PRIMED':
            return DEPLOYMENTS.FIREBOMB_PRIMED.name
        elif deployment.upper() == 'FIREBOMB_BARRAGE':
            return DEPLOYMENTS.FIREBOMB_BARRAGE.name
        elif deployment.upper() == 'SOCIAL_DISTANCING_SIGNS':
            return DEPLOYMENTS.SOCIAL_DISTANCING_SIGNS.name
        elif deployment.upper() == 'SOCIAL_DISTANCING_CELEBRITY':
            return DEPLOYMENTS.SOCIAL_DISTANCING_CELEBRITY.name
        else:
            warnings.warn('Tried to convert string ({}) to DEPLOYMENTS enum and failed; returned NONE'.format(deployment))
            return DEPLOYMENTS.NONE.name


class LOCATIONS(IntEnum):
    CENTER = 4
    N = 1
    S = 7
    E = 5
    W = 3
    NE = 2
    NW = 0
    SE = 8
    SW = 6

    @staticmethod
    def print():
        for location in LOCATIONS:
            print('{0} -> {1}'.format(location.value, location.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(LOCATIONS))

    @staticmethod
    def get_value_from_string(location):
        if location.upper() == 'CENTER':
            return LOCATIONS.CENTER.value
        elif location.upper() == 'N':
            return LOCATIONS.N.value
        elif location.upper() == 'S':
            return LOCATIONS.S.value
        elif location.upper() == 'E':
            return LOCATIONS.E.value
        elif location.upper() == 'W':
            return LOCATIONS.W.value
        elif location.upper() == 'NE':
            return LOCATIONS.NE.value
        elif location.upper() == 'NW':
            return LOCATIONS.NW.value
        elif location.upper() == 'SE':
            return LOCATIONS.SE.value
        elif location.upper() == 'SW':
            return LOCATIONS.SW.value      
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned CENTER'.format(location))
            return LOCATIONS.CENTER.value

    @staticmethod
    def get_name_from_string(location):
        if location.upper() == 'CENTER':
            return LOCATIONS.CENTER.name
        elif location.upper() == 'N':
            return LOCATIONS.N.name
        elif location.upper() == 'S':
            return LOCATIONS.S.name
        elif location.upper() == 'E':
            return LOCATIONS.E.name
        elif location.upper() == 'W':
            return LOCATIONS.W.name
        elif location.upper() == 'NE':
            return LOCATIONS.NE.name
        elif location.upper() == 'NW':
            return LOCATIONS.NW.name
        elif location.upper() == 'SE':
            return LOCATIONS.SE.name
        elif location.upper() == 'SW':
            return LOCATIONS.SW.name
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned CENTER'.format(location))
            return LOCATIONS.CENTER.name
