# 🎬 WatermarkTool

Script automatisé pour remplacer les watermarks sur des vidéos avec un watermark PNG personnalisé. Parfait pour les créateurs de contenu YouTube, TikTok et autres plateformes.

---

## ⚠️ Avertissement Légal Important

**Ce logiciel est fourni uniquement à titre éducatif et de facilitation du travail personnel.**

### Disclaimer de responsabilité

Ce projet est partagé à titre d'outil de facilitation technique uniquement. L'auteur **n'assume aucune responsabilité** pour :

- L'utilisation abusive de cet outil
- Les violations de droit d'auteur ou de propriété intellectuelle
- Les conséquences légales découlant de l'utilisation de ce logiciel
- Les dommages directs ou indirects causés par ce logiciel

**En téléchargeant et en utilisant ce logiciel, vous acceptez d'être seul responsable de vos actions et de respecter toutes les lois applicables.**

### Responsabilités légales de l'utilisateur

- **Respect du droit d'auteur** : Vous êtes seul responsable de l'utilisation de ce logiciel. Ne téléchargez, traitez ou redistribuez JAMAIS de contenu vidéo sans l'autorisation explicite de l'auteur original ou du détenteur des droits d'auteur.
- **Droit à l'image** : Le remplacement de watermarks ou la modification de vidéos ne vous autorise pas à les exploiter commercialement ou à les rediffuser sans consentement.

- **Propriété intellectuelle** : Toute vidéo publiée sur une plateforme (YouTube, TikTok, Instagram, etc.) est protégée par le droit d'auteur automatiquement. Respectez ces droits.

- **Conditions d'utilisation** : Consultez les conditions d'utilisation des plateformes de streaming pour connaître les règles sur les watermarks et la modification de contenu.

### Cas d'utilisation autorisés

✅ Remplacer vos propres watermarks sur **vos propres vidéos**  
✅ Traiter du contenu pour lequel vous disposez de droits explicites  
✅ Usage éducatif ou personnel uniquement

### Cas d'utilisation interdits

❌ Télécharger et traiter des vidéos d'autres personnes sans autorisation  
❌ Supprimer ou modifier les watermarks de contenu protégé  
❌ Redistribuer du contenu modifié comme vôtre  
❌ Violer les conditions d'utilisation de toute plateforme

**En utilisent ce logiciel, vous acceptez d'être seul responsable de vos actions et des conséquences légales.**

---

## 📋 Caractéristiques

- ✅ **Remplacement automatique** de watermarks sur batch de vidéos
- ✅ **Positionnement flexible** : haut-gauche, haut-droite, bas-gauche, bas-droite, centre
- ✅ **Redimensionnement adaptatif** du watermark (échelle ou largeur fixe)
- ✅ **Qualité configurableℜ** (CRF, codec, preset d'encodage)
- ✅ **Support multi-formats** : MP4, MOV, MKV, AVI, WebM, FLV
- ✅ **Conservation de l'audio** et de la résolution originale
- ✅ **Interface colorée** en terminal avec progression en temps réel
- ✅ **Fichier de configuration JSON** facilement modifiable
- ✅ **Version .exe** compilée pour Windows (optionnel)

---

## 🔧 Prérequis

### Dépendances système

- **Python 3.9+** (ou utiliser le `.exe` compilé)
- **FFmpeg** : [Télécharger FFmpeg](https://ffmpeg.org/download.html)

### Installation de FFmpeg

#### Option 1 : Installation complète (recommandée) ✅

L'installation complète ajoute FFmpeg à votre variable d'environnement `PATH`, ce qui le rend accessible depuis n'importe quel dossier du système. **C'est la méthode la plus sûre et recommandée.**

##### Windows

1. Télécharger depuis : https://ffmpeg.org/download.html (chercher "Windows builds")
2. Extraire l'archive complète
3. Ajouter le dossier `bin/` à la variable d'environnement `PATH` :
   - Clic droit sur "Poste de travail" → Propriétés
   - Variables d'environnement globales → PATH → Ajouter le chemin vers `bin/` de FFmpeg
   - Redémarrer le terminal ou l'ordinateur pour appliquer les changements
4. Vérifier : `ffmpeg -version` dans PowerShell

##### macOS

```bash
brew install ffmpeg
```

##### Linux (Ubuntu/Debian)

```bash
sudo apt-get install ffmpeg
```

---

#### Option 2 : FFmpeg portable à côté du .exe ⚠️ (non recommandé)

**Vous pouvez** placer le dossier `bin/` de FFmpeg directement dans le dossier `nowatermark/` à côté de `WatermarkTool.exe`. Cela peut fonctionner dans certains cas, **mais ce n'est pas recommandé** car :

- ❌ Dépend de la configuration du système
- ❌ Peut causer des incompatibilités
- ❌ Augmente la taille totale du projet

**Si vous choisissez cette option :**

```
nowatermark/
├── WatermarkTool.exe
├── watermark.png
├── ffmpeg.exe     ← À côté du .exe
├── ffprobe.exe    ← À côté du .exe
└── .config/
```

**Mieux vaut utiliser l'Option 1 (installation complète) pour éviter les problèmes !**

---

## 📦 Installation

### Option 1 : Utiliser le fichier .exe (Windows recommandé)

1. Télécharger le projet
2. Placer vos vidéos dans le dossier `nowatermark/`
3. Placer votre watermark PNG dans le dossier `nowatermark/` avec le nom `watermark.png`
4. Double-cliquer sur `WatermarkTool.exe`
5. Les vidéos traitées apparaissent dans le dossier `render/`

### Option 2 : Utiliser la version Python

#### Cloner le projet

```bash
git clone https://github.com/Nuxhi/remove-or-add-watermark-for-ytb-tiktok.git
cd remove-or-add-watermark-for-ytb-tiktok
```

#### Créer un environnement Python virtuel

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
source .venv/bin/activate  # Linux/macOS
```

#### Installer les dépendances (optionnel, le script n'en a pas)

```bash
pip install -r requirements.txt  # Si applicable
```

#### Exécuter le script

```bash
python nowatermark/main.py
```

---

## ⚙️ Configuration

Le fichier de configuration se trouve à : `nowatermark/.config/settings.json`

### Paramètres principaux

```json
{
  "position_watermark": "top-left",
  "marge_x": 40,
  "marge_y": 200,
  "echelle_watermark": 0.6,
  "largeur_watermark": null,
  "qualite_crf": 0,
  "codec_video": "libx264",
  "preset_encodage": "veryslow",
  "extensions_video": [".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv"]
}
```

### Explications des paramètres

| Paramètre            | Valeurs                                                          | Description                                                                                              |
| -------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `position_watermark` | `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center` | Position du watermark sur la vidéo                                                                       |
| `marge_x`            | Pixels                                                           | Distance du bord gauche/droit (en pixels)                                                                |
| `marge_y`            | Pixels                                                           | Distance du bord haut/bas (en pixels)                                                                    |
| `echelle_watermark`  | 0.0 - ∞                                                          | 1.0 = taille originale, 0.5 = moitié, 2.0 = double                                                       |
| `largeur_watermark`  | `null` ou pixels                                                 | Largeur fixe du watermark (remplace `echelle_watermark` si défini)                                       |
| `qualite_crf`        | 0 - 51                                                           | 0 = max qualité, 18 = quasi parfait, 23 = bon, 28 = accepte. Plus bas = meilleure qualité + gros fichier |
| `codec_video`        | `libx264`, `libx265`                                             | H.264 (universel) ou H.265 (meilleure compression)                                                       |
| `preset_encodage`    | `ultrafast` à `veryslow`                                         | Équilibre vitesse/compression. `medium` recommandé                                                       |
| `extensions_video`   | Array                                                            | Formats de vidéos à traiter                                                                              |

### Presets recommandés

**Pour YouTube/TikTok (bon compromis)**

```json
{
  "qualite_crf": 18,
  "codec_video": "libx264",
  "preset_encodage": "medium"
}
```

**Qualité maximale (lent, gros fichier)**

```json
{
  "qualite_crf": 0,
  "codec_video": "libx265",
  "preset_encodage": "veryslow"
}
```

**Encoded rapide et léger**

```json
{
  "qualite_crf": 28,
  "codec_video": "libx264",
  "preset_encodage": "fast"
}
```

---

## 🚀 Utilisation

### Préparation des fichiers

1. **Créer la structure** :

   ```
   remove-or-add-watermark-for-ytb-tiktok/
   ├── nowatermark/
   │   ├── main.py
   │   ├── WatermarkTool.exe  (optionnel)
   │   ├── watermark.png      (votre logo/watermark)
   │   ├── .config/
   │   │   └── settings.json
   │   └── video1.mp4         (vos vidéos)
   │   └── video2.mp4
   ├── render/                (sera créé automatiquement)
   ├── README.md
   ├── LICENSE
   └── .gitignore
   ```

2. **Ajouter votre watermark** :
   - Placer votre image PNG dans `nowatermark/watermark.png`
   - Format recommandé : PNG avec transparence
   - Taille : 200-500 pixels de large

3. **Placer vos vidéos** :
   - Mettre toutes les vidéos à traiter dans le dossier `nowatermark/`

4. **Configurer les paramètres** (optionnel) :
   - Éditer `nowatermark/.config/settings.json`
   - Les paramètres peuvent être changés à chaque exécution

### Lancer le traitement

#### Windows (.exe)

```bash
cd nowatermark
WatermarkTool.exe
```

#### Ligne de commande (Python)

```bash
cd nowatermark
python main.py
```

### Résultats

Les vidéos traitées se trouvent dans le dossier `render/` avec le même nom que l'original.

---

## 📝 Exemple d'exécution

```
======================================================================
  🎬 SCRIPT DE REMPLACEMENT DE WATERMARK
  Remplace l'ancien watermark par un nouveau watermark PNG
======================================================================

✅ FFmpeg détecté : ffmpeg version 6.0
✅ Configuration chargée depuis : .config/settings.json

📂 Dossier d'entrée  : C:\...\nowatermark
📂 Dossier de sortie : C:\...\render
🖼️  Watermark         : C:\...\nowatermark\watermark.png

📋 3 vidéo(s) trouvée(s) à traiter :
   1. video1.mp4 (12:34)
   2. video2.mp4 (05:23)
   3. video3.mp4 (08:15)

⚙️  Configuration :
   Position    : top-left
   Marge       : 40px x 200px
   Échelle     : 0.6x
   Qualité CRF : 0
   Codec       : libx264
   Preset      : veryslow

----------------------------------------------------------------------

🔄 [1/3] Traitement de : video1.mp4
   ✅ Terminé en 05:12 — 456.3 Mo

🔄 [2/3] Traitement de : video2.mp4
   ✅ Terminé en 02:18 — 198.7 Mo

🔄 [3/3] Traitement de : video3.mp4
   ✅ Terminé en 03:45 — 287.2 Mo

======================================================================
  📊 RÉSUMÉ
  Vidéos traitées avec succès : 3/3
  Temps total                 : 11:15
  Dossier de sortie           : C:\...\render
======================================================================

🗑️  Voulez-vous supprimer les 3 vidéo(s) originale(s) traitées ?
   - video1.mp4
   - video2.mp4
   - video3.mp4

   Supprimer ? (o/N) : n
   Fichiers originaux conservés.

Appuyez sur Entrée pour fermer...
```

---

## 🛠️ Compilation en .exe (pour développeurs)

Si vous avez modifié le code et voulez regénérer le `.exe` :

```bash
# Installer PyInstaller (une fois)
pip install pyinstaller

# Compiler
pyinstaller --onefile --name WatermarkTool --console nowatermark/main.py

# Le .exe se trouve dans : dist/WatermarkTool.exe
```

---

## 🔗 Ressources externes

- **GitHub du projet** : https://github.com/Nuxhi/remove-or-add-watermark-for-ytb-tiktok
- **FFmpeg** : https://ffmpeg.org/download.html
- **Documentation FFmpeg** : https://ffmpeg.org/documentation.html
- **Overlay Filter FFmpeg** : https://ffmpeg.org/ffmpeg-filters.html#overlay-1
- **Signaler un bug** : https://github.com/Nuxhi/remove-or-add-watermark-for-ytb-tiktok/issues

---

## ⚠️ Dépannage

### ❌ "FFmpeg n'est pas installé"

**Solution** : Télécharger et installer FFmpeg depuis https://ffmpeg.org/download.html, puis ajouter le dossier `bin/` à votre PATH.

### ❌ "Le fichier watermark est introuvable"

**Solution** : Placer votre image PNG nommée `watermark.png` dans le dossier `nowatermark/`.

### ❌ "Erreur de syntaxe dans le fichier de configuration"

**Solution** : Vérifier la syntaxe JSON du fichier `.config/settings.json` (virgules, guillemets, crochets).

### ❌ Le watermark est flou ou trop petit

**Solution** :

- Augmenter `echelle_watermark` (ex: `1.0` au lieu de `0.6`)
- Ou utiliser `largeur_watermark` pour une largeur fixe (ex: `300`)

### ❌ L'encodage est très lent

**Solution** : Réduire le preset d'encodage (`medium` au lieu de `veryslow`).

---

## 📄 Licence

Ce projet est distribué sous la licence **MIT**.

**Vous êtes libre de :**

- ✅ Utiliser le logiciel à titre commercial ou personnel
- ✅ Modifier le code source
- ✅ Distribuer le logiciel modifié
- ✅ Utiliser le code dans vos propres projets

**À condition de :**

- ℹ️ Conserver la notice de copyright et la licence
- ℹ️ Accepter que le logiciel est fourni "tel quel" sans garantie

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

- **Nuxhi**
- Date : 2026-03-08

---

## 🤝 Contribution

Les contributions, suggestions et améliorations sont les bienvenues ! N'hésitez pas à :

- Ouvrir une issue pour signaler un bug ou proposer une feature
- Fork le projet et soumettre une pull request
- Partager le projet si vous le trouvez utile

**Repository** : https://github.com/Nuxhi/remove-or-add-watermark-for-ytb-tiktok

---

**Bonne utilisation ! 🎉**
