from PB_Graph import *
import matplotlib.pyplot as plt

#Limits

#Climate
CO2_concentration = Limit('CO2 Concentration', 417, 350, False)
Radiative_Forcing = Limit('Radiative Forcing', 1, 2.91, False)

#Biosphere
Functional_integrity = Limit('Functional Integrity', 0.3, 0.1, False)
Genetic_Diversity = Limit('Genetic_Diversity', 10, 100, False)

#Water
Blue_Water = Limit('Blue water', 0.102, 0.182, False)
Green_Water = Limit('Green water', 0.111, 0.158, False)

#Biogeochemical flow
Azote = Limit('N', 11, 22.6, False)
Phosphore = Limit('P', 62, 190, False)

#Other
Aerosol_limit = Limit('Aerosol limit', 0.1, 0.076, True)
Ozone_Layer = Limit('Ozone Layer', 284.6, 276, True)
Ocean_Acidification = Limit('Ocean Acidification', 2.8, 2.75, True)
Novel_entity = Limit('Novel Entity', 0.1, 1.80, False)
Land_syst_change = Limit('Land system change', 0.75, 0.6, False)

#Subsystems
Water = Subsystem('Freshwater change', [Blue_Water, Green_Water])
Climate = Subsystem('Climate change', [Radiative_Forcing, CO2_concentration])
Biosphere = Subsystem('Biosphere integrity', [Functional_integrity, Genetic_Diversity])
Flux_Biogeo = Subsystem('Biogeochemical flows', [Azote, Phosphore])
Aerosol = Subsystem('Atmospheric aerosol loading', [Aerosol_limit])
Ozone = Subsystem('Stratospheric ozone depletion', [Ozone_Layer])
Acidification = Subsystem('Ocean Acidification', [Ocean_Acidification])
Nov_Entity = Subsystem('Novel entities', [Novel_entity])
Land_use = Subsystem('Land system change', [Land_syst_change])

#System
Metropole_Lyon = System('Metropole de Lyon', [Ozone, Nov_Entity, Climate, Biosphere, Land_use, Water, Flux_Biogeo, Acidification, Aerosol])
ax = Metropole_Lyon.plot(label=False)               
plt.show()