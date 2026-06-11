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
        
        # 4 : résultat pour l'utilisateur
        if cluster_id == -1:
            print(f"La borne est isolée.")
        else:
            print(f"La borne située à ({lat}, {lon}) appartient au cluster n°{cluster_id}")
        
    except ValueError:
        print("\n entrée invalide")
    except Exception as e:
        print(f"\n échec de l'exécution ")