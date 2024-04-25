############################################################################################################
# EVCHARGING for appdaemon add_on (Home Assistant)
# Author : Gerard Mamelle (2024)
# Version : 1.0.0
# Program under MIT licence
############################################################################################################
import hassapi as hass

# Programme principal
class EVCharging(hass.Hass):

    def initialize(self):
        self.use_battery_level = bool(self.args['use_battery_level'] == 'oui')
        self.heure_creuse = self.get_state(self.args["heure_creuse"])
        self.solar_optimizer = self.get_state(self.args["enable_solar_optimizer"])
        self.start_ev_charging= self.get_state(self.args["start_ev_charging"])
        if self.use_battery_level:
            self.battery_level = self.get_state(self.args["battery_level"])
            self.battery_level_max = self.get_state(self.args["battery_level_max"])
        else:
            self.battery_level = 0
            self.battery_level_max = 100

        # Init listen for charge bmw events
        self.listen_state(self.change_heure_creuse,self.args["heure_creuse"])
        self.listen_state(self.change_command_ev_charging,self.args["command_ev_charging"])
        self.listen_state(self.change_enable_solaroptimizer,self.args["enable_solar_optimizer"])  # status optimizer
        self.listen_state(self.change_start_ev_charging,self.args["start_ev_charging"])  # demande de demarrage de la pac par l'optimizer
        if self.use_battery_level:
            self.listen_state(self.change_battery_level,self.args["battery_level"])  # demande de demarrage de la pac par l'optimizer
            self.listen_state(self.change_battery_level_max,self.args["battery_level_max"])  # demande de demarrage de la pac par l'optimizer

        self.check_ev_charging()

        # Initialisation terminee 
        self.log('EV Charging module initialized OK')
    
    # Declenchement des heures creuses, mise en route de la charge_bmw
    def change_heure_creuse(self, entity, attribute, old_state, new_state, kwargs):
        if new_state == 'unavailable':
            return
        self.heure_creuse = new_state 
        self.check_ev_charging()
    
    # Modification du statut de l'optimisation d'energie 
    def change_enable_solaroptimizer(self, entity, attribute, old_state, new_state, kwargs):
        self.log(f'Solar optimizer = {new_state}')
        self.solar_optimizer = new_state
        self.check_ev_charging()
    
    # demande de demarrage de la charge par solar optimizer
    def change_start_ev_charging(self, entity, attribute, old_state, new_state, kwargs):
        self.log(f'Start charge = {new_state}')
        self.start_ev_charging= new_state
        self.check_ev_charging()

    # modification du niveau de charge de la batterie
    def change_battery_level(self, entity, attribute, old_state, new_state, kwargs):
        self.battery_level = new_state

    # modification du niveau de charge de la batterie
    def change_battery_level_max(self, entity, attribute, old_state, new_state, kwargs):
        self.battery_level_max = new_state

   # Mise en route ou arret manuel de la charge_bmw
    def change_command_ev_charging(self, entity, attribute, old_state, new_state, kwargs):
        if new_state == 'on': 
            self.turn_on(self.args['command_ev_charging'])
            self.log("Demarrage charge")
        else:
            self.turn_off(self.args['command_ev_charging'])
            self.log("Arret charge")
    
    # Regulation de la charge
    def check_ev_charging(self):
        # Regulation de jour en fonction de l'ensoleillement et du niveau de charge
        if self.solar_optimizer == 'on' and self.heure_creuse == 'off':
            if self.start_ev_charging== 'on':
                if self.battery_level < self.battery_level_max:
                    self.turn_on(self.args['command_ev_charging'])
                    self.log("demarrage de la charge (commande optimizer)")
            else: # start charge off
                self.turn_off(self.args['command_ev_charging'])
                self.log("Arret de la charge (commande optimizer)")
            return
        
        # Regulation de nuit en heure creuse
        if self.heure_creuse == 'on':
            if self.battery_level < self.battery_level_max:
                self.turn_on(self.args['command_ev_charging'])
                self.log("Demarrage charge heure creuse")
            else:
                self.turn_off(self.args['command_ev_charging'])
                self.log("Arret charge heure pleine")

            

