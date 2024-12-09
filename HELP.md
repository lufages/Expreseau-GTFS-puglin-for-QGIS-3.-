Aide à l'utilisation du plugin QGIS 3.* **Expreseau GTFS**


## Charger un fichier GTFS (dossier *.zip)

Cela va automatiquement modifier la date pour choisir un mardi. 
Il s'agit du mardi suivant la date minimale enregistrée dans le fichier *calendar.txt*.
La plage horaire est choisie par défaut de 7h à 9h.



#### Figure 1 : Charger un fichier GTFS 




## Indicateurs de performance

### Cartographier la fréquence 
Il est possible de cartographier la fréquence tronçon par tronçon (c'est-à-dire arrêt à arrêt).\
 Le résultat est une couche de lignes avec une valeur numéraire à classer. C'est la variable *nbtrips* 
 (nombre de voyages sur la plage horaire choisie et dans la direction choisie : direction_id = 0 ou 1)

#### Figure 2 : cartographier la fréquence dans la direction 0

#### Figure 3 : Classer la variable *nbtrips* par valeur



#### Cartographier le ré&seau
Si le fichier *shapes.txt* est présent dans le jeu de données GTFS il est possible de cartographier
 chaque ligne du réseau mais également de cartographier la fréquence moyenne par ligne.
 
 
 
### Créer une table csv d'indicateurs de performance
Il est possible de choisir de ne pas calculer certains indicateurs proposés en les
désélectionnant dans la checkable combobox.

Liste d'indicateurs :
    - route_short_name : nom court de la ligne
    - direction_id :  direction du trips : 0 ou 1
    - services par jour : nombre de services par jour dans toutes les directions pour la date choisie
    - freq. moy. de 7 à 9
    - freq. moy. de 12 à 14
    - freq. moy. de 16 à 19
    - hmin : heure du premier départ
    - hmax : heure du dernier départ
    - amplitude(sec) :  amplitude journalière
    - freq. moy. corrigee - 7 a 9, 12 a 14, 16 a 19 : fréquence pondérée par le nombre de voyages par tronçon.


#### Résultats




### Outils issus de la science des graphes :


D'après Cats, Oded. « Topological Evolution of a Metropolitan Rail Transport Network: The Case of Stockholm ».
 Journal of Transport Geography 62 (juin 2017): 172‑83. https://doi.org/10.1016/j.jtrangeo.2017.06.002.
 
 
Les outils ci-dessous créent des couches points qu'il s'agira de faire varier selon les valeurs.

#### Betweenness centrality
Betweenness centrality of a node
is the sum of the fraction of all-pairs shortest paths that pass through
where
is the set of nodes,
is the number of shortest
-paths, and
is the number of those paths passing through some node
other than
. If
,
, and if
,
[2].

#### Closeness centrality
Closeness centrality [1] of a node u is the reciprocal of the average shortest path distance to u over all n-1 reachable nodes.

where d(v, u) is the shortest-path distance between v and u, and n-1 is the number of nodes reachable from u. Notice that the closeness distance function computes the incoming distance to u for directed graphs. To use outward distance, act on G.reverse().

Notice that higher values of closeness indicate higher centrality.

#### Direct centrality

The degree centrality for a node v is the fraction of nodes it is connected to.
 
 
 
 
### Calcul d'itinéraires sur le réseau de transports








 
 





