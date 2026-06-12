import pandas as pd
import joblib
import argparse

def main():
    # 1. Chargement des modèles sauvegardés
    try:
        modele = joblib.load('modele_implantation_optimise.pkl')
        encoder = joblib.load('encodeur_implantation.pkl')
        scaler = joblib.load('scaler_X.pkl')
        colonnes_X = joblib.load('colonnes_X.pkl')
    except FileNotFoundError:
        print("Erreur : Fichiers .pkl introuvables. Vérifie qu'ils sont dans le même dossier.")
        return

    # 2. Configuration pour lire la ligne de commande
    parser = argparse.ArgumentParser(description="Prédiction IA du type d'implantation d'une borne IRVE")
    parser.add_argument('--puissance', type=float, required=True, help="Puissance nominale en kW (ex: 50.0)")
    parser.add_argument('--pdc', type=int, required=True, help="Nombre de points de charge (ex: 2)")
    parser.add_argument('--tarif', type=str, required=True, choices=['bas', 'moyen', 'haut'], help="Tarif (bas, moyen, haut)")
    parser.add_argument('--gratuit', type=str, required=True, choices=['true', 'false'], help="Gratuit (true ou false)")
    parser.add_argument('--pmr', type=str, required=True, help="Accessibilité (ex: Accessible, Non accessible)")

    args = parser.parse_args()

    # 3. Création de la borne avec les données saisies
    nouvelle_borne = pd.DataFrame([{
        'puissance_nominale': args.puissance,
        'nbre_pdc': args.pdc,
        'tarif_level': args.tarif,
        'gratuit': args.gratuit,
        'accessibilite_pmr': args.pmr
    }])

    # 4. Traitement (identique à l'entraînement)
    borne_encoded = pd.get_dummies(nouvelle_borne)
    borne_encoded = borne_encoded.reindex(columns=colonnes_X, fill_value=0)
    borne_scaled = scaler.transform(borne_encoded)

    # 5. Prédiction finale
    prediction_chiffre = modele.predict(borne_scaled)
    prediction_texte = encoder.inverse_transform(prediction_chiffre)

    # 6. Affichage du résultat
    print("\n" + "="*60)
    print(" RÉSULTAT DE LA PRÉDICTION IA ")
    print("="*60)
    print(f"L'Intelligence Artificielle prédit que cette borne est implantée sur :")
    print(f" >>> {prediction_texte[0]} <<<")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
