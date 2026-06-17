 <?php
// 1. Indiquer que la réponse sera au format JSON 
header('Content-Type: application/json; charset=utf-8');

// 2. Vérifier si un département a bien été envoyé dans l'URL
if (!isset($_GET['departement']) || empty($_GET['departement'])) {
    echo json_encode(["erreur" => "Aucun département sélectionné."]);
    exit;
}

$dept = $_GET['departement'];

// 3. Connexion à la base de données MAMP
$host = 'localhost'; // ou 'localhost;port=8889' si localhost seul bloque sur Mac
$dbname = 'projet_irve'; // Le nom exact que je vois sur ta capture
$user = 'root'; // Identifiant par défaut MAMP
$pass = 'root'; // Mot de passe par défaut MAMP Mac

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $user, $pass);
    // Activer l'affichage des erreurs SQL
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo json_encode(["erreur" => "Erreur de connexion : " . $e->getMessage()]);
    exit;
}

// 4. Préparation du tableau qui contiendra toutes les statistiques
$resultats = [];

try {
    // --- STATISTIQUE 1 : Total des stations ---
    $stmt = $pdo->prepare("SELECT COUNT(*) as total FROM stations WHERE code_departement = :dept");
    $stmt->execute(['dept' => $dept]);
    $resultats['total_stations'] = $stmt->fetch(PDO::FETCH_ASSOC)['total'];

    // --- STATISTIQUE 2 : Gratuit vs Payant ---
    $stmt = $pdo->prepare("SELECT gratuit, COUNT(*) as compte FROM stations WHERE code_departement = :dept GROUP BY gratuit");
    $stmt->execute(['dept' => $dept]);
    $resultats['gratuit_payant'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // --- STATISTIQUE 3 : Top 5 des communes ---
    $stmt = $pdo->prepare("SELECT commune, COUNT(*) as compte FROM stations WHERE code_departement = :dept GROUP BY commune ORDER BY compte DESC LIMIT 5");
    $stmt->execute(['dept' => $dept]);
    $resultats['top_communes'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // --- STATISTIQUE 4 : Puissance nominale ---
    $stmt = $pdo->prepare("
        SELECT pc.puissance_nominale, COUNT(*) as compte 
        FROM points_de_charge pc 
        JOIN stations s ON pc.id_station = s.id 
        WHERE s.code_departement = :dept 
        GROUP BY pc.puissance_nominale
    ");
    $stmt->execute(['dept' => $dept]);
    $resultats['puissances'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // 5. Renvoyer les résultats au navigateur en format JSON 
    echo json_encode($resultats);

} catch (PDOException $e) {
    echo json_encode(["erreur" => "Erreur SQL : " . $e->getMessage()]);
}
?>