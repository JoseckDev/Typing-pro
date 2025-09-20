# AUTO-GENERATED INTEGRATED FILE
# This file was produced by merging your original `typing_pro.py` (if present)
# with the refined CTk app `typing_master_pro_full.py`.
# Duplicated top-level class/def blocks found in the refined file were pruned from the original.
# Please review the file before using in production.
# Generated at: 2025-09-02T22:18:59.490161Z

import os
import sys
import json
import csv
import time
import math
import hmac
import hashlib
import base64
import datetime as _dt
import random
import threading
import requests
import tkinter as tk
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any, Tuple, Union
import tkinter.messagebox as messagebox

# Optional dependencies with graceful fallbacks
HAS_PIL = False
try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    print("Pillow library not found. Background images will be disabled.")

HAS_PYGAME = False
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    print("Pygame library not found. Sound will be disabled.")

HAS_TTS = False
try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    print("pyttsx3 library not found. Voice reminders will be disabled.")

HAS_SOCKET = False
try:
    import socket
    HAS_SOCKET = True
except ImportError:
    print("Socket library not available. Multiplayer mode will be disabled.")

# GUI imports
try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    ctk = None
    CTK_AVAILABLE = False
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, simpledialog

# Matplotlib for visualizations
HAS_MATPLOTLIB = False
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    print("Matplotlib not found. Visualizations will be disabled.")

# Configuration constants
BACKGROUND_MUSIC_FILE = "background.mp3"
VICTORY_SOUND_FILE = "victory.wav"
LEADERBOARD_FILE = "leaderboard.json"
USER_PROFILES_FILE = "user_profiles.json"
ACHIEVEMENTS_FILE = "achievements.json"
COUNTDOWN_DEFAULT = 60
BACKGROUND_IMAGE = "background.jpg"
SOUND_CORRECT = "correct.wav"
SOUND_WRONG = "wrong.wav"
SOUND_COMPLETE = "complete.wav"
SOCIAL_SHARE_API = "https://api.example.com/share"

# Sentence banks with multiple languages and difficulty levels
SENTENCES = {
    "English": {
        "Easy": [
            "the quick brown fox jumps over the lazy dog",
            "python is fun and easy to learn",
            "keep practicing every day to improve",
            "hello world from python programming",
            "code more learn more achieve more",
            "simple is better than complex",
            "practice makes perfect in typing",
        ],
        "Medium": [
            "errors should never pass silently unless explicitly silenced",
            "readability counts in python code and documentation",
            "consistent practice produces proficiency in all skills",
            "write tests before you refactor your code",
            "knowledge grows when shared generously with others",
            "the best error message is the one that never shows up",
            "explicit is better than implicit in programming",
        ],
        "Hard": [
            "premature optimization is the root of all evil in programming",
            "abstraction and composition help manage software complexity effectively",
            "concurrency is hard; design for correctness first then performance",
            "guard the boundaries between modules with contracts and tests",
            "cohesion and coupling shape maintainable architectures",
            "the only way to learn a new programming language is by writing programs in it",
            "software entropy increases with each change that reduces structure",
        ],
        "Expert": [
            "metaclasses are deeper magic that 99% of users should never worry about",
            "functional programming emphasizes expressions and declarations rather than statements",
            "design patterns are reusable solutions to commonly occurring problems in software design",
            "the principle of least astonishment applies to user interface design and apis",
            "heisenbugs are bugs that disappear or alter their behavior when one attempts to study them",
            "yagni principle states that you should always implement things when you actually need them",
            "the law of demeter is a design guideline for developing software with minimal coupling",
        ],
        "Nightmare": [
            "quantum entanglement allows particles to remain connected so that actions performed on one affect the other",
            "epigenetics studies changes in gene expression that do not involve alterations to the dna sequence",
            "nanotechnology involves manipulating matter on an atomic molecular and supramolecular scale",
            "the holographic principle suggests that the description of a volume of space can be encoded on a lower dimensional boundary",
            "string theory posits that fundamental particles are one dimensional strings rather than point particles",
            "the many worlds interpretation asserts that all possible outcomes of quantum measurements are realized in some universe",
            "dark matter and dark energy together constitute approximately 95% of the total mass energy content of the universe",
        ],
    },
    "Spanish": {
        "Easy": [
            "el rápido zorro marrón salta sobre el perro perezoso",
            "python es divertido y fácil de aprender",
            "practica todos los días para mejorar",
            "hola mundo desde la programación python",
            "codifica más aprende más logra más",
        ],
        "Medium": [
            "los errores nunca deberían pasar silenciosamente a menos que sean silenciados explícitamente",
            "la legibilidad cuenta en el código y documentación python",
            "la práctica constante produce competencia en todas las habilidades",
        ],
        "Hard": [
            "la optimización prematura es la raíz de todos los males en la programación",
            "la abstracción y la composición ayudan a gestionar la complejidad del software de manera efectiva",
            "la concurrencia es difícil; diseña para la corrección primero y luego el rendimiento",
        ],
    },
    "French": {
        "Easy": [
            "le renard brun rapide saute par-dessus le chien paresseux",
            "python est amusant et facile à apprendre",
            "pratiquez tous les jours pour vous améliorer",
        ],
        "Medium": [
            "les erreurs ne devraient jamais passer silencieusement à moins d'être explicitement réduites au silence",
            "la lisibilité compte dans le code et la documentation python",
        ],
    },
    "German": {
        "Easy": [
            "der schnelle braune Fuchs springt über den faulen Hund",
            "python ist lustig und einfach zu lernen",
            "übe jeden Tag, um dich zu verbessern",
        ],
    },
}

# Typing challenges
CHALLENGES = {
    "Speed Demon": {"target_wpm": 100, "time_limit": 60, "reward": "Speedster Badge"},
    "Accuracy Master": {"target_accuracy": 98, "time_limit": 60, "reward": "Perfectionist Badge"},
    "Marathon Typist": {"target_words": 200, "time_limit": 300, "reward": "Endurance Badge"},
    "Lightning Round": {"target_wpm": 80, "time_limit": 30, "reward": "Quick Fingers Badge"},
    "Multilingual Master": {"languages": 3, "time_limit": 180, "reward": "Polyglot Badge"},
    "Blind Typing": {"blind_mode": True, "time_limit": 120, "reward": "Touch Typist Badge"},
}

# Typing games
GAMES = {
    "Type Defense": {
        "description": "Type words to defend against incoming enemies",
        "duration": 120,
        "difficulty_scaling": True
    },
    "Word Race": {
        "description": "Race against the clock to complete as many words as possible",
        "duration": 60,
        "word_count": 50
    },
    "Typing Snake": {
        "description": "Control a snake by typing words correctly",
        "duration": 90,
        "speed_increase": True
    },
    "Memory Master": {
        "description": "Memorize text and type it from memory",
        "duration": 180,
        "difficulty_levels": 5
    }
}

# Achievements
ACHIEVEMENTS = [
    {"id": "first_blood", "name": "First Blood", "desc": "Complete your first typing test", "icon": "🩸"},
    {"id": "speedster", "name": "Speedster", "desc": "Achieve 100+ WPM", "icon": "⚡"},
    {"id": "perfectionist", "name": "Perfectionist", "desc": "Achieve 98%+ accuracy", "icon": "🎯"},
    {"id": "marathon", "name": "Marathon Runner", "desc": "Complete a 5-minute test", "icon": "🏃"},
    {"id": "nightmare", "name": "Nightmare Mode", "desc": "Complete a Nightmare difficulty test", "icon": "👹"},
    {"id": "streak", "name": "Hot Streak", "desc": "Complete 5 tests in a row", "icon": "🔥"},
    {"id": "explorer", "name": "Explorer", "desc": "Try all difficulty levels", "icon": "🗺️"},
    {"id": "champion", "name": "Champion", "desc": "Reach #1 on leaderboard", "icon": "🏆"},
    {"id": "polyglot", "name": "Polyglot", "desc": "Complete tests in 3 different languages", "icon": "🌍"},
    {"id": "social", "name": "Social Butterfly", "desc": "Share your results on social media", "icon": "🦋"},
    {"id": "daily", "name": "Daily Devotee", "desc": "Complete 7 daily challenges", "icon": "📅"},
    {"id": "game_master", "name": "Game Master", "desc": "Complete all typing games", "icon": "🎮"},
]

# Daily challenges
DAILY_CHALLENGES = [
    {"id": "speed_run", "name": "Speed Run", "desc": "Achieve 80 WPM in Medium difficulty", "type": "speed", "target": 80, "difficulty": "Medium"},
    {"id": "accuracy_check", "name": "Accuracy Check", "desc": "Achieve 95% accuracy in Hard difficulty", "type": "accuracy", "target": 95, "difficulty": "Hard"},
    {"id": "endurance_test", "name": "Endurance Test", "desc": "Complete a 3-minute test with 85% accuracy", "type": "endurance", "duration": 180, "target": 85},
    {"id": "multilingual", "name": "Multilingual Monday", "desc": "Complete tests in 2 different languages", "type": "languages", "target": 2},
    {"id": "blind_typing", "name": "Blind Typing", "desc": "Complete a test without looking at the keyboard", "type": "blind", "difficulty": "Medium"},
]

# Ergonomics tips
ERGONOMICS_TIPS = [
    "Sit up straight with your feet flat on the floor",
    "Keep your wrists straight and elevated",
    "Take a 20-second break every 20 minutes",
    "Blink regularly to prevent eye strain",
    "Position your monitor at eye level",
    "Keep your shoulders relaxed",
    "Maintain a comfortable distance from the screen"
]

# AI Coach tips
AI_COACH_TIPS = {
    "speed": [
        "Focus on rhythm rather than raw speed",
        "Try to type in bursts with short pauses between",
        "Use all your fingers, not just the strongest ones"
    ],
    "accuracy": [
        "Slow down to improve accuracy first",
        "Focus on pressing each key deliberately",
        "Review your weak keys and practice them specifically"
    ],
    "endurance": [
        "Maintain a steady pace you can sustain",
        "Take micro-pauses between sentences",
        "Focus on consistent rhythm rather than speed"
    ]
}

# Utility functions
def load_json_file(path: str, default=None):
    """Safely load a JSON file with proper error handling"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {path}")
        return default
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return default

def save_json_file(path: str, data: Any) -> bool:
    """Save data to a JSON file"""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {path}: {e}")
        return False

def format_time(seconds: int) -> str:
    """Format seconds as MM:SS"""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def calculate_wpm(typed_text: str, time_elapsed: float) -> float:
    """Calculate words per minute"""
    words = len(typed_text.split())
    return (words / time_elapsed) * 60 if time_elapsed > 0 else 0.0

def calculate_accuracy(typed_text: str, target_text: str) -> float:
    """Calculate typing accuracy percentage"""
    correct_chars = sum(1 for a, b in zip(typed_text, target_text) if a == b)
    return (correct_chars / max(1, len(target_text))) * 100.0

def get_daily_challenge() -> Dict:
    """Get today's daily challenge"""
    today = _dt.datetime.now().day
    return DAILY_CHALLENGES[today % len(DAILY_CHALLENGES)]

# Data models
@dataclass
class UserProfile:
    name: str
    created: str
    tests_completed: int = 0
    best_wpm: float = 0.0
    best_accuracy: float = 0.0
    languages_tried: List[str] = field(default_factory=list)
    history: List[Dict[str, Any]] = field(default_factory=list)
    weak_keys: Dict[str, int] = field(default_factory=dict)
    achievements: List[str] = field(default_factory=list)
    games_completed: List[str] = field(default_factory=list)
    daily_challenges: int = 0
    last_daily_challenge: Optional[str] = None
    ergonomics_reminders: int = 0
    last_ergonomics_reminder: Optional[str] = None
    typing_biometrics: Dict[str, Any] = field(default_factory=dict)
    version: int = 2

    @staticmethod
    def new(name: str) -> "UserProfile":
        return UserProfile(
            name=name,
            created=_dt.datetime.now(_dt.UTC).isoformat(timespec="seconds") + "Z",
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_legacy(d: Dict[str, Any]) -> "UserProfile":
        name = d.get("name") or d.get("username") or "Unknown"
        created = d.get("created") or d.get("created_at") or _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds") + "Z"
        tests_completed = d.get("tests_completed") or d.get("tests") or 0
        best_wpm = d.get("best_wpm") or d.get("wpm_best") or 0.0
        best_accuracy = d.get("best_accuracy") or d.get("accuracy_best") or 0.0
        languages_tried = d.get("languages_tried") or d.get("langs") or []
        history = d.get("history") or []
        weak_keys = d.get("weak_keys") or d.get("miss_counts") or {}
        achievements = d.get("achievements") or []
        games_completed = d.get("games_completed") or []
        daily_challenges = d.get("daily_challenges") or 0
        last_daily_challenge = d.get("last_daily_challenge")
        ergonomics_reminders = d.get("ergonomics_reminders") or 0
        last_ergonomics_reminder = d.get("last_ergonomics_reminder")
        typing_biometrics = d.get("typing_biometrics") or {}

        return UserProfile(
            name=name, created=created, tests_completed=int(tests_completed),
            best_wpm=float(best_wpm), best_accuracy=float(best_accuracy),
            languages_tried=list(languages_tried), history=list(history),
            weak_keys=dict(weak_keys), achievements=list(achievements),
            games_completed=list(games_completed), daily_challenges=int(daily_challenges),
            last_daily_challenge=last_daily_challenge,
            ergonomics_reminders=int(ergonomics_reminders),
            last_ergonomics_reminder=last_ergonomics_reminder,
            typing_biometrics=dict(typing_biometrics), version=2
        )

# User Profile Manager
class UserProfileManager:
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(os.path.dirname(__file__), "typing_profiles.json")
        self.profiles: Dict[str, Dict[str, Any]] = {}
        self.settings: Dict[str, Any] = {
            "test_duration": 60, 
            "theme": "System", 
            "sound_enabled": False,
            "music_enabled": False,
            "ergonomics_enabled": True,
            "reminder_interval": 1200  # 20 minutes in seconds
        }
        self.current_profile: Optional[str] = None
        self.load_storage()

    def load_storage(self):
        """Load profiles and settings from storage"""
        data = load_json_file(self.storage_path, default={"profiles": {}, "settings": self.settings})
        
        if not isinstance(data, dict):
            data = {"profiles": {}, "settings": self.settings}
            
        self.settings.update(data.get("settings", {}))
        raw_profiles = data.get("profiles", {})
        
        # Upgrade legacy profiles to v2
        for name, p in raw_profiles.items():
            if isinstance(p, dict):
                if p.get("version", 1) < 2:
                    up = UserProfile.from_legacy(p).to_dict()
                else:
                    up = p
                self.profiles[name] = up
                
        # If none present, create a default
        if not self.profiles:
            self.create_profile("Guest")

    def save_storage(self) -> bool:
        """Save profiles and settings to storage"""
        data = {"profiles": self.profiles, "settings": self.settings}
        return save_json_file(self.storage_path, data)

    def list_profiles(self) -> List[str]:
        """List all profile names"""
        return sorted(self.profiles.keys())

    def get_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a profile by name"""
        return self.profiles.get(name)

    def create_profile(self, name: str) -> bool:
        """Create a new profile"""
        name = (name or "").strip()
        if not name or name in self.profiles:
            return False
        self.profiles[name] = UserProfile.new(name).to_dict()
        self.current_profile = name
        self.save_storage()
        return True

    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        if name in self.profiles:
            del self.profiles[name]
            if self.current_profile == name:
                self.current_profile = None
            self.save_storage()
            return True
        return False

    def load_profile(self, name: str) -> bool:
        """Load a profile as the current profile"""
        if name in self.profiles:
            self.current_profile = name
            return True
        return False

    def update_profile_with_test(self, name: str, wpm: float, accuracy: float, 
                                typed: str, target: str, duration: int = 60, 
                                language: str = "English"):
        """Update a profile with test results"""
        p = self.get_profile(name)
        if not p:
            return False
            
        p["tests_completed"] = int(p.get("tests_completed", 0)) + 1
        p["best_wpm"] = max(float(p.get("best_wpm", 0.0)), float(wpm))
        p["best_accuracy"] = max(float(p.get("best_accuracy", 0.0)), float(accuracy))
        
        if language and language not in p.get("languages_tried", []):
            p.setdefault("languages_tried", []).append(language)
            
        entry = {
            "date": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", 
            "wpm": float(wpm), 
            "accuracy": float(accuracy), 
            "duration": int(duration),
            "language": language
        }
        p.setdefault("history", []).append(entry)
        
        # Track weak keys: increment for mismatches
        wk = p.setdefault("weak_keys", {})
        for a, b in zip(typed, target):
            if a != b:
                wk[b] = int(wk.get(b, 0)) + 1 if isinstance(b, str) and b else wk.get(b, 0)
                
        # Update typing biometrics
        tb = p.setdefault("typing_biometrics", {})
        ep = tb.setdefault("error_patterns", {})
        for a, b in zip(typed, target):
            if a != b:
                error_key = f"{b}->{a}"
                ep[error_key] = ep.get(error_key, 0) + 1
                
        p["version"] = 2
        self.save_storage()
        return True

    def unlock_achievement(self, name: str, achievement_id: str) -> bool:
        """Unlock an achievement for a profile"""
        p = self.get_profile(name)
        if not p:
            return False
            
        achievements = p.setdefault("achievements", [])
        if achievement_id not in achievements:
            achievements.append(achievement_id)
            self.save_storage()
            return True
        return False

    def complete_game(self, name: str, game_id: str) -> None:
        """Mark a game as completed for a profile"""
        p = self.get_profile(name)
        if not p:
            return
            
        games = p.setdefault("games_completed", [])
        if game_id not in games:
            games.append(game_id)
            self.save_storage()

    def complete_daily_challenge(self, name: str) -> None:
        """Mark a daily challenge as completed for a profile"""
        p = self.get_profile(name)
        if not p:
            return
            
        today = _dt.datetime.now().strftime("%Y-%m-%d")
        # Check if already completed today
        if p.get("last_daily_challenge") == today:
            return
            
        p["daily_challenges"] = int(p.get("daily_challenges", 0)) + 1
        p["last_daily_challenge"] = today
        self.save_storage()

    def show_ergonomics_reminder(self, name: str) -> bool:
        """Check if it's time to show an ergonomics reminder"""
        p = self.get_profile(name)
        if not p:
            return False
            
        now = _dt.datetime.now()
        last_reminder = p.get("last_ergonomics_reminder")
        
        # Show reminder every 20 minutes (or configured interval)
        interval = self.settings.get("reminder_interval", 1200)
        if last_reminder:
            last_time = _dt.datetime.strptime(last_reminder, "%Y-%m-%d %H:%M:%S")
            if (now - last_time).total_seconds() < interval:
                return False
                
        p["last_ergonomics_reminder"] = now.strftime("%Y-%m-%d %H:%M:%S")
        p["ergonomics_reminders"] = int(p.get("ergonomics_reminders", 0)) + 1
        self.save_storage()
        return True

    def get_weak_keys(self, name: str, count: int = 5) -> List[str]:
        """Get the keys with most errors for a profile"""
        p = self.get_profile(name)
        if not p:
            return []
            
        weak_keys = p.get("weak_keys", {})
        sorted_weak_keys = sorted(weak_keys.items(), key=lambda x: x[1], reverse=True)
        return [key for key, _ in sorted_weak_keys[:count]]

    def get_key_accuracy(self, name: str) -> Dict[str, float]:
        """Calculate accuracy percentage for each key for a profile"""
        p = self.get_profile(name)
        if not p:
            return {}
            
        key_accuracy = p.get("key_accuracy", {})
        accuracy_data = {}
        for char, stats in key_accuracy.items():
            if stats["total"] > 0:
                accuracy_data[char] = (stats["correct"] / stats["total"]) * 100
        return accuracy_data

    def get_languages_tried(self, name: str) -> int:
        """Get the number of languages tried by a profile"""
        p = self.get_profile(name)
        if not p:
            return 0
        languages = p.get("languages_tried", set())
        return len(languages)

    def get_ai_coach_tip(self, area: str) -> str:
        """Get an AI coach tip for a specific area"""
        if area in AI_COACH_TIPS:
            return random.choice(AI_COACH_TIPS[area])
        return "Keep practicing to improve your typing skills!"

    # Import/Export utilities
    def export_profiles(self, out_path: str) -> bool:
        """Export profiles to a JSON file"""
        return save_json_file(out_path, {"profiles": self.profiles, "settings": self.settings, "version": 2})

    def import_profiles(self, in_path: str, overwrite: bool = False) -> bool:
        """Import profiles from a JSON file"""
        data = load_json_file(in_path, default=None)
        if not isinstance(data, dict):
            return False
            
        src_profiles = data.get("profiles") if "profiles" in data else data
        if not isinstance(src_profiles, dict):
            return False
            
        for name, p in src_profiles.items():
            if not isinstance(p, dict):
                continue
            if p.get("version", 1) < 2:
                p = UserProfile.from_legacy(p).to_dict()
            if overwrite or name not in self.profiles:
                self.profiles[name] = p
                
        self.save_storage()
        return True

    def to_v2_schema(self):
        """Upgrade all profiles to v2 schema"""
        for name, p in list(self.profiles.items()):
            if p.get("version", 1) < 2:
                self.profiles[name] = UserProfile.from_legacy(p).to_dict()
        self.save_storage()

    def export_csv(self, out_path: str) -> bool:
        """Export profiles to a CSV file"""
        try:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["name","created","tests_completed","best_wpm","best_accuracy","languages_tried"])
                for name, p in self.profiles.items():
                    w.writerow([
                        name, p.get("created",""), p.get("tests_completed",0),
                        p.get("best_wpm",0.0), p.get("best_accuracy",0.0),
                        ";".join(p.get("languages_tried",[]))
                    ])
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False

    def import_csv(self, in_path: str, overwrite: bool = False) -> bool:
        """Import profiles from a CSV file"""
        try:
            with open(in_path, "r", newline="", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    name = (row.get("name") or "").strip()
                    if not name:
                        continue
                    p = UserProfile.new(name).to_dict()
                    p["created"] = row.get("created") or p["created"]
                    p["tests_completed"] = int(row.get("tests_completed") or 0)
                    p["best_wpm"] = float(row.get("best_wpm") or 0.0)
                    p["best_accuracy"] = float(row.get("best_accuracy") or 0.0)
                    langs = (row.get("languages_tried") or "").split(";") if row.get("languages_tried") else []
                    p["languages_tried"] = [x for x in (l.strip() for l in langs) if x]
                    if overwrite or name not in self.profiles:
                        self.profiles[name] = p
            self.save_storage()
            return True
        except Exception as e:
            print(f"Error importing CSV: {e}")
            return False

# Secure leaderboard submission
def submit_leaderboard_secure(pm: UserProfileManager, url: str, api_key: Optional[str] = None, 
                             api_secret: Optional[str] = None, timeout: int = 10) -> Tuple[bool, str]:
    """Submit leaderboard data securely to a remote server"""
    payload = {
        "timestamp": int(time.time()),
        "client": "typing-master-pro",
        "version": 2,
        "leaderboard": [
            {"name": n, "best_wpm": p.get("best_wpm",0.0), "best_accuracy": p.get("best_accuracy",0.0), 
             "tests_completed": p.get("tests_completed",0)}
            for n,p in sorted(pm.profiles.items(), key=lambda kv: kv[1].get("best_wpm",0.0), reverse=True)[:50]
        ]
    }
    body = json.dumps(payload, separators=(",",":")).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-Api-Key"] = api_key
    if api_secret:
        sig = hmac.new(api_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        headers["X-Signature"] = sig
        
    # Try requests, fallback to urllib
    try:
        import requests
        r = requests.post(url, data=body, headers=headers, timeout=timeout)
        ok = (200 <= r.status_code < 300)
        return ok, f"{r.status_code}: {r.text}"
    except Exception as e:
        try:
            import urllib.request
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                txt = resp.read().decode("utf-8","replace")
                ok = (200 <= code < 300)
                return ok, f"{code}: {txt}"
        except Exception as e2:
            return False, f"Network error: {e2}"

# Achievement System
class AchievementSystem:
    """Manage achievements and notifications"""
    def __init__(self):
        self.achievements = {ach["id"]: ach for ach in ACHIEVEMENTS}
        
    def check_achievements(self, profile: Dict, wpm: float, accuracy: float,
                           difficulty: str, language: str = "English") -> List[str]:
        """Check if any achievements were unlocked"""
        newly_unlocked = []
        
        # First Blood
        if profile["tests_completed"] == 1 and "first_blood" not in profile["achievements"]:
            newly_unlocked.append("first_blood")
            
        # Speedster
        if wpm >= 100 and "speedster" not in profile["achievements"]:
            newly_unlocked.append("speedster")
            
        # Perfectionist
        if accuracy >= 98 and "perfectionist" not in profile["achievements"]:
            newly_unlocked.append("perfectionist")
            
        # Marathon
        if COUNTDOWN_DEFAULT >= 300 and "marathon" not in profile["achievements"]:
            newly_unlocked.append("marathon")
            
        # Nightmare
        if difficulty == "Nightmare" and "nightmare" not in profile["achievements"]:
            newly_unlocked.append("nightmare")
            
        # Hot Streak
        if profile["tests_completed"] >= 5 and "streak" not in profile["achievements"]:
            # Check if last 5 tests were consecutive
            if len(profile["history"]) >= 5:
                dates = [_dt.datetime.strptime(h["date"], "%Y-%m-%d %H:%M")
                         for h in profile["history"][-5:]]
                consecutive = all(
                    (dates[i] - dates[i-1]).total_seconds() < 86400 for i in range(1, 5))
                if consecutive:
                    newly_unlocked.append("streak")
                    
        # Explorer
        difficulties_completed = set(h["difficulty"] for h in profile["history"])
        if len(difficulties_completed) >= 5 and "explorer" not in profile["achievements"]:
            newly_unlocked.append("explorer")
            
        # Polyglot
        languages_tried = profile.get("languages_tried", set())
        if len(languages_tried) >= 3 and "polyglot" not in profile["achievements"]:
            newly_unlocked.append("polyglot")
            
        # Daily Devotee
        if profile.get("daily_challenges", 0) >= 7 and "daily" not in profile["achievements"]:
            newly_unlocked.append("daily")
            
        # Game Master
        games_completed = profile.get("games_completed", [])
        if len(games_completed) >= len(GAMES) and "game_master" not in profile["achievements"]:
            newly_unlocked.append("game_master")
            
        # Champion (will be checked elsewhere)
        return newly_unlocked

    def show_achievement_popup(self, master, achievement_id: str) -> None:
        """Show a popup for an unlocked achievement"""
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return
            
        popup = ctk.CTkToplevel(master)
        popup.title("Achievement Unlocked!")
        popup.geometry("400x250")
        popup.resizable(False, False)
        
        ctk.CTkLabel(popup, text="Achievement Unlocked!",
                     font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(popup, text=f"{achievement['icon']} {achievement['name']}", 
                     font=("Arial", 24, "bold")).pack(pady=5)
        ctk.CTkLabel(popup, text=achievement["desc"], 
                     font=("Arial", 14)).pack(pady=5)
        
        # Share button
        share_btn = ctk.CTkButton(popup, text="Share Achievement",
                                  command=lambda: master.share_achievement(achievement_id))
        share_btn.pack(pady=5)
        
        ctk.CTkButton(popup, text="Awesome!",
                      command=popup.destroy).pack(pady=10)

# Daily Challenge System
class DailyChallengeSystem:
    """Manage daily challenges"""
    def __init__(self, user_profile_manager: UserProfileManager):
        self.user_profile = user_profile_manager
        self.current_challenge = get_daily_challenge()
        self.completed_today = self._check_completed_today()
        
    def _check_completed_today(self) -> bool:
        """Check if the daily challenge was already completed today"""
        if not self.user_profile.current_profile:
            return False
            
        profile = self.user_profile.profiles[self.user_profile.current_profile]
        last_challenge = profile.get("last_daily_challenge")
        if last_challenge:
            last_date = _dt.datetime.strptime(last_challenge, "%Y-%m-%d")
            today = _dt.datetime.now().date()
            return last_date.date() == today
        return False

    def check_challenge_completion(self, wpm: float, accuracy: float,
                                   difficulty: str, duration: int) -> bool:
        """Check if the daily challenge was completed"""
        if self.completed_today:
            return False
            
        challenge = self.current_challenge
        
        # Check different challenge types
        if challenge["type"] == "speed" and difficulty == challenge["difficulty"]:
            return wpm >= challenge["target"]
        elif challenge["type"] == "accuracy" and difficulty == challenge["difficulty"]:
            return accuracy >= challenge["target"]
        elif challenge["type"] == "endurance" and duration >= challenge.get("duration", 0):
            return accuracy >= challenge["target"]
        elif challenge["type"] == "languages":
            # This would be checked elsewhere
            return False
        elif challenge["type"] == "blind" and difficulty == challenge["difficulty"]:
            # This would be checked elsewhere
            return False
        return False

    def complete_challenge(self) -> None:
        """Mark the daily challenge as completed"""
        if not self.completed_today and self.user_profile.current_profile:
            self.user_profile.complete_daily_challenge(self.user_profile.current_profile)
            self.completed_today = True

# Popup Classes
class ConfettiPopup(ctk.CTkToplevel):
    """Popup for celebrating #1 ranking"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Congratulations!")
        self.geometry("500x300")
        self.resizable(False, False)
        
        ctk.CTkLabel(self, text="🎉 Congratulations! 🎉", 
                     font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="You've reached #1 on the leaderboard!", 
                     font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(self, text="Your typing skills are exceptional!", 
                     font=("Arial", 16)).pack(pady=10)
        
        ctk.CTkButton(self, text="Awesome!", 
                      command=self.destroy).pack(pady=20)

class MedalPopup(ctk.CTkToplevel):
    """Popup for earning a medal"""
    def __init__(self, master, place: int, difficulty: str, wpm: float):
        super().__init__(master)
        self.title("Medal Earned!")
        self.geometry("400x250")
        self.resizable(False, False)
        
        medal_emoji = "🥇" if place == 1 else "🥈" if place == 2 else "🥉"
        ctk.CTkLabel(self, text=f"{medal_emoji} You earned a medal! {medal_emoji}", 
                     font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"Place: #{place} in {difficulty} difficulty", 
                     font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(self, text=f"Speed: {wpm:.1f} WPM", 
                     font=("Arial", 16)).pack(pady=5)
        
        ctk.CTkButton(self, text="Great Job!", 
                      command=self.destroy).pack(pady=20)

class DailyChallengePopup(ctk.CTkToplevel):
    """Popup for daily challenge completion"""
    def __init__(self, master, challenge: Dict, reward: str):
        super().__init__(master)
        self.title("Daily Challenge Complete!")
        self.geometry("450x300")
        self.resizable(False, False)
        
        ctk.CTkLabel(self, text="🏆 Daily Challenge Complete! 🏆", 
                     font=("Arial", 20, "bold")).pack(pady=15)
        ctk.CTkLabel(self, text=challenge["name"], 
                     font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(self, text=challenge["desc"], 
                     font=("Arial", 14), wraplength=400).pack(pady=10)
        ctk.CTkLabel(self, text=f"Reward: {reward}", 
                     font=("Arial", 16, "bold"), text_color="#4CAF50").pack(pady=10)
        
        ctk.CTkButton(self, text="Awesome!", 
                      command=self.destroy).pack(pady=15)

class ErgonomicsReminder(ctk.CTkToplevel):
    """Popup for ergonomics reminders"""
    def __init__(self, master, tip: str):
        super().__init__(master)
        self.title("Ergonomics Reminder")
        self.geometry("400x250")
        self.resizable(False, False)
        
        ctk.CTkLabel(self, text="💡 Ergonomics Reminder", 
                     font=("Arial", 18, "bold")).pack(pady=15)
        ctk.CTkLabel(self, text=tip, 
                     font=("Arial", 14), wraplength=350).pack(pady=10)
        
        def speak_tip():
            if HAS_TTS:
                try:
                    engine = pyttsx3.init()
                    engine.say(tip)
                    engine.runAndWait()
                except Exception as e:
                    print(f"Text-to-speech error: {e}")
                    
        if HAS_TTS:
            ctk.CTkButton(self, text="🔊 Speak", 
                          command=speak_tip).pack(pady=5)
        
        ctk.CTkButton(self, text="Got it!", 
                      command=self.destroy).pack(pady=10)

# Typing Heatmap Visualization
class TypingHeatmap(ctk.CTkToplevel):
    """Visualize typing accuracy heatmap on a keyboard layout"""
    def __init__(self, master, accuracy_data: Dict[str, float]):
        super().__init__(master)
        self.title("Typing Heatmap")
        self.geometry("800x400")
        self.resizable(False, False)
        
        self.accuracy_data = accuracy_data
        self.keyboard_layout = [
            "` 1 2 3 4 5 6 7 8 9 0 - =",
            "q w e r t y u i o p [ ] \\",
            "a s d f g h j k l ; '",
            "z x c v b n m , . /"
        ]
        
        self._create_ui()
        self.draw_heatmap(accuracy_data)
        
    def _create_ui(self):
        """Create the heatmap UI"""
        # Title
        title_label = ctk.CTkLabel(
            self, text="Typing Accuracy Heatmap", 
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=10)
        
        # Legend
        legend_frame = ctk.CTkFrame(self)
        legend_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(legend_frame, text="Accuracy:").pack(side="left", padx=5)
        
        legend_items = [
            ("95%+", "#00cc00"),
            ("85-94%", "#00ff00"),
            ("70-84%", "#ffff00"),
            ("50-69%", "#ff9900"),
            ("<50%", "#ff0000")
        ]
        
        for text, color in legend_items:
            item_frame = ctk.CTkFrame(legend_frame)
            item_frame.pack(side="left", padx=5)
            
            color_box = ctk.CTkFrame(item_frame, width=20, height=20)
            color_box.pack(side="left", padx=2)
            color_box.configure(fg_color=color)
            
            ctk.CTkLabel(item_frame, text=text).pack(side="left", padx=2)
        
        # Canvas for keyboard
        self.canvas = tk.Canvas(self, bg="#333333", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Close button
        close_btn = ctk.CTkButton(self, text="Close", command=self.destroy)
        close_btn.pack(pady=10)
        
    def draw_heatmap(self, accuracy_data: Dict[str, float]) -> None:
        """Draw keyboard with heatmap colors based on accuracy data"""
        key_width = 50
        key_height = 50
        x_start = 20
        y_start = 20
        
        for row_idx, row in enumerate(self.keyboard_layout):
            keys = row.split()
            x_offset = x_start
            # Center some rows
            if row_idx == 1:  # QWERTY row
                x_offset += 25
            elif row_idx == 2:  # ASDF row
                x_offset += 50
            elif row_idx == 3:  # ZXCV row
                x_offset += 75
                
            for key in keys:
                # Get accuracy for this key
                char = key[0].lower()
                accuracy = accuracy_data.get(char, 0)
                
                # Determine color based on accuracy
                if accuracy >= 95:
                    color = "#00cc00"  # Green
                elif accuracy >= 85:
                    color = "#00ff00"  # Light green
                elif accuracy >= 70:
                    color = "#ffff00"  # Yellow
                elif accuracy >= 50:
                    color = "#ff9900"  # Orange
                else:
                    color = "#ff0000"  # Red
                
                # Draw key
                self.canvas.create_rectangle(
                    x_offset, y_start + row_idx * (key_height + 10),
                    x_offset + key_width, y_start + row_idx * (key_height + 10) + key_height,
                    fill=color, outline="#555", width=1
                )
                
                # Draw key label
                self.canvas.create_text(
                    x_offset + key_width // 2, y_start + row_idx * (key_height + 10) + key_height // 2,
                    text=key[0].upper(), font=("Arial", 16, "bold"), fill="white"
                )
                
                x_offset += key_width + 5

# Practice Mode for Weak Keys
class PracticeMode(ctk.CTkToplevel):
    """Practice mode focusing on weak keys"""
    def __init__(self, master, weak_keys: List[str], user_profile_manager: UserProfileManager):
        super().__init__(master)
        self.title("Practice Mode - Weak Keys")
        self.geometry("800x500")
        self.resizable(False, False)
        
        self.weak_keys = weak_keys
        self.user_profile = user_profile_manager
        self.current_sentence = ""
        self.start_time = None
        self.timer_running = False
        
        self._create_ui()
        self.generate_practice_sentence()
        
    def _create_ui(self):
        """Create the practice mode UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="Practice Mode - Weak Keys", 
                     font=("Arial", 20, "bold")).pack(side="left", padx=10)
        
        # Stats
        self.stats_label = ctk.CTkLabel(
            header_frame, text="WPM: 0.00 | Accuracy: 0.00%", 
            font=("Arial", 14)
        )
        self.stats_label.pack(side="right", padx=10)
        
        # Coach tip
        self.coach_label = ctk.CTkLabel(
            self, text="", font=("Arial", 14), text_color="#4CAF50"
        )
        self.coach_label.pack(pady=5)
        
        # Sentence display
        self.sentence_label = ctk.CTkLabel(
            self, text="", wraplength=700, font=("Arial", 18)
        )
        self.sentence_label.pack(pady=10)
        
        # Typing area
        typing_frame = ctk.CTkFrame(self)
        typing_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.textbox = tk.Text(typing_frame, height=8, width=80, 
                               font=("Consolas", 16), wrap="word")
        self.textbox.pack(pady=5)
        self.textbox.bind("<KeyRelease>", self._on_typing)
        
        # Tags for coloring
        self.textbox.tag_configure("correct", foreground="lime")
        self.textbox.tag_configure("wrong", foreground="red")
        self.textbox.tag_configure("pending", foreground="gray")
        
        # Control buttons
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            control_frame, text="Start Practice", command=self.start_practice
        )
        self.start_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(
            control_frame, text="New Sentence", command=self.generate_practice_sentence
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            control_frame, text="Close", command=self.destroy
        ).pack(side="right", padx=5)
        
    def generate_practice_sentence(self) -> None:
        """Generate a practice sentence focusing on weak keys"""
        # Create a sentence with repeated weak keys
        words = []
        for key in [k for k in self.weak_keys if str(k).isalpha()]:
            # Create simple words with the weak key
            words.append(key * 3)  # e.g., "aaa"
            words.append(key + "a")  # e.g., "aa"
            words.append("a" + key)  # e.g., "aa"
            words.append(key + key + "a")  # e.g., "aaa"
            
        # Add some common words to make it more natural
        common_words = ["the", "and", "for", "are", "but", "not", "you", "all", "can", "had"]
        words.extend(random.choices(common_words, k=5))
        
        # Shuffle and join
        random.shuffle(words)
        self.current_sentence = " ".join(words)
        self.sentence_label.configure(text=self.current_sentence)
        self.reset_typing_area()
        
    def reset_typing_area(self) -> None:
        """Reset the typing area"""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self._apply_pending_tags()
        self.stats_label.configure(text="WPM: 0.00 | Accuracy: 0.00%")
        self.coach_label.configure(text="")
        self.timer_running = False
        
    def start_practice(self) -> None:
        """Start the practice session"""
        self.reset_typing_area()
        self.start_time = time.time()
        self.timer_running = True
        
        # Show AI coach tip
        if self.user_profile.current_profile:
            tip = self.user_profile.get_ai_coach_tip("accuracy")
            self.coach_label.configure(text=f"💡 AI Coach: {tip}")
            
    def _on_typing(self, event=None) -> None:
        """Handle typing events"""
        typed = self.textbox.get("1.0", "end-1c")
        
        # Clear previous tags
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        self.textbox.tag_remove("pending", "1.0", "end")
        
        # Apply color tags
        for i, target_char in enumerate(self.current_sentence):
            start_index = f"1.{i}"
            end_index = f"1.{i+1}"
            
            if i < len(typed):
                if typed[i] == target_char:
                    self.textbox.tag_add("correct", start_index, end_index)
                else:
                    self.textbox.tag_add("wrong", start_index, end_index)
            else:
                self.textbox.tag_add("pending", start_index, end_index)
                
        # Update stats if timer is running
        if self.start_time and self.timer_running:
            elapsed = time.time() - self.start_time
            words = len(typed.split())
            wpm = (words / elapsed) * 60 if elapsed > 0 else 0.0
            
            # Calculate accuracy
            correct_chars = sum(1 for a, b in zip(typed, self.current_sentence) if a == b)
            accuracy = (correct_chars / max(1, len(self.current_sentence))) * 100.0
            
            self.stats_label.configure(
                text=f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")
                
    def _apply_pending_tags(self) -> None:
        """Apply pending tags to all characters"""
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        self.textbox.tag_remove("pending", "1.0", "end")
        
        for i, _ in enumerate(self.current_sentence):
            self.textbox.tag_add("pending", f"1.{i}", f"1.{i+1}")

# Typing Games
class TypeDefenseGame(ctk.CTkToplevel):
    """Type Defense mini-game"""
    def __init__(self, master, difficulty="Medium"):
        super().__init__(master)
        self.title("Type Defense")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.difficulty = difficulty
        self.game_duration = 120  # 2 minutes
        self.time_left = self.game_duration
        self.game_running = False
        self.current_word = ""
        self.enemy_position = 0
        self.enemy_speed = 2.0
        self.difficulty_scaling = True
        self.words_defeated = 0
        self.score = 0
        self.lives = 3
        self.defense_line_y = 500
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the game UI"""
        # Header with timer and stats
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        self.timer_label = ctk.CTkLabel(
            header_frame, text=f"Time: {format_time(self.time_left)}", 
            font=("Arial", 16)
        )
        self.timer_label.pack(side="left", padx=10)
        
        self.words_label = ctk.CTkLabel(
            header_frame, text="Words: 0", 
            font=("Arial", 16)
        )
        self.words_label.pack(side="left", padx=10)
        
        self.score_label = ctk.CTkLabel(
            header_frame, text="Score: 0", 
            font=("Arial", 16)
        )
        self.score_label.pack(side="left", padx=10)
        
        self.lives_label = ctk.CTkLabel(
            header_frame, text="Lives: 3", 
            font=("Arial", 16)
        )
        self.lives_label.pack(side="right", padx=10)
        
        # Game canvas
        self.game_canvas = tk.Canvas(self, bg="#1a1a1a", highlightthickness=0)
        self.game_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Draw defense line
        self.game_canvas.create_line(
            0, self.defense_line_y, 800, self.defense_line_y, 
            fill="#4CAF50", width=3, tags="defense_line"
        )
        
        # Word display
        word_frame = ctk.CTkFrame(self)
        word_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(word_frame, text="Type the word:", 
                     font=("Arial", 14)).pack(side="left", padx=5)
        
        self.word_label = ctk.CTkLabel(
            word_frame, text="", font=("Arial", 18, "bold")
        )
        self.word_label.pack(side="left", padx=10)
        
        # Typing area
        self.textbox = tk.Text(word_frame, height=2, width=30, 
                               font=("Consolas", 16))
        self.textbox.pack(side="left", padx=10)
        self.textbox.bind("<KeyRelease>", self._on_typing)
        
        # Control buttons
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            control_frame, text="Start Game", command=self._start_game
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.pause_btn = ctk.CTkButton(
            control_frame, text="Pause", command=self._toggle_pause
        )
        self.pause_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(
            control_frame, text="Quit", command=self._quit_game
        ).pack(side="right", padx=5)
        
    def _start_game(self) -> None:
        """Start the game"""
        self.game_running = True
        self._spawn_enemy()
        self._game_loop()
        self._timer_loop()
        
    def _spawn_enemy(self) -> None:
        """Spawn a new enemy with a word"""
        if not self.game_running:
            return
            
        # Get a word based on difficulty
        if self.difficulty == "Easy":
            word_pool = SENTENCES["English"]["Easy"]
        elif self.difficulty == "Medium":
            word_pool = SENTENCES["English"]["Medium"]
        elif self.difficulty == "Hard":
            word_pool = SENTENCES["English"]["Hard"]
        else:
            word_pool = SENTENCES["English"]["Easy"]
            
        # Get a random word from the pool
        sentence = random.choice(word_pool)
        words = sentence.split()
        self.current_word = random.choice(words)
        
        # Display the word
        self.word_label.configure(text=self.current_word)
        
        # Clear the textbox
        self.textbox.delete("1.0", "end")
        
        # Create enemy on canvas
        self.enemy_position = 0
        enemy_id = self.game_canvas.create_rectangle(
            50, self.enemy_position, 100, self.enemy_position + 30,
            fill="red", tags="enemy"
        )
        
        # Create word text above enemy
        text_id = self.game_canvas.create_text(
            75, self.enemy_position - 10, text=self.current_word,
            fill="white", font=("Arial", 12), tags="enemy_text"
        )
        
        # Store IDs for later updates
        self.enemy_ids = [enemy_id, text_id]
        
    def _game_loop(self) -> None:
        """Main game loop for enemy movement"""
        if not self.game_running:
            return
            
        # Move enemy down
        self.enemy_position += self.enemy_speed
        
        # Update enemy position on canvas
        if hasattr(self, 'enemy_ids'):
            self.game_canvas.coords(
                self.enemy_ids[0],  # Enemy rectangle
                50, self.enemy_position, 100, self.enemy_position + 30
            )
            self.game_canvas.coords(
                self.enemy_ids[1],  # Enemy text
                75, self.enemy_position - 10
            )
            
        # Check if enemy reached defense line
        if self.enemy_position >= self.defense_line_y:
            self._enemy_reached_line()
            return
            
        # Continue game loop
        self.after(50, self._game_loop)
        
    def _timer_loop(self) -> None:
        """Timer loop for game duration"""
        if not self.game_running:
            return
            
        self.time_left -= 1
        self.timer_label.configure(text=f"Time: {format_time(self.time_left)}")
        
        # Check if game time is up
        if self.time_left <= 0:
            self._end_game()
            return
            
        # Continue timer loop
        self.after(1000, self._timer_loop)
        
    def _on_typing(self, event=None) -> None:
        """Handle typing events"""
        typed = self.textbox.get("1.0", "end-1c")
        
        # Check if typed word matches current word
        if typed == self.current_word:
            # Word defeated!
            self._defeat_enemy()
            
    def _defeat_enemy(self) -> None:
        """Handle defeating an enemy"""
        self.words_defeated += 1
        self.score += len(self.current_word) * 10
        
        # Update UI
        self.words_label.configure(text=f"Words: {self.words_defeated}")
        self.score_label.configure(text=f"Score: {self.score}")
        
        # Remove enemy from canvas
        if hasattr(self, 'enemy_ids'):
            for enemy_id in self.enemy_ids:
                self.game_canvas.delete(enemy_id)
                
        # Play sound if available
        if self.master.sound_enabled and HAS_PYGAME and SOUND_CORRECT:
            try:
                sound = pygame.mixer.Sound(SOUND_CORRECT)
                sound.play()
            except Exception:
                pass
                
        # Increase difficulty if enabled
        if self.difficulty_scaling and self.words_defeated % 5 == 0:
            self.enemy_speed += 0.5
            
        # Spawn new enemy
        self._spawn_enemy()
        
    def _enemy_reached_line(self) -> None:
        """Handle enemy reaching the defense line"""
        self.lives -= 1
        self.lives_label.configure(text=f"Lives: {self.lives}")
        
        # Remove enemy from canvas
        if hasattr(self, 'enemy_ids'):
            for enemy_id in self.enemy_ids:
                self.game_canvas.delete(enemy_id)
                
        # Play sound if available
        if self.master.sound_enabled and HAS_PYGAME and SOUND_WRONG:
            try:
                sound = pygame.mixer.Sound(SOUND_WRONG)
                sound.play()
            except Exception:
                pass
                
        # Check if game over
        if self.lives <= 0:
            self._end_game()
            return
            
        # Spawn new enemy
        self._spawn_enemy()
        
    def _toggle_pause(self) -> None:
        """Toggle game pause state"""
        self.game_running = not self.game_running
        if self.game_running:
            self.pause_btn.configure(text="Pause")
            self._game_loop()
            self._timer_loop()
        else:
            self.pause_btn.configure(text="Resume")
            
    def _quit_game(self) -> None:
        """Quit the game early"""
        self.game_running = False
        self._end_game()
        
    def _end_game(self) -> None:
        """End the game and show results"""
        self.game_running = False
        
        # Play completion sound if available
        if self.master.sound_enabled and HAS_PYGAME and SOUND_COMPLETE:
            try:
                sound = pygame.mixer.Sound(SOUND_COMPLETE)
                sound.play()
            except Exception:
                pass
                
        # Update user profile if logged in
        if self.master.user_profile.current_profile:
            self.master.user_profile.complete_game("Type Defense")
            
        # Show results
        result_popup = ctk.CTkToplevel(self)
        result_popup.title("Game Over!")
        result_popup.geometry("400x300")
        result_popup.resizable(False, False)
        
        ctk.CTkLabel(result_popup, text="Game Over!", 
                     font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(result_popup, text=f"Final Score: {self.score}", 
                     font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(result_popup, text=f"Words Defeated: {self.words_defeated}", 
                     font=("Arial", 18)).pack(pady=5)
        
        # Calculate WPM
        elapsed_minutes = (self.game_duration - self.time_left) / 60
        wpm = self.words_defeated / elapsed_minutes if elapsed_minutes > 0 else 0
        ctk.CTkLabel(result_popup, text=f"Average WPM: {wpm:.2f}", 
                     font=("Arial", 18)).pack(pady=5)
        
        # Close button
        ctk.CTkButton(result_popup, text="Close", 
                      command=result_popup.destroy).pack(pady=20)

class MemoryMasterGame(ctk.CTkToplevel):
    """Memory Master mini-game - trains and tests brain memory"""
    def __init__(self, master, difficulty="Medium"):
        super().__init__(master)
        self.title("Memory Master")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.difficulty = difficulty
        self.game_duration = 180  # 3 minutes
        self.time_left = self.game_duration
        self.game_running = False
        self.game_phase = "memorize"  # "memorize" or "recall"
        self.current_text = ""
        self.accuracy = 0.0
        self.score = 0
        self.recall_start_time = None
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the game UI"""
        # Header with timer and phase
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        self.timer_label = ctk.CTkLabel(
            header_frame, text=f"Time: {format_time(self.time_left)}", 
            font=("Arial", 16)
        )
        self.timer_label.pack(side="left", padx=10)
        
        self.phase_label = ctk.CTkLabel(
            header_frame, text="Phase: Memorize", 
            font=("Arial", 16)
        )
        self.phase_label.pack(side="right", padx=10)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=400, height=20)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Text display frame (for memorize phase)
        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.text_display = ctk.CTkTextbox(
            self.text_frame, wrap="word", font=("Arial", 16)
        )
        self.text_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Typing frame (for recall phase)
        self.typing_frame = ctk.CTkFrame(self)
        
        typing_label = ctk.CTkLabel(
            self.typing_frame, text="Type the text from memory:", 
            font=("Arial", 14)
        )
        typing_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.textbox = tk.Text(
            self.typing_frame, wrap="word", font=("Consolas", 16)
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.textbox.bind("<KeyRelease>", self._on_typing)
        
        # Accuracy display
        self.accuracy_label = ctk.CTkLabel(
            self.typing_frame, text="Accuracy: 0.0%", 
            font=("Arial", 14)
        )
        self.accuracy_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Score display
        self.score_label = ctk.CTkLabel(
            self.typing_frame, text="Score: 0", 
            font=("Arial", 14)
        )
        self.score_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Control buttons
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            control_frame, text="Start Game", command=self._start_game
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.pause_btn = ctk.CTkButton(
            control_frame, text="Pause", command=self._toggle_pause
        )
        self.pause_btn.pack(side="left", padx=5)
        
        self.skip_memorize_btn = ctk.CTkButton(
            control_frame, text="Skip to Recall", 
            command=self._skip_to_recall, state="disabled"
        )
        self.skip_memorize_btn.pack(side="left", padx=5)
        
        self.quit_btn = ctk.CTkButton(
            control_frame, text="Quit", command=self._quit_game
        )
        self.quit_btn.pack(side="right", padx=5)
        
        # Initially hide typing frame
        self.typing_frame.pack_forget()
        
    def _start_game(self) -> None:
        """Start the game"""
        self.game_running = True
        self._load_memory_text()
        self._show_memorize_phase()
        self._timer_loop()
        
    def _load_memory_text(self) -> None:
        """Load text for memory challenge based on difficulty"""
        # Get text based on difficulty
        if self.difficulty == "Easy":
            # Short simple sentences
            texts = [
                "The quick brown fox jumps over the lazy dog.",
                "Python is a popular programming language.",
                "Practice makes perfect when learning to type.",
                "The sun rises in the east and sets in the west.",
                "Reading books can expand your knowledge and vocabulary."
            ]
        elif self.difficulty == "Medium":
            # Medium length paragraphs
            texts = [
                "In the heart of the forest, a small stream meanders through the trees, reflecting the dappled sunlight that filters through the canopy above. Birds sing melodiously from their perches, creating a symphony of natural sounds that soothes the soul.",
                "Technology has revolutionized the way we communicate, work, and live. From smartphones to artificial intelligence, these innovations have transformed our daily routines and opened up new possibilities for human achievement.",
                "The art of cooking is a delicate balance of science and creativity. Understanding the chemistry of ingredients while allowing room for intuition and personal expression is what separates good cooks from great chefs."
            ]
        elif self.difficulty == "Hard":
            # Longer complex paragraphs
            texts = [
                "Quantum mechanics represents one of the most profound scientific achievements of the 20th century, fundamentally altering our understanding of reality at the smallest scales. The theory describes a universe governed by probability rather than certainty, where particles can exist in multiple states simultaneously and can influence each other instantaneously across vast distances through the phenomenon of entanglement.",
                "Climate change poses an unprecedented challenge to global ecosystems and human societies. Rising temperatures, shifting weather patterns, and increasing frequency of extreme weather events threaten biodiversity, food security, and economic stability. Addressing this crisis requires coordinated international action, technological innovation, and fundamental changes in how we produce and consume energy.",
                "The philosophy of existentialism emerged in the 20th century as a response to the perceived meaninglessness of a world without inherent purpose. Thinkers like Jean-Paul Sartre, Albert Camus, and Simone de Beauvoir explored themes of freedom, responsibility, and the human condition, arguing that individuals must create their own meaning in an indifferent universe."
            ]
        else:  # Expert or Nightmare
            # Very long and complex texts
            texts = [
                "The intersection of neuroscience and artificial intelligence represents one of the most promising frontiers of contemporary research. By understanding the neural mechanisms that underpin human cognition, scientists hope to develop more sophisticated AI systems that can mimic human-like reasoning and problem-solving abilities. Conversely, insights from AI research are providing new frameworks for understanding how the brain processes information, makes decisions, and adapts to new situations. This bidirectional exchange of ideas has the potential to revolutionize both fields, leading to breakthroughs that were previously unimaginable. However, this convergence also raises important ethical questions about the nature of consciousness, the limits of machine intelligence, and the implications of creating systems that may one day rival or even surpass human cognitive abilities.",
                "The global economic landscape has been fundamentally transformed by the forces of globalization, technological advancement, and demographic change. Traditional manufacturing powerhouses have given way to service-based economies, while digital platforms have created new forms of value that challenge conventional economic metrics. At the same time, growing inequality within and between nations has fueled political polarization and social unrest, threatening the stability of democratic institutions. The COVID-19 pandemic further accelerated these trends, exposing vulnerabilities in global supply chains while highlighting the importance of essential workers and public health infrastructure. As we look to the future, policymakers face the daunting challenge of fostering inclusive growth that addresses these structural inequities while harnessing the potential of emerging technologies to create a more sustainable and equitable world."
            ]
            
        self.current_text = random.choice(texts)
        
        # Display the text
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.insert("1.0", self.current_text)
        self.text_display.configure(state="disabled")
        
    def _show_memorize_phase(self) -> None:
        """Show the memorize phase of the game"""
        self.game_phase = "memorize"
        self.phase_label.configure(text="Phase: Memorize")
        self.memorize_time = self.game_duration // 2  # Half the time for memorizing
        
        # Show text display, hide typing area
        self.text_frame.grid()
        self.typing_frame.grid_remove()
        
        # Enable skip button
        self.skip_memorize_btn.configure(state="normal")
        
    def _show_recall_phase(self) -> None:
        """Show the recall phase of the game"""
        self.game_phase = "recall"
        self.phase_label.configure(text="Phase: Recall")
        self.recall_start_time = time.time()
        
        # Hide text display, show typing area
        self.text_frame.grid_remove()
        self.typing_frame.grid()
        
        # Clear typing area
        self.textbox.delete("1.0", "end")
        
        # Focus on typing area
        self.textbox.focus_set()
        
        # Disable skip button
        self.skip_memorize_btn.configure(state="disabled")
        
    def _skip_to_recall(self) -> None:
        """Skip to the recall phase"""
        if self.game_phase == "memorize":
            self._show_recall_phase()
            
    def _timer_loop(self) -> None:
        """Timer loop for game duration"""
        if not self.game_running:
            return
            
        self.time_left -= 1
        self.timer_label.configure(text=f"Time: {format_time(self.time_left)}")
        
        # Update progress bar
        if self.game_phase == "memorize":
            self.memorize_time -= 1
            progress = 1 - (self.memorize_time / (self.game_duration // 2))
            self.progress.set(max(0, progress))
            
            # Automatically switch to recall phase when memorize time is up
            if self.memorize_time <= 0:
                self._show_recall_phase()
        else:  # recall phase
            elapsed = time.time() - self.recall_start_time
            max_time = self.game_duration // 2
            progress = min(1, elapsed / max_time)
            self.progress.set(progress)
            
        # Check if game time is up
        if self.time_left <= 0:
            self._end_game()
            return
            
        # Continue timer loop
        self.after(1000, self._timer_loop)
        
    def _on_typing(self, event=None) -> None:
        """Handle typing events"""
        if self.game_phase != "recall":
            return
            
        typed = self.textbox.get("1.0", "end-1c")
        
        # Clear previous tags
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        
        # Apply color tags
        for i, target_char in enumerate(self.current_text):
            start_index = f"1.{i}"
            end_index = f"1.{i+1}"
            
            if i < len(typed):
                if typed[i] == target_char:
                    self.textbox.tag_add("correct", start_index, end_index)
                else:
                    self.textbox.tag_add("wrong", start_index, end_index)
                    
        # Calculate accuracy
        correct_chars = sum(1 for a, b in zip(typed, self.current_text) if a == b)
        self.accuracy = (correct_chars / max(1, len(self.current_text))) * 100.0
        self.accuracy_label.configure(text=f"Accuracy: {self.accuracy:.1f}%")
        
        # Calculate score based on accuracy and time
        if self.accuracy == 100:
            elapsed = time.time() - self.recall_start_time
            time_bonus = max(0, 100 - elapsed)  # Bonus for speed
            self.score = int(self.accuracy * 10 + time_bonus)
            self.score_label.configure(text=f"Score: {self.score}")
            
        # Check if typing is complete
        if len(typed) >= len(self.current_text):
            self._end_game()
            
    def _toggle_pause(self) -> None:
        """Toggle game pause state"""
        self.game_running = not self.game_running
        if self.game_running:
            self.pause_btn.configure(text="Pause")
            if self.game_phase == "recall":
                self.recall_start_time = time.time() - (len(self.textbox.get("1.0", "end-1c")) / 10)
            self._timer_loop()
        else:
            self.pause_btn.configure(text="Resume")
            
    def _quit_game(self) -> None:
        """Quit the game early"""
        self.game_running = False
        self._end_game()
        
    def _end_game(self) -> None:
        """End the game and show results"""
        self.game_running = False
        
        # Play completion sound if available
        if self.master.sound_enabled and HAS_PYGAME and SOUND_COMPLETE:
            try:
                sound = pygame.mixer.Sound(SOUND_COMPLETE)
                sound.play()
            except Exception:
                pass
                
        # Update user profile if logged in
        if self.master.user_profile.current_profile:
            self.master.user_profile.complete_game("Memory Master")
            
        # Show results
        result_popup = ctk.CTkToplevel(self)
        result_popup.title("Game Over!")
        
        # Make results popup responsive
        self.update_idletasks()
        width = max(500, int(self.winfo_screenwidth() * 0.4))
        height = max(400, int(self.winfo_screenheight() * 0.4))
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        result_popup.geometry(f"{width}x{height}+{x}+{y}")
        result_popup.resizable(True, True)
        
        ctk.CTkLabel(result_popup, text="Memory Master Results!", 
                     font=("Arial", 24, "bold")).pack(pady=20)
        
        # Calculate elapsed time
        if self.game_phase == "recall":
            elapsed = time.time() - self.recall_start_time
        else:
            elapsed = 0
            
        # Calculate final score
        if self.accuracy == 100:
            time_bonus = max(0, 100 - elapsed)
            final_score = int(self.accuracy * 10 + time_bonus)
        else:
            # Lower score for incomplete text
            final_score = int(self.accuracy * 5)
            
        ctk.CTkLabel(result_popup, text=f"Final Score: {final_score}", 
                     font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(result_popup, text=f"Accuracy: {self.accuracy:.1f}%", 
                     font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(result_popup, text=f"Time: {elapsed:.1f} seconds", 
                     font=("Arial", 18)).pack(pady=5)
        
        # Performance message
        if self.accuracy == 100:
            message = "Perfect memory! Incredible achievement!"
        elif self.accuracy >= 90:
            message = "Excellent memory! Very impressive!"
        elif self.accuracy >= 75:
            message = "Good memory! Keep practicing to improve!"
        elif self.accuracy >= 50:
            message = "Not bad! With more practice, you'll get better!"
        else:
            message = "Keep practicing! Memory improves with training!"
            
        ctk.CTkLabel(result_popup, text=message, 
                     font=("Arial", 16)).pack(pady=10)
        
        # Close button
        ctk.CTkButton(result_popup, text="Close", 
                      command=result_popup.destroy).pack(pady=20)

# Humanitarian Challenge
class HumanitarianChallenge(ctk.CTkToplevel):
    """Humanitarian typing challenges that make a real-world difference"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Type for Humanity")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the humanitarian challenge UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="Type for Humanity", 
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header_frame, text="Make a difference with your typing skills", 
                     font=("Arial", 16)).pack(pady=5)
        
        # Challenges
        challenges_frame = ctk.CTkScrollableFrame(self)
        challenges_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        challenges = [
            {
                "icon": "📚",
                "title": "Education for All",
                "desc": "Every 100 words typed helps provide educational materials to children in need",
                "progress": 75420,
                "goal": 100000,
                "partner": "UNICEF"
            },
            {
                "icon": "🌳",
                "title": "Plant a Tree",
                "desc": "Every 50 words typed contributes to planting trees in deforested areas",
                "progress": 42180,
                "goal": 50000,
                "partner": "One Tree Planted"
            },
            {
                "icon": "🍲",
                "title": "Fight Hunger",
                "desc": "Every 200 words typed helps provide meals to families facing food insecurity",
                "progress": 31250,
                "goal": 100000,
                "partner": "World Food Programme"
            },
            {
                "icon": "💧",
                "title": "Clean Water",
                "desc": "Every 150 words typed helps provide clean water access to communities",
                "progress": 18760,
                "goal": 50000,
                "partner": "charity: water"
            }
        ]
        
        for challenge in challenges:
            self._display_challenge(challenges_frame, challenge)
            
        # Info
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(info_frame, text="How it works:", 
                     font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(info_frame, text="1. Select a cause you care about", 
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(info_frame, text="2. Complete typing tests and games", 
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(info_frame, text="3. Your typing contributes to the cause", 
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(info_frame, text="4. Track your impact on the world", 
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
        
        # Close button
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=10)
        
    def _display_challenge(self, parent, challenge):
        """Display a single humanitarian challenge"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        # Icon and title
        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frame, text=challenge["icon"], 
                     font=("Arial", 24)).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text=challenge["title"], 
                     font=("Arial", 18, "bold")).pack(side="left", padx=5)
        
        # Description
        ctk.CTkLabel(frame, text=challenge["desc"], 
                     font=("Arial", 14), wraplength=600).pack(padx=10, pady=5)
        
        # Progress bar
        progress_frame = ctk.CTkFrame(frame)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        progress = ctk.CTkProgressBar(progress_frame, width=500)
        progress.pack(side="left", padx=5)
        progress.set(challenge["progress"] / challenge["goal"])
        
        ctk.CTkLabel(progress_frame, text=f"{challenge['progress']:,} / {challenge['goal']:,}", 
                     font=("Arial", 12)).pack(side="left", padx=5)
        
        # Partner
        ctk.CTkLabel(frame, text=f"In partnership with: {challenge['partner']}", 
                     font=("Arial", 12, "italic")).pack(padx=10, pady=2)
        
        # Join button
        ctk.CTkButton(frame, text="Join This Cause", 
                      command=lambda c=challenge: self.start_challenge(c)).pack(anchor="e", padx=10, pady=5)
        
    def start_challenge(self, challenge):
        """Start a humanitarian typing challenge"""
        # In a real implementation, this would start a special typing session
        # that tracks progress toward the humanitarian goal
        messagebox.showinfo("Type for Humanity", 
                            f"Thank you for supporting {challenge['title']}! "
                            f"Your typing will now contribute to the cause.")
        self.destroy()

# Inspirational Stories
class InspirationalStories(ctk.CTkToplevel):
    """Showcase stories of people transformed by typing skills"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Inspirational Stories")
        self.geometry("900x700")
        self.resizable(True, True)
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the inspirational stories UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="Inspirational Stories", 
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header_frame, text="Real people transformed by typing skills", 
                     font=("Arial", 16)).pack(pady=5)
        
        # Notebook for categories
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Career Transformation tab
        self._add_stories("Career Transformation", [
            {
                "name": "Sarah Johnson",
                "location": "Chicago, USA",
                "story": "Sarah was working as a retail cashier with limited career prospects. After discovering Typing Master Pro, she dedicated 30 minutes daily to improving her typing skills. Within six months, her speed increased from 35 WPM to 85 WPM with 95% accuracy. This transformation helped her secure a position as a data entry specialist, doubling her income and opening doors to further career advancement.",
                "quote": "Typing skills didn't just change my job; they changed my life's trajectory.",
                "achievement": "Promoted to Senior Data Analyst within 2 years"
            },
            {
                "name": "Miguel Rodriguez",
                "location": "Mexico City, Mexico",
                "story": "Miguel dreamed of working in the tech industry but struggled with slow typing speed. He used Typing Master Pro for three months, focusing on accuracy first. His improved typing skills helped him land a customer support role at a major tech company. Today, he's a junior developer, crediting his typing proficiency as the foundation that made his career transition possible.",
                "quote": "Every keystroke I practiced built the bridge to my dream career.",
                "achievement": "Now developing mobile applications for a Fortune 500 company"
            }
        ])
        
        # Education tab
        self._add_stories("Education Success", [
            {
                "name": "Aisha Patel",
                "location": "Mumbai, India",
                "story": "As a university student, Aisha struggled to keep up with assignments due to slow typing. She began using Typing Master Pro between classes, improving from 25 WPM to 70 WPM in one semester. This transformation allowed her to complete papers efficiently, participate more in class discussions, and maintain a better work-life balance. She graduated with honors and now mentors other students on digital skills.",
                "quote": "My typing speed didn't just improve my grades; it gave me back my time and confidence.",
                "achievement": "Graduated with First Class Honors in Computer Science"
            },
            {
                "name": "James Wilson",
                "location": "London, UK",
                "story": "James, a PhD candidate in history, was falling behind on his dissertation due to slow typing. He dedicated his summer break to Typing Master Pro, increasing his speed from 40 WPM to 90 WPM. This improvement allowed him to complete his literature review and research notes efficiently. He successfully defended his dissertation and is now a published author in his field.",
                "quote": "The ability to type as fast as I think transformed my academic journey.",
                "achievement": "Published two research papers in leading history journals"
            }
        ])
        
        # Personal Growth tab
        self._add_stories("Personal Growth", [
            {
                "name": "Elena Kowalski",
                "location": "Warsaw, Poland",
                "story": "After developing carpal tunnel syndrome, Elena feared she'd lose her ability to work as a writer. Through Typing Master Pro's ergonomic guidance and gradual practice, she not only recovered but developed a typing technique that reduced her symptoms. Today, she types pain-free at 75 WPM and has published her first novel, something she thought would never be possible.",
                "quote": "Learning to type properly didn't just save my career; it healed my hands and reignited my passion.",
                "achievement": "Debut novel selected for a national literary award"
            },
            {
                "name": "Kenji Tanaka",
                "location": "Tokyo, Japan",
                "story": "As a retiree, Kenji wanted to stay mentally active and connected with family abroad. He started using Typing Master Pro to improve his English typing skills. Within a year, he was typing emails comfortably at 60 WPM and video chatting with grandchildren in English. His cognitive skills improved, and he now volunteers teaching computer skills to other seniors.",
                "quote": "At 70, I thought learning new skills was behind me. Typing opened a whole new chapter.",
                "achievement": "Recognized as Senior Volunteer of the Year in his community"
            }
        ])
        
        # Share your story button
        share_frame = ctk.CTkFrame(self)
        share_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(share_frame, text="Share Your Story", 
                      command=self.share_story).pack(pady=10)
        
    def _add_stories(self, tab_name, stories):
        """Add a tab with stories"""
        tab = self.notebook.add(tab_name)
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for story in stories:
            self._display_story(scroll_frame, story)
            
    def _display_story(self, parent, story):
        """Display a single story"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frame, text=story["name"], 
                     font=("Arial", 18, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text=f"📍 {story['location']}", 
                     font=("Arial", 14)).pack(side="right", padx=5)
        
        # Story
        ctk.CTkLabel(frame, text=story["story"], 
                     font=("Arial", 14), wraplength=700, justify="left").pack(padx=10, pady=5)
        
        # Quote
        quote_frame = ctk.CTkFrame(frame, fg_color=("gray90", "gray20"))
        quote_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(quote_frame, text=f'"{story["quote"]}"', 
                     font=("Arial", 16, "italic")).pack(padx=10, pady=5)
        
        # Achievement
        ctk.CTkLabel(frame, text=f"Achievement: {story['achievement']}", 
                     font=("Arial", 14, "bold"), text_color="#4CAF50").pack(padx=10, pady=5)
        
    def share_story(self):
        """Open dialog to share a story"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Share Your Story")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        ctk.CTkLabel(dialog, text="Inspire Others With Your Journey", 
                     font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(dialog, text="Share how typing skills have transformed your life", 
                     font=("Arial", 14)).pack(pady=5)
        
        # Form
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Your Name:").pack(anchor="w", padx=5, pady=(5, 0))
        name_entry = ctk.CTkEntry(form_frame, width=400)
        name_entry.pack(fill="x", padx=5, pady=(0, 10))
        
        # Location
        ctk.CTkLabel(form_frame, text="Location:").pack(anchor="w", padx=5, pady=(5, 0))
        location_entry = ctk.CTkEntry(form_frame, width=400)
        location_entry.pack(fill="x", padx=5, pady=(0, 10))
        
        # Story
        ctk.CTkLabel(form_frame, text="Your Story:").pack(anchor="w", padx=5, pady=(5, 0))
        story_text = tk.Text(form_frame, height=10, width=50, font=("Arial", 12))
        story_text.pack(fill="both", expand=True, padx=5, pady=(0, 10))
        
        # Quote
        ctk.CTkLabel(form_frame, text="Inspirational Quote:").pack(anchor="w", padx=5, pady=(5, 0))
        quote_entry = ctk.CTkEntry(form_frame, width=400)
        quote_entry.pack(fill="x", padx=5, pady=(0, 10))
        
        # Achievement
        ctk.CTkLabel(form_frame, text="Key Achievement:").pack(anchor="w", padx=5, pady=(5, 0))
        achievement_entry = ctk.CTkEntry(form_frame, width=400)
        achievement_entry.pack(fill="x", padx=5, pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        def submit_story():
            # In a real implementation, this would send the story to a server
            messagebox.showinfo("Thank You", 
                                "Your story has been submitted for review. "
                                "It may inspire thousands of others around the world!")
            dialog.destroy()
            
        ctk.CTkButton(button_frame, text="Submit Story", 
                      command=submit_story).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", 
                      command=dialog.destroy).pack(side="right", padx=5)

# World Typing Championship
class WorldChampionship(ctk.CTkToplevel):
    """World Typing Championship interface"""
    def __init__(self, master):
        super().__init__(master)
        self.title("World Typing Championship")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the championship UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="🏆 World Typing Championship 🏆", 
                     font=("Arial", 28, "bold")).pack(pady=10)
        ctk.CTkLabel(header_frame, text="Compete against the best typists in the world", 
                     font=("Arial", 16)).pack(pady=5)
        
        # Notebook for sections
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self._add_leaderboard_tab()
        self._add_events_tab()
        self._add_qualifiers_tab()
        self._add_champions_tab()
        
        # Join button
        join_frame = ctk.CTkFrame(self)
        join_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(join_frame, text="Join Championship", 
                      command=self.join_championship).pack(pady=10)
        
    def _add_leaderboard_tab(self):
        """Add the global leaderboard tab"""
        tab = self.notebook.add("Global Leaderboard")
        
        # Filter options
        filter_frame = ctk.CTkFrame(tab)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Filter by:").pack(side="left", padx=5)
        
        regions = ["All Regions", "Americas", "Europe", "Asia", "Africa", "Oceania"]
        region_var = tk.StringVar(value="All Regions")
        region_menu = ctk.CTkOptionMenu(filter_frame, values=regions, variable=region_var)
        region_menu.pack(side="left", padx=5)
        
        age_groups = ["All Ages", "Under 18", "18-30", "31-45", "46-60", "60+"]
        age_var = tk.StringVar(value="All Ages")
        age_menu = ctk.CTkOptionMenu(filter_frame, values=age_groups, variable=age_var)
        age_menu.pack(side="left", padx=5)
        
        # Leaderboard
        leaderboard_frame = ctk.CTkFrame(tab)
        leaderboard_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create treeview for leaderboard
        columns = ("Rank", "Name", "Country", "WPM", "Accuracy", "Score")
        tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings", height=20)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
            
        # Add sample data
        # In a real implementation, this would be fetched from a server
        sample_data = [
            (1, "Alexandra Chen", "Canada", 210.5, 99.2, 20882),
            (2, "Marcus Johnson", "USA", 208.7, 98.9, 20640),
            (3, "Sofia Rodriguez", "Spain", 205.3, 99.5, 20427),
            (4, "Kenji Tanaka", "Japan", 203.8, 98.7, 20115),
            (5, "Priya Sharma", "India", 201.2, 99.1, 19939),
            (6, "Oliver Mueller", "Germany", 199.6, 98.8, 19721),
            (7, "Fatima Al-Farsi", "UAE", 198.4, 99.3, 19696),
            (8, "Ngozi Adekunle", "Nigeria", 196.7, 98.5, 19375),
            (9, "Elena Petrov", "Russia", 195.2, 99.0, 19324),
            (10, "Carlos Mendoza", "Mexico", 193.8, 98.6, 19109)
        ]
        
        for data in sample_data:
            tree.insert("", "end", values=data)
            
        tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(leaderboard_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
    def _add_events_tab(self):
        """Add the championship events tab"""
        tab = self.notebook.add("Events")
        
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Upcoming events
        ctk.CTkLabel(scroll_frame, text="Upcoming Championship Events", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        events = [
            {
                "name": "Regional Qualifiers: Europe",
                "date": "October 15-17, 2023",
                "location": "Berlin, Germany",
                "description": "Top 100 typists from Europe qualify for the global finals",
                "prize": "$20,000 total prize pool"
            },
            {
                "name": "Regional Qualifiers: Asia-Pacific",
                "date": "October 22-24, 2023",
                "location": "Tokyo, Japan",
                "description": "Top 100 typists from Asia-Pacific qualify for the global finals",
                "prize": "$20,000 total prize pool"
            },
            {
                "name": "Regional Qualifiers: Americas",
                "date": "November 5-7, 2023",
                "location": "New York, USA",
                "description": "Top 100 typists from the Americas qualify for the global finals",
                "prize": "$20,000 total prize pool"
            },
            {
                "name": "Global Finals",
                "date": "December 15-17, 2023",
                "location": "Virtual Event",
                "description": "Top 30 typists from around the world compete for the championship title",
                "prize": "$40,000 total prize pool"
            }
        ]
        
        for event in events:
            self._display_event(scroll_frame, event)
            
    def _display_event(self, parent, event):
        """Display a single event"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        # Event name and date
        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frame, text=event["name"], 
                     font=("Arial", 16, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text=event["date"], 
                     font=("Arial", 14)).pack(side="right", padx=5)
        
        # Location
        ctk.CTkLabel(frame, text=f"📍 {event['location']}", 
                     font=("Arial", 14)).pack(anchor="w", padx=10, pady=2)
        
        # Description
        ctk.CTkLabel(frame, text=event["description"], 
                     font=("Arial", 14), wraplength=700, justify="left").pack(padx=10, pady=5)
        
        # Prize
        ctk.CTkLabel(frame, text=f"🏆 {event['prize']}", 
                     font=("Arial", 14, "bold"), text_color="#FFD700").pack(anchor="w", padx=10, pady=2)
        
        # Register button
        ctk.CTkButton(frame, text="Register Now", width=120).pack(anchor="e", padx=10, pady=5)
        
    def _add_qualifiers_tab(self):
        """Add the qualifiers information tab"""
        tab = self.notebook.add("Qualifiers")
        
        content = ctk.CTkFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="How to Qualify for the World Championship", 
                     font=("Arial", 20, "bold")).pack(pady=10)
        
        # Qualification criteria
        criteria_frame = ctk.CTkFrame(content)
        criteria_frame.pack(fill="x", padx=10, pady=10)
        
        criteria = [
            "Achieve a minimum typing speed of 150 WPM with 95% accuracy",
            "Participate in at least 5 official qualifying events",
            "Finish in the top 30% of your regional leaderboard",
            "Complete all championship training modules",
            "Submit a 1-minute video explaining your typing journey"
        ]
        
        for i, criterion in enumerate(criteria, start=1):
            ctk.CTkLabel(criteria_frame, text=f"{i}. {criterion}", 
                         font=("Arial", 14)).pack(anchor="w", padx=10, pady=5)
        
        # Training modules
        training_frame = ctk.CTkFrame(content)
        training_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(training_frame, text="Championship Training Modules", 
                     font=("Arial", 18, "bold")).pack(pady=5)
        
        modules = [
            "Speed Building Techniques",
            "Accuracy Under Pressure",
            "Endurance Training",
            "Complex Text Mastery",
            "Mental Preparation"
        ]
        
        for module in modules:
            module_frame = ctk.CTkFrame(training_frame)
            module_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(module_frame, text=f"• {module}", 
                         font=("Arial", 14)).pack(side="left", padx=5)
            
            progress = ctk.CTkProgressBar(module_frame, width=200)
            progress.pack(side="right", padx=5)
            progress.set(0.0)  # Would be updated based on user progress
        
        # Start training button
        ctk.CTkButton(content, text="Start Championship Training", 
                      command=self.start_training).pack(pady=10)
        
    def _add_champions_tab(self):
        """Add the past champions tab"""
        tab = self.notebook.add("Hall of Fame")
        
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="World Typing Champions", 
                     font=("Arial", 20, "bold")).pack(pady=10)
        
        champions = [
            {
                "year": "2022",
                "name": "Elena Petrov",
                "country": "Russia",
                "wpm": 212.3,
                "accuracy": 99.4,
                "quote": "Precision over speed, speed over everything else.",
                "story": "Elena, a concert pianist, applied her musical training to achieve unprecedented typing rhythm and accuracy."
            },
            {
                "year": "2021",
                "name": "Marcus Johnson",
                "country": "USA",
                "wpm": 208.7,
                "accuracy": 98.9,
                "quote": "Champions are made when no one is watching.",
                "story": "Marcus practiced 4 hours daily for 3 years while working full-time as a night security guard."
            },
            {
                "year": "2020",
                "name": "Sofia Rodriguez",
                "country": "Spain",
                "wpm": 205.3,
                "accuracy": 99.5,
                "quote": "Your fingers can fly when your mind is free.",
                "story": "A former journalist, Sofia developed her typing skills covering breaking news under tight deadlines."
            }
        ]
        
        for champion in champions:
            self._display_champion(scroll_frame, champion)
            
    def _display_champion(self, parent, champion):
        """Display a single champion"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frame, text=f"{champion['year']} Champion", 
                     font=("Arial", 16, "bold"), text_color="#FFD700").pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text=f"{champion['name']} - {champion['country']}", 
                     font=("Arial", 18, "bold")).pack(side="right", padx=5)
        
        # Stats
        stats_frame = ctk.CTkFrame(frame)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(stats_frame, text=f"Speed: {champion['wpm']} WPM", 
                     font=("Arial", 14)).pack(side="left", padx=10)
        ctk.CTkLabel(stats_frame, text=f"Accuracy: {champion['accuracy']}%", 
                     font=("Arial", 14)).pack(side="left", padx=10)
        
        # Quote
        quote_frame = ctk.CTkFrame(frame, fg_color=("gray90", "gray20"))
        quote_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(quote_frame, text=f'"{champion["quote"]}"', 
                     font=("Arial", 16, "italic")).pack(padx=10, pady=5)
        
        # Story
        ctk.CTkLabel(frame, text=champion["story"], 
                     font=("Arial", 14), wraplength=700, justify="left").pack(padx=10, pady=5)
        
    def join_championship(self):
        """Join the championship"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Join World Championship")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        ctk.CTkLabel(dialog, text="Join the World Typing Championship", 
                     font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(dialog, text="Compete against the best typists in the world", 
                     font=("Arial", 14)).pack(pady=5)
        
        # Registration form
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Full Name:").pack(anchor="w", padx=5, pady=(5, 0))
        name_entry = ctk.CTkEntry(form_frame, width=400)
        name_entry.pack(fill="x", padx=5, pady=(0, 10))
        
        # Country
        ctk.CTkLabel(form_frame, text="Country:").pack(anchor="w", padx=5, pady=(5, 0))
        countries = ["USA", "Canada", "UK", "Germany", "France", "Spain", "Italy", 
                     "Russia", "China", "Japan", "India", "Australia", "Brazil", "Other"]
        country_var = tk.StringVar()
        country_menu = ctk.CTkOptionMenu(form_frame, values=countries, variable=country_var)
        country_menu.pack(fill="x", padx=5, pady=(0, 10))
        
        # Age group
        ctk.CTkLabel(form_frame, text="Age Group:").pack(anchor="w", padx=5, pady=(5, 0))
        age_groups = ["Under 18", "18-30", "31-45", "46-60", "60+"]
        age_var = tk.StringVar()
        age_menu = ctk.CTkOptionMenu(form_frame, values=age_groups, variable=age_var)
        age_menu.pack(fill="x", padx=5, pady=(0, 10))
        
        # Experience
        ctk.CTkLabel(form_frame, text="Typing Experience:").pack(anchor="w", padx=5, pady=(5, 0))
        experience = ["Beginner", "Intermediate", "Advanced", "Professional"]
        exp_var = tk.StringVar()
        exp_menu = ctk.CTkOptionMenu(form_frame, values=experience, variable=exp_var)
        exp_menu.pack(fill="x", padx=5, pady=(0, 10))
        
        # Terms
        terms_frame = ctk.CTkFrame(form_frame)
        terms_frame.pack(fill="x", padx=5, pady=10)
        
        terms_var = tk.BooleanVar()
        terms_check = ctk.CTkCheckBox(
            terms_frame,
            text="I agree to the championship rules and terms",
            variable=terms_var
        )
        terms_check.pack(anchor="w", padx=5, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        def register():
            # In a real implementation, this would send registration data to a server
            messagebox.showinfo("Registration Successful", 
                                "You have registered for the World Typing Championship! "
                                "Check your email for next steps.")
            dialog.destroy()
            
        ctk.CTkButton(button_frame, text="Register Now", 
                      command=register).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", 
                      command=dialog.destroy).pack(side="right", padx=5)
        
    def start_training(self):
        """Start championship training"""
        messagebox.showinfo("Championship Training", 
                            "Championship training modules will be available soon. "
                            "Keep practicing to improve your skills!")

# Daily Inspiration System
class DailyInspiration(ctk.CTkToplevel):
    """Daily inspiration and motivation system"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Daily Inspiration")
        self.geometry("600x500")
        self.resizable(False, False)
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the daily inspiration UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="✨ Daily Inspiration ✨", 
                     font=("Arial", 24, "bold")).pack(pady=10)
        
        # Notebook for sections
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Quote of the day tab
        quote_tab = self.notebook.add("Quote of the Day")
        self._add_quote_of_the_day(quote_tab)
        
        # Success story tab
        story_tab = self.notebook.add("Success Story")
        self._add_success_story(story_tab)
        
        # Tip of the day tab
        tip_tab = self.notebook.add("Tip of the Day")
        self._add_tip_of_the_day(tip_tab)
        
        # Challenge of the day tab
        challenge_tab = self.notebook.add("Challenge of the Day")
        self._add_challenge_of_the_day(challenge_tab)
        
        # Close button
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=10)
        
    def _add_quote_of_the_day(self, parent):
        """Add quote of the day section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame, text="Quote of the Day", 
                     font=("Arial", 18, "bold")).pack(pady=5)
        
        # In a real implementation, quotes would be fetched from a database
        quotes = [
            "The only way to do great work is to love what you type. - Adapted from Steve Jobs",
            "Every expert was once a beginner. Every pro was once an amateur. Every icon was once an unknown.",
            "Your keyboard is the paintbrush, your mind is the canvas. Create something beautiful today.",
            "The difference between ordinary and extraordinary is that little 'extra' in your typing practice.",
            "Success is not final, failure is not fatal: It is the courage to continue typing that counts.",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "The future belongs to those who believe in the beauty of their keystrokes.",
            "It does not matter how slowly you go as long as you do not stop typing. - Adapted from Confucius"
        ]
        
        quote = random.choice(quotes)
        
        quote_frame = ctk.CTkFrame(frame, fg_color=("gray90", "gray20"))
        quote_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(quote_frame, text=f'"{quote}"', 
                     font=("Arial", 16, "italic")).pack(padx=10, pady=10)
        
    def _add_success_story(self, parent):
        """Add success story of the day section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame, text="Success Story of the Day", 
                     font=("Arial", 18, "bold")).pack(pady=5)
        
        # In a real implementation, stories would be fetched from a database
        stories = [
            {
                "name": "Raj from India",
                "story": "Raj, a rickshaw driver in Mumbai, learned typing using a mobile app. After 6 months of practice, he got a job as a data entry clerk, tripling his income and providing better education for his children."
            },
            {
                "name": "Maria from Brazil",
                "story": "Maria, a single mother of two, learned typing while her children slept. She now works remotely as a transcriptionist, allowing her to be there for her kids while supporting her family."
            },
            {
                "name": "Ahmed from Egypt",
                "story": "Ahmed lost his job during the pandemic. He dedicated himself to learning typing and digital skills. Today, he runs a successful e-commerce business and has hired 5 people from his community."
            }
        ]
        
        story = random.choice(stories)
        
        story_frame = ctk.CTkFrame(frame)
        story_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(story_frame, text=story["name"], 
                     font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=2)
        ctk.CTkLabel(story_frame, text=story["story"], 
                     font=("Arial", 14), wraplength=550, justify="left").pack(padx=5, pady=5)
        
    def _add_tip_of_the_day(self, parent):
        """Add tip of the day section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame, text="Tip of the Day", 
                     font=("Arial", 18, "bold")).pack(pady=5)
        
        # In a real implementation, tips would be fetched from a database
        tips = [
            "Take a 20-second break every 20 minutes to prevent eye strain and fatigue.",
            "Focus on accuracy first, speed will follow naturally with practice.",
            "Use all ten fingers - it may feel slower at first but will pay off in the long run.",
            "Practice with texts you enjoy - it makes learning more enjoyable and sustainable.",
            "Set small, achievable goals and celebrate when you reach them.",
            "Record your progress to see how far you've come - it's great motivation!",
            "Try typing with your eyes closed to improve muscle memory.",
            "Maintain good posture - sit up straight with your feet flat on the floor."
        ]
        
        tip = random.choice(tips)
        
        tip_frame = ctk.CTkFrame(frame, fg_color=("gray90", "gray20"))
        tip_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(tip_frame, text=f"💡 {tip}", 
                     font=("Arial", 16)).pack(padx=10, pady=10)
        
    def _add_challenge_of_the_day(self, parent):
        """Add challenge of the day section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame, text="Challenge of the Day", 
                     font=("Arial", 18, "bold")).pack(pady=5)
        
        # In a real implementation, challenges would be fetched from a database
        challenges = [
            {
                "title": "Accuracy Focus",
                "description": "Complete a 1-minute test with 98% accuracy or higher",
                "difficulty": "Medium"
            },
            {
                "title": "Speed Sprint",
                "description": "Type 100 words as quickly as possible with 95% accuracy",
                "difficulty": "Hard"
            },
            {
                "title": "Endurance Test",
                "description": "Maintain 60 WPM for 5 minutes without dropping below 95% accuracy",
                "difficulty": "Expert"
            },
            {
                "title": "Blind Typing",
                "description": "Complete a test without looking at the keyboard",
                "difficulty": "Medium"
            }
        ]
        
        challenge = random.choice(challenges)
        
        challenge_frame = ctk.CTkFrame(frame)
        challenge_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(challenge_frame, text=challenge["title"], 
                     font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=2)
        ctk.CTkLabel(challenge_frame, text=f"Difficulty: {challenge['difficulty']}", 
                     font=("Arial", 14)).pack(anchor="w", padx=5, pady=2)
        ctk.CTkLabel(challenge_frame, text=challenge["description"], 
                     font=("Arial", 14), wraplength=550, justify="left").pack(padx=5, pady=5)
        
        ctk.CTkButton(challenge_frame, text="Accept Challenge", 
                      width=150).pack(anchor="e", padx=5, pady=5)

# Global Impact Dashboard
class GlobalImpactDashboard(ctk.CTkToplevel):
    """Dashboard showing the global impact of Typing Master Pro"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Global Impact Dashboard")
        self.geometry("900x700")
        self.resizable(True, True)
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the global impact dashboard UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="🌍 Global Impact Dashboard 🌍", 
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header_frame, text="See how Typing Master Pro is making a difference worldwide", 
                     font=("Arial", 16)).pack(pady=5)
        
        # Stats overview
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(stats_frame, text="Global Statistics", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        # Create a grid for stats
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(pady=10)
        
        # Stats data (in a real app, this would be fetched from a server)
        stats_data = [
            ("Users Worldwide", "2.5M+"),
            ("Tests Completed", "50M+"),
            ("Hours Practiced", "15M+"),
            ("Countries Reached", "180+"),
            ("Languages Supported", "12"),
            ("Lives Impacted", "500K+")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_frame = ctk.CTkFrame(stats_grid)
            stat_frame.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")
            
            ctk.CTkLabel(stat_frame, text=value, 
                         font=("Arial", 24, "bold"), text_color="#4CAF50").pack(pady=5)
            ctk.CTkLabel(stat_frame, text=label, 
                         font=("Arial", 14)).pack(pady=5)
        
        # Configure grid weights
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
        for i in range(2):
            stats_grid.grid_rowconfigure(i, weight=1)
        
        # Impact areas
        impact_frame = ctk.CTkFrame(self)
        impact_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(impact_frame, text="Impact Areas", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        # Notebook for impact areas
        self.notebook = ctk.CTkTabview(impact_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Education tab
        self._add_education_tab()
        
        # Employment tab
        self._add_employment_tab()
        
        # Accessibility tab
        self._add_accessibility_tab()
        
        # Close button
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=10)
        
    def _add_education_tab(self):
        """Add education impact tab"""
        tab = self.notebook.add("Education")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="Educational Impact", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        # Stats
        stats_frame = ctk.CTkFrame(content)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        stats_data = [
            ("Students Using Typing Master Pro", "1.2M+"),
            ("Schools and Universities", "5,000+"),
            ("Average Grade Improvement", "12%"),
            ("Typing Speed Improvement", "65%")
        ]
        
        for label, value in stats_data:
            stat_row = ctk.CTkFrame(stats_frame)
            stat_row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(stat_row, text=f"{label}:", 
                         font=("Arial", 14)).pack(side="left", padx=5)
            ctk.CTkLabel(stat_row, text=value, 
                         font=("Arial", 14, "bold"), text_color="#4CAF50").pack(side="right", padx=5)
        
        # Testimonials
        ctk.CTkLabel(content, text="Success Stories", 
                     font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        testimonials = [
            {
                "quote": "Typing Master Pro transformed our computer literacy program. Students now complete assignments in half the time.",
                "author": "Dr. Sarah Johnson, Education Director",
                "institution": "Global Education Initiative"
            },
            {
                "quote": "The improvement in our students' typing skills has been remarkable. It's boosted their confidence across all subjects.",
                "author": "Michael Chen, Principal",
                "institution": "Riverside Academy"
            }
        ]
        
        for testimonial in testimonials:
            test_frame = ctk.CTkFrame(content, fg_color=("gray90", "gray20"))
            test_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(test_frame, text=f'"{testimonial["quote"]}"', 
                         font=("Arial", 14, "italic")).pack(padx=10, pady=10)
            ctk.CTkLabel(test_frame, text=f"- {testimonial['author']}", 
                         font=("Arial", 12, "bold")).pack(anchor="e", padx=10)
            ctk.CTkLabel(test_frame, text=testimonial["institution"], 
                         font=("Arial", 12)).pack(anchor="e", padx=10, pady=(0, 10))
        
    def _add_employment_tab(self):
        """Add employment impact tab"""
        tab = self.notebook.add("Employment")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="Employment Impact", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        # Stats
        stats_frame = ctk.CTkFrame(content)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        stats_data = [
            ("Job Seekers Trained", "750K+"),
            ("Career Advancements", "300K+"),
            ("Average Salary Increase", "23%"),
            ("Employment Rate Improvement", "18%")
        ]
        
        for label, value in stats_data:
            stat_row = ctk.CTkFrame(stats_frame)
            stat_row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(stat_row, text=f"{label}:", 
                         font=("Arial", 14)).pack(side="left", padx=5)
            ctk.CTkLabel(stat_row, text=value, 
                         font=("Arial", 14, "bold"), text_color="#4CAF50").pack(side="right", padx=5)
        
        # Industry breakdown
        ctk.CTkLabel(content, text="Industry Breakdown", 
                     font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        industries = [
            ("Technology", 35),
            ("Healthcare", 20),
            ("Education", 15),
            ("Business Services", 12),
            ("Government", 10),
            ("Other", 8)
        ]
        
        industry_frame = ctk.CTkFrame(content)
        industry_frame.pack(fill="x", padx=10, pady=10)
        
        for industry, percentage in industries:
            row = ctk.CTkFrame(industry_frame)
            row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(row, text=industry, 
                         font=("Arial", 14)).pack(side="left", padx=5)
            
            progress = ctk.CTkProgressBar(row, width=200)
            progress.pack(side="left", padx=10)
            progress.set(percentage / 100)
            
            ctk.CTkLabel(row, text=f"{percentage}%", 
                         font=("Arial", 14)).pack(side="left", padx=5)
        
        # Testimonials
        ctk.CTkLabel(content, text="Success Stories", 
                     font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        testimonials = [
            {
                "quote": "After completing Typing Master Pro, I landed my dream job as a medical transcriptionist. My typing speed doubled in just three months!",
                "author": "Maria Rodriguez",
                "role": "Medical Transcriptionist"
            },
            {
                "quote": "The skills I gained from Typing Master Pro helped me transition from retail to an administrative role with a 40% salary increase.",
                "author": "James Wilson",
                "role": "Administrative Assistant"
            }
        ]
        
        for testimonial in testimonials:
            test_frame = ctk.CTkFrame(content, fg_color=("gray90", "gray20"))
            test_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(test_frame, text=f'"{testimonial["quote"]}"', 
                         font=("Arial", 14, "italic")).pack(padx=10, pady=10)
            ctk.CTkLabel(test_frame, text=f"- {testimonial['author']}, {testimonial['role']}", 
                         font=("Arial", 12, "bold")).pack(anchor="e", padx=10, pady=(0, 10))
        
    def _add_accessibility_tab(self):
        """Add accessibility impact tab"""
        tab = self.notebook.add("Accessibility")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="Accessibility Impact", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        # Stats
        stats_frame = ctk.CTkFrame(content)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        stats_data = [
            ("Users with Disabilities", "120K+"),
            ("Accessibility Features", "15+"),
            ("Screen Reader Compatible", "Yes"),
            ("Customizable Interface", "Yes")
        ]
        
        for label, value in stats_data:
            stat_row = ctk.CTkFrame(stats_frame)
            stat_row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(stat_row, text=f"{label}:", 
                         font=("Arial", 14)).pack(side="left", padx=5)
            ctk.CTkLabel(stat_row, text=value, 
                         font=("Arial", 14, "bold"), text_color="#4CAF50").pack(side="right", padx=5)
        
        # Features
        ctk.CTkLabel(content, text="Accessibility Features", 
                     font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        features = [
            "High-contrast mode for visually impaired users",
            "Customizable font sizes and styles",
            "Keyboard navigation for motor-impaired users",
            "Screen reader compatibility",
            "Color-blind friendly color schemes",
            "Adjustable typing sensitivity",
            "Voice command support (experimental)",
            "One-handed typing mode"
        ]
        
        features_frame = ctk.CTkFrame(content)
        features_frame.pack(fill="x", padx=10, pady=10)
        
        for feature in features:
            feature_row = ctk.CTkFrame(features_frame)
            feature_row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(feature_row, text=f"• {feature}", 
                         font=("Arial", 14)).pack(anchor="w", padx=5)
        
        # Testimonials
        ctk.CTkLabel(content, text="User Stories", 
                     font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        testimonials = [
            {
                "quote": "As someone with limited vision, the high-contrast mode and screen reader support have made Typing Master Pro accessible to me. I've improved my typing speed by 40 WPM!",
                "author": "David Kim",
                "role": "Accessibility Advocate"
            },
            {
                "quote": "The one-handed typing mode allowed me to continue practicing after my injury. I'm now back to my full typing speed and back at work.",
                "author": "Jennifer Adams",
                "role": "Recovering User"
            }
        ]
        
        for testimonial in testimonials:
            test_frame = ctk.CTkFrame(content, fg_color=("gray90", "gray20"))
            test_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(test_frame, text=f'"{testimonial["quote"]}"', 
                         font=("Arial", 14, "italic")).pack(padx=10, pady=10)
            ctk.CTkLabel(test_frame, text=f"- {testimonial['author']}, {testimonial['role']}", 
                         font=("Arial", 12, "bold")).pack(anchor="e", padx=10, pady=(0, 10))

# Stats Dashboard
class StatsDashboard(ctk.CTkToplevel):
    """Detailed statistics dashboard for user profiles"""
    def __init__(self, master, profile_data):
        super().__init__(master)
        self.title("Statistics Dashboard")
        self.geometry("900x700")
        self.resizable(True, True)
        
        self.profile_data = profile_data
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the statistics dashboard UI"""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text=f"📊 Statistics for {self.profile_data.get('name', 'User')}", 
                     font=("Arial", 24, "bold")).pack(pady=10)
        
        # Notebook for sections
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Overview tab
        self._add_overview_tab()
        
        # Progress tab
        self._add_progress_tab()
        
        # Weak Keys tab
        self._add_weak_keys_tab()
        
        # History tab
        self._add_history_tab()
        
        # Close button
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=10)
        
    def _add_overview_tab(self):
        """Add overview statistics tab"""
        tab = self.notebook.add("Overview")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Key stats
        stats_frame = ctk.CTkFrame(content)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(stats_frame, text="Key Statistics", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        # Create a grid for stats
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(pady=10)
        
        stats_data = [
            ("Tests Completed", str(self.profile_data.get("tests_completed", 0))),
            ("Best WPM", f"{self.profile_data.get('best_wpm', 0):.1f}"),
            ("Best Accuracy", f"{self.profile_data.get('best_accuracy', 0):.1f}%"),
            ("Languages Tried", str(len(self.profile_data.get("languages_tried", [])))),
            ("Achievements", str(len(self.profile_data.get("achievements", [])))),
            ("Games Completed", str(len(self.profile_data.get("games_completed", []))))
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_frame = ctk.CTkFrame(stats_grid)
            stat_frame.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")
            
            ctk.CTkLabel(stat_frame, text=value, 
                         font=("Arial", 24, "bold"), text_color="#4CAF50").pack(pady=5)
            ctk.CTkLabel(stat_frame, text=label, 
                         font=("Arial", 14)).pack(pady=5)
        
        # Configure grid weights
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
        for i in range(2):
            stats_grid.grid_rowconfigure(i, weight=1)
        
        # Recent activity
        activity_frame = ctk.CTkFrame(content)
        activity_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(activity_frame, text="Recent Activity", 
                     font=("Arial", 16, "bold")).pack(pady=10)
        
        history = self.profile_data.get("history", [])[-5:]
        if history:
            for entry in reversed(history):
                entry_frame = ctk.CTkFrame(activity_frame)
                entry_frame.pack(fill="x", padx=10, pady=5)
                
                date = entry.get("date", "")[:10]  # Just the date part
                wpm = entry.get("wpm", 0)
                accuracy = entry.get("accuracy", 0)
                duration = entry.get("duration", 0)
                language = entry.get("language", "English")
                
                ctk.CTkLabel(entry_frame, text=f"{date} - {language}", 
                             font=("Arial", 12, "bold")).pack(anchor="w", padx=5)
                ctk.CTkLabel(entry_frame, 
                             text=f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}% | Duration: {duration}s", 
                             font=("Arial", 12)).pack(anchor="w", padx=5)
        else:
            ctk.CTkLabel(activity_frame, text="No activity yet", 
                         font=("Arial", 14)).pack(pady=10)
        
    def _add_progress_tab(self):
        """Add progress tracking tab"""
        tab = self.notebook.add("Progress")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="Progress Over Time", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        if HAS_MATPLOTLIB:
            # Create WPM progress chart
            wpm_frame = ctk.CTkFrame(content)
            wpm_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(wpm_frame, text="WPM Progress", 
                         font=("Arial", 16, "bold")).pack(pady=5)
            
            fig = plt.Figure(figsize=(8, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            history = self.profile_data.get("history", [])
            if history:
                dates = [_dt.datetime.strptime(h["date"], "%Y-%m-%d %H:%M") for h in history]
                wpms = [h.get("wpm", 0) for h in history]
                
                ax.plot(dates, wpms, marker='o', linestyle='-', color='#4CAF50')
                ax.set_title("WPM Over Time")
                ax.set_xlabel("Date")
                ax.set_ylabel("WPM")
                ax.grid(True)
                
                fig.tight_layout()
                
                canvas = FigureCanvasTkAgg(fig, master=wpm_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
            else:
                ctk.CTkLabel(wpm_frame, text="No data available", 
                             font=("Arial", 14)).pack(pady=20)
            
            # Create accuracy progress chart
            acc_frame = ctk.CTkFrame(content)
            acc_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(acc_frame, text="Accuracy Progress", 
                         font=("Arial", 16, "bold")).pack(pady=5)
            
            fig = plt.Figure(figsize=(8, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            if history:
                dates = [_dt.datetime.strptime(h["date"], "%Y-%m-%d %H:%M") for h in history]
                accuracies = [h.get("accuracy", 0) for h in history]
                
                ax.plot(dates, accuracies, marker='o', linestyle='-', color='#2196F3')
                ax.set_title("Accuracy Over Time")
                ax.set_xlabel("Date")
                ax.set_ylabel("Accuracy (%)")
                ax.set_ylim(0, 100)
                ax.grid(True)
                
                fig.tight_layout()
                
                canvas = FigureCanvasTkAgg(fig, master=acc_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
            else:
                ctk.CTkLabel(acc_frame, text="No data available", 
                             font=("Arial", 14)).pack(pady=20)
        else:
            ctk.CTkLabel(content, text="Charts require matplotlib library", 
                         font=("Arial", 14)).pack(pady=20)
        
    def _add_weak_keys_tab(self):
        """Add weak keys analysis tab"""
        tab = self.notebook.add("Weak Keys")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="Weak Keys Analysis", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        weak_keys = self.profile_data.get("weak_keys", {})
        if weak_keys:
            # Sort weak keys by error count
            sorted_weak_keys = sorted(weak_keys.items(), key=lambda x: x[1], reverse=True)
            
            # Top weak keys
            top_frame = ctk.CTkFrame(content)
            top_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(top_frame, text="Top Weak Keys", 
                         font=("Arial", 16, "bold")).pack(pady=5)
            
            for key, count in sorted_weak_keys[:10]:
                key_frame = ctk.CTkFrame(top_frame)
                key_frame.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(key_frame, text=f"Key '{key}':", 
                             font=("Arial", 14)).pack(side="left", padx=5)
                
                progress = ctk.CTkProgressBar(key_frame, width=200)
                progress.pack(side="left", padx=10)
                
                # Normalize progress (assuming max errors is 20 for visualization)
                max_errors = max(count for _, count in sorted_weak_keys[:10])
                progress.set(count / max_errors if max_errors > 0 else 0)
                
                ctk.CTkLabel(key_frame, text=f"{count} errors", 
                             font=("Arial", 14)).pack(side="left", padx=5)
            
            # Practice recommendation
            rec_frame = ctk.CTkFrame(content)
            rec_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(rec_frame, text="Practice Recommendation", 
                         font=("Arial", 16, "bold")).pack(pady=5)
            
            recommendation = (
                "Focus on practicing words and sentences that contain your weak keys. "
                "Use the Practice Mode to specifically target these keys for improvement."
            )
            
            ctk.CTkLabel(rec_frame, text=recommendation, 
                         font=("Arial", 14), wraplength=700, justify="left").pack(padx=10, pady=10)
            
            # Practice button
            ctk.CTkButton(rec_frame, text="Start Practice Mode", 
                          command=self._start_practice_mode).pack(pady=10)
        else:
            ctk.CTkLabel(content, text="No weak keys data available yet", 
                         font=("Arial", 14)).pack(pady=20)
        
    def _add_history_tab(self):
        """Add detailed history tab"""
        tab = self.notebook.add("History")
        
        content = ctk.CTkScrollableFrame(tab)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(content, text="Test History", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        history = self.profile_data.get("history", [])
        if history:
            # Create treeview for history
            columns = ("Date", "WPM", "Accuracy", "Duration", "Language")
            tree = ttk.Treeview(content, columns=columns, show="headings", height=15)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            # Add history entries
            for entry in reversed(history):  # Most recent first
                date = entry.get("date", "")
                wpm = f"{entry.get('wpm', 0):.1f}"
                accuracy = f"{entry.get('accuracy', 0):.1f}%"
                duration = f"{entry.get('duration', 0)}s"
                language = entry.get("language", "English")
                
                tree.insert("", "end", values=(date, wpm, accuracy, duration, language))
            
            tree.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)
        else:
            ctk.CTkLabel(content, text="No test history available", 
                         font=("Arial", 14)).pack(pady=20)
        
    def _start_practice_mode(self):
        """Start practice mode for weak keys"""
        weak_keys = list(self.profile_data.get("weak_keys", {}).keys())
        if weak_keys:
            PracticeMode(self.master, weak_keys[:5], self.master.user_profile)
        else:
            messagebox.showinfo("Practice Mode", "No weak keys identified yet. Complete more typing tests.")

# Main Application
class TypingMasterPro(ctk.CTk):
    """Main application class for Typing Master Pro"""
    def __init__(self):
        super().__init__()
        
        # Initialize application
        self.title("Typing Master Pro — Enhanced Edition")
        self.geometry("1200x760")
        
        # Initialize managers
        self.user_profile = UserProfileManager()
        self.achievement_system = AchievementSystem()
        self.daily_challenge_system = DailyChallengeSystem(self.user_profile)
        
        # Initialize variables
        self.current_theme = self.user_profile.settings.get("theme", "System")
        self.sound_enabled = self.user_profile.settings.get("sound_enabled", False)
        self.music_enabled = self.user_profile.settings.get("music_enabled", False)
        self.ergonomics_enabled = self.user_profile.settings.get("ergonomics_enabled", True)
        
        self.language = "English"
        self.difficulty = "Easy"
        self.current_mode = "Standard"
        self.current_challenge = None
        self.blind_mode = False
        self.custom_text = ""
        
        self.current_sentence = ""
        self.start_time = None
        self.timer_running = False
        self.round_seconds = COUNTDOWN_DEFAULT
        self.time_left = COUNTDOWN_DEFAULT
        self.current_wpm = 0.0
        self.current_accuracy = 0.0
        
        self.player_name = "Guest"
        
        # Sound effects
        self.sounds = {}
        if HAS_PYGAME:
            pygame.mixer.init()
            try:
                if os.path.exists(SOUND_CORRECT):
                    self.sounds[SOUND_CORRECT] = pygame.mixer.Sound(SOUND_CORRECT)
                if os.path.exists(SOUND_WRONG):
                    self.sounds[SOUND_WRONG] = pygame.mixer.Sound(SOUND_WRONG)
                if os.path.exists(SOUND_COMPLETE):
                    self.sounds[SOUND_COMPLETE] = pygame.mixer.Sound(SOUND_COMPLETE)
            except Exception as e:
                print(f"Error loading sounds: {e}")
        
        # Set theme
        try:
            ctk.set_appearance_mode(self.current_theme)
        except Exception:
            ctk.set_appearance_mode("System")
        
        # Load custom theme if available
        theme_path = os.path.join(os.path.dirname(__file__), "ctk_theme.json")
        try:
            if os.path.exists(theme_path):
                ctk.set_default_color_theme(theme_path)
            else:
                ctk.set_default_color_theme("blue")
        except Exception:
            ctk.set_default_color_theme("blue")
        
        # Create UI
        self._create_ui()
        
        # Load background image if available
        self._load_background_image()
        
        # Bind events
        self._bind_events()
        
        # Load data
        self._load_data()
        
        # Schedule ergonomics reminders
        self.after(60000, self._schedule_ergonomics_reminder)  # Start after 1 minute
        
        # Show welcome dialog for new users
        if not self.user_profile.profiles or len(self.user_profile.profiles) == 1 and "Guest" in self.user_profile.profiles:
            self._show_welcome_dialog()
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Configure grid weights
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        
        # Build UI sections
        self._build_header()
        self._build_content()
        self._build_footer()
        
        # Initial UI state
        self._update_profile_menu()
        self._update_profile_stats()
        self._update_leaderboard_preview()
        self.load_new_sentence()
    
    def _build_header(self):
        """Build the header section"""
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))
        
        # Title
        title = ctk.CTkLabel(
            header, text="🔥 Typing Master Pro — Enhanced Edition 🔥", 
            font=("Arial", 28, "bold")
        )
        title.grid(row=0, column=0, padx=10, pady=8, sticky="w")
        
        # Daily inspiration button
        self.inspiration_btn = ctk.CTkButton(
            header, text="✨ Daily Inspiration", command=self.show_daily_inspiration
        )
        self.inspiration_btn.grid(row=0, column=1, padx=10, pady=8)
        
        # Humanitarian challenges button
        self.humanitarian_btn = ctk.CTkButton(
            header, text="🌍 Type for Humanity", command=self.show_humanitarian_challenges
        )
        self.humanitarian_btn.grid(row=0, column=2, padx=10, pady=8)
        
        # World championship button
        self.championship_btn = ctk.CTkButton(
            header, text="🏆 World Championship", command=self.show_world_championship
        )
        self.championship_btn.grid(row=0, column=3, padx=10, pady=8)
        
        # User profile section
        profile_frame = ctk.CTkFrame(header, fg_color=("gray95", "gray25"))
        profile_frame.grid(row=0, column=4, padx=20, pady=8, sticky="ew")
        
        ctk.CTkLabel(profile_frame, text="Profile:", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        
        self.profile_var = tk.StringVar(value="Guest")
        self.profile_menu = ctk.CTkOptionMenu(
            profile_frame,
            values=["Guest"] + list(self.user_profile.profiles.keys()),
            variable=self.profile_var,
            command=self._on_profile_change
        )
        self.profile_menu.grid(row=0, column=1, padx=5)
        
        self.create_profile_btn = ctk.CTkButton(
            profile_frame, text="New", width=40, command=self._create_profile
        )
        self.create_profile_btn.grid(row=0, column=2, padx=5)
        
        # Theme selector
        theme_frame = ctk.CTkFrame(header, fg_color=("gray95", "gray25"))
        theme_frame.grid(row=0, column=5, padx=20, pady=8)
        
        ctk.CTkLabel(theme_frame, text="Theme:", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            command=self._on_theme_change
        )
        self.theme_menu.set(self.current_theme)
        self.theme_menu.grid(row=0, column=1, padx=5)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            header, text="⚙️ Settings", command=self._open_settings
        )
        self.settings_btn.grid(row=0, column=6, padx=10, pady=8)
    
    def _build_content(self):
        """Build the main content area"""
        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=8)
        
        # Left panel - Typing area
        left_panel = ctk.CTkFrame(content, fg_color=("gray95", "gray25"))
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        # Mode selector
        mode_frame = ctk.CTkFrame(left_panel)
        mode_frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(mode_frame, text="Mode:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.mode_var = tk.StringVar(value="Standard")
        mode_menu = ctk.CTkOptionMenu(
            mode_frame,
            values=["Standard", "Challenge", "Custom", "Game"],
            variable=self.mode_var,
            command=self._on_mode_change
        )
        mode_menu.pack(side="left", padx=5)
        
        # Language selector
        lang_frame = ctk.CTkFrame(left_panel)
        lang_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(lang_frame, text="Language:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=list(SENTENCES.keys()),
            command=self._on_language_change
        )
        self.lang_menu.set(self.language)
        self.lang_menu.pack(side="left", padx=5)
        
        # Challenge selector (initially hidden)
        self.challenge_frame = ctk.CTkFrame(left_panel)
        
        ctk.CTkLabel(self.challenge_frame, text="Challenge:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.challenge_var = tk.StringVar()
        self.challenge_menu = ctk.CTkOptionMenu(
            self.challenge_frame,
            values=list(CHALLENGES.keys()),
            variable=self.challenge_var,
            command=self._on_challenge_change
        )
        self.challenge_menu.pack(side="left", padx=5)
        self.challenge_frame.pack_forget()
        
        # Game selector (initially hidden)
        self.game_frame = ctk.CTkFrame(left_panel)
        
        ctk.CTkLabel(self.game_frame, text="Game:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.game_var = tk.StringVar()
        self.game_menu = ctk.CTkOptionMenu(
            self.game_frame,
            values=list(GAMES.keys()),
            variable=self.game_var,
            command=self._on_game_change
        )
        self.game_menu.pack(side="left", padx=5)
        self.game_frame.pack_forget()
        
        # Difficulty selector
        diff_frame = ctk.CTkFrame(left_panel)
        diff_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(diff_frame, text="Difficulty:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.diff_menu = ctk.CTkOptionMenu(
            diff_frame,
            values=list(SENTENCES.get(self.language, {}).keys()),
            command=self._on_difficulty_change
        )
        self.diff_menu.set(self.difficulty)
        self.diff_menu.pack(side="left", padx=5)
        
        # Blind mode checkbox
        self.blind_var = tk.BooleanVar(value=False)
        blind_check = ctk.CTkCheckBox(
            diff_frame,
            text="Blind Mode",
            variable=self.blind_var,
            command=self._on_blind_mode_change
        )
        blind_check.pack(side="left", padx=20)
        
        # Custom text import (initially hidden)
        self.custom_frame = ctk.CTkFrame(left_panel)
        
        ctk.CTkLabel(self.custom_frame, text="Custom Text:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.import_btn = ctk.CTkButton(
            self.custom_frame, text="Import Text", command=self._import_custom_text
        )
        self.import_btn.pack(side="left", padx=5)
        self.custom_frame.pack_forget()
        
        # Target sentence
        self.sentence_label = ctk.CTkLabel(
            left_panel, text="", wraplength=700, font=("Arial", 20)
        )
        self.sentence_label.pack(pady=(18, 10))
        
        # Typing area
        typing_frame = ctk.CTkFrame(left_panel)
        typing_frame.pack(fill="x", pady=10)
        
        self.textbox = tk.Text(typing_frame, height=6, width=80, font=("Consolas", 18), wrap="word")
        self.textbox.pack(pady=5)
        self.textbox.bind("<KeyRelease>", self._on_typing)
        
        # Tags for coloring
        self.textbox.tag_configure("correct", foreground="lime")
        self.textbox.tag_configure("wrong", foreground="red")
        self.textbox.tag_configure("pending", foreground="gray")
        
        # Timer and progress
        timer_frame = ctk.CTkFrame(left_panel)
        timer_frame.pack(fill="x", pady=10)
        
        self.timer_label = ctk.CTkLabel(
            timer_frame, text=f"Time left: {self.time_left}s", font=("Arial", 16)
        )
        self.timer_label.pack(side="left", padx=10)
        
        self.progress = ctk.CTkProgressBar(timer_frame, width=400)
        self.progress.pack(side="left", padx=10)
        self.progress.set(1)
        
        # Live stats
        self.stats_label = ctk.CTkLabel(
            left_panel, text="WPM: 0.00 | Accuracy: 0.00%", font=("Arial", 16)
        )
        self.stats_label.pack(pady=5)
        
        # Motivation messages
        self.motivation_label = ctk.CTkLabel(
            left_panel, text="", font=("Arial", 18, "bold")
        )
        self.motivation_label.pack(pady=5)
        
        # Right panel - Stats and info
        right_panel = ctk.CTkFrame(content, fg_color=("gray95", "gray25"))
        right_panel.pack(side="right", fill="y", padx=(8, 0))
        right_panel.pack_propagate(False)
        
        # Profile stats
        profile_stats_frame = ctk.CTkFrame(right_panel)
        profile_stats_frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(profile_stats_frame, text="Your Stats", font=("Arial", 18, "bold")).pack(pady=5)
        
        self.profile_stats_label = ctk.CTkLabel(
            profile_stats_frame, text="No profile selected", font=("Arial", 14)
        )
        self.profile_stats_label.pack(pady=5)
        
        # Daily challenge
        daily_frame = ctk.CTkFrame(right_panel)
        daily_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(daily_frame, text="Daily Challenge", font=("Arial", 18, "bold")).pack(pady=5)
        
        challenge = self.daily_challenge_system.current_challenge
        self.daily_label = ctk.CTkLabel(
            daily_frame, text=challenge["name"], font=("Arial", 14)
        )
        self.daily_label.pack(pady=2)
        
        self.daily_desc_label = ctk.CTkLabel(
            daily_frame, text=challenge["desc"], font=("Arial", 12), wraplength=250
        )
        self.daily_desc_label.pack(pady=2)
        
        # Achievements
        achievements_frame = ctk.CTkFrame(right_panel)
        achievements_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(achievements_frame, text="Recent Achievements", font=("Arial", 18, "bold")).pack(pady=5)
        
        self.achievements_label = ctk.CTkLabel(
            achievements_frame, text="None yet", font=("Arial", 14)
        )
        self.achievements_label.pack(pady=5)
        
        # Leaderboard preview
        leaderboard_frame = ctk.CTkFrame(right_panel)
        leaderboard_frame.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(leaderboard_frame, text="Top Players", font=("Arial", 18, "bold")).pack(pady=5)
        
        self.leaderboard_text = tk.Text(
            leaderboard_frame, height=10, width=30, font=("Courier New", 10)
        )
        self.leaderboard_text.pack(pady=5)
        self.leaderboard_text.configure(state="disabled")
    
    def _build_footer(self):
        """Build the footer section"""
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=(8, 16))
        
        # Action buttons
        self.start_btn = ctk.CTkButton(
            footer, text="Start", command=self.start_round
        )
        self.start_btn.grid(row=0, column=0, padx=10)
        
        self.finish_btn = ctk.CTkButton(
            footer, text="Finish", command=self.finish_round
        )
        self.finish_btn.grid(row=0, column=1, padx=10)
        
        self.retry_btn = ctk.CTkButton(
            footer, text="Retry", command=self.retry_round
        )
        self.retry_btn.grid(row=0, column=2, padx=10)
        
        # Music toggle
        self.music_btn = ctk.CTkButton(
            footer, text="🎵 Music", command=self.toggle_music
        )
        self.music_btn.grid(row=0, column=3, padx=10)
        
        # Sound toggle
        self.sound_btn = ctk.CTkButton(
            footer, text="🔊 Sound", command=self.toggle_sound
        )
        self.sound_btn.grid(row=0, column=4, padx=10)
        
        # Stats button
        self.stats_btn = ctk.CTkButton(
            footer, text="📊 Stats", command=self.show_stats
        )
        self.stats_btn.grid(row=0, column=5, padx=10)
        
        # Leaderboard button
        self.lb_btn = ctk.CTkButton(
            footer, text="🏆 Leaderboard", command=self.show_leaderboard
        )
        self.lb_btn.grid(row=0, column=6, padx=10)
        
        # Heatmap button
        self.heatmap_btn = ctk.CTkButton(
            footer, text="🔥 Heatmap", command=self.show_heatmap
        )
        self.heatmap_btn.grid(row=0, column=7, padx=10)
        
        # Practice button
        self.practice_btn = ctk.CTkButton(
            footer, text="🎯 Practice", command=self.start_practice_mode
        )
        self.practice_btn.grid(row=0, column=8, padx=10)
        
        # Inspirational stories button
        self.stories_btn = ctk.CTkButton(
            footer, text="📖 Stories", command=self.show_inspirational_stories
        )
        self.stories_btn.grid(row=0, column=9, padx=10)
        
        # Global impact button
        self.impact_btn = ctk.CTkButton(
            footer, text="🌍 Impact", command=self.show_global_impact
        )
        self.impact_btn.grid(row=0, column=10, padx=10)
    
    def _bind_events(self):
        """Bind application events"""
        self.bind("<Configure>", self._on_window_resize)
    
    def _load_data(self):
        """Load application data"""
        # Load profiles
        self.user_profile.load_storage()
        
        # Update UI
        self._update_profile_menu()
        self._update_profile_stats()
        self._update_leaderboard_preview()
    
    def _load_background_image(self):
        """Load and set the background image if available"""
        if not HAS_PIL:
            print("Pillow library not available. Skipping background image.")
            return
            
        if os.path.exists(BACKGROUND_IMAGE):
            try:
                img = PILImage.open(BACKGROUND_IMAGE)
                # Keep original PIL image so we can resize later
                self._bg_original_img = img
                # Initial CTkImage with current window size
                self.background_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(self.winfo_width(), self.winfo_height())
                )
                self.bg_label = ctk.CTkLabel(
                    self, text="", image=self.background_image
                )
                self.bg_label.place(relwidth=1, relheight=1)
                # Ensure main UI stays on top
                if hasattr(self, "main_container"):
                    try:
                        self.bg_label.lower(self.main_container)
                    except Exception:
                        self.main_container.lift()
                print("Background image loaded successfully!")
            except Exception as e:
                print(f"Error loading background image: {e}")
        else:
            print(f"Background image file not found: {BACKGROUND_IMAGE}")
    
    def _resize_background(self, event):
        """Resize background dynamically when window size changes"""
        if hasattr(self, "_bg_original_img") and self._bg_original_img:
            if event.width > 2 and event.height > 2:
                try:
                    self.background_image = ctk.CTkImage(
                        light_image=self._bg_original_img,
                        dark_image=self._bg_original_img,
                        size=(event.width, event.height)
                    )
                    self.bg_label.configure(image=self.background_image)
                except Exception as e:
                    print("Background resize error:", e)
    
    def _on_window_resize(self, event):
        """Handle window resize events for responsive design"""
        if event.widget == self:
            # Debounce resize events
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(200, self._adjust_ui)
    
    def _adjust_ui(self):
        """Adjust UI elements based on window size"""
        try:
            width = self.winfo_width()
            height = self.winfo_height()
            
            # Calculate font sizes based on window dimensions
            title_font_size = max(20, int(width / 50))
            header_font_size = max(16, int(width / 70))
            text_font_size = max(14, int(width / 80))
            stats_font_size = max(12, int(width / 90))
            button_font_size = max(10, int(width / 100))
            
            # Update UI elements with new font sizes
            try:
                # Header elements
                if hasattr(self, 'profile_menu'):
                    self.profile_menu.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'theme_menu'):
                    self.theme_menu.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'settings_btn'):
                    self.settings_btn.configure(font=("Arial", button_font_size))
                
                # Content elements
                if hasattr(self, 'mode_menu'):
                    self.mode_menu.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'lang_menu'):
                    self.lang_menu.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'diff_menu'):
                    self.diff_menu.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'sentence_label'):
                    self.sentence_label.configure(font=("Arial", text_font_size))
                if hasattr(self, 'textbox'):
                    self.textbox.configure(font=("Consolas", text_font_size))
                if hasattr(self, 'timer_label'):
                    self.timer_label.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'stats_label'):
                    self.stats_label.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'motivation_label'):
                    self.motivation_label.configure(font=("Arial", stats_font_size))
                
                # Right panel elements
                if hasattr(self, 'profile_stats_label'):
                    self.profile_stats_label.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'daily_label'):
                    self.daily_label.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'daily_desc_label'):
                    self.daily_desc_label.configure(font=("Arial", stats_font_size))
                if hasattr(self, 'achievements_label'):
                    self.achievements_label.configure(font=("Arial", stats_font_size))
                
                # Footer buttons
                buttons = [
                    'start_btn', 'finish_btn', 'retry_btn', 'music_btn',
                    'sound_btn', 'stats_btn', 'lb_btn', 'heatmap_btn',
                    'practice_btn', 'stories_btn', 'impact_btn'
                ]
                for button_name in buttons:
                    if hasattr(self, button_name):
                        getattr(self, button_name).configure(font=("Arial", button_font_size))
            except Exception as e:
                print(f"Error adjusting font sizes: {e}")
        except Exception as e:
            print(f"Error in UI adjustment: {e}")
    
    def _show_welcome_dialog(self):
        """Show a welcome dialog for new users"""
        if not self.user_profile.profiles:
            dialog = ctk.CTkToplevel(self)
            dialog.title("Welcome to Typing Master Pro!")
            dialog.geometry("500x300")
            dialog.resizable(False, False)
            
            ctk.CTkLabel(dialog, text="Welcome to Typing Master Pro!", 
                         font=("Arial", 24, "bold")).pack(pady=20)
            ctk.CTkLabel(dialog, text="Create a profile to track your progress and unlock achievements.", 
                         font=("Arial", 14)).pack(pady=10)
            
            # Profile name entry
            name_frame = ctk.CTkFrame(dialog)
            name_frame.pack(pady=20)
            
            ctk.CTkLabel(name_frame, text="Your Name:").pack(side="left", padx=5)
            name_entry = ctk.CTkEntry(name_frame, width=200)
            name_entry.pack(side="left", padx=5)
            
            def create():
                name = name_entry.get().strip()
                if name:
                    if self.user_profile.create_profile(name):
                        self.user_profile.load_profile(name)
                        self.profile_var.set(name)
                        self._update_profile_menu()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Profile name already exists!")
            
            ctk.CTkButton(dialog, text="Create", command=create).pack(pady=10)
            ctk.CTkButton(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def _update_profile_menu(self):
        """Update the profile menu with current profiles"""
        profiles = ["Guest"] + list(self.user_profile.profiles.keys())
        self.profile_menu.configure(values=profiles)
    
    def _on_profile_change(self, value):
        """Handle profile selection change"""
        if value == "Guest":
            self.user_profile.current_profile = None
        else:
            self.user_profile.load_profile(value)
        self._update_profile_stats()
    
    def _on_theme_change(self, value):
        """Handle theme change"""
        self.current_theme = value
        self.user_profile.settings["theme"] = value
        self.user_profile.save_storage()
        ctk.set_appearance_mode(value)
    
    def _on_mode_change(self, value):
        """Handle mode change"""
        self.current_mode = value
        
        # Show/hide relevant UI elements
        if value == "Challenge":
            self.challenge_frame.pack(fill="x", pady=5)
            self.game_frame.pack_forget()
            self.custom_frame.pack_forget()
        elif value == "Game":
            self.game_frame.pack(fill="x", pady=5)
            self.challenge_frame.pack_forget()
            self.custom_frame.pack_forget()
        elif value == "Custom":
            self.custom_frame.pack(fill="x", pady=5)
            self.challenge_frame.pack_forget()
            self.game_frame.pack_forget()
        else:  # Standard
            self.challenge_frame.pack_forget()
            self.game_frame.pack_forget()
            self.custom_frame.pack_forget()
        
        self.current_challenge = None
    
    def _on_language_change(self, value):
        """Handle language change"""
        self.language = value
        
        # Update difficulty options
        difficulties = list(SENTENCES.get(value, {}).keys())
        self.diff_menu.configure(values=difficulties)
        if difficulties:
            self.difficulty = difficulties[0]
            self.diff_menu.set(self.difficulty)
        
        self.load_new_sentence()
    
    def _on_difficulty_change(self, value):
        """Handle difficulty change"""
        self.difficulty = value
        self.load_new_sentence()
    
    def _on_blind_mode_change(self):
        """Handle blind mode toggle"""
        self.blind_mode = self.blind_var.get()
        if self.blind_mode:
            messagebox.showinfo("Blind Mode", "Blind mode activated! Try not to look at the keyboard while typing.")
    
    def _on_challenge_change(self, value):
        """Handle challenge selection"""
        self.current_challenge = value
        challenge = CHALLENGES[value]
        
        # Set round duration
        self.round_seconds = challenge["time_limit"]
        self.time_left = self.round_seconds
        self.timer_label.configure(text=f"Time left: {self.time_left}s")
        self.progress.set(1)
        
        # Update motivation label
        self.motivation_label.configure(
            text=f"Challenge: {value} - {challenge['reward']}"
        )
        
        # Special handling for blind mode challenge
        if challenge.get("blind_mode"):
            self.blind_var.set(True)
            self._on_blind_mode_change()
    
    def _on_game_change(self, value):
        """Handle game selection"""
        game = GAMES[value]
        
        # Update motivation label
        self.motivation_label.configure(
            text=f"Game: {value} - {game['description']}"
        )
        
        # Special handling for Memory Master game
        if value == "Memory Master":
            self.motivation_label.configure(
                text=f"Game: {value} - Train your brain memory!"
            )
    
    def _import_custom_text(self):
        """Import custom text for typing practice"""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.custom_text = f.read()
                
                # Use the first sentence or a portion of the text
                sentences = self.custom_text.split('.')
                if sentences:
                    self.current_sentence = sentences[0].strip() + '.'
                else:
                    # If no sentences, take the first 100 characters
                    self.current_sentence = self.custom_text[:100] + "..."
                
                self.sentence_label.configure(text=self.current_sentence)
                self.reset_typing_area()
                messagebox.showinfo("Success", "Custom text imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import text: {str(e)}")
    
    def _update_profile_stats(self):
        """Update the profile stats display"""
        if self.user_profile.current_profile:
            profile = self.user_profile.profiles[self.user_profile.current_profile]
            stats_text = (
                f"Tests: {profile['tests_completed']}\n"
                f"Best WPM: {profile['best_wpm']:.2f}\n"
                f"Best Accuracy: {profile['best_accuracy']:.2f}%\n"
                f"Languages: {len(profile.get('languages_tried', set()))}"
            )
            self.profile_stats_label.configure(text=stats_text)
            
            # Update achievements
            if profile["achievements"]:
                latest = profile["achievements"][-1]
                ach = next((a for a in ACHIEVEMENTS if a["id"] == latest), None)
                if ach:
                    self.achievements_label.configure(
                        text=f"{ach['icon']} {ach['name']}"
                    )
        else:
            self.profile_stats_label.configure(text="No profile selected")
            self.achievements_label.configure(text="None yet")
    
    def _update_leaderboard_preview(self):
        """Update the leaderboard preview"""
        board = load_json_file(LEADERBOARD_FILE, [])
        if board:
            sorted_board = sorted(
                board, key=lambda x: x.get("wpm", 0.0), reverse=True
            )
            top5 = sorted_board[:5]
            
            self.leaderboard_text.configure(state="normal")
            self.leaderboard_text.delete("1.0", "end")
            
            for i, entry in enumerate(top5, start=1):
                self.leaderboard_text.insert("end", f"{i}. {entry['name']}\n")
                self.leaderboard_text.insert(
                    "end", f"   {entry['wpm']:.1f} WPM\n"
                )
            
            self.leaderboard_text.configure(state="disabled")
    
    def _open_settings(self):
        """Open the settings dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Settings")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        
        # Theme settings
        theme_frame = ctk.CTkFrame(dialog)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(theme_frame, text="Theme Settings", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(theme_frame, text="Current Theme:").pack(anchor="w", padx=10)
        
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            command=self._on_theme_change
        )
        theme_menu.set(self.current_theme)
        theme_menu.pack(fill="x", padx=10, pady=5)
        
        # Background image
        bg_frame = ctk.CTkFrame(dialog)
        bg_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(bg_frame, text="Background Image", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(bg_frame, text="Current: " + (BACKGROUND_IMAGE if os.path.exists(BACKGROUND_IMAGE) else "None")).pack(anchor="w", padx=10)
        
        def change_background():
            file_path = filedialog.askopenfilename(
                title="Select Background Image",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
            )
            if file_path:
                global BACKGROUND_IMAGE
                BACKGROUND_IMAGE = file_path
                self._load_background_image()
                dialog.destroy()
                self._open_settings()  # Reopen to show updated path
        
        ctk.CTkButton(bg_frame, text="Change Background", 
                      command=change_background).pack(pady=5)
        
        # Sound settings
        sound_frame = ctk.CTkFrame(dialog)
        sound_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(sound_frame, text="Sound Settings", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        sound_var = tk.BooleanVar(value=self.sound_enabled)
        sound_check = ctk.CTkCheckBox(
            sound_frame,
            text="Enable Sound Effects",
            variable=sound_var,
            command=lambda: setattr(self, 'sound_enabled', sound_var.get())
        )
        sound_check.pack(anchor="w", padx=10, pady=5)
        
        music_var = tk.BooleanVar(value=self.music_enabled)
        music_check = ctk.CTkCheckBox(
            sound_frame,
            text="Enable Background Music",
            variable=music_var,
            command=lambda: setattr(self, 'music_enabled', music_var.get())
        )
        music_check.pack(anchor="w", padx=10, pady=5)
        
        # Ergonomics settings
        ergo_frame = ctk.CTkFrame(dialog)
        ergo_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(ergo_frame, text="Ergonomics Settings", 
                     font=("Arial", 18, "bold")).pack(pady=10)
        
        ergo_var = tk.BooleanVar(value=self.ergonomics_enabled)
        ergo_check = ctk.CTkCheckBox(
            ergo_frame,
            text="Enable Ergonomics Reminders",
            variable=ergo_var,
            command=lambda: setattr(self, 'ergonomics_enabled', ergo_var.get())
        )
        ergo_check.pack(anchor="w", padx=10, pady=5)
        
        # Test reminder button
        def test_reminder():
            tip = random.choice(ERGONOMICS_TIPS)
            ErgonomicsReminder(self, tip)
        
        ctk.CTkButton(ergo_frame, text="Test Reminder", 
                      command=test_reminder).pack(pady=5)
        
        # Close button
        ctk.CTkButton(dialog, text="Close", 
                      command=dialog.destroy).pack(pady=20)
    
    def _schedule_ergonomics_reminder(self):
        """Schedule ergonomics reminders"""
        if self.ergonomics_enabled:
            if self.user_profile.current_profile:
                if self.user_profile.show_ergonomics_reminder(self.user_profile.current_profile):
                    tip = random.choice(ERGONOMICS_TIPS)
                    ErgonomicsReminder(self, tip)
        
        # Schedule next reminder
        interval = self.user_profile.settings.get("reminder_interval", 1200)
        self.after(interval * 1000, self._schedule_ergonomics_reminder)
    
    def load_new_sentence(self):
        """Load a new random sentence based on difficulty and language"""
        if self.current_mode == "Custom" and self.custom_text:
            # Use custom text if available
            sentences = self.custom_text.split('.')
            if sentences:
                self.current_sentence = random.choice(sentences).strip() + '.'
            else:
                self.current_sentence = self.custom_text[:100] + "..."
        else:
            # Use predefined sentences
            pool = SENTENCES.get(self.language, {}).get(self.difficulty, SENTENCES["English"]["Easy"])
            self.current_sentence = random.choice(pool)
        
        self.sentence_label.configure(text=self.current_sentence)
        self.reset_typing_area()
    
    def reset_typing_area(self):
        """Reset the typing area and stats"""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self._apply_pending_tags()
        self.current_wpm = 0.0
        self.current_accuracy = 0.0
        self.stats_label.configure(text="WPM: 0.00 | Accuracy: 0.00%")
        self.time_left = self.round_seconds
        self.timer_label.configure(text=f"Time left: {self.time_left}s")
        self.progress.set(1)
        self.motivation_label.configure(text="")
        self.timer_running = False
    
    def start_round(self):
        """Start a new typing round"""
        # Handle game mode
        if self.current_mode == "Game":
            game = self.game_var.get()
            if game == "Type Defense":
                TypeDefenseGame(self, self.difficulty)
            elif game == "Memory Master":
                MemoryMasterGame(self, self.difficulty)
            return
        
        # Update player name
        name = self.profile_var.get().strip()
        self.player_name = name if name else "Guest"
        
        # Reset UI and timing
        self.reset_typing_area()
        self.start_time = time.time()
        self.timer_running = True
        self._tick_timer()
        
        # Start background music
        if self.music_enabled and HAS_PYGAME and os.path.exists(BACKGROUND_MUSIC_FILE):
            try:
                pygame.mixer.music.play(-1)
                self.music_btn.configure(text="🔇 Music")
            except Exception:
                pass
    
    def finish_round(self):
        """Finish the current round early"""
        if not self.start_time:
            messagebox.showinfo("Info", "Click Start to begin the round.")
            return
        
        self.timer_running = False
        self._finalize_round()
    
    def retry_round(self):
        """Retry with a new sentence"""
        self.load_new_sentence()
    
    def toggle_music(self):
        """Toggle background music"""
        if not HAS_PYGAME:
            messagebox.showinfo("Music", "pygame not available. Install with: pip install pygame")
            return
        
        if not os.path.exists(BACKGROUND_MUSIC_FILE):
            messagebox.showinfo("Music", f"Missing {BACKGROUND_MUSIC_FILE}. Place an mp3 next to the script.")
            return
        
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                self.music_btn.configure(text="🎵 Music")
            else:
                pygame.mixer.music.play(-1)
                self.music_btn.configure(text="🔇 Music")
        except Exception as e:
            print("Music toggle error:", e)
    
    def toggle_sound(self):
        """Toggle sound effects"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.configure(text="🔊 Sound")
        else:
            self.sound_btn.configure(text="🔇 Sound")
    
    def show_stats(self):
        """Show the statistics dashboard"""
        if self.user_profile.current_profile:
            profile = self.user_profile.profiles[self.user_profile.current_profile]
            StatsDashboard(self, profile)
        else:
            messagebox.showinfo("Stats", "Please create or select a profile to view statistics.")
    
    def show_leaderboard(self):
        """Show the full leaderboard"""
        board = load_json_file(LEADERBOARD_FILE, [])
        if not board:
            messagebox.showinfo("Leaderboard", "No scores yet! Play a round first.")
            return
        
        # Sort by WPM desc
        sorted_board = sorted(
            board, key=lambda x: x.get("wpm", 0.0), reverse=True
        )
        top50 = sorted_board[:50]
        bottom10 = sorted_board[-10:] if len(sorted_board) >= 10 else sorted_board[-len(sorted_board):]
        
        # Create popup window
        win = ctk.CTkToplevel(self)
        win.title("Leaderboard — Top 50 & Bottom 10")
        win.geometry("900x620")
        
        # Top section
        section_top = ctk.CTkFrame(win)
        section_top.pack(fill="both", expand=True, padx=10, pady=(10, 6))
        
        lbl_top = ctk.CTkLabel(
            section_top, text="🏆 Top 50 Overall (by WPM)", font=("Arial", 22, "bold")
        )
        lbl_top.pack(pady=8)
        
        txt_top = tk.Text(section_top, height=16, width=110, font=("Courier New", 12))
        txt_top.pack(padx=8, pady=6)
        
        # Header line
        txt_top.insert(
            "end", f"{'#':<4}{'Name':<18}{'WPM':>8}{'Acc%':>8}{'Difficulty':>14}{'Language':>10}{'Date':>16}\n"
        )
        txt_top.insert("end", "-" * 90 + "\n")
        
        for i, e in enumerate(top50, start=1):
            txt_top.insert(
                "end",
                f"{i:<4}{e.get('name', ''):<18}{e.get('wpm', 0):>8.2f}{e.get('accuracy', 0):>8.2f}{e.get('difficulty', ''):>14}{e.get('language', ''):>10}{e.get('date', ''):>16}\n"
            )
        
        txt_top.configure(state="disabled")
        
        # Bottom section
        section_bottom = ctk.CTkFrame(win)
        section_bottom.pack(fill="both", expand=True, padx=10, pady=(6, 10))
        
        lbl_bottom = ctk.CTkLabel(
            section_bottom, text="😬 Bottom 10 Overall (by WPM)", font=("Arial", 20, "bold")
        )
        lbl_bottom.pack(pady=8)
        
        txt_bottom = tk.Text(section_bottom, height=10, width=110, font=("Courier New", 12))
        txt_bottom.pack(padx=8, pady=6)
        
        txt_bottom.insert(
            "end", f"{'#':<4}{'Name':<18}{'WPM':>8}{'Acc%':>8}{'Difficulty':>14}{'Language':>10}{'Date':>16}\n"
        )
        txt_bottom.insert("end", "-" * 90 + "\n")
        
        for i, e in enumerate(bottom10, start=1):
            txt_bottom.insert(
                "end",
                f"{i:<4}{e.get('name', ''):<18}{e.get('wpm', 0):>8.2f}{e.get('accuracy', 0):>8.2f}{e.get('difficulty', ''):>14}{e.get('language', ''):>10}{e.get('date', ''):>16}\n"
            )
        
        txt_bottom.configure(state="disabled")
    
    def show_heatmap(self):
        """Show the typing heatmap"""
        if self.user_profile.current_profile:
            accuracy_data = self.user_profile.get_key_accuracy(self.user_profile.current_profile)
            if accuracy_data:
                TypingHeatmap(self, accuracy_data)
            else:
                messagebox.showinfo("Heatmap", "Not enough data to generate heatmap. Complete more typing tests.")
        else:
            messagebox.showinfo("Heatmap", "Please create or select a profile to view heatmap.")
    
    def start_practice_mode(self):
        """Start practice mode for weak keys"""
        if self.user_profile.current_profile:
            weak_keys = self.user_profile.get_weak_keys(self.user_profile.current_profile, 5)
            if weak_keys:
                PracticeMode(self, weak_keys, self.user_profile)
            else:
                messagebox.showinfo("Practice", "No weak keys identified yet. Complete more typing tests.")
        else:
            messagebox.showinfo("Practice", "Please create or select a profile to use practice mode.")
    
    def show_daily_challenge(self):
        """Show the daily challenge details"""
        challenge = self.daily_challenge_system.current_challenge
        dialog = ctk.CTkToplevel(self)
        dialog.title("Daily Challenge")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        
        ctk.CTkLabel(dialog, text="📅 Daily Challenge", 
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(dialog, text=challenge["name"], 
                     font=("Arial", 20)).pack(pady=5)
        ctk.CTkLabel(dialog, text=challenge["desc"], 
                     font=("Arial", 16), wraplength=450).pack(pady=10)
        
        status = "Completed!" if self.daily_challenge_system.completed_today else "Not completed yet"
        status_color = "#4CAF50" if self.daily_challenge_system.completed_today else "#f44336"
        ctk.CTkLabel(dialog, text=status, 
                     font=("Arial", 16), text_color=status_color).pack(pady=5)
        
        ctk.CTkButton(dialog, text="Close", 
                      command=dialog.destroy).pack(pady=20)
    
    def share_achievement(self, achievement_id):
        """Share an achievement on social media"""
        if not self.user_profile.current_profile:
            messagebox.showinfo("Share", "Please log in to share achievements.")
            return
        
        # Get achievement details
        achievement = next((a for a in ACHIEVEMENTS if a["id"] == achievement_id), None)
        if not achievement:
            return
        
        # Create share message
        profile = self.user_profile.profiles[self.user_profile.current_profile]
        message = f"I just unlocked the {achievement['name']} achievement in Typing Master Pro! {achievement['icon']}"
        
        # Try to share via API (placeholder)
        try:
            # This is a placeholder for actual social media sharing
            # In a real implementation, you would use the appropriate APIs
            response = requests.post(
                SOCIAL_SHARE_API,
                json={"message": message, "achievement": achievement_id}
            )
            if response.status_code == 200:
                messagebox.showinfo("Success", "Achievement shared successfully!")
                # Unlock social butterfly achievement if not already unlocked
                if self.user_profile.unlock_achievement(self.user_profile.current_profile, "social"):
                    self.achievement_system.show_achievement_popup(self, "social")
            else:
                messagebox.showinfo("Share", f"Share message copied to clipboard: {message}")
        except:
            # Fallback to clipboard
            self.clipboard_clear()
            self.clipboard_append(message)
            messagebox.showinfo("Share", f"Share message copied to clipboard: {message}")
    
    def show_humanitarian_challenges(self):
        """Show humanitarian challenges"""
        HumanitarianChallenge(self)
    
    def show_inspirational_stories(self):
        """Show inspirational stories"""
        InspirationalStories(self)
    
    def show_world_championship(self):
        """Show world championship"""
        WorldChampionship(self)
    
    def show_daily_inspiration(self):
        """Show daily inspiration"""
        DailyInspiration(self)
    
    def show_global_impact(self):
        """Show global impact dashboard"""
        GlobalImpactDashboard(self)
    
    def _tick_timer(self):
        """Timer scheduler"""
        if not self.timer_running:
            return
        
        elapsed = int(time.time() - self.start_time)
        self.time_left = max(self.round_seconds - elapsed, 0)
        self.timer_label.configure(text=f"Time left: {self.time_left}s")
        
        # Update progress bar
        self.progress.set(
            self.time_left / self.round_seconds if self.round_seconds else 0
        )
        
        # Motivational messages
        if self.time_left == 45:
            self.motivation_label.configure(text="⚡ Keep the rhythm!")
        elif self.time_left == 30:
            self.motivation_label.configure(text="🔥 Halfway there — focus!")
        elif self.time_left == 10:
            self.motivation_label.configure(text="⏳ Final push! You got this!")
        
        if self.time_left <= 0:
            self.timer_running = False
            self._finalize_round()
        else:
            self.after(1000, self._tick_timer)
    
    def _on_typing(self, event=None):
        """Handle typing events with sound effects"""
        typed = self.textbox.get("1.0", "end-1c")
        
        # Clear previous tags
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        self.textbox.tag_remove("pending", "1.0", "end")
        
        # Apply color tags and play sounds
        for i, target_char in enumerate(self.current_sentence):
            start_index = f"1.{i}"
            end_index = f"1.{i+1}"
            
            if i < len(typed):
                if typed[i] == target_char:
                    self.textbox.tag_add("correct", start_index, end_index)
                    # Play correct sound if enabled
                    if self.sound_enabled and SOUND_CORRECT in self.sounds:
                        self.sounds[SOUND_CORRECT].play()
                else:
                    self.textbox.tag_add("wrong", start_index, end_index)
                    # Play wrong sound if enabled
                    if self.sound_enabled and SOUND_WRONG in self.sounds:
                        self.sounds[SOUND_WRONG].play()
            else:
                self.textbox.tag_add("pending", start_index, end_index)
        
        # Update stats if timer is running
        if self.start_time and self.timer_running:
            elapsed = time.time() - self.start_time
            words = len(typed.split())
            wpm = (words / elapsed) * 60 if elapsed > 0 else 0.0
            
            # Calculate accuracy
            correct_chars = sum(1 for a, b in zip(typed, self.current_sentence) if a == b)
            accuracy = (correct_chars / max(1, len(self.current_sentence))) * 100.0
            
            self.current_wpm = round(wpm, 2)
            self.current_accuracy = round(accuracy, 2)
            self.stats_label.configure(
                text=f"WPM: {self.current_wpm:.2f} | Accuracy: {self.current_accuracy:.2f}%"
            )
    
    def _apply_pending_tags(self):
        """Apply pending tags to all characters"""
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        self.textbox.tag_remove("pending", "1.0", "end")
        
        for i, _ in enumerate(self.current_sentence):
            self.textbox.tag_add("pending", f"1.{i}", f"1.{i+1}")
    
    def _finalize_round(self):
        """Finalize the round and save results"""
        # Stop music
        if HAS_PYGAME:
            try:
                pygame.mixer.music.stop()
                self.music_btn.configure(text="🎵 Music")
            except Exception:
                pass
        
        # Play completion sound
        if self.sound_enabled and SOUND_COMPLETE in self.sounds:
            self.sounds[SOUND_COMPLETE].play()
        
        # Lock typing box
        self.textbox.configure(state="disabled")
        
        # Calculate final stats
        typed = self.textbox.get("1.0", "end-1c")
        elapsed = max(time.time() - (self.start_time or time.time()), 0.0001)
        words = len(typed.split())
        wpm = (words / elapsed) * 60
        correct_chars = sum(1 for a, b in zip(typed, self.current_sentence) if a == b)
        accuracy = (correct_chars / max(1, len(self.current_sentence))) * 100.0
        
        self.current_wpm = round(wpm, 2)
        self.current_accuracy = round(accuracy, 2)
        self.stats_label.configure(
            text=f"WPM: {self.current_wpm:.2f} | Accuracy: {self.current_accuracy:.2f}%"
        )
        
        # Check challenge completion
        if self.current_mode == "Challenge" and self.current_challenge:
            challenge = CHALLENGES[self.current_challenge]
            reward = None
            if challenge.get("target_wpm") and wpm >= challenge.get("target_wpm"):
                reward = challenge["reward"]
            elif challenge.get("target_accuracy") and accuracy >= challenge.get("target_accuracy"):
                reward = challenge["reward"]
            elif challenge.get("target_words") and words >= challenge.get("target_words"):
                reward = challenge["reward"]
            
            if reward:
                messagebox.showinfo("Challenge Complete!", f"You've earned the {reward}!")
        
        # Check daily challenge completion
        if self.daily_challenge_system.check_challenge_completion(
                wpm, accuracy, self.difficulty, self.round_seconds):
            self.daily_challenge_system.complete_challenge()
            DailyChallengePopup(
                self, self.daily_challenge_system.current_challenge, "XP Boost"
            )
        
        # Save to leaderboard
        entry = {
            "name": self.player_name,
            "wpm": self.current_wpm,
            "accuracy": round(self.current_accuracy, 2),
            "difficulty": self.difficulty,
            "language": self.language,
            "date": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        board = load_json_file(LEADERBOARD_FILE, [])
        board.append(entry)
        save_json_file(LEADERBOARD_FILE, board)
        
        # Update user profile if logged in
        if self.user_profile.current_profile:
            self.user_profile.update_profile_with_test(
                self.user_profile.current_profile,
                self.current_wpm,
                self.current_accuracy,
                typed,
                self.current_sentence,
                duration=self.round_seconds,
                language=self.language
            )
            
            # Check achievements
            profile = self.user_profile.profiles[self.user_profile.current_profile]
            newly_unlocked = self.achievement_system.check_achievements(
                profile, self.current_wpm, self.current_accuracy, self.difficulty, self.language
            )
            
            for ach_id in newly_unlocked:
                if self.user_profile.unlock_achievement(self.user_profile.current_profile, ach_id):
                    self.achievement_system.show_achievement_popup(self, ach_id)
            
            # Update profile stats display
            self._update_profile_stats()
        
        # Evaluate rankings
        self._evaluate_rewards(entry, board)
        
        # Update leaderboard preview
        self._update_leaderboard_preview()
    
    def _evaluate_rewards(self, entry, board):
        """Evaluate rewards and show popups"""
        # Overall sorted by WPM (desc)
        overall_sorted = sorted(
            board, key=lambda x: x.get("wpm", 0.0), reverse=True
        )
        
        # Rank of current entry among overall
        overall_rank = next(
            (i+1 for i, e in enumerate(overall_sorted) if e is entry or e == entry), None
        )
        
        # If the player is #1 overall, show celebration
        if overall_rank == 1:
            # Play victory sound
            if HAS_PYGAME and os.path.exists(VICTORY_SOUND_FILE):
                try:
                    sfx = pygame.mixer.Sound(VICTORY_SOUND_FILE)
                    sfx.play()
                except Exception:
                    pass
            
            ConfettiPopup(self)
            
            # Unlock champion achievement if logged in
            if self.user_profile.current_profile:
                if self.user_profile.unlock_achievement(self.user_profile.current_profile, "champion"):
                    self.achievement_system.show_achievement_popup(self, "champion")
        
        # Rank within difficulty
        same_diff = [e for e in board if e.get("difficulty") == entry.get("difficulty")]
        diff_sorted = sorted(
            same_diff, key=lambda x: x.get("wpm", 0.0), reverse=True
        )
        diff_rank = next(
            (i+1 for i, e in enumerate(diff_sorted) if e is entry or e == entry), None
        )
        
        if diff_rank is not None and diff_rank <= 3:
            MedalPopup(
                self, 
                place=diff_rank, 
                difficulty=entry.get("difficulty", ""), 
                wpm=entry.get("wpm", 0.0)
            )
        else:
            # Encouragement for others
            messagebox.showinfo(
                "Nice Run!", "Good effort! Keep practicing to climb the ranks."
            )
    
    def _create_profile(self):
        """Create a new user profile"""
        name = None
        try:
            name = ctk.CTkInputDialog(text="Enter profile name", title="Create Profile").get_input()
        except Exception:
            name = simpledialog.askstring("Create Profile", "Enter profile name:", parent=self)
        
        if not name:
            return
        
        if self.user_profile.create_profile(name.strip()):
            self._update_profile_menu()
            self._update_profile_stats()
            messagebox.showinfo("Success", f"Profile '{name}' created successfully!")
        else:
            messagebox.showerror("Error", "Profile name already exists or is invalid!")

# CLI functionality
def main_cli(argv=None):
    """Command-line interface for Typing Master Pro"""
    argv = argv or sys.argv[1:]
    
    import argparse
    ap = argparse.ArgumentParser(prog="typing-master-pro", description="Typing Master Pro - full integrated app")
    sub = ap.add_subparsers(dest="cmd")
    
    sub.add_parser("run-gui", help="Run the GUI (CTk if available, else Tk)")
    sub.add_parser("list", help="List profiles")
    
    ap_create = sub.add_parser("create", help="Create profile")
    ap_create.add_argument("name")
    
    ap_delete = sub.add_parser("delete", help="Delete profile")
    ap_delete.add_argument("name")
    
    ap_export = sub.add_parser("export", help="Export profiles to JSON")
    ap_export.add_argument("out")
    
    ap_import = sub.add_parser("import", help="Import profiles from JSON")
    ap_import.add_argument("inp")
    ap_import.add_argument("--overwrite", action="store_true")
    
    ap_csv_exp = sub.add_parser("csv-export", help="Export profiles to CSV")
    ap_csv_exp.add_argument("out")
    
    ap_csv_imp = sub.add_parser("csv-import", help="Import profiles from CSV")
    ap_csv_imp.add_argument("inp")
    ap_csv_imp.add_argument("--overwrite", action="store_true")
    
    sub.add_parser("to-v2", help="Upgrade all profiles to v2 schema")
    
    ap_submit = sub.add_parser("submit", help="Submit leaderboard to remote")
    ap_submit.add_argument("url")
    ap_submit.add_argument("--api-key")
    ap_submit.add_argument("--api-secret")
    
    args = ap.parse_args(argv)
    
    pm = UserProfileManager()
    
    if args.cmd == "run-gui" or args.cmd is None:
        if CTK_AVAILABLE:
            app = TypingMasterPro()
            app.mainloop()
        else:
            # Fallback to Tk if CTk is not available
            from tkinter import Tk, Label, Button, Entry, Text, END, messagebox, filedialog
            import tkinter as tk
            
            class TypingMasterProTk:
                def __init__(self, pm):
                    self.pm = pm
                    self.root = Tk()
                    self.root.title("Typing Master Pro")
                    self.root.geometry("1000x680")
                    self._build_ui()
                    self._reload_profiles()
                
                def _build_ui(self):
                    self.root.rowconfigure(1, weight=1)
                    self.root.columnconfigure(1, weight=1)
                    
                    Label(self.root, text="Typing Master Pro").grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=6)
                    
                    # Left
                    lf = ttk.Frame(self.root)
                    lf.grid(row=1, column=0, sticky="nsw", padx=(10,6), pady=10)
                    
                    Label(lf, text="Profiles").grid(row=0, column=0, sticky="w")
                    self.profile_list = tk.Listbox(lf, height=12)
                    self.profile_list.grid(row=1, column=0, sticky="ew")
                    
                    ttk.Button(lf, text="New", command=self._create_profile).grid(row=2, column=0, sticky="ew", pady=(6,0))
                    ttk.Button(lf, text="Delete", command=self._delete_profile).grid(row=3, column=0, sticky="ew", pady=4)
                    
                    # Center
                    cf = ttk.Frame(self.root)
                    cf.grid(row=1, column=1, sticky="nsew", padx=6, pady=10)
                    cf.rowconfigure(3, weight=1)
                    
                    Label(cf, text="Type the sentence:").grid(row=0, column=0, sticky="w")
                    self.target = Text(cf, height=4, wrap="word")
                    self.target.grid(row=1, column=0, sticky="ew")
                    self.target.insert("1.0", "The quick brown fox jumps over the lazy dog.")
                    self.target.configure(state="disabled")
                    
                    Label(cf, text="Your input:").grid(row=2, column=0, sticky="w")
                    self.input = Text(cf, height=10, wrap="word")
                    self.input.grid(row=3, column=0, sticky="nsew")
                    
                    ttk.Button(cf, text="Finish", command=self._finish).grid(row=4, column=0, sticky="e", pady=6)
                    
                    # Right
                    rf = ttk.Frame(self.root)
                    rf.grid(row=1, column=2, sticky="nse", padx=(6,10), pady=10)
                    
                    Label(rf, text="Leaderboard").grid(row=0, column=0, sticky="w")
                    self.lb = Text(rf, height=10, width=32)
                    self.lb.grid(row=1, column=0)
                
                def _reload_profiles(self):
                    self.profile_list.delete(0, "end")
                    for n in self.pm.list_profiles():
                        self.profile_list.insert("end", n)
                
                def _create_profile(self):
                    name = simpledialog.askstring("Create Profile", "Name:", parent=self.root)
                    if name and self.pm.create_profile(name.strip()):
                        self._reload_profiles()
                
                def _delete_profile(self):
                    sel = self.profile_list.curselection()
                    if not sel: return
                    name = self.profile_list.get(sel[0])
                    self.pm.delete_profile(name)
                    self._reload_profiles()
                
                def _finish(self):
                    typed = self.input.get("1.0", "end-1c")
                    try:
                        target = self.target.get("1.0","end-1c").strip()
                    except Exception:
                        target = ""
                    
                    if not self.pm.current_profile and self.pm.list_profiles():
                        self.pm.load_profile(self.pm.list_profiles()[0])
                    
                    if not self.pm.current_profile:
                        return
                    
                    words = len(typed.split())
                    wpm = words * 2  # naive
                    correct = sum(1 for a,b in zip(typed, target) if a==b)
                    acc = (correct/max(1,len(target)))*100 if target else 0.0
                    
                    self.pm.update_profile_with_test(
                        self.pm.current_profile, wpm, acc, typed, target, duration=60
                    )
                    self._refresh_lb()
                    messagebox.showinfo("Result", f"WPM: {wpm:.1f}\nAccuracy: {acc:.1f}%")
                
                def _refresh_lb(self):
                    lbs = sorted(self.pm.profiles.items(), key=lambda kv: kv[1].get("best_wpm",0.0), reverse=True)[:10]
                    txt = "\n".join([f"{i+1}. {n} - {p.get('best_wpm',0.0):.1f} WPM" for i,(n,p) in enumerate(lbs)]) or "--"
                    self.lb.delete("1.0","end")
                    self.lb.insert("1.0", txt)
                
                def run(self):
                    self.root.mainloop()
            
            gui = TypingMasterProTk(pm)
            gui.run()
        
        return 0
    
    if args.cmd == "list":
        for n in pm.list_profiles():
            print(n)
        return 0 if pm.list_profiles() else 1
    
    if args.cmd == "create":
        ok = pm.create_profile(args.name)
        print("OK" if ok else "Exists/invalid")
        return 0 if ok else 2
    
    if args.cmd == "delete":
        ok = pm.delete_profile(args.name)
        print("OK" if ok else "Not found")
        return 0 if ok else 3
    
    if args.cmd == "export":
        ok = pm.export_profiles(args.out)
        print("OK" if ok else "Failed")
        return 0 if ok else 4
    
    if args.cmd == "import":
        ok = pm.import_profiles(args.inp, overwrite=args.overwrite)
        print("OK" if ok else "Failed")
        return 0 if ok else 5
    
    if args.cmd == "csv-export":
        ok = pm.export_csv(args.out)
        print("OK" if ok else "Failed")
        return 0 if ok else 6
    
    if args.cmd == "csv-import":
        ok = pm.import_csv(args.inp, overwrite=args.overwrite)
        print("OK" if ok else "Failed")
        return 0 if ok else 7
    
    if args.cmd == "to-v2":
        pm.to_v2_schema()
        print("Upgraded to v2.")
        return 0
    
    if args.cmd == "submit":
        ok, msg = submit_leaderboard_secure(pm, args.url, args.api_key, args.api_secret)
        print(msg)
        return 0 if ok else 8
    
    ap.print_help()
    return 1

# App entrypoint
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        main_cli(["--help"])
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        # CLI mode
        raise SystemExit(main_cli())
    else:
        # GUI mode
        if CTK_AVAILABLE:
            app = TypingMasterPro()
            app.mainloop()
        else:
            print("CustomTkinter not available. Running in CLI mode.")
            raise SystemExit(main_cli(["run-gui"]))