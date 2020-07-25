from tkinter import*
import json
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS

class GUI(Frame):
    def __init__(self, root, zgame):
        super().__init__(root)
        self.root = root
        print('Starting new game with human play!')
        self.env = zgame.env
        self.DATA_LOG_FILE_NAME = zgame.DATA_LOG_FILE_NAME
        self.GAME_ID = zgame.GAME_ID
        self.env.reset()
        self.turn = zgame.turn
        self.max_turns = zgame.max_turns
        self.neighborhoods, self.score, self.total_score, self.fear, self.orig_alive, self.orig_dead, self.turn_description_info = self.env.render(mode='human')
        self.deployments_action = []
        self.locations_action = []
        #Constants
        self.HEIGHT = 620
        self.WIDTH  = 1250
        canvas = Canvas(self.root, height= self.HEIGHT, width= self.WIDTH)
        canvas.pack()
        self.create_screen()

    def create_screen(self):
        frame = Frame(self.root, bg = "#263D42", bd = 5) #hex teal blue
        frame.place(relx = 0.5, rely= 0.01, relwidth= 1, relheight= 0.97, anchor = 'n')

        TitleCard = Label(frame, text="Zombies or Flu", font=('Courier', 18))
        TitleCard.place(relx=0.5, rely=0.001, relwidth=0.49, relheight=0.075, anchor='n')  # header with game title

        ###Notification Bar###
        self.NotifBar = Button(frame, font=('Courier', 9), command = lambda: self.open_log())
        self.NotifBar.place(relx=0.5, rely=0.08, relwidth=0.49, relheight=0.025, anchor='n')

        Turn = Label(frame, text = ' Turn: {0} of {1}'.format(self.turn, self.max_turns) , font = ('Courier', 8))
        Turn.place(relx = 0.75, rely = 0.001, relwidth = 0.1, relheight = 0.05) #Label for turn counter

        Score = Label(frame, text = 'Turn Score:{0}(Total Score: {1})'.format(self.score, self.total_score), font = ('Courier', 7), justify = 'left')
        Score.place(relx = 0.853, rely = 0.001, relwidth = 0.135, relheight = 0.05) #Label for total score

        Fear = Label(frame, text = ' Fear: {}'.format(self.fear), font = ('Courier', 10))
        Fear.place(relx =0.75, rely = 0.055, relwidth = 0.239, relheight = 0.05) #Label for fear counter

        DeployFrame = Label(frame, bg = 'gray', bd = 5)
        DeployFrame.place(relwidth= 0.25, relheight= 0.99) #frame to hold the 25 Deployment buttons

        ###The 25 Deployment Buttons ###
        for i in range(25):
            button = Button(DeployFrame, text = DEPLOYMENTS(i).name, font = ('Courier', 7), command=lambda x=i:self.add_deployment(x))
            button.place(rely = i * 0.04, relwidth = 1)
            
        self.create_neighborhoods()

    def create_neighborhoods(self):
        ### The 9 Neighborhoods ###
        #Include city stats
        #Information is what's printed for each neighborhood
        #It should be in the form of [statistic_name, statistc data for neighborhoodNW, N, NE, W, ...
        information = [["Active"] + [self.env.city.show_data(nbh, nbh.local_fear, nbh.num_active) for nbh in self.neighborhoods],
            ["Sickly"] + [self.env.city.show_data(nbh, nbh.local_fear, nbh.num_sickly) for nbh in self.neighborhoods],
            ["Zombies"] + [self.env.city.show_data(nbh, nbh.local_fear, nbh.num_zombie) for nbh in self.neighborhoods],
            ["Dead"] + [self.env.city.show_data(nbh, nbh.local_fear, nbh.num_dead) for nbh in self.neighborhoods],
            ["Dead Ashen"] + [self.env.city.show_data(nbh, nbh.local_fear, nbh.num_ashen) for nbh in self.neighborhoods],
            ["Living at Start"] + [nbh.orig_alive for nbh in self.neighborhoods],
            ["Dead at Start"] + [nbh.orig_dead for nbh in self.neighborhoods],
            ["Local Fear"] + [nbh.local_fear for nbh in self.neighborhoods]]

        formated_information = []
        for i in range(len(self.neighborhoods)):
            text = ''
            for elem in information:
                text += '{}: {}'.format(elem[0], elem[i+1]) + '\n'
            formated_information.append(text)

        CityFrame = Frame(self.root, bg = 'gray', bd = 5)
        CityFrame.place(relx = 0.255, rely = 0.13, relwidth = 0.725, relheight = 0.83) #Frame to hold all 9 City labels

        NWest = Button(CityFrame, text = formated_information[0], command=lambda x=LOCATIONS.NW.value:self.add_location(x), bd = 5)
        NWest.place(relwidth = 0.33, relheight = 0.33)

        North = Button(CityFrame, text = formated_information[1], command=lambda x=LOCATIONS.N.value:self.add_location(x), bd = 5)
        North.place(relx = 0.335, relwidth = 0.33, relheight = 0.33)

        NEast = Button(CityFrame, text = formated_information[2], command=lambda x=LOCATIONS.NE.value:self.add_location(x), bd = 5)
        NEast.place(relx = 0.669, relwidth = 0.33, relheight = 0.33)

        West = Button(CityFrame, text = formated_information[3], command=lambda x=LOCATIONS.W.value:self.add_location(x), bd = 5)
        West.place(rely = 0.335, relwidth =  0.33, relheight = 0.33)

        Center = Button(CityFrame, text = formated_information[4], command=lambda x=LOCATIONS.CENTER.value:self.add_location(x), bd = 5)
        Center.place(relx = 0.335, rely = 0.335, relwidth = 0.33, relheight = 0.33)

        East = Button(CityFrame, text = formated_information[5], command=lambda x=LOCATIONS.E.value:self.add_location(x), bd = 5)
        East.place(relx = 0.669, rely = 0.335, relwidth = 0.33, relheight = 0.33)

        SWest = Button(CityFrame, text = formated_information[6], command=lambda x=LOCATIONS.SW.value:self.add_location(x), bd = 5)
        SWest.place(rely = 0.67, relwidth = 0.33, relheight = 0.33)

        South = Button(CityFrame, text = formated_information[7], command=lambda x=LOCATIONS.S.value:self.add_location(x), bd = 5)
        South.place(relx = 0.335, rely = 0.67, relwidth = 0.33, relheight = 0.33)

        SEast = Button(CityFrame, text = formated_information[8], command=lambda x=LOCATIONS.SE.value:self.add_location(x), bd = 5)
        SEast.place(relx = 0.669, rely = 0.67, relwidth = 0.33, relheight = 0.33)

    def add_deployment(self, deployment):
        num_d = len(self.deployments_action)
        num_l = len(self.locations_action)
        if  num_d == 0:
            self.deployments_action.append(deployment)
        elif num_d == 1 and num_l < 2 :
            self.deployments_action.append(deployment)
        elif num_d  == 1 and num_l == 2 :
            self.deployments_action.append(deployment)
            self._do_turn()
        print(self.deployments_action)

        self.NotifBar['text'] = "Deployment:  " + DEPLOYMENTS(deployment).name

    def add_location(self, location):
        num_d = len(self.deployments_action)
        num_l = len(self.locations_action)
        if  num_l == 0:
            self.locations_action.append(location)
        elif num_l == 1 and num_d < 2 :
            self.locations_action.append(location)
        elif num_l  == 1 and num_d == 2 :
            self.locations_action.append(location)
            self._do_turn()
        print(self.locations_action)

        self.NotifBar['text'] = " Location: " + LOCATIONS(location).name

    def open_log(self): ###the notif bar opens the data log
        if self.turn > 0:
            top = Toplevel()
            top.title('Log')
            data_log = self.turn_description_info
            Turn_num = Label(top, text = data_log[-1]["Global"][0], bd = 5)
            Turn_num.grid(row=0)

            def format_for_grid(nbh_name):
                var_names = ["Active","Sickly","Zombies","Dead","Living at Start","Dead at Start","Local Fear"]
                text = ''
                for i in range(len(data_log[-1][nbh_name])):
                    text += '{} : {}'.format(var_names[i], data_log[-1][nbh_name][i]) + '\n'
                return text

            NWest_turn_desc = Label(top, text = format_for_grid(LOCATIONS.NW.name), bd = 5)
            NWest_turn_desc.grid(row = 1, column = 0)

            North_turn_desc = Label(top, text = format_for_grid(LOCATIONS.N.name), bd = 5)
            North_turn_desc.grid(row = 1, column = 1)

            NEast_turn_desc = Label(top, text = format_for_grid(LOCATIONS.NE.name), bd = 5)
            NEast_turn_desc.grid(row = 1, column = 2)

            West_turn_desc = Label(top, text = format_for_grid(LOCATIONS.W.name), bd = 5)
            West_turn_desc.grid(row = 2, column = 0)

            Center_turn_desc = Label(top, text = format_for_grid(LOCATIONS.CENTER.name), bd = 5)
            Center_turn_desc.grid(row = 2, column = 1)

            East_turn_desc = Label(top, text = format_for_grid(LOCATIONS.E.name), bd = 5)
            East_turn_desc.grid(row = 2, column = 2)

            SWest_turn_desc = Label(top, text = format_for_grid(LOCATIONS.SW.name), bd = 5)
            SWest_turn_desc.grid(row = 3, column = 0)

            South_turn_desc = Label(top, text = format_for_grid(LOCATIONS.S.name), bd = 5)
            South_turn_desc.grid(row = 3, column = 1)

            SEast_turn_desc = Label(top, text = format_for_grid(LOCATIONS.SE.name), bd = 5)
            SEast_turn_desc.grid(row = 3, column = 2)
        else:
            pass
        
    def _do_turn(self):
        actions = self.env.encode_raw_action(location_1=LOCATIONS(self.locations_action[0]),
                                                 deployment_1=DEPLOYMENTS(self.deployments_action[0]),
                                                 location_2=LOCATIONS(self.locations_action[1]),
                                                 deployment_2=DEPLOYMENTS(self.deployments_action[1]))
        observation, reward, done, info = self.env.step(actions)
        
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

        self.update_screen()
    
    def update_screen(self):
        self.neighborhoods, self.score, self.total_score, self.fear, self.orig_alive, self.orig_dead, self.turn_description_info = self.env.render(mode='human')
        self.create_screen()
        self.deployments_action = []
        self.locations_action = []

    def done(self):
        print("Episode finished after {} turns".format(self.turn))
        self._cleanup()

    def _cleanup(self):
        self.env.close()
            
