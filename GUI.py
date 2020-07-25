from tkinter import*
import json
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS

class GUI():
    def __init__(self, root, zgame):
        self.GAME_ID = zgame.GAME_ID
        print('Starting new game with human play!')
        #Variables for tkinter GUI
        self.root = root
        #Variables for Game
        self.env = zgame.env
        self.env.reset()
        self.DATA_LOG_FILE_NAME = zgame.DATA_LOG_FILE_NAME
        self.turn = zgame.turn
        self.max_turns = zgame.max_turns
        self.neighborhoods, self.score, self.total_score, self.fear, self.resources, self.orig_alive, self.orig_dead = self.env.render(mode='human')
        self.temp_data = {}
        self.turn_description_info = []
        self.turn_desc_log_index = -1
        self.deployments_action = []
        self.locations_action = []
        #Constants
        self.HEIGHT = 620
        self.WIDTH  = 1250
        canvas = Canvas(self.root, height= self.HEIGHT, width= self.WIDTH)
        canvas.pack()
        self.create_screen()

    def create_screen(self):
        #Creates the background for the GUI
        back_frame = Frame(self.root, bg = "#263D42", bd = 5) #hex teal blue
        back_frame.place(relx = 0.5, rely= 0.01, relwidth= 1, relheight= 0.97, anchor = 'n')

        TitleCard = Label(back_frame, text="Zombies or Flu", font=('Courier', 18))
        TitleCard.place(relx=0.5, rely=0.001, relwidth=0.49, relheight=0.075, anchor='n')  # header with game title

        ###Notification Bar###
        self.NotifBar = Button(back_frame, font=('Courier', 9), command = lambda: self.open_log())
        self.NotifBar.place(relx=0.5, rely=0.08, relwidth=0.49, relheight=0.025, anchor='n')

        #Label for turn counter
        Turn = Label(back_frame, text = ' Turn: {0} of {1}'.format(self.turn, self.max_turns) , font = ('Courier', 8))
        Turn.place(relx = 0.75, rely = 0.001, relwidth = 0.1, relheight = 0.05) 

        #Label for total score
        Score = Label(back_frame, text = 'Turn Score:{0}(Total Score: {1})'.format(self.score, self.total_score), font = ('Courier', 7), justify = 'left')
        Score.place(relx = 0.853, rely = 0.001, relwidth = 0.135, relheight = 0.05) 

        #Label for fear counter
        Fear = Label(back_frame, text = ' Fear: {}'.format(self.fear), font = ('Courier', 10))
        Fear.place(relx =0.75, rely = 0.055, relwidth = 0.239, relheight = 0.05) 

        #Frame to hold the 25 Deployment buttons
        DeployFrame = Label(back_frame, bg = 'gray', bd = 5)
        DeployFrame.place(relwidth= 0.25, relheight= 0.99) 

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
        self.information = [["Active"] + [self.env.city.show_data(nbh.local_fear, nbh.num_active) for nbh in self.neighborhoods],
            ["Sickly"] + [self.env.city.show_data(nbh.local_fear, nbh.num_sickly) for nbh in self.neighborhoods],
            ["Zombies"] + [self.env.city.show_data(nbh.local_fear, nbh.num_zombie) for nbh in self.neighborhoods],
            ["Dead"] + [self.env.city.show_data(nbh.local_fear, nbh.num_dead) for nbh in self.neighborhoods],
            ["Living at Start"] + [nbh.orig_alive for nbh in self.neighborhoods],
            ["Dead at Start"] + [nbh.orig_dead for nbh in self.neighborhoods],
            ["Local Fear"] + [nbh.local_fear for nbh in self.neighborhoods]]

        #Formats the information to display
        formatted_information = []
        for i in range(len(self.neighborhoods)):
            text = ''
            for elem in self.information:
                text += '{}: {}'.format(elem[0], elem[i+1]) + '\n'
            formatted_information.append(text)

        CityFrame = Frame(self.root, bg = 'gray', bd = 5)
        CityFrame.place(relx = 0.255, rely = 0.13, relwidth = 0.725, relheight = 0.83) #Frame to hold all 9 City labels

        NWest = Button(CityFrame, text = formatted_information[0], command=lambda x=LOCATIONS.NW.value:self.add_location(x), bd = 5)
        NWest.place(relwidth = 0.33, relheight = 0.33)

        North = Button(CityFrame, text = formatted_information[1], command=lambda x=LOCATIONS.N.value:self.add_location(x), bd = 5)
        North.place(relx = 0.335, relwidth = 0.33, relheight = 0.33)

        NEast = Button(CityFrame, text = formatted_information[2], command=lambda x=LOCATIONS.NE.value:self.add_location(x), bd = 5)
        NEast.place(relx = 0.669, relwidth = 0.33, relheight = 0.33)

        West = Button(CityFrame, text = formatted_information[3], command=lambda x=LOCATIONS.W.value:self.add_location(x), bd = 5)
        West.place(rely = 0.335, relwidth =  0.33, relheight = 0.33)

        Center = Button(CityFrame, text = formatted_information[4], command=lambda x=LOCATIONS.CENTER.value:self.add_location(x), bd = 5)
        Center.place(relx = 0.335, rely = 0.335, relwidth = 0.33, relheight = 0.33)

        East = Button(CityFrame, text = formatted_information[5], command=lambda x=LOCATIONS.E.value:self.add_location(x), bd = 5)
        East.place(relx = 0.669, rely = 0.335, relwidth = 0.33, relheight = 0.33)

        SWest = Button(CityFrame, text = formatted_information[6], command=lambda x=LOCATIONS.SW.value:self.add_location(x), bd = 5)
        SWest.place(rely = 0.67, relwidth = 0.33, relheight = 0.33)

        South = Button(CityFrame, text = formatted_information[7], command=lambda x=LOCATIONS.S.value:self.add_location(x), bd = 5)
        South.place(relx = 0.335, rely = 0.67, relwidth = 0.33, relheight = 0.33)

        SEast = Button(CityFrame, text = formatted_information[8], command=lambda x=LOCATIONS.SE.value:self.add_location(x), bd = 5)
        SEast.place(relx = 0.669, rely = 0.67, relwidth = 0.33, relheight = 0.33)

    def add_deployment(self, deployment):
        if self.turn < self.max_turns:
            #Adds deployments to deployments list cant exceed 2 actions per turn
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
        if self.turn < self.max_turns:
            #Adds locations to locations list cant exceed 2 actions per turn
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

    def open_log(self): 
        #Creates the data logs
        ###The notif bar opens the data log
        if self.turn > 0:
            top = Toplevel()
            top.title('Log')
            data_log = self.get_turn_desc()
            turn_num = Label(top, text = "End of Turn: {}".format(data_log[self.turn_desc_log_index]["Global"][0]), bd = 5)
            turn_num.grid(row=0)

            #Global stats
            score_turn_desc = Label(top, text = 'Total Score: {}    {}'.format(data_log[self.turn_desc_log_index]["Global"][1], 
            data_log[self.turn_desc_log_index]["delta_Global"][1] if data_log[self.turn_desc_log_index]["delta_Global"][1] < 0 else "+" 
            + str(data_log[self.turn_desc_log_index]["delta_Global"][1])), bd = 5)
            score_turn_desc.grid(row = 1, column = 0) 

            fear_turn_desc = Label(top, text = 'Fear: {}    {}'.format(data_log[self.turn_desc_log_index]["Global"][2], 
            data_log[self.turn_desc_log_index]["delta_Global"][2] if data_log[self.turn_desc_log_index]["delta_Global"][2] < 0 else "+" 
            + str(data_log[self.turn_desc_log_index]["delta_Global"][2])), bd = 5)
            fear_turn_desc.grid(row = 1, column = 1)

            resource_turn_desc = Label(top, text = 'Resources: {}    {}'.format(data_log[self.turn_desc_log_index]["Global"][3], 
            data_log[self.turn_desc_log_index]["delta_Global"][3] if data_log[self.turn_desc_log_index]["delta_Global"][3] < 0 else "+" 
            + str(data_log[self.turn_desc_log_index]["delta_Global"][3])), bd = 5)
            resource_turn_desc.grid(row = 1, column = 2)

            def format_for_grid(nbh_name):
                var_names = ["Active","Sickly","Zombies","Dead","Living at Start","Dead at Start","Local Fear"]
                text = ''
                for i in range(len(data_log[self.turn_desc_log_index][nbh_name])):
                    text += '{} : {}       {}'.format(var_names[i], data_log[self.turn_desc_log_index][nbh_name][i], data_log[self.turn_desc_log_index]["delta_"+nbh_name][i] if data_log[self.turn_desc_log_index]["delta_"+nbh_name][i] < 0 else "+" + str(data_log[self.turn_desc_log_index]["delta_"+nbh_name][i])) + '\n'
                return text

            NWest_turn_desc = Label(top, text = format_for_grid(LOCATIONS.NW.name), bd = 5)
            NWest_turn_desc.grid(row = 2, column = 0)

            North_turn_desc = Label(top, text = format_for_grid(LOCATIONS.N.name), bd = 5)
            North_turn_desc.grid(row = 2, column = 1)

            NEast_turn_desc = Label(top, text = format_for_grid(LOCATIONS.NE.name), bd = 5)
            NEast_turn_desc.grid(row = 2, column = 2)

            West_turn_desc = Label(top, text = format_for_grid(LOCATIONS.W.name), bd = 5)
            West_turn_desc.grid(row = 3, column = 0)

            Center_turn_desc = Label(top, text = format_for_grid(LOCATIONS.CENTER.name), bd = 5)
            Center_turn_desc.grid(row = 3, column = 1)

            East_turn_desc = Label(top, text = format_for_grid(LOCATIONS.E.name), bd = 5)
            East_turn_desc.grid(row = 3, column = 2)

            SWest_turn_desc = Label(top, text = format_for_grid(LOCATIONS.SW.name), bd = 5)
            SWest_turn_desc.grid(row = 4, column = 0)

            South_turn_desc = Label(top, text = format_for_grid(LOCATIONS.S.name), bd = 5)
            South_turn_desc.grid(row = 4, column = 1)

            SEast_turn_desc = Label(top, text = format_for_grid(LOCATIONS.SE.name), bd = 5)
            SEast_turn_desc.grid(row = 4, column = 2)

            action_turn_desc_text = "You deployed {} in {} \n".format(DEPLOYMENTS(data_log[self.turn_desc_log_index]["actions"][0][0]).name,LOCATIONS(data_log[self.turn_desc_log_index]["actions"][1][0]).name)
            action_turn_desc_text += "You then deployed {} in {}".format(DEPLOYMENTS(data_log[self.turn_desc_log_index]["actions"][0][1]).name,LOCATIONS(data_log[self.turn_desc_log_index]["actions"][1][1]).name)
            action_turn_desc = Label(top, text = action_turn_desc_text, bd = 5)
            action_turn_desc.grid(row = 5, column = 0, columnspan = 2)

            events_turn_desc_text = "Events:"
            events_turn_desc = Label(top, text = events_turn_desc_text, bd = 5)
            events_turn_desc.grid(row = 2, column = 4, sticky = N)

            prev_button = Button(top, text = "Previous", command=lambda: self.prev_log(), bd = 5)
            prev_button.grid(row = 6, column = 0)

            next_button = Button(top, text = "Next", command=lambda:self.next_log(), bd = 5)
            next_button.grid(row = 6, column = 1)
 
        else:
            self.NotifBar['text'] = "No Turn Description Available"
    
    def prev_log(self):
        #Button to iterate through past data logs
        if len(self.turn_description_info)*-1 < self.turn_desc_log_index:
            self.turn_desc_log_index -= 1
            self.open_log()
    
    def next_log(self):
        current_index = self.turn_desc_log_index
        if current_index < -1:
            self.turn_desc_log_index += 1
            self.open_log()

    def _get_turn_desc_data(self):
        ##Gets data for the data log
        #Capture Global Data
        turn_desc_data = {}
        turn_desc_data["Global"] = [self.turn, self.total_score,self.fear,self.resources]
        #Capture Neighborhood Data
        for i in range(len(self.neighborhoods)):
            nbh = self.neighborhoods[i]
            turn_desc_data[nbh.location.name] = [stat[i+1] for stat in self.information]
        return turn_desc_data

    
    def _create_turn_desc(self, prev_stats, curr_stats):
        turn_desc_container = {}
        #Calculates the changes and adds them to the dictionary along with the statistics for that turn
        #To add: events
        for k, v in prev_stats.items():
            turn_desc_container["delta_"+k] = [curr_stats[k][i]-v[i] for i in range(len(v))]
        turn_desc_container.update(prev_stats)
        turn_desc_container.update({"actions" : [self.deployments_action]+[self.locations_action]})
        self.turn_description_info.append(turn_desc_container)

    def get_turn_desc(self):
        return self.turn_description_info

    def _do_turn(self):
        self.temp_data = self._get_turn_desc_data()
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
        self._create_turn_desc(self.temp_data,self._get_turn_desc_data())
        self.turn_desc_log_index = -1
        self.deployments_action = []
        self.locations_action = []

    def update_screen(self):
        self.neighborhoods, self.score, self.total_score, self.fear, self.resources, self.orig_alive, self.orig_dead = self.env.render(mode='human')
        self.create_screen()

    def summary_screen(self):
        #self.root.winfo_children()[0].quit()
        pass

    def done(self):
        print("Episode finished after {} turns".format(self.turn))
        self.summary_screen()
        self._cleanup()

    def _cleanup(self):
        self.env.close()