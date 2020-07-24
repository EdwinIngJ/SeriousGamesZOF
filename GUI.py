from tkinter import*
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS

class GUI(Frame):
    def __init__(self, root, zgame):
        super().__init__(root)
        self.root = root
        print('Starting new game with human play!')
        self.env = zgame.env
        self.env.reset()
        self.turn = zgame.turn
        self.max_turns = zgame.max_turns
        self.neighborhoods, self.score, self.total_score, self.fear, self.orig_alive, self.orig_dead = self.env.render(mode='human')
        #Constants
        self.HEIGHT = 620
        self.WIDTH  = 1250
        self.create_screen()
        self.deployments_action = []
        self.locations_actions = []

    def create_screen(self):
        canvas = Canvas(self.root, height= self.HEIGHT, width= self.WIDTH)
        canvas.pack()

        frame = Frame(self.root, bg = "#263D42", bd = 5) #hex teal blue
        frame.place(relx = 0.5, rely= 0.01, relwidth= 1, relheight= 0.97, anchor = 'n')

        TitleCard = Label(frame, text = "Zombies or Flu", font = ('Courier', 18))
        TitleCard.place(relx = 0.5, rely = 0.001, relwidth = 0.49, relheight  = 0.1, anchor = 'n') #header with game title

        Turn = Label(frame, text = 'Turn: ', font = ('Courier', 12))
        Turn.place(relx = 0.75, rely = 0.001, relwidth = 0.1, relheight = 0.05) #Label for turn counter

        Score = Label(frame, text = 'Score: ', font = ('Courier', 12))
        Score.place(relx = 0.853, rely = 0.001, relwidth = 0.1, relheight = 0.05) #Label for total score

        Fear = Label(frame, text = 'Fear: ', font = ('Courier', 12))
        Fear.place(relx =0.75, rely = 0.055, relwidth = 0.204, relheight = 0.05) #Label for fear counter

        CityFrame = Frame(self.root, bg = 'gray', bd = 5)
        CityFrame.place(relx = 0.255, rely = 0.13, relwidth = 0.725, relheight = 0.83) #Frame to hold all 9 City labels
        self.create_neighborhoods()

    def create_neighborhoods(self):
        ### The 9 Neighborhoods ###
        # Include city stats
        def add_under_location_symbol_text(information): #2-D Array of [[statistic_name, data for each neighborhood in one row] for each statistic]
            text = ""
            for statistic_type in information:
                for nbh_information in statistic_type[1:]:
                    text += PBack.blue + '==' + PBack.reset + ' {}: {}'.format(statistic_type[0], nbh_information).ljust(28)
                text += PBack.blue + '==' + PBack.reset + '\n'
            return text
        def location_line_symbol_text(information): #Array of [top line statistic_name, (data, neighborhood symbol) for each neighborhood in one row]
            text = ""
            for nbh_information in information[1:]:
                text += PBack.blue + '==' + PBack.reset + ' {}: {}'.format(information[0], nbh_information[0]).ljust(23) + \
                        PFont.bold + PFont.underline + PFore.purple + '{}'.format(nbh_information[1]) + PControl.reset + ' '
            text += PBack.blue + '==' + PBack.reset + '\n'
            return text
        def city_status(information): # 2-D Array of [[statistic_name, data for nbh1, data for nbh2, ...] for each statistic]
            symbols = ["  ", "(NW)", " (N)", "(NE)", " (W)", " (C)", " (E)", "(SW)", " (S)", "(SE)"]
            information_top_location_line = [information[0][0]] + [(information[0][i], symbols[i]) for i in range(1,4)]
            information_top_statistics = [([information[i][0]] + [information[i][j] for j in range(1,4)]) for i in range(1,len(information))]
            information_center_location_line = [information[0][0]] + [(information[0][i], symbols[i]) for i in range(4,7)]
            information_center_statistics = [([information[i][0]] + [information[i][j] for j in range(4,7)]) for i in range(1,len(information))]
            information_bottom_location_line = [information[0][0]] + [(information[0][i], symbols[i]) for i in range(7,10)]
            information_bottom_statistics = [([information[i][0]] + [information[i][j] for j in range(7,10)]) for i in range(1,len(information))]

            text = PBack.blue + '=====================================  CITY STATUS  ========================================' + PBack.reset + '\n'
            text += location_line_symbol_text(information_top_location_line)
            text += add_under_location_symbol_text(information_top_statistics)
            text += PBack.blue + '============================================================================================' + PBack.reset + '\n'
            text += location_line_symbol_text(information_center_location_line)
            text += add_under_location_symbol_text(information_center_statistics)
            text += PBack.blue + '============================================================================================' + PBack.reset + '\n'
            text += location_line_symbol_text(information_bottom_location_line)
            text += add_under_location_symbol_text(information_bottom_statistics)
            text += PBack.blue + '============================================================================================' + PBack.reset + '\n'
            return text
            
        #Information is what's printed for each neighborhood
        #It should be in the form of [statistic_name, statistc data for neighborhoodNW, N, NE, W, ...

        information = [["Active"] + [self._show_data(nbh.num_active) for nbh in self.neighborhoods],
            ["Sickly"] + [self._show_data(nbh.num_sickly) for nbh in self.neighborhoods],
            ["Zombies"] + [self._show_data(nbh.num_zombie) for nbh in self.neighborhoods],
            ["Dead"] + [self._show_data(nbh.num_dead) for nbh in self.neighborhoods],
            ["Living at Start"] + [nbh.orig_alive for nbh in self.neighborhoods],
            ["Dead at Start"] + [nbh.orig_dead for nbh in self.neighborhoods],
            ["Local Fear"] + [nbh.local_fear for nbh in self.neighborhoods]]
        city = city_status(information)

        for i in len(self.neighborhoods):
            


        NWest = Label(CityFrame, text = 'hi', bd = 5)
        NWest.place(relwidth = 0.33, relheight = 0.33)

        North = Label(CityFrame, text = 'hi', bd = 5)
        North.place(relx = 0.335, relwidth = 0.33, relheight = 0.33)

        NEast = Label(CityFrame, text = 'hi', bd = 5)
        NEast.place(relx = 0.669, relwidth = 0.33, relheight = 0.33)

        West = Label(CityFrame, text = 'hi', bd = 5)
        West.place(rely = 0.335, relwidth =  0.33, relheight = 0.33)

        Center = Label(CityFrame, text = 'hi', bd = 5)
        Center.place(relx = 0.335, rely = 0.335, relwidth = 0.33, relheight = 0.33)

        East = Label(CityFrame, text = 'hi', bd = 5)
        East.place(relx = 0.669, rely = 0.335, relwidth = 0.33, relheight = 0.33)

        SWest = Label(CityFrame, text = 'hi', bd = 5)
        SWest.place(rely = 0.67, relwidth = 0.33, relheight = 0.33)

        South = Label(CityFrame, text = 'hi', bd = 5)
        South.place(relx = 0.335, rely = 0.67, relwidth = 0.33, relheight = 0.33)

        SEast = Label(CityFrame, text = 'hi', bd = 5)
        SEast.place(relx = 0.669, rely = 0.67, relwidth = 0.33, relheight = 0.33)

        DeployFrame = Label(frame, bg = 'gray', bd = 5)
        DeployFrame.place(relwidth= 0.25, relheight= 0.99) #frame to hold the 25 Deployment buttons

        ###The 25 Buttons ###

        for i in range(25):
            button = Button(DeployFrame, text = DEPLOYMENTS(i).name, font = ('Courier', 7))
            button.place(rely = i * 0.04, relwidth = 1)
    def add_deployment(self, deployments):
        if len(self.deployments_action) < 2:
            self.deployments_action.append(deployments)
        else:

    def add_location(self, location):
        if len(self.locations_actions) < 2:
            self.locations_action.append(deployments)
        else:
             

    def update_screen(self):
        self.neighborhoods, self.score, self.total_score, self.fear, self.orig_alive, self.orig_dead = self.env.render(mode='human')

# Build up console output
        header = pf.figlet_format('ZGame Status')
        fbuffer = PBack.red + '--------------------------------------------------------------------------------------------' + PBack.reset + '\n' + header + \
                  PBack.red + '********************************************************************************************' + PBack.reset + '\n'
        ebuffer = PBack.red + '********************************************************************************************' + PBack.reset + '\n' + \
                  PBack.red + '--------------------------------------------------------------------------------------------' + PBack.reset + '\n'

        fancy_string = PControl.cls + PControl.home + fbuffer

        # Include global stats
        global_stats = PBack.purple + '#####################################  GLOBAL STATUS  ######################################' + PBack.reset + '\n'
        global_stats += ' Turn: {0} of {1}'.format(self.turn, self.max_turns).ljust(42) + 'Turn Score: {0} (Total Score: {1})'.format(self.get_score(), self.total_score) + '\n'
        global_stats += ' Fear: {}'.format(self.fear).ljust(42) + 'Living at Start: {}'.format(self.orig_alive) + '\n'
        global_stats += ' Resources: {}'.format(self.resources).ljust(42) + 'Dead at Start: {}'.format(self.orig_dead) + '\n'
        global_stats += PBack.purple + '############################################################################################' + PBack.reset + '\n'
        fancy_string += global_stats

        

        
        fancy_string += city

        # Close out console output
        fancy_string += ebuffer
        print(fancy_string)
        return fancy_string



        for turn in range(self.max_turns):
            self.env.print_player_action_selections()

            location_1 = self._read_action("location", "1")
            deployment_1 = self._read_action("deployment", "1")
            location_2 = self._read_action("location", "2")
            deployment_2 = self._read_action("deployment", "2")
                
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

        print("Started GUI!")
