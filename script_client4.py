import joblib

# 1. Chargement direct des ressources
encoder = joblib.load("encoder_implantation.pkl")
model = joblib.load("modele_puissance.pkl")

def c_bool(message):
    """
    Pose une question à l'utilisateur et convertit sa réponse en 0 ou 1
    selon le modèle de nettoyage du Notebook.
    """
    valeur = input(message)
    
    if not valeur:
        return 0

    valeur = str(valeur).strip().lower()

    if valeur in ["true", "1", "oui", "yes", "o"]:
        return 1

    return 0


if __name__ == "__main__":

    try:
        
        # Saisies principales
        nbre_pdc = int(input("Nombre de points de contact : "))
        annee = int(input("Année de mise en service : "))
        lat = float(input("Latitude : "))
        lon = float(input("Longitude : "))
        
        # Gestion et encodage de l'implantation
        imp = input(f"Implantation ({', '.join(encoder.classes_)}) : ").strip()
        imp = imp if imp in encoder.classes_ else encoder.classes_[0]
        imp_encoded = encoder.transform([imp])[0]
        
        # Construction directe du vecteur (respect de l'ordre exact du modèle)
        X = [
            nbre_pdc,
            c_bool("Prise Type E/F ? (o/n) : "),
            c_bool("Prise Type 2 ? (o/n) : "),
            c_bool("Prise Type Combo-CCS ? (o/n) : "),
            c_bool("Prise Type CHAdeMO ? (o/n) : "),
            c_bool("Autre type de prise ? (o/n) : "),
            c_bool("Gratuit ? (o/n) : "),
            c_bool("Paiement à l'acte ? (o/n) : "),
            c_bool("Réservation possible ? (o/n) : "),
            c_bool("Accessible PMR ? (o/n) : "),
            c_bool("Adapté deux-roues ? (o/n) : "),
            annee,
            imp_encoded,
            lat,
            lon
        ]
        
        # Prédiction et affichage
        puissance = model.predict([X])[0]
        print(f"\nPUISSANCE NOMINALE ESTIMÉE : {puissance:.2f} kW")

    except Exception as e:
        print(f"\nImpossible de calculer la prédiction")