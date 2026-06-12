from google.colab import files
uploaded = files.upload()

#ENCODAGE


import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 1. CHARGEMENT DES DONNÉES
df = pd.read_csv('export_IA.csv')
df = df.dropna(subset=['implantation_station'])

# 2. SÉLECTION DES VARIABLES
y = df['implantation_station'] # cz que l'ia doit deviner
X = df[['puissance_nominale', 'nbre_pdc', 'tarif_level', 'gratuit', 'accessibilite_pmr']] #indices

# 3. ENCODAGE
encoder_y = LabelEncoder() #voirie=0, Parking=1
y_encoded = encoder_y.fit_transform(y)
joblib.dump(encoder_y, 'encodeur_implantation.pkl')

X_encoded = pd.get_dummies(X, drop_first=True) #catégories
colonnes_X = X_encoded.columns
joblib.dump(colonnes_X, 'colonnes_X.pkl') #sauvegarde

# 4. SÉPARATION ENTRAÎNEMENT / TEST (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# 5. NORMALISATION
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, 'scaler_X.pkl')

print("Données préparées avec succès.  Scaler et Encodeur sauvegardés.")

#IA


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# 1. On définit l'algorithme de base
rf = RandomForestClassifier(random_state=42) # pour le 375

# 2. grille des paramètres à tester
param_grid = {
    'n_estimators': [50, 100],        # Nb arbres forêt
    'max_depth': [10, 20, None],       # Profondeur max arbres
    'min_samples_split': [2, 5]        # Nombre mini données pour créer branche
}

print("Recherche du meilleur modèle en cours (GridSearchCV)... ça peut prendre 1 à 2 minutes.")

# 3. Configuration et lancement de la recherche
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_scaled, y_train)

# 4. On récupère le meilleur modèle trouvé
meilleur_modele = grid_search.best_estimator_
print(f"\n[SUCCÈS] Meilleurs paramètres trouvés : {grid_search.best_params_}")

# 5. ÉVALUATION DU MODÈLE
y_pred = meilleur_modele.predict(X_test_scaled) #20% restants
print(f"Précision globale du modèle (Accuracy) : {accuracy_score(y_test, y_pred) * 100:.2f}%\n")

print("Rapport détaillé de classification :")
# Désencodage
print(classification_report(y_test, y_pred, target_names=encoder_y.classes_))

# 6. ENREGISTREMENT DU MODÈLE FINAL OPTIMISÉ
joblib.dump(meilleur_modele, 'modele_implantation_optimise.pkl')
print("\nModèle final sauvegardé sous 'modele_implantation_optimise.pkl' !")


#SCRIPT




%%writefile script_besoin3.py
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
    print(" 🤖 RÉSULTAT DE LA PRÉDICTION IA 🤖")
    print("="*60)
    print(f"L'Intelligence Artificielle prédit que cette borne est implantée sur :")
    print(f" >>> {prediction_texte[0]} <<<")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()


#EXEMPLE

!python script_besoin3.py --puissance 300 --pdc 4 --tarif haut --gratuit false --pmr Accessible
