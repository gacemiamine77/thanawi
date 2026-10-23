# 🔍 Audit, corrections et suggestions

## 1. Erreurs trouvées sur l'ancien site (et corrigées)

| # | Fichier | Erreur | Correction |
|---|---|---|---|
| 1 | `index.html` | **Fichier tronqué** (2 333 octets) : le code s'arrêtait au milieu du CSS (`#r{...displa`), sans `</style>`, sans corps HTML, sans JavaScript → **page blanche** | Réécriture complète : site fonctionnel en un fichier |
| 2 | `index.html` ↔ `lessons2.json` | La page ne chargeait jamais le fichier de contenu : les **13 leçons étaient invisibles** | Le site charge `data/content.json` qui contient les 13 leçons migrées + 14 nouvelles (27 au total) |
| 3 | `admin.html` | Il cherchait `data/content.json` (avec `levels`/`subjects`) qui **n'existait pas** → connexion impossible | `data/content.json` créé avec la structure attendue (`levels`, `streams`, `subjects`, `items`) ; l'admin propose aussi de le créer s'il manque |
| 4 | `admin.html` | Les noms de niveaux/matières sont devenus trilingues (`{ar,fr,en}`) : l'ancien code (`x.name` texte) aurait affiché `[object Object]` | Admin mis à jour (affichage selon la langue, AR/FR) |
| 5 | `admin.html` | Encodage base64 avec `escape()`/`unescape()` (dépréciés) ; token stocké durablement dans `localStorage` sans choix | `TextEncoder`/`TextDecoder` ; token en **session** par défaut, conservation optionnelle avec avertissement |
| 6 | `lessons2.json` | Tous les `url` vides → **aucun téléchargement** ; pas de `format`, pas de filière, pas de langue | Schéma enrichi : `format`, `size`, `duration`, `stream`, `lang`, `desc` ; vrais fichiers de démonstration PDF/DOCX/EPUB générés dans `files/` |
| 7 | `lessons2.json` | **Solutions collées aux énoncés** dans les exercices/sujets : impossible de s'entraîner avant de voir la réponse | Séparation automatique énoncé/solution ; la solution est **masquée** et révélée au clic (ou en PDF séparé) |
| 8 | Contenu | 10 ressources sur 13 en 3AS, 1 seule en 1AS ; aucun format fichier/vidéo | Rééquilibrage : 5×1AS, 5×2AS, 15×3AS ; ajout PDF/DOCX/EPUB/vidéos/résumés/livres |
| 9 | `README.md` | Texte cassé : `# dz-thanawi"# thanawi"` | README complet (installation, GitHub Pages, admin, schéma de données) |
| 10 | Général | Arabe uniquement, pas de SEO, pas de lecteur intégré, pas de favoris/progression | Interface **AR/FR/EN** (RTL/LTR), méta SEO, lecteur PDF + vidéo intégrés, favoris/progression, impression des cours, mode sombre, manifeste PWA |

## 2. Fonctionnalités ajoutées

- **Téléchargements réels** : PDF, Word, EPUB, PPT, ZIP, MP4 (admin accepte ces formats ; les fichiers sont servis depuis `files/`).
- **Visionneuses** : PDF et vidéo (YouTube intégré quand le lien contient un ID, sinon bouton externe ; MP4 natif) directement dans la page.
- **Cours en ligne** : leçons HTML lisibles sur place, avec bouton **Imprimer / enregistrer en PDF**.
- **Solutions à la demande** : bouton « Afficher la solution », corrigés PDF téléchargeables séparément.
- **Filtres** : niveau (1AS/2AS/3AS), filière (8 filières algériennes), matière (11), type, format, langue + recherche plein texte + tri.
- **Élève** : favoris ⭐, « marqué comme terminé » ✔, progression, compte à rebours du Bac (estimation mi-juin).
- **Admin v2** : édition des ressources, filière/langue/description, texte de cours en ligne, solution texte **ou** fichier, détection auto du format, FR/AR.

## 3. Suggestions inspirées de sites similaires

Comparaison réalisée avec les références algériennes et internationales (détails aussi sur la page « Conseils & sites similaires » du site) :

| Site | Sa force | Suggestion pour Thanawi |
|---|---|---|
| **DzExams** | Banque immense de devoirs/compositions classés par niveau et matière, corrigés types, très « mobile-first » (≈15 M de visites/mois) | Constituer progressivement une **banque de sujets par trimestre** (froud/ikhtibarat) ; garder le design rapide et léger pour mobile (c'est déjà le cas : 1 seul fichier HTML) |
| **Eddirasa** | Solutions des exercices des **manuels scolaires officiels** | Ajouter un type « حلول الكتاب المدرسي » : type `exercise` + chapitre = numéro d'exercice du manuel |
| **Ency Education** | Guides méthodologiques (comment réviser, méthodologie par matière) | Déjà amorcé (EPUB dissertation, page Conseils) — ajouter une méthodologie par matière (maths : rédaction d'une récurrence ; physique : analyse dimensionnelle…) |
| **ONEC / Ministère** | Sujets et corrigés **officiels** du Bac | Chaque juin, archiver les sujets officiels + corrigés types (PDF) par filière — la fonctionnalité existe déjà (sujet PDF + corrigé séparé) |
| **ONEFD** | Cours à distance structurés avec auto-évaluation | Ajouter des **QCM interactifs** corrigés instantanément (prochaine étape technique la plus utile) |
| **Khan Academy** | Parcours par chapitres, points, suivi de progression | Déjà : progression locale. Ensuite : « parcours chapitre » (cours → vidéo → exercices → sujet) enchaînés, badges |

### Feuille de route proposée (par priorité)

1. **Contenu** (le plus important) : viser au moins 1 cours + 1 série d'exercices + 1 sujet par chapitre et par matière principale ; archiver les sujets du Bac 2008→2026.
2. **QCM interactifs** avec correction immédiate et score (très demandé par les élèves, format ONFD/Khan).
3. **Vos propres vidéos YouTube** : créer une chaîne, puis coller les liens dans l'admin (les vidéos de démo pointent vers des recherches YouTube, à remplacer).
4. **Recherche dans les PDF** et sommaires de chapitres (table des matières par matière/niveau, façon manuel).
5. **Espace enseignants** : permettre à plusieurs professeurs de contribuer (chacun son token GitHub limité au dépôt) — déjà possible techniquement.
6. **Application mobile** : le site est installable (PWA, manifeste ajouté) ; une vraie app Android peut se générer plus tard à partir du même contenu.
7. **Statistiques de visites** respectueuses de la vie privée (compteur par ressource) pour savoir quoi produire en priorité.
8. **Accessibilité** : police agrandissable, lecture audio des cours (utile en langues), contraste renforcé.

## 4. Limites connues (à connaître)

- Site **statique** (GitHub Pages) : pas de comptes élèves ni de sauvegarde centralisée — favoris et progression restent **sur l'appareil**.
- Upload via l'API GitHub : fichiers conseillés **< 25 Mo** ; pour les vidéos, hébergez sur YouTube et collez le lien.
- Le contenu HTML des leçons (`body`) est considéré **de confiance** (publié par l'administrateur) : ne donnez le token qu'aux enseignants de confiance.
- Les 2 ressources vidéo de démonstration renvoient vers des **recherches YouTube** : remplacez-les par vos liens de vidéos pour un affichage intégré.
- Compte à rebours du Bac : **estimation** (mi-juin) en attendant la date officielle ONEC.
