Expreseau GTFS

![logo2](logo2.png)


Aide Ã  l'utilisation du plugin QGIS 3.* **Expreseau GTFS**
Plugin pour QGIS basÃ© sur la librairie python expreseau_gtfs : https://github.com/lufages/expreseau_gtfs

## Charger un fichier GTFS (dossier *.zip)

Cela va automatiquement modifier la date pour choisir un mardi. 
Il s'agit du mardi suivant la date minimale enregistrÃ©e dans le fichier *calendar.txt*.
La plage horaire est choisie par dÃ©faut de 7h Ã  9h.



#### Figure : Charger un fichier GTFS 

![isochrones](img/isochrones.png)



## Indicateurs de performance

### Cartographier la frÃ©quence 
Il est possible de cartographier la frÃ©quence tronÃ§on par tronÃ§on (c'est-Ã -dire arrÃªt Ã  arrÃªt)./
 Le rÃ©sultat est une couche de lignes avec une valeur numÃ©raire Ã  classer. C'est la variable *nbtrips* 
 (nombre de voyages sur la plage horaire choisie et dans la direction choisie : direction_id = 0 ou 1)

#### Figure : cartographier la frÃ©quence dans la direction 0

![isochrones](img/frequency.png)

#### Figure : Classer la variable *nbtrips* par valeur

![isochrones](img/load_files.png)



### Cartographier le rÃ©seau
Si le fichier *shapes.txt* est prÃ©sent dans le jeu de donnÃ©es GTFS il est possible de cartographier
 chaque ligne du rÃ©seau mais Ã©galement de cartographier la frÃ©quence moyenne par ligne.
 
 
 
### CrÃ©er une table csv d'indicateurs de performance
Il est possible de choisir de ne pas calculer certains indicateurs proposÃ©s en les
dÃ©sÃ©lectionnant dans la checkable combobox.

Liste d'indicateurs :
 - route_short_name : nom court de la ligne
 - direction_id :  direction du trips : 0 ou 1
 - services par jour : nombre de services par jour dans toutes les directions pour la date choisie
 - freq. moy. de 7 Ã  9
 - freq. moy. de 12 Ã  14
 - freq. moy. de 16 Ã  19
 - hmin : heure du premier dÃ©part
 - hmax : heure du dernier dÃ©part
 - amplitude(sec) :  amplitude journaliÃ¨re
 - freq. moy. corrigee - 7 a 9, 12 a 14, 16 a 19 : frÃ©quence pondÃ©rÃ©e par le nombre de voyages par tronÃ§on.


![image2](img/csv_indicators.png)


#### RÃ©sultats

![isochrones](img/export_csv.png)


## Tracer l'evolution journaliere de la frequence sur le reseau

![isochrones](img/plot_evol.png)

Il est possible de choisir des lignes à tracer (point 1. cf. image ci-dessus).
L'evolution est tracee entre 5h et minuit.


### Outils issus de la science des graphes :


D'aprÃ¨s Cats, Oded. Â« Topological Evolution of a Metropolitan Rail Transport Network: The Case of Stockholm Â».
 Journal of Transport Geography 62 (juin 2017): 172â€‘83. https://doi.org/10.1016/j.jtrangeo.2017.06.002.
 
--Figure : Graph tools**

![isochrones](img/graph_tools.png)
 
Les outils ci-dessous crÃ©ent des couches de points qu'il s'agira de faire varier selon les valeurs.
Issus de : https://networkx.org/

#### Betweenness centrality

L'indicateur *Betweeness centrality* est, pour un noeud donnÃ©, la fraction de la somme de l'ensemble des itinÃ©raires de toutes les paires de noeuds passant par le noeud.
La fraction signifie que la valeur est divisÃ©e par le nombre de noeuds du graphe.

Ci-dessous, l'indicateur calculÃ© Ã  chaque noeud (arrÃªt du rÃ©seau). La valeur varie avec la taille. Les valeurs Ã©levÃ©es permettent de voir quels sont les noeuds les plus empruntÃ©s du rÃ©seau,
ce qui montre d'une part la desserte du noeud et d'autre part les points de fragilitÃ© du rÃ©seau,
dans la mesure où un ou plusieurs noeuds successifs prÃ©sentant des valeurs Ã©levÃ©es sont en rÃ©alitÃ© des goulots d'Ã©tranglement.

**Figure : Betweenness centrality**

![bet_centr](img/bet_centr.png)


#### Closeness centrality

L'indicateur de *Closeness centrality* correspond Ã  pour chacun des noeud du graphe Ã  l'inverse de la somme des temps de parcours vers l'ensemble des noeuds du graphe.
Plus l'indicateur est Ã©levÃ©, plus la somme des temps pour rejoindre l'ensemble des arrÃªts du rÃ©seau est faible,et cela signifie que le noeud est trÃ¨s bien desservi.

Ci-dessous, l'exemple de Clermont-Ferrand, montre les noeuds et les Â«couloirsÂ« de desserte Ã©levÃ©e.

**Figure : Closeness centrality**

![clsn_centr](img/clsn_centr.png)

#### Degree centrality


L'indicateur *Degree centrality*, est, pour un noeud, la fraction de noeuds qui lui est connectÃ©e. Plus le degrÃ© est Ã©levÃ©, plus le noeud est connectÃ© au rÃ©seau.


**Figure : Closeness centrality**

![deg_centrality](img/deg_centrality.png)


## Calcul d'itinÃ©raires sur le rÃ©seau de transports

Le calcul d'itinÃ©raire repose sur les algorithmes de calcul du plus court chemin en science des graphes.
Ici, nous avons adaptÃ© l'algorithme de Dijkstra au calcul d'itinÃ©raire sur un rÃ©seau de transports.
Les noeuds du graphe sont les arrÃªts du rÃ©seau et les arÃªtes du graphe sont les connexions entre les arrÃªts.
La pondÃ©ration utilisÃ©e pour l'algorithme Dijsktra est le temps de parcours entre deux arrÃªts, issu des tables horaires.
On considÃ¨re que le transfer entre deux arrÃªts (correspondance de ligne) se fait Ã  pied, Ã  une vitesse de marche de 4 km.h-1
 et que l'individu peut atteindre les arrÃªts autour de lui dans un rayon Ã  vol d'oiseau, pondÃ©rÃ© par un facteur Â«crow flies distanceÂ«, mais
 il est tout Ã  fait possible de faire varier ces paramÃ¨tres d'entrÃ©e et en particulier l'algorithme :

  - Dijkstra with max transfer : Dijsktra adaptÃ© avec un nombre de correspondances maximales ;
  - Dijkstra classique ;
  - Plus court chemin sans pondÃ©ration.
  
  
Ã©tapes :
1. SÃ©lectionner les points (couche point) ou cliquer sur le bouton et sÃ©lectionner la position dans le fond de carte en LAMBERT 93 pour les points de dÃ©part et d'arrivÃ©e ;
2. ParamÃ¨tres modifiables ;
3. Cliquer sur "Calcul d'itinÃ©raire". Une fois le calcul terminÃ©, le temps s'affichera et la couche ligne de l'itinÃ©raire sera crÃ©Ã©e.
On peut distinguer la couche par ligne en catÃ©gorisant la couche par la variable Â«routeÂ«.

**Exemple**
![routing](img/routing.png)

**RÃ©sultats - issus du calculateur d'itinÃ©raires de T2C (RÃ©gie de transports Ã Clermont-Ferrand)** 

![res_routing](res_routing.png)

**Remarques** :  le calculateur ne permet pas de calculer un trajet Ã un horaire prÃ©cis en donnant des horaires de correspondances prÃ©cis.
L'outil permet de calculer le trajet le plus court en temps entre deux points, sur une plage horaire. 
Il est davantage conçu pour dÃ©terminer une accessibilitÃ© en temps de parcours que pour renvoyer une feuille de route.

 
## Isochrones

Le calculateur d'isochrones fonctionne sur la base de l'algorithme Dijkstra : il dÃ©termine les arrÃªts atteignables dans le temps imparti.
A chaque arrÃªt de l'enveloppe concave, on rÃ©cupÃ¨re le temps potentiel de parcours restant
(c'est-Ã-dire, si le temps de parcours maximal est de 1h, si l'individu met 45min Ã  atteindre un arrÃªt,
le temps potentiel de parcours restant est de 1h - 45min = 15min), et on trace un buffer d'une distance
correspondant Ã  la distance rÃ©alisable Ã  la vitesse spÃ©cifiÃ©e, le tout pondÃ©rÃ© par un facteur *crow flies distance*.


**ParamÃ©trage**
 
Il est possible d'amender le calcul d'isochrones avec une API de l'IGN qui permet de calculer un isochrone sur la base du rÃ©seau routier ou pÃ©destre français.
 
![isochrones](img/load_files.png)

**RÃ©sultats**

![res_isochrones](img/isochrones_2.png)

 

## Indice d'accessibilitÃ© - *PTAL : Public Transport Accessibility Network*

D'aprÃ¨s : Transports for London. "Assessing transport connectivity in London", 2015. 

Le PTAL est une mesure de l'accessibilitÃ© au rÃ©seau de transports en commun utilisÃ©e par les amÃ©nageurs de l'espace public Ã  Londres.
Pour chaque Ã©lÃ©ment discret, le PTAL reprÃ©sente comment l'Ã©lÃ©ment est connectÃ© au rÃ©seau de transports.
Il peut Ãªtre vu comme la mesure de la densitÃ© spatiale de transport public.
Le PTAL varie de 0 Ã  40 ou plus (elle est ensuite ramenÃ©e de 0 Ã  6). Un Ã©lÃ©ment aura une valeur Ã©levÃ©e si :
- Il y a une courte distance Ã  pied Ã  rÃ©aliser pour rejoindre des arrÃªts ;
- Les temps d'attentes aux arrÃªts les plus proches sont faibles ;
- La desserte Ã  ces arrÃªts est bonne ;
- Il y a un arrÃªts majeur du rÃ©seau proche ;
- Une combinaisons des caractÃ©ristiques ci-dessus.


    
Les recommandations d'accessibilitÃ© par les amÃ©nageurs se font selon la densitÃ© de population, c'est ce que montre la figure ci-dessous.

**Figure : PTAL vs. densitÃ© de population, d'aprÃ¨s : Transports for London. "Assessing transport connectivity in London", 2015, page 6**
![ptal](img/res_ptal_reco_density.png)

Le calcul d'accessibilitÃ© via l'indicateur PTAL permet de dÃ©finir un niveau d'accessibilitÃ© partout sur le territoire de l'AOM le jour et la plage horaire choisie.

Il est ensuite possible de choisir la taille des Ã©lÃ©ments de la grille de dÃ©coupage du territoire (voir sur la figure ci-dessous, *element size*).

La grille se construit en prenant l'emprise rectangulaire que forment les arrÃªts (lattitude min et max, longitude min et max). 
Elle est ensuite dÃ©coupÃ©e en Ã©lÃ©ments carrÃ©s de taille spÃ©cifiÃ©e.



**Figure : mise en oeuvre de l'indicateur**

![ptal](img/ptal_init.png)

**Figure : rÃ©sultats sur le PTU de Clermont-Ferrand**

![ptal](img/ptal.png)

Dans notre exemple les valeurs les plus Ã©levÃ©es de PTAL se concentrent dans les zones urbaines les plus denses, autour du rÃ©seau de tramways.

**Figure : que dit la documentation de l'indicateur ?**

D'après Transports for London. "Assessing transport connectivity in London", 2015, page 19.
![ptal](img/res_ptal_values.png)

 
 





