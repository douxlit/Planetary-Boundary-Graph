
class Limit:
        def __init__(self, name: str, impact: float, limit: float, state: bool, max=None):
                self.name = name
                self.impact = impact
                self.limit = limit
                self.state = state
                self.max = max
        
        def __repr__(self) -> str:
                cls = self.__class__.__name__
                return f"{cls}('{self.name}', {self.impact}, {self.limit}, {self.state})"
                
        def normal(self, state: bool, impact: float, limit: float) -> float :
                if state == None or impact == None:
                        return None
                else:
                        if not state :
                                if impact > limit :
                                        return impact/limit
                                else :
                                        return 1 + abs((impact - limit)/limit)
                        else :
                                if impact < limit :
                                        return impact/limit
                                else :
                                        return 1 - abs((impact - limit)/limit)
        
        def norm(self) -> float:
                return self.normal(self.state, self.impact, self.limit)

        def norm_max(self) -> float:
                return self.normal(False, self.max, self.limit)


class Subsystem:
        def __init__(self, name: str, limits: list[Limit]):
                self.name = name
                self.limits = limits
                self.size = len(limits)

        def __repr__(self) -> str:
                cls = self.__class__.__name__
                return f"{cls}('{self.name}', {self.limits})"

        def names(self) -> list[str]:
                names = []
                for l in self.limits :
                        names.append(l.name)
                return names


class System:
        def __init__(self, name: str, subsystems: list[Subsystem]):
                self.name = name
                self.subsystems = subsystems
                self.size = len(subsystems)

        def __repr__(self) -> str:
                cls = self.__class__.__name__
                return f"{cls}('{self.name}', {self.subsystems})"

        def names(self) -> list[str]:
                names = []
                for s in self.subsystems :
                        names.append(s.name)
                return names

        def plot(self) :
                import numpy as np
                import matplotlib.pyplot as plt
                import matplotlib.colors as mcolors
                import math as m

                # Fonction pour créer un dégradé de couleur
                def gradient_color(start_color, end_color, steps):
                        start_color = np.array(mcolors.to_rgba(start_color))
                        end_color = np.array(mcolors.to_rgba(end_color))
                        return [start_color * (1 - i / steps) + end_color * (i / steps) for i in range(steps)]

                #Def graphique
                ax = plt.subplot(projection='polar')

                Nb_syst = self.size
                subsysts = self.subsystems
                width = 2*np.pi/Nb_syst - np.pi/(10*Nb_syst) #width of each subsystem in the plot
                theta = np.linspace(0, 2 * np.pi, Nb_syst, endpoint=False) #position of each subsystem in the plot
                n = 0
                t_manip = []
                H = 0
                for s in subsysts :

                        nb_cat = s.size #number of limit for the subsystem
                        w = width/nb_cat #width of each limit in the plot
                        t_start = theta[n] - (nb_cat-1)*w/2
                        n += 1

                        t_list = list(np.linspace(t_start, t_start + (nb_cat-1)*w, nb_cat))

                        if nb_cat>1 :
                                t_manip += list(np.linspace(t_start + w/2, t_start + (nb_cat-1)*w + w/2, nb_cat-1, endpoint=False))

                        rk = 0
                        none = 0

                        for l in s.limits :
                                height = l.norm()
                                M = l.norm_max()

                                if height != None :
                                        #manage upper boundary
                                        if height > H :
                                                H = height
                                                if M != None and M > H :
                                                        H = M
                                        none = 1
                                        num_segments = 1000
                                        segment_height = height/num_segments
                                        t = t_list[rk]
                                        rk+=1
                                        colors = []

                                        for i in range(num_segments):
                                                # Déterminer la hauteur du segment
                                                current_height = i * segment_height
                                                if current_height <= 1:
                                                        # Vert pour les hauteurs <= 1
                                                        colors.append(mcolors.to_rgba('green'))
                                                else:
                                                        # Gradient jaune vers rouge pour les hauteurs > 1
                                                        gradient_pos = (current_height - 1) / (height - 1)
                                                        colors.append(gradient_color('yellow', 'red', 100)[int(gradient_pos * 99)])
                                        
                                        # Tracer chaque segment avec la couleur correspondante
                                        for i in range(num_segments):
                                                ax.bar(t, segment_height, width=w, color=colors[i], bottom=i * segment_height)

                                        # Tracer un segment au max
                                        if M != None :
                                                ax.bar(t, 0.025, width=w, color='indigo', bottom = M)
                        
                        if none == 0 :
                                s.name = s.name + '\n(not yet quantified)'

                #SOS
                # Tracer un contour de cercle vert à r = 1
                theta_circle = np.linspace(0, 2 * np.pi, 100)
                r_circle = np.full_like(theta_circle, 1)
                ax.plot(theta_circle, r_circle, color='green', linewidth=1, linestyle='--')  # Contour de cercle

                #Manage grid
                ax.grid(True, linewidth=0)
                angles = np.degrees(theta)
                ax.set_thetagrids(angles)
                ax.set_xticklabels(self.names())  # Labels des ticks
                ax.set_rticks([0, max(m.floor(H)+1,2)])

                # Ajouter manuellement les lignes theta
                theta2 = list(np.linspace(np.pi/Nb_syst, 2 * np.pi + np.pi/Nb_syst, Nb_syst, endpoint=False))
                for angle in theta2:
                        ax.axvline(x=angle, color='grey', linestyle='-', linewidth=1)

                for angle in t_manip :
                        ax.axvline(x=angle, color='white', linestyle='-', linewidth=0.5)


                # Enlever le contour du cercle extérieur
                ax.spines['polar'].set_visible(False)

                # Enlever les libellés des graduations radiales
                ax.set_yticklabels([])

                return ax