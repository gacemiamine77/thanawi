# 🎓 Thanawi — Plateforme d'études secondaires

Site **gratuit et trilingue (arabe / français / anglais)** pour les élèves du secondaire
(**1AS, 2AS, 3AS — année du Bac**) :

- 📥 **Télécharger** cours, exercices et sujets d'examen : **PDF, Word (DOCX), EPUB, PowerPoint, ZIP, MP4…**
- 📚 **Suivre des cours en ligne** (leçons HTML lisibles dans le site, imprimables)
- 🎬 **Regarder des vidéos** (lecteur YouTube/MP4 intégré)
- 👁 **Visualiser les solutions** : énoncés et corrigés séparés — l'élève cherche d'abord, puis révèle la solution (ou télécharge le corrigé PDF)
- 🔎 **Filtrer** par niveau, filière, matière, type, format et langue + recherche libre
- ⭐ **Favoris et progression** (sauvegardés sur l'appareil), mode sombre, compte à rebours du Bac
- 💡 **Conseils de révision** et sélection de sites similaires/officiels

## Structure du projet

| Fichier | Rôle |
|---|---|
| `index.html` | Le site (une seule page, aucun build nécessaire) |
| `admin.html` | Panneau d'administration : publier/modifier/supprimer des ressources via l'API GitHub |
| `data/content.json` | Base de données du site : niveaux, filières, matières, ressources |
| `files/` | Fichiers téléchargeables (PDF, DOCX, EPUB…) |
| `lessons2.json` | Ancienne base (13 leçons) — déjà migrée vers `data/content.json`, conservée comme archive |
| `tools/build_content.py` | Script de migration/génération de `data/content.json` |
| `tools/gen_samples.py` | Régénère les fichiers d'exemple dans `files/` |
| `SUGGESTIONS.md` | Audit des erreurs corrigées + suggestions inspirées de sites similaires |

## Lancer le site en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

> ⚠️ Ouvrez le site via un serveur (http), pas en double-cliquant `index.html` :
> le chargement de `data/content.json` est bloqué par les navigateurs en `file://`.

## Publier sur GitHub Pages

1. Poussez le dépôt sur GitHub.
2. *Settings → Pages → Build and deployment → Source : Deploy from a branch → `main` / racine*.
3. Le site est en ligne sur `https://<votre-compte>.github.io/<dépôt>/` en 1–2 minutes.

## Ajouter du contenu (sans coder)

1. Ouvrez `admin.html` sur le site publié.
2. Créez un **Fine-grained token** GitHub limité à ce dépôt, avec la permission
   **Contents: Read and write** (*Settings → Developer settings → Fine-grained tokens*).
3. Renseignez compte / dépôt / branche / token, puis **Connexion**.
4. Ajoutez une ressource : niveau, matière, filière, type, titre, puis au choix
   **texte de cours en ligne**, **lien YouTube** ou **fichier** (PDF, Word, EPUB, MP4…)
   et sa **solution** (texte ou fichier séparé).
5. **Publier** → le site se met à jour automatiquement en 1–2 minutes.

Le token n'est jamais envoyé ailleurs qu'à `api.github.com` et n'est conservé que dans
votre navigateur (session, ou durablement si vous cochez l'option).

## Format d'une ressource (`data/content.json`)

```json
{
  "id": "abc123", "level": "3as", "stream": "sci-exp", "subject": "math",
  "chapter": "Fonctions", "type": "lesson|exercise|exam|video|summary|book",
  "title": "…", "desc": "…", "lang": "ar|fr|en",
  "url": "files/cours.pdf", "format": "pdf|docx|epub|youtube|mp4|html",
  "size": "320 Ko", "duration": "12 min",
  "body": "<h3>Leçon en ligne…</h3>",
  "solution": "<div class='bx solbox'>Corrigé…</div>",
  "solutionUrl": "files/corrige.pdf",
  "date": "2026-10-23"
}
```

## منصة ثانوي — باختصار

منصة مجانية ثلاثية اللغة لتلاميذ الطور الثانوي (الأولى والثانية والثالثة ثانوي):
تحميل الدروس والتمارين والمواضيع بصيغ PDF وWord وEPUB، متابعة دروس مصوّرة ودروس على الخط،
والاطلاع على الحلول بعد المحاولة. تتم إضافة المحتوى من صفحة `admin.html` دون الحاجة إلى برمجة.
