#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 Script de remplacement automatique de watermark sur des vidéos
=============================================================================

 Ce script parcourt un dossier contenant des vidéos et applique un watermark
 PNG par-dessus l'ancien watermark "Internet Render" (en haut à gauche).

 Il utilise FFmpeg via subprocess pour superposer l'image PNG sur chaque
 vidéo, du début à la fin, tout en conservant la résolution, la qualité
 et l'audio d'origine.

 Auteur : Nuxhi
 Date   : 2026-03-08
=============================================================================
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path


# =============================================================================
# ========================= COULEURS CONSOLE ==================================
# =============================================================================
# Codes ANSI pour colorer le texte dans le terminal

class Couleurs:
    """Classe contenant les codes ANSI pour colorer le texte dans le terminal."""
    RESET   = "\033[0m"       # Réinitialiser la couleur
    ROUGE   = "\033[91m"      # Erreurs
    VERT    = "\033[92m"      # Succès
    JAUNE   = "\033[93m"      # Avertissements
    BLEU    = "\033[94m"      # Informations
    MAGENTA = "\033[95m"      # Titres / mise en avant
    CYAN    = "\033[96m"      # Détails / configuration
    GRAS    = "\033[1m"       # Texte en gras
    DIM     = "\033[2m"       # Texte atténué


# Activer les couleurs ANSI sur Windows (cmd / PowerShell)
if sys.platform == "win32":
    os.system("")


# =============================================================================
# Détection du répertoire de base :
#   - Si on est dans un .exe compilé (PyInstaller), on utilise le dossier du .exe
#   - Sinon, on utilise le dossier du script .py
# =============================================================================
if getattr(sys, 'frozen', False):
    # Mode .exe : sys.executable = chemin du .exe
    DOSSIER_BASE = os.path.dirname(os.path.abspath(sys.executable))
else:
    # Mode script Python normal
    DOSSIER_BASE = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# ========================= SECTION DE CONFIGURATION ==========================
# =============================================================================

# Chemin vers le fichier de configuration JSON
CHEMIN_CONFIG = os.path.join(DOSSIER_BASE, ".config", "settings.json")

def charger_configuration():
    """
    Charge la configuration depuis le fichier .config/settings.json.
    Si le fichier n'existe pas, crée un fichier par défaut.
    Retourne un dictionnaire avec les paramètres.
    """
    # Valeurs par défaut si le fichier n'existe pas
    config_defaut = {
        "position_watermark": "top-left",
        "marge_x": 40,
        "marge_y": 200,
        "echelle_watermark": 0.6,
        "largeur_watermark": None,
        "qualite_crf": 0,
        "codec_video": "libx264",
        "preset_encodage": "veryslow",
        "extensions_video": [".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv"]
    }

    if not os.path.isfile(CHEMIN_CONFIG):
        # Créer le dossier .config et le fichier par défaut
        print(f"{Couleurs.JAUNE}⚠️  Fichier de configuration introuvable.{Couleurs.RESET}")
        print(f"{Couleurs.JAUNE}   Création du fichier par défaut : {CHEMIN_CONFIG}{Couleurs.RESET}")
        os.makedirs(os.path.dirname(CHEMIN_CONFIG), exist_ok=True)
        with open(CHEMIN_CONFIG, "w", encoding="utf-8") as f:
            json.dump(config_defaut, f, indent=4, ensure_ascii=False)
        return config_defaut

    try:
        with open(CHEMIN_CONFIG, "r", encoding="utf-8") as f:
            config_fichier = json.load(f)
        # Fusionner : les valeurs du fichier écrasent les valeurs par défaut
        # Les clés commençant par "_" sont des commentaires, on les ignore
        for cle, valeur in config_fichier.items():
            if not cle.startswith("_"):
                config_defaut[cle] = valeur
        print(f"{Couleurs.VERT}✅ Configuration chargée depuis : {CHEMIN_CONFIG}{Couleurs.RESET}")
        return config_defaut
    except json.JSONDecodeError as e:
        print(f"{Couleurs.ROUGE}❌ Erreur de syntaxe dans le fichier de configuration :{Couleurs.RESET}")
        print(f"{Couleurs.ROUGE}   {e}{Couleurs.RESET}")
        print(f"{Couleurs.JAUNE}   Utilisation des valeurs par défaut.{Couleurs.RESET}")
        return config_defaut
    except Exception as e:
        print(f"{Couleurs.ROUGE}❌ Erreur lors du chargement de la configuration : {e}{Couleurs.RESET}")
        return config_defaut


# Charger la configuration au démarrage
CONFIG = charger_configuration()

# Dossier contenant les vidéos à traiter (même dossier que le .exe ou le script)
DOSSIER_ENTREE = DOSSIER_BASE

# Dossier de sortie pour les vidéos traitées (sera créé automatiquement)
DOSSIER_SORTIE = os.path.join(DOSSIER_BASE, "..", "render")

# Chemin vers l'image PNG du watermark
CHEMIN_WATERMARK = os.path.join(DOSSIER_BASE, "watermark.png")

# Paramètres chargés depuis le fichier de configuration
POSITION_WATERMARK = CONFIG["position_watermark"]
MARGE_X            = CONFIG["marge_x"]
MARGE_Y            = CONFIG["marge_y"]
ECHELLE_WATERMARK  = CONFIG["echelle_watermark"]
LARGEUR_WATERMARK  = CONFIG["largeur_watermark"]
EXTENSIONS_VIDEO   = tuple(CONFIG["extensions_video"])
QUALITE_CRF        = CONFIG["qualite_crf"]
CODEC_VIDEO        = CONFIG["codec_video"]
PRESET_ENCODAGE    = CONFIG["preset_encodage"]


# =============================================================================
# ========================= FONCTIONS UTILITAIRES =============================
# =============================================================================

def verifier_ffmpeg():
    """
    Vérifie que FFmpeg est installé et accessible dans le PATH.
    Quitte le programme avec un message d'erreur si FFmpeg est introuvable.
    """
    try:
        # On exécute 'ffmpeg -version' pour vérifier sa présence
        resultat = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        if resultat.returncode == 0:
            # Extraire la première ligne pour afficher la version
            version = resultat.stdout.decode("utf-8", errors="replace").split("\n")[0]
            print(f"{Couleurs.VERT}✅ FFmpeg détecté : {version}{Couleurs.RESET}")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"{Couleurs.ROUGE}❌ FFmpeg n'est pas installé ou n'est pas dans le PATH.{Couleurs.RESET}")
        print(f"{Couleurs.ROUGE}   Téléchargez-le depuis : https://ffmpeg.org/download.html{Couleurs.RESET}")
        print(f"{Couleurs.ROUGE}   Sous Windows, ajoutez le dossier bin/ de FFmpeg à votre variable PATH.{Couleurs.RESET}")
        sys.exit(1)


def verifier_fichiers():
    """
    Vérifie que le dossier d'entrée et le fichier watermark existent.
    Crée le dossier de sortie s'il n'existe pas.
    """
    # Vérifier le dossier d'entrée
    if not os.path.isdir(DOSSIER_ENTREE):
        print(f"{Couleurs.ROUGE}❌ Le dossier d'entrée n'existe pas : {DOSSIER_ENTREE}{Couleurs.RESET}")
        sys.exit(1)

    # Vérifier le fichier watermark
    if not os.path.isfile(CHEMIN_WATERMARK):
        print(f"{Couleurs.ROUGE}❌ Le fichier watermark est introuvable : {CHEMIN_WATERMARK}{Couleurs.RESET}")
        print(f"{Couleurs.ROUGE}   Placez votre image PNG dans : {CHEMIN_WATERMARK}{Couleurs.RESET}")
        sys.exit(1)

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(DOSSIER_SORTIE, exist_ok=True)
    print(f"{Couleurs.BLEU}📂 Dossier d'entrée  : {os.path.abspath(DOSSIER_ENTREE)}{Couleurs.RESET}")
    print(f"{Couleurs.BLEU}📂 Dossier de sortie : {os.path.abspath(DOSSIER_SORTIE)}{Couleurs.RESET}")
    print(f"{Couleurs.BLEU}🖼️  Watermark         : {os.path.abspath(CHEMIN_WATERMARK)}{Couleurs.RESET}")


def lister_videos(dossier):
    """
    Liste tous les fichiers vidéo dans le dossier donné (non récursif).
    Retourne une liste de chemins absolus triés par nom.
    """
    videos = []
    for fichier in os.listdir(dossier):
        # Vérifier si l'extension correspond à un format vidéo supporté
        if any(fichier.lower().endswith(ext) for ext in EXTENSIONS_VIDEO):
            chemin_complet = os.path.join(dossier, fichier)
            # Ne prendre que les fichiers (pas les dossiers)
            if os.path.isfile(chemin_complet):
                videos.append(chemin_complet)
    # Tri alphabétique pour un traitement prévisible
    videos.sort()
    return videos


def calculer_position_overlay():
    """
    Génère la chaîne de positionnement FFmpeg pour l'overlay
    en fonction de la configuration POSITION_WATERMARK, MARGE_X et MARGE_Y.

    Retourne une chaîne au format FFmpeg pour le filtre overlay.
    Exemples : "10:10" (haut-gauche), "main_w-overlay_w-10:10" (haut-droite)
    """
    positions = {
        "top-left":     f"{MARGE_X}:{MARGE_Y}",
        "top-right":    f"main_w-overlay_w-{MARGE_X}:{MARGE_Y}",
        "bottom-left":  f"{MARGE_X}:main_h-overlay_h-{MARGE_Y}",
        "bottom-right": f"main_w-overlay_w-{MARGE_X}:main_h-overlay_h-{MARGE_Y}",
        "center":       "(main_w-overlay_w)/2:(main_h-overlay_h)/2",
    }

    if POSITION_WATERMARK not in positions:
        print(f"⚠️  Position inconnue '{POSITION_WATERMARK}', utilisation de 'top-left' par défaut.")
        return positions["top-left"]

    return positions[POSITION_WATERMARK]


def obtenir_duree_video(chemin_video):
    """
    Utilise ffprobe pour obtenir la durée de la vidéo en secondes.
    Retourne un float ou None en cas d'erreur.
    """
    try:
        resultat = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                chemin_video
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        duree = float(resultat.stdout.decode("utf-8").strip())
        return duree
    except (ValueError, Exception):
        return None


def formater_duree(secondes):
    """
    Convertit un nombre de secondes en format lisible HH:MM:SS.
    """
    if secondes is None:
        return "??:??:??"
    heures = int(secondes // 3600)
    minutes = int((secondes % 3600) // 60)
    secs = int(secondes % 60)
    if heures > 0:
        return f"{heures:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def construire_filtre_watermark():
    """
    Construit le filtre complexe FFmpeg pour superposer le watermark.

    Le filtre :
    1. Redimensionne le watermark selon ECHELLE_WATERMARK ou LARGEUR_WATERMARK
    2. Superpose le watermark sur la vidéo à la position configurée

    Retourne la chaîne du filtre complexe FFmpeg.
    """
    position = calculer_position_overlay()

    # Construction du redimensionnement du watermark
    if LARGEUR_WATERMARK is not None:
        # Largeur fixe en pixels, hauteur proportionnelle
        scale_filter = f"[1:v]scale={LARGEUR_WATERMARK}:-1[wm]"
    elif ECHELLE_WATERMARK != 1.0:
        # Échelle relative (multiplication de la taille originale)
        scale_filter = f"[1:v]scale=iw*{ECHELLE_WATERMARK}:ih*{ECHELLE_WATERMARK}[wm]"
    else:
        # Pas de redimensionnement, taille originale
        scale_filter = "[1:v]copy[wm]"

    # Filtre complet : redimensionner le watermark puis le superposer
    filtre = f"{scale_filter};[0:v][wm]overlay={position}"

    return filtre


def traiter_video(chemin_video, chemin_sortie):
    """
    Applique le watermark PNG sur une vidéo donnée avec FFmpeg.

    Args:
        chemin_video: Chemin absolu vers la vidéo source
        chemin_sortie: Chemin absolu vers le fichier de sortie

    Retourne True si le traitement a réussi, False sinon.
    """
    # Construire le filtre de watermark
    filtre = construire_filtre_watermark()

    # Construction de la commande FFmpeg
    commande = [
        "ffmpeg",
        "-y",                       # Écraser le fichier de sortie s'il existe
        "-i", chemin_video,         # Vidéo source (input 0)
        "-i", CHEMIN_WATERMARK,     # Image watermark (input 1)
        "-filter_complex", filtre,  # Filtre de superposition
        "-c:v", CODEC_VIDEO,        # Codec vidéo
        "-preset", PRESET_ENCODAGE, # Preset d'encodage
        "-crf", str(QUALITE_CRF),  # Qualité (CRF)
        "-c:a", "copy",             # Copier l'audio sans ré-encodage
        "-movflags", "+faststart",  # Optimisation pour lecture web
        chemin_sortie               # Fichier de sortie
    ]

    try:
        # Exécuter FFmpeg et capturer la sortie en temps réel
        processus = subprocess.Popen(
            commande,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )

        # Attendre la fin du processus et récupérer la sortie d'erreur
        _, stderr = processus.communicate()

        if processus.returncode == 0:
            return True
        else:
            # Afficher l'erreur FFmpeg pour le débogage
            erreur = stderr.decode("utf-8", errors="replace")
            print(f"\n{Couleurs.ROUGE}❌ Erreur FFmpeg (code {processus.returncode}) :{Couleurs.RESET}")
            # Afficher seulement les dernières lignes pertinentes
            lignes_erreur = erreur.strip().split("\n")
            for ligne in lignes_erreur[-5:]:
                print(f"{Couleurs.DIM}   {ligne}{Couleurs.RESET}")
            return False

    except FileNotFoundError:
        print(f"{Couleurs.ROUGE}❌ FFmpeg introuvable. Vérifiez votre installation.{Couleurs.RESET}")
        return False
    except Exception as e:
        print(f"{Couleurs.ROUGE}❌ Erreur inattendue : {e}{Couleurs.RESET}")
        return False


# =============================================================================
# ========================= FONCTION PRINCIPALE ===============================
# =============================================================================

def main():
    """
    Point d'entrée principal du script.
    Orchestre la vérification, le listage et le traitement de toutes les vidéos.
    """
    print(f"{Couleurs.MAGENTA}{Couleurs.GRAS}{"=" * 70}{Couleurs.RESET}")
    print(f"{Couleurs.MAGENTA}{Couleurs.GRAS}  🎬 SCRIPT DE REMPLACEMENT DE WATERMARK{Couleurs.RESET}")
    print(f"{Couleurs.MAGENTA}  Remplace l'ancien watermark par un nouveau watermark PNG{Couleurs.RESET}")
    print(f"{Couleurs.MAGENTA}{Couleurs.GRAS}{"=" * 70}{Couleurs.RESET}")
    print()

    # Étape 1 : Vérifier que FFmpeg est installé
    verifier_ffmpeg()
    print()

    # Étape 2 : Vérifier les fichiers et dossiers
    verifier_fichiers()
    print()

    # Étape 3 : Lister les vidéos à traiter
    videos = lister_videos(DOSSIER_ENTREE)

    if not videos:
        print(f"{Couleurs.JAUNE}⚠️  Aucune vidéo trouvée dans : {os.path.abspath(DOSSIER_ENTREE)}{Couleurs.RESET}")
        print(f"{Couleurs.JAUNE}   Extensions supportées : {', '.join(EXTENSIONS_VIDEO)}{Couleurs.RESET}")
        sys.exit(0)

    print(f"{Couleurs.CYAN}📋 {len(videos)} vidéo(s) trouvée(s) à traiter :{Couleurs.RESET}")
    for i, video in enumerate(videos, 1):
        nom = os.path.basename(video)
        duree = obtenir_duree_video(video)
        print(f"{Couleurs.CYAN}   {i}. {nom} ({formater_duree(duree)}){Couleurs.RESET}")
    print()

    # Étape 4 : Afficher la configuration utilisée
    print(f"{Couleurs.CYAN}⚙️  Configuration :{Couleurs.RESET}")
    print(f"{Couleurs.DIM}   Position    : {POSITION_WATERMARK}{Couleurs.RESET}")
    print(f"{Couleurs.DIM}   Marge       : {MARGE_X}px x {MARGE_Y}px{Couleurs.RESET}")
    if LARGEUR_WATERMARK:
        print(f"{Couleurs.DIM}   Largeur WM  : {LARGEUR_WATERMARK}px{Couleurs.RESET}")
    else:
        print(f"{Couleurs.DIM}   Échelle     : {ECHELLE_WATERMARK}x{Couleurs.RESET}")
    print(f"{Couleurs.DIM}   Qualité CRF : {QUALITE_CRF}{Couleurs.RESET}")
    print(f"{Couleurs.DIM}   Codec       : {CODEC_VIDEO}{Couleurs.RESET}")
    print(f"{Couleurs.DIM}   Preset      : {PRESET_ENCODAGE}{Couleurs.RESET}")
    print()

    # Étape 5 : Traiter chaque vidéo
    print("-" * 70)
    succes = 0
    echecs = 0
    temps_debut_total = time.time()

    for i, chemin_video in enumerate(videos, 1):
        nom_fichier = os.path.basename(chemin_video)
        # Le fichier de sortie garde le même nom dans le dossier de sortie
        chemin_sortie = os.path.join(DOSSIER_SORTIE, nom_fichier)

        print(f"\n{Couleurs.BLEU}{Couleurs.GRAS}🔄 [{i}/{len(videos)}] Traitement de : {nom_fichier}{Couleurs.RESET}")

        # Obtenir la durée pour l'affichage
        duree = obtenir_duree_video(chemin_video)
        if duree:
            print(f"{Couleurs.DIM}   Durée : {formater_duree(duree)}{Couleurs.RESET}")

        temps_debut = time.time()

        # Lancer le traitement FFmpeg
        resultat = traiter_video(chemin_video, chemin_sortie)

        temps_ecoule = time.time() - temps_debut

        if resultat:
            # Vérifier que le fichier de sortie existe et a une taille > 0
            if os.path.isfile(chemin_sortie) and os.path.getsize(chemin_sortie) > 0:
                taille_mo = os.path.getsize(chemin_sortie) / (1024 * 1024)
                print(f"{Couleurs.VERT}   ✅ Terminé en {formater_duree(temps_ecoule)} — {taille_mo:.1f} Mo{Couleurs.RESET}")
                succes += 1
            else:
                print(f"{Couleurs.ROUGE}   ❌ Le fichier de sortie est vide ou introuvable{Couleurs.RESET}")
                echecs += 1
        else:
            echecs += 1
            print(f"{Couleurs.ROUGE}   ❌ Échec du traitement{Couleurs.RESET}")

    # Étape 6 : Résumé final
    temps_total = time.time() - temps_debut_total
    print()
    print(f"{Couleurs.MAGENTA}{Couleurs.GRAS}{"=" * 70}{Couleurs.RESET}")
    print(f"{Couleurs.MAGENTA}{Couleurs.GRAS}  📊 RÉSUMÉ{Couleurs.RESET}")
    print(f"{Couleurs.VERT}  Vidéos traitées avec succès : {succes}/{len(videos)}{Couleurs.RESET}")
    if echecs > 0:
        print(f"{Couleurs.ROUGE}  Vidéos en erreur            : {echecs}{Couleurs.RESET}")
    print(f"{Couleurs.CYAN}  Temps total                 : {formater_duree(temps_total)}{Couleurs.RESET}")
    print(f"{Couleurs.CYAN}  Dossier de sortie           : {os.path.abspath(DOSSIER_SORTIE)}{Couleurs.RESET}")
    print(f"{Couleurs.MAGENTA}{Couleurs.GRAS}{"=" * 70}{Couleurs.RESET}")

    # Étape 7 : Proposer la suppression des fichiers originaux traités
    if succes > 0:
        print()
        # Liste des vidéos qui ont été traitées avec succès
        videos_a_supprimer = []
        for chemin_video in videos:
            nom_fichier = os.path.basename(chemin_video)
            chemin_sortie = os.path.join(DOSSIER_SORTIE, nom_fichier)
            # Ne proposer que les vidéos dont le rendu a réussi
            if os.path.isfile(chemin_sortie) and os.path.getsize(chemin_sortie) > 0:
                videos_a_supprimer.append(chemin_video)

        if videos_a_supprimer:
            print(f"{Couleurs.JAUNE}🗑️  Voulez-vous supprimer les {len(videos_a_supprimer)} vidéo(s) originale(s) traitées ?{Couleurs.RESET}")
            for v in videos_a_supprimer:
                print(f"{Couleurs.DIM}   - {os.path.basename(v)}{Couleurs.RESET}")
            print()
            reponse = input(f"{Couleurs.JAUNE}   Supprimer ? (o/N) : {Couleurs.RESET}").strip().lower()
            if reponse in ("o", "oui", "y", "yes"):
                for v in videos_a_supprimer:
                    try:
                        os.remove(v)
                        print(f"{Couleurs.VERT}   ✅ Supprimé : {os.path.basename(v)}{Couleurs.RESET}")
                    except Exception as e:
                        print(f"{Couleurs.ROUGE}   ❌ Impossible de supprimer {os.path.basename(v)} : {e}{Couleurs.RESET}")
            else:
                print(f"{Couleurs.DIM}   Fichiers originaux conservés.{Couleurs.RESET}")


# =============================================================================
# Point d'entrée du script
# =============================================================================
if __name__ == "__main__":
    main()
    # Pause pour que la fenêtre reste ouverte quand on lance le .exe
    print()
    input("Appuyez sur Entrée pour fermer...")
