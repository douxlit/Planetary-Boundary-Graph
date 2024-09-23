from PB_Graph import *
import matplotlib.pyplot as plt

#Limits
Emissions = Limit('Emissions', 4, 3.82, False)
Empreinte = Limit('Empreinte', 8.4, 3.82, False)
Biosphere_integrity = Limit('Functional Integrity', 0.58, 1, False, max=0.29)
Natural_area = Limit('Natural Area', 0, 0, None)
Water_surf = Limit('Surface water', 0.036, 0.2, True, max=0.73)
Water_under = Limit('Underground water', 1446, 4200, True)
Aerosol_limit = Limit('Aerosol limit', 0, 0, None)
Azote = Limit('N', 0, 0, None)
Phosphore = Limit('P', 0, 0, None)

#Subsystems
Water = Subsystem('Water', [Water_surf, Water_under])
Climate = Subsystem('Climate', [Emissions, Empreinte])
Biosphere = Subsystem('Biosphere', [Biosphere_integrity, Natural_area])
Aerosol = Subsystem('Aerosol', [Aerosol_limit])
Flux_Biogeo = Subsystem('Flux biogeochimique', [Azote, Phosphore])

#System
Metropole_Lyon = System('Metropole de Lyon', [Aerosol, Biosphere, Climate, Flux_Biogeo, Water])
ax = Metropole_Lyon.plot()               
plt.show()