# -*- coding: utf-8 -*-
"""
Public Transport Accessibility Level Application for QGIS plugin expreseau GTFS


Created on Tue Dec 10 17:40:30 2024

@author: Lucas Fages

"""

import numpy as np
from shapely import Polygon
import geopandas as gpd
from pyproj import Proj, transform
import pandas as pd

class PTAL(object):

    def __init__(self,
                 gtfs_feed,
                 size:int):
                
        self._gtfs_feed = gtfs_feed
        self._size = size

    
    def _get_grid_emprise(self):
        """
        

        Returns
        -------
        geo_series : TYPE
            DESCRIPTION.

        """
        
        feed = self._gtfs_feed
        
        stops = feed.stops
        
        # Convertir de WGS84 à Lambert 93
        wgs84 = Proj(init='epsg:4326')  # WGS84
        lambert93 = Proj(init='epsg:2154')  # Lambert 93
        x, y = transform(wgs84, lambert93, stops.stop_lon, stops.stop_lat)
        stops['stop_lon'] = x
        stops['stop_lat'] = y
        # on détermine l'emprise des tracés des lignes :
        min_lat = stops.stop_lat.min()
        max_lat = stops.stop_lat.max()
        min_lon = stops.stop_lon.min()
        max_lon = stops.stop_lon.max()
        # print(min_lat, max_lat)
        
        p1 = np.array([max_lon, max_lat])
        p2 = np.array([min_lon, max_lat])
        p3 = np.array([min_lon, min_lat])
        p4 = np.array([max_lon, min_lat])
        
        size = self._size
        # print(size)
        cols = round(np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) / size)
        rows = round(np.sqrt((p4[0] - p1[0])**2 + (p4[1] - p1[1])**2) / size)
        print(cols, rows)
        
        # Interpolation des points sur les bords du rectangle
        top_edge = np.linspace(p1, p2, cols + 1)  # Bord supérieur
        bottom_edge = np.linspace(p4, p3, cols + 1)  # Bord inférieur
        
        # Créer une grille en interpolant verticalement entre les bords
        grid = np.array([
            np.linspace(top_edge[i], bottom_edge[i], rows + 1)
            for i in range(cols + 1)])
        
        # geo_series.explore()
        polygons = []
        
        rows, cols, _ = grid.shape
        print(cols, rows)
        for i in range(rows - 1):  # Parcourir les lignes de la grille
            for j in range(cols - 1):  # Parcourir les colonnes de la grille
                # Points du polygone (cellule)
                p1 = grid[i, j]        # Haut-gauche
                p2 = grid[i, j + 1]    # Haut-droit
                p3 = grid[i + 1, j + 1]  # Bas-droit
                p4 = grid[i + 1, j]    # Bas-gauche
                
                # Créer un polygone
                polygon = Polygon([p1, p2, p3, p4, p1])  # Boucle fermée
                polygons.append(polygon)
        
        # Créer une GeoSeries contenant tous les polygones
        geo_series = gpd.GeoSeries(polygons, crs = 2154)
        print(f" geoserie : {geo_series.shape}")
        return geo_series
    
    def _get_table_passages(self):
        
        feed = self._gtfs_feed
   
        routes = feed.routes
        stops = feed.stops
        #table horaire :
        trips_stops = feed.table_horaire()
        trips_stops = trips_stops[['route_id','route_short_name', 'trip_id',
                    'direction_id', 'service_id', "stop_sequence", 'stop_id']]
        
        # on merge avec la route pour avoir le numéro :
        trips_stops = trips_stops.merge(routes[["route_id", "route_type"]],
                                        on = "route_id", how="right").merge(stops[["stop_id", "stop_name"]])
        # on groupe par arret pour avoir le nombre de passage, par type de ligne
        trips_stops = trips_stops[['stop_name', 'route_type',"stop_id"]].groupby(['stop_name', "route_type"]).count().reset_index()
        trips_stops = trips_stops.merge(stops[['stop_name', 'stop_lon', 'stop_lat']]).groupby(["stop_name", "route_type", "stop_id"]).mean().reset_index()
        wgs84 = Proj(init='epsg:4326')  # WGS84
        lambert93 = Proj(init='epsg:2154')  # Lambert 93
        
        x, y = transform(wgs84,
                         lambert93, 
                         trips_stops.stop_lon,
                         trips_stops.stop_lat)
        
        
        trips_stops['stop_lon'] = x
        trips_stops['stop_lat'] = y
        trips_stops.columns = ['stop_name', 'route_type', 'nb_trips', 'stop_lon', 'stop_lat']
        
        return trips_stops
        
        
    
    def _get_compute_ptal(self):
        
        grid = self._get_grid_emprise().centroid
        print(f" grid : {grid.shape}")
        
        trips_stops = self._get_table_passages()
        
        l_ptal = list()
        
        for xc, yc in zip(grid.geometry.x, grid.geometry.y):
       
            xg = trips_stops.stop_lon
            yg = trips_stops.stop_lat
        
            # résultats en kilomètres :
            dist_eucli = np.sqrt((xg-xc)**2 + (yg - yc)**2)
            
            # on fait une copie du df existant contenant les arrets et leurs nombre de passages
            df = trips_stops.copy()
            # on ajoute les distances aux arrêts depuis les centres des carreaux
            df['distance_euclidienne'] = dist_eucli
            # on instancie un df temporaire qui contiendra pour les arrêts les plus proches les équivalents 
            t = pd.DataFrame()
            # On instancie une amplitude horaire de la periode observee 
            _AMPLI_ = 2
            # print(df.shape)
            # On boucle sur la jointure de liste {type, distance, facteur de fiabilité}
            # 0 : tram/metro, 1 : metro, 3 : bus, 7 : funiculaire
            for route_type, dist, AWT in zip([0,1,3,7],
                                 [750, 1000,300,500],
                                 [1, 0.75, 2, 1]):
        
                temp = df[(df['route_type']==route_type) \
                       & (df['distance_euclidienne'].values <= (dist+100))] 
        
                if temp.empty:
                    EDF = 0
                else:
                    # print("temp non nul")
                    v_m = 4 * 1000 / 60 # v en m/min
                    d = temp.distance_euclidienne # distance en kilomètres
                    d_m = d #* 1000 # distance en mètres
                    SAP = d_m / v_m # temps en minutes
                    #frequence : nombre de passages / par amplitude horaire / 2 : donne temps d'attente moyen
                    SWT = 0.5*(_AMPLI_/temp.nb_trips )*60
                    TAT = SAP + SWT + AWT
                    # equivalent fréquence
                    EDF = 0.5*(60/(TAT))
                    temp['TAT'] = TAT
                    temp['SAP'] = SAP
                    temp['SWT'] = SWT
                    temp['AWT'] = AWT
                temp['EDF'] = EDF
            
                # on concatène dans le DF temporaire
                t = pd.concat([t, temp])
                # print(t.columns)
                    # on parcourt toutes les lignes du df temporaire pour calculer le PTAL
            ptal = 0
            for edf in t.EDF:
                coef = 0.5
                if edf == max(t.EDF.values):
                    coef = 1
                ptal += coef * edf
    
            l_ptal.append(ptal)
        print(f"longueur ptal : {len(l_ptal)}")
        gdf_PTAL = gpd.GeoDataFrame(data = pd.DataFrame(l_ptal, columns=['PTAL']),
                                    geometry = self._get_grid_emprise())
        print(gdf_PTAL.shape)

        return gdf_PTAL
                