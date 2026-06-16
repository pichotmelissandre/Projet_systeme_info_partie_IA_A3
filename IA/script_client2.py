import os
import joblib
import numpy as np

NOM_MODELE = "modele_hdbscan_optimal.pkl"


def charger_modele_production(chemin_modele=NOM_MODELE):

    if not os.path.exists(chemin_modele):
        raise FileNotFoundError(
            f"Erreur : Le fichier '{chemin_modele}' est introuvable.\n"
            "Assurez-vous qu'il est placé dans le même dossier que ce script."
        )
    return joblib.load(chemin_modele)


def determiner_cluster_nouvelle_borne(modele_hdb, latitude, longitude):

    point_saisi = np.array([[latitude, longitude]])
    
    # récupération des données 
    X_entrainement = modele_hdb._raw_data
    labels_entrainement = modele_hdb.labels_
    
    # calcul de la distance entre la nouvelle borne et toutes les autres
    distances = np.linalg.norm(X_entrainement - point_saisi, axis=1)
    
    # point le plus proche
    indice_plus_proche = np.argmin(distances)
    cluster_attribue = labels_entrainement[indice_plus_proche]
    
    return cluster_attribue
def obtenir_nom_region(modele_hdb, cluster_id):

    if cluster_id == -1:
        return "Zone isolée"
        
    # extraction des points du cluster depuis la mémoire du modèle
    X_entrainement = modele_hdb._raw_data
    labels_entrainement = modele_hdb.labels_
    points_cluster = X_entrainement[labels_entrainement == cluster_id]
    
    # calcul du centre du cluster
    lat_moy = points_cluster[:, 0].mean()
    lon_moy = points_cluster[:, 1].mean()
    
    # Grille de décision géographique
    if lat_moy > 47.5 and lon_moy < -0.5: return "Grand Ouest (Bretagne / Pays de la Loire)"
    if lat_moy > 49.3 and lon_moy > 1.5:  return "Nord / Hauts-de-France"
    if 48.0 <= lat_moy <= 49.2 and 1.5 <= lon_moy <= 3.0: return "Bassin Parisien / Île-de-France"
    if lat_moy > 47.2 and lon_moy > 5.5:  return "Grand Est / Alsace"
    if 44.5 <= lat_moy <= 47.2 and 4.2 <= lon_moy <= 6.5: return "Couloir Rhodanien / Auvergne-Rhône-Alpes"
    if lat_moy < 44.0 and lon_moy > 6.5:  return "Côte d'Azur / Nice"
    if lat_moy < 44.2 and 2.5 <= lon_moy <= 6.5: return "Arc Méditerranéen / Midi"
    if lat_moy < 45.2 and lon_moy < 0.5:  return "Sud-Ouest / Aquitaine"
    if 43.0 <= lat_moy <= 44.5 and 0.5 <= lon_moy <= 2.5: return "Occitanie / Toulouse"
    if 41.3 <= lat_moy <= 43.1 and 8.5 <= lon_moy <= 9.6: return "Corse"
    
    # nom par défaut si le cluster est à la frontière de deux zones
    orient_lat = "Nord" if lat_moy > 46.5 else "Sud"
    orient_lon = "Est" if lon_moy > 2.5 else "Ouest"
    return f"Secteur {orient_lat}-{orient_lon}"


if __name__ == "__main__":

    
    try:
        # 1 : Chargement du modèle
        hdb_production = charger_modele_production(NOM_MODELE)
        
        # 2 : récupération des coordonnées de la nouvelle borne
        print("Veuillez entrer les coordonnées de la borne en nombre décimal :")
        lat = float(input("Latitude de la borne : "))
        lon = float(input("Longitude de la borne : "))
        
        # 3 : Calcul de la prédiction
        cluster_id = determiner_cluster_nouvelle_borne(hdb_production, lat, lon)
        nom_region = obtenir_nom_region(hdb_production, cluster_id)
        # 4 : résultat pour l'utilisateur
        if cluster_id == -1:
            print(f"La borne est isolée.")
        else:
            print(f"La borne située à ({lat}, {lon}) appartient au cluster n°{cluster_id} : {nom_region}")

    
    except ValueError:
        print("\n entrée invalide")
    except Exception as e:
        print(f"\n échec de l'exécution ")
