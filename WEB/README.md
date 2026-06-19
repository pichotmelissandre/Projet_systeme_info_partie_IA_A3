Description des fichiers 

- Fonctionnalité 1 : Accueil
    HTML : page_d_accueil.html 
    CSS : style.css 
    Illustrations : 
        logo : charging-station.png
        première image : images_bornes.png
        graphique : Immatriculations_et_parc_de_VE_et_VHR
        logo ISEN : logo.png

- Fonctionnalité 2 : Points de charge (tableau et carte)
    HTML : points_de_charge.html
    CSS : style.css
    JavaScript : script_get_bornes.js
    PHP : point_de_charge_tab_maps_mp.php
    Illustrations : 
        icône en-tête : charging-station.png

- Fonctionnalité 3 : Statistiques des stations
    HTML : statistiques_des_stations.html
    CSS : style_FN.css
    PHP : prediction_FN.php
    JavaScript : statistiques.js

- Fonctionnalité 4 : Prédiction en masse des clusters
    HTML : prediction_cluster.html
    CSS : style.css
    JavaScript : script_maps_cluster_mp.js
    PHP : cluster_maps_mp.php
    Python : script_client2.py
            modele_hdbscan_optimal.pkl

- Fonctionnalité 5 : Prédiction de la puissance nominale et de l'implantation (Machine Learning)
    HTML : prediction_puissance_nominale.html
    HTML secondaire : prediction_type_implantation.html
    CSS : style_FN.css
    PHP : get_prediction_puissance.php
    Python : predict_puissance.py
             predict_implantation.py
             Random Forest : modele_puissance.pkl
             LabelEncoder : encoder_implantation.pkl

