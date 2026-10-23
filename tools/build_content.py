#!/usr/bin/env python3
"""Construit data/content.json (base unifiée du site) à partir de l'ancien
lessons2.json (13 leçons migrées, solutions séparées des énoncés pour les
exercices/sujets) + nouvelles ressources de démonstration (PDF/DOCX/EPUB/vidéo).
Réexécutable : python3 tools/build_content.py   (après tools/gen_samples.py)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def human_size(path):
    n = os.path.getsize(path)
    return f"{n / 1024:.0f} Ko" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} Mo"


LEVELS = [
    {"id": "1as", "name": {"ar": "السنة الأولى ثانوي", "fr": "1ère année secondaire", "en": "1st year secondary"}},
    {"id": "2as", "name": {"ar": "السنة الثانية ثانوي", "fr": "2e année secondaire", "en": "2nd year secondary"}},
    {"id": "3as", "name": {"ar": "السنة الثالثة ثانوي (بكالوريا)", "fr": "3e année secondaire (Bac)", "en": "3rd year secondary (Bac)"}},
]

STREAMS = [
    {"id": "all", "name": {"ar": "كل الشعب", "fr": "Toutes filières", "en": "All streams"}},
    {"id": "tronc-sciences", "name": {"ar": "جذع مشترك علوم وتكنولوجيا", "fr": "Tronc commun Sciences", "en": "Common core Science"}},
    {"id": "tronc-lettres", "name": {"ar": "جذع مشترك آداب", "fr": "Tronc commun Lettres", "en": "Common core Letters"}},
    {"id": "sci-exp", "name": {"ar": "علوم تجريبية", "fr": "Sciences expérimentales", "en": "Experimental Sciences"}},
    {"id": "math", "name": {"ar": "رياضيات", "fr": "Mathématiques", "en": "Mathematics"}},
    {"id": "tech-math", "name": {"ar": "تقني رياضي", "fr": "Technique mathématique", "en": "Technical Mathematics"}},
    {"id": "gestion-eco", "name": {"ar": "تسيير واقتصاد", "fr": "Gestion et économie", "en": "Management & Economics"}},
    {"id": "lettres-philo", "name": {"ar": "آداب وفلسفة", "fr": "Lettres et philosophie", "en": "Letters & Philosophy"}},
    {"id": "langues", "name": {"ar": "لغات أجنبية", "fr": "Langues étrangères", "en": "Foreign Languages"}},
]

SUBJECTS = [
    {"id": "math", "icon": "📐", "color": "#2563eb", "name": {"ar": "الرياضيات", "fr": "Mathématiques", "en": "Mathematics"}},
    {"id": "physics", "icon": "⚛️", "color": "#7c3aed", "name": {"ar": "العلوم الفيزيائية", "fr": "Physique", "en": "Physics"}},
    {"id": "science", "icon": "🧬", "color": "#059669", "name": {"ar": "علوم الطبيعة والحياة", "fr": "Sciences naturelles", "en": "Natural Sciences"}},
    {"id": "arabic", "icon": "📖", "color": "#b45309", "name": {"ar": "اللغة العربية", "fr": "Langue arabe", "en": "Arabic"}},
    {"id": "french", "icon": "🇫🇷", "color": "#dc2626", "name": {"ar": "اللغة الفرنسية", "fr": "Français", "en": "French"}},
    {"id": "english", "icon": "🇬🇧", "color": "#0891b2", "name": {"ar": "اللغة الإنجليزية", "fr": "Anglais", "en": "English"}},
    {"id": "history", "icon": "🏛️", "color": "#9333ea", "name": {"ar": "التاريخ والجغرافيا", "fr": "Histoire-Géographie", "en": "History-Geography"}},
    {"id": "philo", "icon": "💭", "color": "#db2777", "name": {"ar": "الفلسفة", "fr": "Philosophie", "en": "Philosophy"}},
    {"id": "islamic", "icon": "🕌", "color": "#65a30d", "name": {"ar": "العلوم الإسلامية", "fr": "Sciences islamiques", "en": "Islamic Sciences"}},
    {"id": "informatique", "icon": "💻", "color": "#475569", "name": {"ar": "المعلوماتية", "fr": "Informatique", "en": "Computer Science"}},
    {"id": "eco", "icon": "📊", "color": "#ea580c", "name": {"ar": "الاقتصاد والتسيير", "fr": "Économie et gestion", "en": "Economics & Management"}},
]

LANG_GUESS = {"french": "fr", "english": "en"}
STREAM_GUESS = {"philo": "lettres-philo"}

# --- Migration des anciennes leçons -------------------------------------
old = json.load(open(os.path.join(ROOT, "lessons2.json"), encoding="utf-8"))
SOL_RE = re.compile(r"<div class='bx'><b>الحل:</b>.*?</div>", re.S)

items = []
for it in old["items"]:
    body, solution = it.get("body", ""), ""
    if it["type"] in ("exercise", "exam"):  # séparer énoncé / solution
        sols = SOL_RE.findall(body)
        if sols:
            solution = "".join(
                f"<div class='bx solbox'><b>الحل {n}:</b> " + re.sub(r"^<div class='bx'><b>الحل:</b>\s*|</div>$", "", s) + "</div>"
                for n, s in enumerate(sols, 1)
            )
            body = SOL_RE.sub("", body)
    items.append({
        "id": it["id"], "level": it["level"], "stream": STREAM_GUESS.get(it["subject"], "all"),
        "subject": it["subject"], "chapter": it.get("chapter", ""), "type": it["type"],
        "title": it["title"], "desc": "", "lang": LANG_GUESS.get(it["subject"], "ar"),
        "url": it.get("url", ""), "format": "html", "size": "", "duration": "",
        "body": body, "solution": solution, "solutionUrl": "", "date": it.get("date", "2026-10-23"),
    })

# --- Nouvelles ressources -------------------------------------------------
def sz(rel):
    return human_size(os.path.join(ROOT, rel))

NEW = [
    {  # Cours PDF
        "id": "n1", "level": "3as", "stream": "sci-exp", "subject": "math",
        "chapter": "Fonctions exponentielle et logarithme", "type": "lesson",
        "title": "Fonctions exponentielle et logarithme népérien — cours complet (PDF)",
        "desc": "Cours PDF complet : définitions, propriétés, limites, croissances comparées, exemples corrigés et exercices d'application.",
        "lang": "fr", "url": "files/cours-exp-ln.pdf", "format": "pdf", "size": sz("files/cours-exp-ln.pdf"),
        "duration": "", "body": "", "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Sujet PDF + corrigé PDF séparé
        "id": "n2", "level": "3as", "stream": "sci-exp", "subject": "physics",
        "chapter": "Électricité — circuit RC", "type": "exam",
        "title": "Sujet type Bac — Physique : charge d'un condensateur (circuit RC) + corrigé PDF",
        "desc": "Sujet d'entraînement au format PDF (7 points, 1 h) avec corrigé type détaillé dans un fichier séparé : cherche d'abord, puis vérifie !",
        "lang": "fr", "url": "files/sujet-rc.pdf", "format": "pdf", "size": sz("files/sujet-rc.pdf"),
        "duration": "1 h", "body": "", "solution": "", "solutionUrl": "files/sujet-rc-corrige.pdf", "date": "2026-10-23",
    },
    {  # Exercices DOCX + solution HTML révélable
        "id": "n3", "level": "2as", "stream": "all", "subject": "math",
        "chapter": "Équations du second degré", "type": "exercise",
        "title": "Série d'exercices Word — Équations du second degré (DOCX)",
        "desc": "Fiche d'exercices au format Word (modifiable par l'enseignant) : discriminant, somme et produit, signe du trinôme, problème concret, paramètre m.",
        "lang": "fr", "url": "files/exercices-second-degre.docx", "format": "docx", "size": sz("files/exercices-second-degre.docx"),
        "duration": "", "body": "",
        "solution": "<div class='bx solbox'><b>Exercice 1 :</b> a) Δ = 1, x = 2 ou x = 3. b) Δ = 25, x = 1/2 ou x = −2. c) Δ = −16 &lt; 0 : aucune solution réelle. d) Δ = 0 : solution double x = 3/2.</div><div class='bx solbox'><b>Exercice 2 :</b> S = 7, P = 12 → 3 et 4 (racines de x² − 7x + 12 = 0). S = −3, P = −10 → 2 et −5.</div><div class='bx solbox'><b>Exercice 3 :</b> f(x) = −(x − 1)(x − 3). f(x) ≥ 0 sur [1 ; 3] (signe opposé à a entre les racines).</div><div class='bx solbox'><b>Exercice 4 :</b> demi-périmètre = 17, aire = 60 → les dimensions sont racines de x² − 17x + 60 = 0 : 5 m et 12 m.</div><div class='bx solbox'><b>Exercice 5 :</b> Δ = 4(m + 1)² − 4m² = 8m + 4. Solution double si m = −1/2 ; deux solutions distinctes si m &gt; −1/2.</div>",
        "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Livre EPUB
        "id": "n4", "level": "3as", "stream": "lettres-philo", "subject": "philo",
        "chapter": "Méthodologie", "type": "book",
        "title": "Livre numérique (EPUB) — Méthodologie de la dissertation philosophique",
        "desc": "E-book à lire sur téléphone ou liseuse : analyser un sujet, construire une problématique, choisir un plan (dialectique, analytique, comparatif) et rédiger.",
        "lang": "fr", "url": "files/methodo-dissertation.epub", "format": "epub", "size": sz("files/methodo-dissertation.epub"),
        "duration": "", "body": "", "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Cours vidéo (lien YouTube externe — à remplacer par vos vraies vidéos via l'admin)
        "id": "n5", "level": "3as", "stream": "all", "subject": "math",
        "chapter": "الدوال والنهايات", "type": "video",
        "title": "🎬 دروس فيديو: النهايات والاشتقاق (يوتيوب)",
        "desc": "Sélection de cours vidéo sur YouTube (limites et dérivées). Astuce enseignant : remplacez ce lien par vos propres vidéos depuis la page d'administration — elles s'afficheront directement dans le site.",
        "lang": "ar", "url": "https://www.youtube.com/results?search_query=%D8%A7%D9%84%D9%86%D9%87%D8%A7%D9%8A%D8%A7%D8%AA+%D9%88%D8%A7%D9%84%D8%A7%D8%B4%D8%AA%D9%82%D8%A7%D9%82+%D8%A7%D9%84%D8%AB%D8%A7%D9%84%D8%AB%D8%A9+%D8%AB%D8%A7%D9%86%D9%88%D9%8A",
        "format": "youtube", "size": "", "duration": "", "body": "", "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Cours vidéo EN
        "id": "n6", "level": "2as", "stream": "all", "subject": "english",
        "chapter": "Grammar — tenses", "type": "video",
        "title": "🎬 Video lessons: Present Perfect vs Past Simple (YouTube)",
        "desc": "Watch curated video lessons on YouTube to master the difference between the present perfect and the past simple, with practice examples.",
        "lang": "en", "url": "https://www.youtube.com/results?search_query=present+perfect+vs+past+simple",
        "format": "youtube", "size": "", "duration": "", "body": "", "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Leçon en ligne 1AS physique
        "id": "n7", "level": "1as", "stream": "tronc-sciences", "subject": "physics",
        "chapter": "الحركة والقوة", "type": "lesson",
        "title": "وصف الحركة: المسار والسرعة المتوسطة والسرعة اللحظية",
        "desc": "Leçon en ligne : référentiel, trajectoire, vitesse moyenne et instantanée, exemples et exercice corrigé.",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>المرجع والمسار</h3><p>لا معنى لوصف الحركة دون اختيار <b>مرجع</b> (جسم نعتبره ساكنًا). <b>المسار</b> هو مجموعة المواضع المتتالية التي يشغلها الجسم المتحرك: مستقيم أو منحني (دائري، قطع مكافئ...).</p><h3>السرعة المتوسطة</h3><div class='bx'>V = d / Δt &nbsp;حيث d المسافة المقطوعة و Δt المدة الزمنية. الوحدة الدولية: m/s. للتحويل: 1 m/s = 3,6 km/h.</div><h3>السرعة اللحظية</h3><p>هي سرعة الجسم في لحظة معينة، وتُقدر عمليًا بحساب السرعة المتوسطة بين لحظتين متقاربتين جدًا حول تلك اللحظة (كما في التسجيل بالتصوير المتعاقب).</p><h3>مثال محلول</h3><p>سيارة تقطع 180 km خلال ساعتين: V = 180/2 = 90 km/h = 90/3,6 = 25 m/s.</p><h3>تمرين</h3><p>درّاج يقطع 12 km خلال 30 دقيقة. احسب سرعته المتوسطة بـ km/h ثم بـ m/s.</p>",
        "solution": "<div class='bx solbox'><b>الحل:</b> Δt = 0,5 h إذن V = 12 / 0,5 = 24 km/h. وبـ m/s: 24 / 3,6 ≈ 6,7 m/s.</div>",
        "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Leçon en ligne 1AS français
        "id": "n8", "level": "1as", "stream": "all", "subject": "french",
        "chapter": "Le texte narratif", "type": "lesson",
        "title": "Le texte narratif : schéma narratif et temps du récit",
        "desc": "Cours en ligne : les 5 étapes du schéma narratif, le narrateur, et les temps verbaux du récit (imparfait / passé simple).",
        "lang": "fr", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>Qu'est-ce qu'un texte narratif ?</h3><p>Un texte narratif <b>raconte une histoire</b> : des événements qui se succèdent dans le temps, vécus par des personnages, réels ou fictifs.</p><h3>Le schéma narratif (5 étapes)</h3><div class='bx'>1) <b>Situation initiale</b> : le cadre, les personnages (équilibre).<br>2) <b>Élément déclencheur</b> : un événement perturbe l'équilibre.<br>3) <b>Péripéties</b> : les actions et les obstacles.<br>4) <b>Dénouement</b> : la résolution du problème.<br>5) <b>Situation finale</b> : un nouvel équilibre.</div><h3>Les temps du récit</h3><div class='bx'><b>Imparfait</b> : descriptions, arrière-plan, habitudes (« Il faisait nuit… »).<br><b>Passé simple</b> : actions qui font avancer l'histoire (« Soudain, la porte s'ouvrit. »).</div><h3>Le narrateur</h3><p>Le narrateur peut être <b>extérieur</b> à l'histoire (3e personne) ou <b>personnage</b> de l'histoire (1re personne : « je »). Il ne faut pas le confondre avec l'auteur.</p>",
        "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Exercices 2AS arabe avec solution
        "id": "n9", "level": "2as", "stream": "all", "subject": "arabic",
        "chapter": "النحو: الممنوع من الصرف", "type": "exercise",
        "title": "تمارين في الممنوع من الصرف (مع الحلول)",
        "desc": "Exercices en ligne : repérer les noms interdits de déclinaison complète (ممنوع من الصرف) et justifier. Solutions révélables après avoir cherché.",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>التمرين 1</h3><p>استخرج من الجمل الآتية الأسماء الممنوعة من الصرف وبيّن سبب المنع:<br>1) سافرتُ إلى وهرانَ.<br>2) مررتُ بمساجدَ كثيرةٍ.<br>3) قرأتُ عن عمرَ بن الخطاب.</p><h3>التمرين 2</h3><p>ضع الاسم «أحمد» و«فاطمة» في جملتين: مرة مجرورًا بحرف جر، ومرة مجرورًا بالإضافة، ولاحظ الفرق في الإعراب.</p>",
        "solution": "<div class='bx solbox'><b>التمرين 1:</b> «وهران» علم مؤنث (مدينة) + زيادة الألف والنون — مجرور بالفتحة. «مساجد» على وزن مَفاعِل (صيغة منتهى الجموع) — مجرور بالفتحة. «عمر» علم على وزن فُعَل مغير عن عامر (العلمية والعدل) — مجرور بالفتحة نيابة عن الكسرة.</div><div class='bx solbox'><b>التمرين 2:</b> بحرف الجر: «مررتُ بأحمدَ» (فتحة نيابة عن الكسرة). بالإضافة: «هذا كتابُ أحمدٍ» (يعود إلى الكسرة، لأن الممنوع من الصرف إذا أُضيف أو دخلت عليه «ال» جُرّ بالكسرة). ومثله: «سلّمتُ على فاطمةَ» / «حقيبةُ فاطمةٍ».</div>",
        "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Résumé histoire
        "id": "n10", "level": "3as", "stream": "all", "subject": "history",
        "chapter": "الحرب الباردة", "type": "summary",
        "title": "ملخص: الحرب الباردة (1947-1991) في صفحة واحدة",
        "desc": "Résumé express pour réviser avant le bac : causes, crises majeures (Berlin, Corée, Cuba), détente et fin de la guerre froide.",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>التعريف</h3><p>صراع إيديولوجي وسياسي وعسكري غير مباشر بين المعسكر الغربي بقيادة الولايات المتحدة والمعسكر الشرقي بقيادة الاتحاد السوفياتي، دون مواجهة عسكرية مباشرة بينهما.</p><h3>محطات أساسية</h3><div class='bx'>1947: مبدأ ترومان ومشروع مارشال.<br>1948-1949: حصار برلين والجسر الجوي.<br>1949: قيام حلف الناتو.<br>1950-1953: حرب كوريا.<br>1955: حلف وارسو.<br>1961: بناء جدار برلين.<br>1962: أزمة الصواريخ في كوبا (ذروة الخطر النووي).<br>1970s: مرحلة الانفراج (الوفاق) واتفاقيات الحد من الأسلحة.<br>1989: سقوط جدار برلين.<br>1991: تفكك الاتحاد السوفياتي ونهاية الحرب الباردة.</div><h3>مفهوم مفتاحي</h3><p><b>توازن الرعب النووي</b>: امتلاك الطرفين أسلحة نووية كافية لتدمير بعضهما جعل الحرب المباشرة مستحيلة، فتحولت المواجهة إلى حروب بالوكالة وسباق تسلح وسباق نحو الفضاء.</p>",
        "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Leçon 1AS sciences
        "id": "n11", "level": "1as", "stream": "tronc-sciences", "subject": "science",
        "chapter": "الخلية وحدة بنيوية", "type": "lesson",
        "title": "الخلية: البنية المجهرية ووظائف العضيات",
        "desc": "Leçon en ligne : structure de la cellule (membrane, cytoplasme, noyau, mitochondries…) et comparaison cellule animale / végétale.",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>مكونات الخلية</h3><div class='bx'><b>الغشاء الهيولي:</b> يحمي الخلية وينظم تبادل المواد مع الوسط الخارجي.<br><b>الهيولى (السيتوبلازم):</b> وسط شبه سائل تحدث فيه أغلب التفاعلات وتسبح فيه العضيات.<br><b>النواة:</b> تحتوي على المادة الوراثية (ADN) وتسير نشاط الخلية.<br><b>الميتوكوندري:</b> مقر التنفس الخلوي وإنتاج الطاقة (ATP).<br><b>الشبكة الهيولية وجهاز غولجي:</b> تركيب ونقل وتغليف البروتينات.</div><h3>الخلية النباتية تتميز بـ</h3><p>جدار خلوي (سليلوزي) يعطي الشكل والصلابة، وبلاستيدات خضراء (مقر التخليق الضوئي)، وفجوة عصارية كبيرة. أما الخلية الحيوانية فتفتقر إلى هذه العناصر الثلاثة.</p><h3>مثال تطبيقي</h3><p>خلايا العضلات غنية بالميتوكوندريات لأنها تحتاج إلى كمية كبيرة من الطاقة للانقباض: البنية مرتبطة بالوظيفة.</p>",
        "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Leçon informatique 1AS
        "id": "n12", "level": "1as", "stream": "all", "subject": "informatique",
        "chapter": "المحيط التكنولوجي", "type": "lesson",
        "title": "مكونات الحاسوب: العتاد الصلب والبرمجيات",
        "desc": "Leçon en ligne : matériel (processeur, mémoire RAM/ROM, périphériques d'entrée/sortie) et logiciels (système d'exploitation, applications).",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>العتاد الصلب (Hardware)</h3><div class='bx'><b>وحدة المعالجة المركزية (CPU):</b> تنفذ التعليمات وتعالج المعطيات.<br><b>ذاكرة RAM:</b> ذاكرة حية سريعة تُمحى عند إطفاء الجهاز.<br><b>القرص الصلب / SSD:</b> تخزين دائم للملفات والبرامج.<br><b>لوحات الإدخال:</b> لوحة المفاتيح، الفأرة، الماسح الضوئي.<br><b>لوحات الإخراج:</b> الشاشة، الطابعة، مكبرات الصوت.</div><h3>البرمجيات (Software)</h3><p><b>نظام التشغيل</b> (Windows, Linux, Android) يدير العتاد ويسمح بتشغيل التطبيقات. <b>التطبيقات</b> برامج موجهة لمهام محددة: معالج النصوص، الجداول، المتصفح...</p><h3>وحدات قياس السعة</h3><div class='bx'>1 Ko = 1024 Octets &nbsp;|&nbsp; 1 Mo = 1024 Ko &nbsp;|&nbsp; 1 Go = 1024 Mo &nbsp;|&nbsp; 1 To = 1024 Go</div>",
        "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
]

NEW += [
    {  # Sciences islamiques 1AS
        "id": "n13", "level": "1as", "stream": "all", "subject": "islamic",
        "chapter": "مقاصد الشريعة", "type": "lesson",
        "title": "مقاصد الشريعة الإسلامية الخمسة (الكليات)",
        "desc": "Leçon en ligne : les cinq finalités essentielles de la charia (religion, vie, raison, descendance, biens) avec exemples d'application.",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>ما المقصود بمقاصد الشريعة؟</h3><p>هي الغايات والحِكم التي شرع الله تعالى الأحكام لأجل تحقيقها، جلبًا للمصالح ودفعًا للمفاسد عن العباد في الدنيا والآخرة.</p><h3>الكليات الخمس (الضروريات)</h3><div class='bx'>1) <b>حفظ الدين:</b> شرع العبادات وحرية المعتقد.<br>2) <b>حفظ النفس:</b> تحريم القتل والقصاص وتحريم الاعتداء على الأبدان.<br>3) <b>حفظ العقل:</b> تحريم الخمر والمخدرات وكل ما يغيّبه.<br>4) <b>حفظ النسل/العرض:</b> تنظيم الزواج وتحريم الزنا والقذف.<br>5) <b>حفظ المال:</b> تحريم السرقة والربا والغش، وشرع الزكاة والمعاملات.</div><h3>مراتب المقاصد</h3><p>تترتب المقاصد إلى: <b>ضروريات</b> (لا تقوم الحياة إلا بها)، و<b>حاجيات</b> (تيسّر الحياة كالرخص في السفر)، و<b>تحسينيات</b> (مكارم الأخلاق والآداب). وعند التعارض يُقدَّم الأقوى: فالضروري قبل الحاجي، وحفظ النفس قبل حفظ المال.</p><h3>تطبيق</h3><p>منع قيادة السيارة تحت تأثير المسكر يجمع بين حفظ العقل وحفظ النفس وحفظ المال — مثال على اجتماع عدة كليات في حكم واحد.</p>",
        "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
    {  # Économie/gestion 3AS
        "id": "n14", "level": "3as", "stream": "gestion-eco", "subject": "eco",
        "chapter": "المحاسبة: الميزانية", "type": "lesson",
        "title": "الميزانية الختامية: الأصول (الاستعمالات) والخصوم (الموارد)",
        "desc": "Leçon en ligne pour la filière Gestion et économie : lire un bilan comptable, actif vs passif, et l'équilibre Actif = Passif.",
        "lang": "ar", "url": "", "format": "html", "size": "", "duration": "",
        "body": "<h3>تعريف الميزانية</h3><p>الميزانية وثيقة محاسبية تلخص في تاريخ معين (عادة 31 ديسمبر) ما تملكه المؤسسة وما عليها من التزامات: صورة فورية للذمة المالية.</p><h3>جانب الأصول (الاستعمالات)</h3><div class='bx'><b>أصول غير جارية:</b> تثبيتات (أراضٍ، مبانٍ، معدات) تستعمل لأكثر من سنة.<br><b>أصول جارية:</b> مخزونات، ديون على الزبائن، نقد في الصندوق والبنك — تتحول إلى سيولة خلال السنة.</div><h3>جانب الخصوم (الموارد)</h3><div class='bx'><b>الأموال الخاصة:</b> رأس المال + الاحتياطيات + نتيجة الدورة.<br><b>خصوم غير جارية:</b> قروض طويلة الأجل.<br><b>خصوم جارية:</b> ديون الموردين، أجور وضرائب مستحقة قصيرة الأجل.</div><h3>قاعدة التوازن</h3><p>في كل لحظة: <b>مجموع الأصول = مجموع الخصوم</b>، لأن كل مورد مالي (خصم) له استعمال (أصل). مثال: قرض بنكي بقيمة 1.000.000 دج لشراء آلة → الخصوم +1.000.000 (قرض) والأصول +1.000.000 (آلة): تبقى الميزانية متوازنة.</p>",
        "solution": "", "solutionUrl": "", "date": "2026-10-23",
    },
]

items = NEW + items  # nouveautés d'abord (tri par défaut = ordre d'ajout inverse géré côté site)
items.sort(key=lambda x: x["date"], reverse=True)

db = {"levels": LEVELS, "streams": STREAMS, "subjects": SUBJECTS, "items": items}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
out = os.path.join(ROOT, "data", "content.json")
json.dump(db, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"content.json écrit : {len(items)} ressources ({len(old['items'])} migrées + {len(NEW)} nouvelles), {os.path.getsize(out)} octets")
