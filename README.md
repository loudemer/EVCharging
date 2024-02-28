# EVCharging
Cette application tourne sous [appdaemon](https://appdaemon.readthedocs.io/en/latest/INSTALL.html) pour Home Assistant permet de contrloer la charge d'un véhicule électrique. Elle est couplée à l’application **[PVOptimizer](https://github.com/loudemer/pvoptimizer)** qui controle la distribution d’énergie solaire à tous les appareils gros consommateurs de la maison.

# Fonctionnement
L'application permet d'ajuster la charge à un niveau prédéterminé sous réserve de pouvoir disposer du niveau de charge du véhicule au travers d'une API.
Si la charge ne peut être réalisée de jour du fait d'un ensoleillement insuffisant, elle assure la charge de nuit.
Elle ne gère pas la charge adaptative avec des puissances de charge variables 

![Icon](https://github.com/loudemer/pvoptimizer/blob/main/images/applications.png?raw=true)

# Prérequis
- Installation de **[appdaemon](https://appdaemon.readthedocs.io/en/latest/INSTALL.html)**
- Installation de **[PVOptimizer](https://github.com/loudemer/pvoptimizer)**
- Sensor Heures Creuses disponible dans l’**[API RTE](https://www.api-couleur-tempo.fr/api)**
- Sensor niveau de charge du véhicule (facultatif)

# Installation
1. Installer **[appdaemon](https://appdaemon.readthedocs.io/en/latest/INSTALL.html)** à partir de paramètres / modules complémentaires si cela n’est pas déjà fait.
2. **[Télécharger le dépôt](https://github.com/loudemer/evcharging/)**
3. Mettre les fichiers `evcharging.py` et `evcharging.yaml`*` dans le répertoire `addon\_configs/a0d7b954\_appdaemon/apps`

# Configuration
1. Ajouter dans le fichier `addon_configs/a0d7b954_appdaemon/appdaemon.yaml`
```   
      evcharging_log :
        name: ECChargingLog
        filename: /homeassistant/log/evcharging.log
        log_generations: 3
        log_size: 100000
```
   Ceci vous permet de lire les log de l’application dans le fichier /config/ pvheatpump\_log  ou directement dans la [console appdaemon](http://ip\_ha:5050)

2. **Compléter** le fichier `/addon_configs/a0d7b954_appdaemon/apps/EVCharging.yaml` :

   Pour les autres, il faut créer les sensors qui ne sont pas déjà présents dans votre configuration.

```
EVCharging:
  class: EVCharging
  module: EVCharging
  log: evcharging_log
  # Permet d'inactiver l'application EVCharging
  constrain_input_boolean: input_boolean.enable_ev_charging

  # sensor heures creuses RTE ou autre
  heure_creuse: binary_sensor.rte_tempo_heures_creuses
  # switch de commande de la pse de charge ou directement du chargeur
  command_ev_charging: switch.ev_charging
  # Demande de charge aupres de PVOptimizer
  request_ev_charging: input_boolean.device_request_6
  # Activation de la charge par PVOptimizer
  start_ev_charging: input_boolean.start_device_6
  # Etat de l'activation de l'application PVOptimizer
  enable_solar_optimizer: input_boolean.enable_solar_optimizer
  # Utilisation du niveau de charge du vehicule (oui / non)
  use_battery_level: non
  # Sensor du niveau de batterie du vehicule donne par l'API
  # none si aucun
  battery_level: none
  # niveau maximum de charge du vehicule
  battery_level_max: input_number.ev_max_battery_level

```

3. **Ajouter si besoin les sensors suivants :**
   
```
input_number:
  ev_max_battery_level:
    name: "Charge max voiture"
    min: 0.0
    max: 100.0
    unit_of_measurement: "%"
    step: 10.0
    icon: mdi:thermometer
    mode: box

input_boolean:  
  input_boolean.enable_ev_charging:
    name: "Application Activation"
```

# Le Dashboard
Il reste à réaliser avec les quelques sensors manquants :
- activation de l'application : `constrain_input_boolean: input_boolean.enable_ev_charging`
- Niveau maximum de charge
- Niveau acuel de charge

# Mode d’emploi
Une fois l’installation réalisée, l’intégration est opérationnelle.
Vous pouvez ajuster le niveau maximum de charge si vous l'utilisez.

La mise en route de la charge se fait à partir du dashboard de PVOptimizer:

Pour demander la mise en route de la charge, il faut cliquer sur l'icône charge VE, à gauche. Il passe du gris au vert.
Si la production solaire est suffisante, l'appareil est mis en route, le deuxième icône devient vert et la puissance de fonctionnement s'affiche sur le 3eme icône et la durée de fonctionnement sur le 4ème icône.
La charge s'arrêtera au bout du délai imparti ou lorsque le niveau maximum sera atteint.

# Visualisation des problèmes
L’intégration génère un fichier de log qui est stocké dans le fichier `/config/log/evcharging.log`.
Il est possible aussi d’avoir plus de détails en appelant directement la **[console de debug d’appdaemon](http://<ip_homeassistant>:5050)**

Vous pourrez alors voir le démarrage et l’arrêt de l’intégration dans `main_log`, les erreurs éventuelles dans `error_log` et le déroulement de l’activité de l’intégration dans `evcharging_log`.
# Désinstallation
Il faut retirer les 2 fichiers `EVcharging.py` et `EVcharging.py.yaml` dans le répertoire `addon\_configs/a0d7b954\_appdaemon/apps/`
Redémarrer HA.

