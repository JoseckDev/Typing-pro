# Typing Master Pro — Enhanced Edition
# -------------------------------------------------------------
# New Features Added:
# - Background/cover image support
# - Dynamic theme switching (light/dark/custom)
# - Typing heatmap visualization
# - Achievement system with badges
# - Practice mode for weak keys
# - Detailed statistics dashboard
# - Sound effects for keystrokes
# - Customizable typing tests
# - User profiles with progress tracking
# - Typing challenges and tournaments
# - Multiplayer mode
# - Custom text import
# - Typing games
# - Language support
# - Ergonomics reminders
# - Social sharing
# - AI coach
# - Typing biometrics analysis
# - Daily challenges
# -------------------------------------------------------------
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import time
import random
import json
import os
from datetime import datetime
import math
from collections import defaultdict
import statistics
import threading
import requests
from typing import Dict, List, Tuple, Optional, Any

# PIL for image handling
try:
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except ImportError:
    PILImage = None
    PIL_AVAILABLE = False
    print("Pillow library not found. Background images will be disabled.")

# pygame is used for background music + sound effects
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False
    print("Pygame library not found. Sound will be disabled.")

# For text-to-speech in ergonomics reminders
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("pyttsx3 library not found. Voice reminders will be disabled.")

# For multiplayer mode
try:
    import socket
    SOCKET_AVAILABLE = True
except ImportError:
    SOCKET_AVAILABLE = False
    print("Socket library not available. Multiplayer mode will be disabled.")

# -------------------------------
# CONFIG / CONSTANTS
# -------------------------------
BACKGROUND_MUSIC_FILE = "background.mp3"
VICTORY_SOUND_FILE = "victory.wav"
LEADERBOARD_FILE = "leaderboard.json"
USER_PROFILES_FILE = "user_profiles.json"
ACHIEVEMENTS_FILE = "achievements.json"
COUNTDOWN_DEFAULT = 60
BACKGROUND_IMAGE = "background.jpg"  # Default background image
SOUND_CORRECT = "correct.wav"
SOUND_WRONG = "wrong.wav"
SOUND_COMPLETE = "complete.wav"
# Placeholder for social sharing API
SOCIAL_SHARE_API = "https://api.example.com/share"

# Extended sentence banks with more difficulty levels and languages
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

# Typing games dictionary
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
    {"id": "first_blood", "name": "First Blood",
     "desc": "Complete your first typing test", "icon": "🩸"},
    {"id": "speedster", "name": "Speedster",
     "desc": "Achieve 100+ WPM", "icon": "⚡"},
    {"id": "perfectionist", "name": "Perfectionist",
     "desc": "Achieve 98%+ accuracy", "icon": "🎯"},
    {"id": "marathon", "name": "Marathon Runner",
     "desc": "Complete a 5-minute test", "icon": "🏃"},
    {"id": "nightmare", "name": "Nightmare Mode",
     "desc": "Complete a Nightmare difficulty test", "icon": "👹"},
    {"id": "streak", "name": "Hot Streak",
     "desc": "Complete 5 tests in a row", "icon": "🔥"},
    {"id": "explorer", "name": "Explorer",
     "desc": "Try all difficulty levels", "icon": "🗺️"},
    {"id": "champion", "name": "Champion",
     "desc": "Reach #1 on leaderboard", "icon": "🏆"},
    {"id": "polyglot", "name": "Polyglot",
     "desc": "Complete tests in 3 different languages", "icon": "🌍"},
    {"id": "social", "name": "Social Butterfly",
     "desc": "Share your results on social media", "icon": "🦋"},
    {"id": "daily", "name": "Daily Devotee",
     "desc": "Complete 7 daily challenges", "icon": "📅"},
    {"id": "game_master", "name": "Game Master",
     "desc": "Complete all typing games", "icon": "🎮"},
]

# Daily challenges
DAILY_CHALLENGES = [
    {"id": "speed_run", "name": "Speed Run", "desc": "Achieve 80 WPM in Medium difficulty",
        "type": "speed", "target": 80, "difficulty": "Medium"},
    {"id": "accuracy_check", "name": "Accuracy Check", "desc": "Achieve 95% accuracy in Hard difficulty",
        "type": "accuracy", "target": 95, "difficulty": "Hard"},
    {"id": "endurance_test", "name": "Endurance Test", "desc": "Complete a 3-minute test with 85% accuracy",
        "type": "endurance", "duration": 180, "target": 85},
    {"id": "multilingual", "name": "Multilingual Monday",
        "desc": "Complete tests in 2 different languages", "type": "languages", "target": 2},
    {"id": "blind_typing", "name": "Blind Typing",
        "desc": "Complete a test without looking at the keyboard", "type": "blind", "difficulty": "Medium"},
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

# -------------------------------
# Helper functions
# -------------------------------


def load_leaderboard():
    """Load the leaderboard data."""
    return load_json_file(LEADERBOARD_FILE, [])


def save_leaderboard(data):
    """Save the leaderboard data."""
    save_json_file(LEADERBOARD_FILE, data)


def load_json_file(filename: str, default: Any = None) -> Any:
    """Load JSON file with error handling."""
    if default is None:
        default = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    return default


def save_json_file(filename: str, data: Any) -> None:
    """Save data to JSON file with error handling."""
    try:
        # Convert defaultdict to regular dict for JSON serialization
        if isinstance(data, defaultdict):
            data = dict(data)
        elif isinstance(data, list):
            data = [dict(item) if isinstance(item, defaultdict)
                    else item for item in data]

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"Error saving {filename}: {e}")


def get_daily_challenge() -> Dict:
    """Get today's daily challenge."""
    today = datetime.now().day
    return DAILY_CHALLENGES[today % len(DAILY_CHALLENGES)]


def format_time(seconds: int) -> str:
    """Format seconds as MM:SS."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def calculate_wpm(typed_text: str, time_elapsed: float) -> float:
    """Calculate words per minute."""
    words = len(typed_text.split())
    return (words / time_elapsed) * 60 if time_elapsed > 0 else 0.0


def calculate_accuracy(typed_text: str, target_text: str) -> float:
    """Calculate typing accuracy percentage."""
    correct_chars = sum(1 for a, b in zip(typed_text, target_text) if a == b)
    return (correct_chars / max(1, len(target_text))) * 100.0

# -------------------------------
# Popup Classes
# -------------------------------


class ConfettiPopup(ctk.CTkToplevel):
    """Popup for celebrating #1 ranking."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Congratulations!")
        self.geometry("400x300")
        self.resizable(False, False)

        # Celebration message
        ctk.CTkLabel(self, text="🎉 Congratulations! 🎉",
                     font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="You're #1 on the leaderboard!",
                     font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(self, text="Amazing typing skills!",
                     font=("Arial", 16)).pack(pady=10)

        # Share button
        share_btn = ctk.CTkButton(self, text="Share Achievement",
                                  command=lambda: master.share_achievement("champion"))
        share_btn.pack(pady=10)

        # Close button
        ctk.CTkButton(self, text="Awesome!",
                      command=self.destroy).pack(pady=10)


class MedalPopup(ctk.CTkToplevel):
    """Popup for earning a medal."""

    def __init__(self, master, place: int, difficulty: str, wpm: float):
        super().__init__(master)
        self.title("Medal Earned!")
        self.geometry("400x300")
        self.resizable(False, False)

        # Medal emoji based on place
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        medal = medals.get(place, "🏅")

        # Celebration message
        ctk.CTkLabel(self, text=f"{medal} Medal Earned! {medal}",
                     font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"You placed #{place} in {difficulty} difficulty!",
                     font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self, text=f"Speed: {wpm:.1f} WPM",
                     font=("Arial", 16)).pack(pady=5)

        # Share button
        share_btn = ctk.CTkButton(self, text="Share Achievement",
                                  command=lambda: master.share_achievement(f"medal_{place}"))
        share_btn.pack(pady=10)

        # Close button
        ctk.CTkButton(self, text="Cool!",
                      command=self.destroy).pack(pady=10)


class DailyChallengePopup(ctk.CTkToplevel):
    """Popup for daily challenge completion."""

    def __init__(self, master, challenge: Dict, reward: str):
        super().__init__(master)
        self.title("Daily Challenge Complete!")
        self.geometry("400x300")
        self.resizable(False, False)

        # Celebration message
        ctk.CTkLabel(self, text="🌟 Daily Challenge Complete! 🌟",
                     font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=challenge["name"],
                     font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(self, text=f"Reward: {reward}",
                     font=("Arial", 16)).pack(pady=5)

        # Share button
        share_btn = ctk.CTkButton(self, text="Share Achievement",
                                  command=lambda: master.share_achievement("daily_challenge"))
        share_btn.pack(pady=10)

        # Close button
        ctk.CTkButton(self, text="Awesome!",
                      command=self.destroy).pack(pady=10)


class ErgonomicsReminder(ctk.CTkToplevel):
    """Popup for ergonomics reminders."""

    def __init__(self, master, tip: str):
        super().__init__(master)
        self.title("Ergonomics Reminder")
        self.geometry("400x200")
        self.resizable(False, False)

        # Reminder message
        ctk.CTkLabel(self, text="💡 Ergonomics Tip",
                     font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(self, text=tip,
                     font=("Arial", 16), wraplength=350).pack(pady=10)

        # Voice option if available
        if TTS_AVAILABLE:
            def speak_tip():
                try:
                    engine = pyttsx3.init()
                    engine.say(tip)
                    engine.runAndWait()
                except Exception as e:
                    print(f"Text-to-speech error: {e}")

            ctk.CTkButton(self, text="🔊 Speak", command=speak_tip).pack(pady=5)

        # Close button
        ctk.CTkButton(self, text="Got it!",
                      command=self.destroy).pack(pady=10)

# -------------------------------
# Typing Heatmap Visualization
# -------------------------------


class TypingHeatmap(ctk.CTkToplevel):
    """Visualize typing accuracy heatmap on a keyboard layout."""

    def __init__(self, master, accuracy_data: Dict[str, float]):
        super().__init__(master)
        self.title("Typing Heatmap")
        self.geometry("800x400")
        self.resizable(False, False)

        # Keyboard layout (simplified QWERTY)
        self.keyboard_layout = [
            "`~ 1! 2@ 3# 4$ 5% 6^ 7& 8* 9( 0) -_ =+",
            "qQ wW eE rR tT yY uU iI oO pP [{ ]}",
            "aA sS dD fF gG hH jJ kK lL ;: '\" \\|",
            "zZ xX cC vV bB nN mM ,< .> /?",
        ]

        # Canvas for keyboard
        self.canvas = tk.Canvas(
            self, width=780, height=350, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Draw keyboard with heatmap colors
        self.draw_heatmap(accuracy_data)

        # Legend
        legend_frame = ctk.CTkFrame(self)
        legend_frame.pack(pady=5)
        ctk.CTkLabel(legend_frame, text="Accuracy: ").pack(side="left")
        colors = ["#ff0000", "#ff9900", "#ffff00", "#00ff00", "#00cc00"]
        labels = ["<50%", "50-70%", "70-85%", "85-95%", ">95%"]
        for color, label in zip(colors, labels):
            color_box = tk.Canvas(legend_frame, width=20,
                                  height=20, bg=color, highlightthickness=0)
            color_box.pack(side="left", padx=2)
            ctk.CTkLabel(legend_frame, text=label).pack(
                side="left", padx=(0, 10))

    def draw_heatmap(self, accuracy_data: Dict[str, float]) -> None:
        """Draw keyboard with heatmap colors based on accuracy data."""
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
                    x_offset + key_width, y_start + row_idx *
                    (key_height + 10) + key_height,
                    fill=color, outline="#555", width=1
                )

                # Draw key label
                self.canvas.create_text(
                    x_offset + key_width // 2, y_start + row_idx *
                    (key_height + 10) + key_height // 2,
                    text=key[0].upper(), font=("Arial", 16, "bold"), fill="white"
                )

                x_offset += key_width + 5

# -------------------------------
# User Profile System
# -------------------------------


class UserProfile:
    """Manage user profiles and progress tracking."""

    def __init__(self):
        self.profiles = load_json_file(USER_PROFILES_FILE, {})
        self.current_profile = None

    def create_profile(self, name: str) -> bool:
        """Create a new user profile."""
        if name in self.profiles:
            return False

        self.profiles[name] = {
            "name": name,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tests_completed": 0,
            "total_words": 0,
            "total_time": 0,
            "best_wpm": 0,
            "best_accuracy": 0,
            "achievements": [],
            "weak_keys": {},
            "key_accuracy": {},
            "history": [],
            "languages_tried": set(),
            "games_completed": [],
            "daily_challenges": 0,
            "last_daily_challenge": None,
            "ergonomics_reminders": 0,
            "last_ergonomics_reminder": None,
            "typing_biometrics": {
                "avg_keypress_duration": 0,
                "rhythm_consistency": 0,
                "error_patterns": {}
            }
        }

        save_json_file(USER_PROFILES_FILE, self.profiles)
        return True

    def load_profile(self, name: str) -> bool:
        """Load a user profile."""
        if name in self.profiles:
            self.current_profile = name
            return True
        return False

    def update_profile(self, wpm: float, accuracy: float, difficulty: str,
                       typed_text: str, target_text: str, language: str = "English") -> None:
        """Update current profile with test results."""
        if not self.current_profile:
            return

        profile = self.profiles[self.current_profile]
        profile["tests_completed"] += 1
        profile["total_words"] += len(typed_text.split())
        profile["total_time"] += COUNTDOWN_DEFAULT

        if wpm > profile["best_wpm"]:
            profile["best_wpm"] = wpm
        if accuracy > profile["best_accuracy"]:
            profile["best_accuracy"] = accuracy

        # Update language stats
        if "languages_tried" not in profile:
            profile["languages_tried"] = set()
        profile["languages_tried"].add(language)

        # Update key accuracy stats
        for i, (typed_char, target_char) in enumerate(zip(typed_text, target_text)):
            if i < len(typed_text):
                char = target_char.lower()

                # Initialize key_accuracy if needed
                if "key_accuracy" not in profile:
                    profile["key_accuracy"] = {}
                if char not in profile["key_accuracy"]:
                    profile["key_accuracy"][char] = {"correct": 0, "total": 0}

                profile["key_accuracy"][char]["total"] += 1
                if typed_char == target_char:
                    profile["key_accuracy"][char]["correct"] += 1
                else:
                    # Update weak keys
                    if "weak_keys" not in profile:
                        profile["weak_keys"] = {}
                    profile["weak_keys"][char] = profile["weak_keys"].get(
                        char, 0) + 1

                    # Update error patterns
                    if "typing_biometrics" not in profile:
                        profile["typing_biometrics"] = {"error_patterns": {}}
                    if "error_patterns" not in profile["typing_biometrics"]:
                        profile["typing_biometrics"]["error_patterns"] = {}

                    error_key = f"{char}->{typed_char.lower()}"
                    profile["typing_biometrics"]["error_patterns"][error_key] = \
                        profile["typing_biometrics"]["error_patterns"].get(
                            error_key, 0) + 1

        # Add to history
        if "history" not in profile:
            profile["history"] = []
        profile["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "wpm": wpm,
            "accuracy": accuracy,
            "difficulty": difficulty,
            "language": language
        })

        # Keep only last 50 history entries
        if len(profile["history"]) > 50:
            profile["history"] = profile["history"][-50:]

        save_json_file(USER_PROFILES_FILE, self.profiles)

    def get_weak_keys(self, count: int = 5) -> List[str]:
        """Get the keys with most errors."""
        if not self.current_profile:
            return []

        profile = self.profiles[self.current_profile]
        weak_keys = profile.get("weak_keys", {})
        sorted_weak_keys = sorted(
            weak_keys.items(), key=lambda x: x[1], reverse=True)
        return [key for key, _ in sorted_weak_keys[:count]]

    def get_key_accuracy(self) -> Dict[str, float]:
        """Calculate accuracy percentage for each key."""
        if not self.current_profile:
            return {}

        profile = self.profiles[self.current_profile]
        key_accuracy = profile.get("key_accuracy", {})
        accuracy_data = {}

        for char, stats in key_accuracy.items():
            if stats["total"] > 0:
                accuracy_data[char] = (stats["correct"] / stats["total"]) * 100

        return accuracy_data

    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement for the current profile."""
        if not self.current_profile:
            return False

        profile = self.profiles[self.current_profile]
        if "achievements" not in profile:
            profile["achievements"] = []

        if achievement_id not in profile["achievements"]:
            profile["achievements"].append(achievement_id)
            save_json_file(USER_PROFILES_FILE, self.profiles)
            return True
        return False

    def complete_game(self, game_id: str) -> None:
        """Mark a game as completed for the current profile."""
        if not self.current_profile:
            return

        profile = self.profiles[self.current_profile]
        if "games_completed" not in profile:
            profile["games_completed"] = []

        if game_id not in profile["games_completed"]:
            profile["games_completed"].append(game_id)
            save_json_file(USER_PROFILES_FILE, self.profiles)

    def complete_daily_challenge(self) -> None:
        """Mark a daily challenge as completed."""
        if not self.current_profile:
            return

        profile = self.profiles[self.current_profile]
        today = datetime.now().strftime("%Y-%m-%d")

        # Check if already completed today
        if profile.get("last_daily_challenge") == today:
            return

        profile["daily_challenges"] = profile.get("daily_challenges", 0) + 1
        profile["last_daily_challenge"] = today
        save_json_file(USER_PROFILES_FILE, self.profiles)

    def show_ergonomics_reminder(self) -> bool:
        """Check if it's time to show an ergonomics reminder."""
        if not self.current_profile:
            return False

        profile = self.profiles[self.current_profile]
        now = datetime.now()
        last_reminder = profile.get("last_ergonomics_reminder")

        # Show reminder every 20 minutes
        if last_reminder:
            last_time = datetime.strptime(last_reminder, "%Y-%m-%d %H:%M:%S")
            if (now - last_time).total_seconds() < 1200:  # 20 minutes
                return False

        profile["last_ergonomics_reminder"] = now.strftime("%Y-%m-%d %H:%M:%S")
        profile["ergonomics_reminders"] = profile.get(
            "ergonomics_reminders", 0) + 1
        save_json_file(USER_PROFILES_FILE, self.profiles)
        return True

    def get_languages_tried(self) -> int:
        """Get the number of languages tried."""
        if not self.current_profile:
            return 0

        profile = self.profiles[self.current_profile]
        languages = profile.get("languages_tried", set())
        return len(languages)

    def get_ai_coach_tip(self, area: str) -> str:
        """Get an AI coach tip for a specific area."""
        if area in AI_COACH_TIPS:
            return random.choice(AI_COACH_TIPS[area])
        return "Keep practicing to improve your typing skills!"

# -------------------------------
# Achievement System
# -------------------------------


class AchievementSystem:
    """Manage achievements and notifications."""

    def __init__(self):
        self.achievements = {a["id"]: a for a in ACHIEVEMENTS}
        self.unlocked = load_json_file(ACHIEVEMENTS_FILE, [])

    def check_achievements(self, profile: Dict, wpm: float, accuracy: float,
                           difficulty: str, language: str = "English") -> List[str]:
        """Check if any achievements were unlocked."""
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
                dates = [datetime.strptime(h["date"], "%Y-%m-%d %H:%M")
                         for h in profile["history"][-5:]]
                consecutive = all(
                    (dates[i] - dates[i-1]).total_seconds() < 86400 for i in range(1, 5))
                if consecutive:
                    newly_unlocked.append("streak")

        # Explorer
        difficulties_completed = set(h["difficulty"]
                                     for h in profile["history"])
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
        """Show a popup for an unlocked achievement."""
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return

        popup = ctk.CTkToplevel(master)
        popup.title("Achievement Unlocked!")
        popup.geometry("400x250")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Achievement Unlocked!",
                     font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(popup, text=f"{achievement['icon']} {achievement['name']}", font=(
            "Arial", 24, "bold")).pack(pady=5)
        ctk.CTkLabel(popup, text=achievement["desc"], font=(
            "Arial", 14)).pack(pady=5)

        # Share button
        share_btn = ctk.CTkButton(popup, text="Share Achievement",
                                  command=lambda: master.share_achievement(achievement_id))
        share_btn.pack(pady=5)

        ctk.CTkButton(popup, text="Awesome!",
                      command=popup.destroy).pack(pady=10)

# -------------------------------
# Practice Mode for Weak Keys
# -------------------------------


class PracticeMode(ctk.CTkToplevel):
    """Practice mode focusing on weak keys."""

    def __init__(self, master, weak_keys: List[str], user_profile: UserProfile):
        super().__init__(master)
        self.title("Practice Mode - Weak Keys")
        self.geometry("800x500")
        self.resizable(False, False)

        self.weak_keys = weak_keys
        self.user_profile = user_profile
        self.current_sentence = ""
        self.start_time = None
        self.timer_running = False

        # Build UI
        self._build_ui()
        self.generate_practice_sentence()

    def _build_ui(self) -> None:
        """Build the main application UI with responsive design."""
        # Main container with transparent background
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # Configure grid weights for responsive design
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Header
        self._build_header()
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(header, text="Practice Your Weak Keys",
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text=f"Focus on: {', '.join(self.weak_keys)}", font=(
            "Arial", 16)).pack()

        # Content
        self._build_content()
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=16, pady=8)

        # Footer
        self._build_footer()

        # Bind resize event for responsive design
        self.bind("<Configure>", self._on_window_resize)

        # Initial font size adjustment
        self.after(100, self._adjust_font_sizes)

        # Sentence label
        self.sentence_label = ctk.CTkLabel(
            content, text="", wraplength=700, font=("Arial", 20))
        self.sentence_label.pack(pady=(18, 10))

        # Typing area
        self.textbox = tk.Text(content, height=4, width=90,
                               font=("Consolas", 16), wrap="word")
        self.textbox.pack(pady=(4, 8))
        self.textbox.bind("<KeyRelease>", self._on_typing)

        # Tags for coloring
        self.textbox.tag_configure("correct", foreground="lime")
        self.textbox.tag_configure("wrong", foreground="red")
        self.textbox.tag_configure("pending", foreground="gray")

        # Stats
        self.stats_label = ctk.CTkLabel(
            content, text="WPM: 0.00 | Accuracy: 0.00%", font=("Arial", 16))
        self.stats_label.pack(pady=6)

        # AI Coach tip
        self.coach_label = ctk.CTkLabel(
            content, text="", font=("Arial", 14), wraplength=700)
        self.coach_label.pack(pady=6)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=16, pady=(8, 16))

        self.start_btn = ctk.CTkButton(
            button_frame, text="Start Practice", command=self.start_practice)
        self.start_btn.grid(row=0, column=0, padx=10, sticky="nsew")

        self.new_btn = ctk.CTkButton(
            button_frame, text="New Sentence", command=self.generate_practice_sentence)
        self.new_btn.grid(row=0, column=1, padx=10, sticky="nsew")

        self.close_btn = ctk.CTkButton(
            button_frame, text="Close", command=self.destroy)
        self.close_btn.grid(row=0, column=2, padx=10, sticky="nsew")

    def generate_practice_sentence(self) -> None:
        """Generate a practice sentence focusing on weak keys."""
        # Create a sentence with repeated weak keys
        words = []
        for key in [k for k in self.weak_keys if str(k).isalpha()]:
            # Create simple words with the weak key
            words.append(key * 3)  # e.g., "aaa"
            words.append(key + "a")  # e.g., "aa"
            words.append("a" + key)  # e.g., "aa"
            words.append(key + key + "a")  # e.g., "aaa"

        # Add some common words to make it more natural
        common_words = ["the", "and", "for", "are",
                        "but", "not", "you", "all", "can", "had"]
        words.extend(random.choices(common_words, k=5))

        # Shuffle and join
        random.shuffle(words)
        self.current_sentence = " ".join(words)
        self.sentence_label.configure(text=self.current_sentence)
        self.reset_typing_area()

    def reset_typing_area(self) -> None:
        """Reset the typing area."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self._apply_pending_tags()
        self.stats_label.configure(text="WPM: 0.00 | Accuracy: 0.00%")
        self.coach_label.configure(text="")
        self.timer_running = False

    def start_practice(self) -> None:
        """Start the practice session."""
        self.reset_typing_area()
        self.start_time = time.time()
        self.timer_running = True

        # Show AI coach tip
        if self.user_profile.current_profile:
            tip = self.user_profile.get_ai_coach_tip("accuracy")
            self.coach_label.configure(text=f"💡 AI Coach: {tip}")

    def _on_typing(self, event=None) -> None:
        """Handle typing events."""
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
            correct_chars = sum(1 for a, b in zip(
                typed, self.current_sentence) if a == b)
            accuracy = (correct_chars /
                        max(1, len(self.current_sentence))) * 100.0

            self.stats_label.configure(
                text=f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

    def _apply_pending_tags(self) -> None:
        """Apply pending tags to all characters."""
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        self.textbox.tag_remove("pending", "1.0", "end")

        for i, _ in enumerate(self.current_sentence):
            self.textbox.tag_add("pending", f"1.{i}", f"1.{i+1}")

# -------------------------------
# Typing Games
# -------------------------------


class TypeDefenseGame(ctk.CTkToplevel):
    """Type Defense mini-game."""

    def __init__(self, master, difficulty: str = "Medium"):
        super().__init__(master)
        self.title("Type Defense - Typing Game")
        self.geometry("900x600")
        self.resizable(False, False)

        self.master = master
        self.difficulty = difficulty
        self.words_defeated = 0
        self.lives = 3
        self.score = 0
        self.game_duration = GAMES["Type Defense"]["duration"]
        self.time_left = self.game_duration
        self.game_running = False
        self.current_word = ""
        self.enemy_position = 0
        self.enemy_speed = 2  # Pixels per update
        self.difficulty_scaling = GAMES["Type Defense"]["difficulty_scaling"]

        # Build UI
        self._build_ui()
        self._start_game()

    def _build_ui(self) -> None:
        """Build the game UI."""
        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))

        ctk.CTkLabel(header, text="Type Defense - Type words to defeat enemies!",
                     font=("Arial", 20, "bold")).pack(pady=10)

        # Game stats
        stats_frame = ctk.CTkFrame(header)
        stats_frame.pack(fill="x", padx=20)

        self.score_label = ctk.CTkLabel(stats_frame, text=f"Score: {self.score}",
                                        font=("Arial", 16))
        self.score_label.pack(side="left", padx=20)

        self.words_label = ctk.CTkLabel(stats_frame, text=f"Words: {self.words_defeated}",
                                        font=("Arial", 16))
        self.words_label.pack(side="left", padx=20)

        self.lives_label = ctk.CTkLabel(stats_frame, text=f"Lives: {self.lives}",
                                        font=("Arial", 16))
        self.lives_label.pack(side="left", padx=20)

        self.timer_label = ctk.CTkLabel(stats_frame, text=f"Time: {format_time(self.time_left)}",
                                        font=("Arial", 16))
        self.timer_label.pack(side="left", padx=20)

        # Game area
        self.game_canvas = tk.Canvas(self, width=850, height=400, bg="#1a1a1a")
        self.game_canvas.pack(pady=10)

        # Draw defense line
        self.defense_line_y = 350
        self.game_canvas.create_line(0, self.defense_line_y, 850, self.defense_line_y,
                                     fill="green", width=3, tags="defense_line")

        # Typing area
        typing_frame = ctk.CTkFrame(self)
        typing_frame.pack(fill="x", padx=16, pady=8)

        self.word_label = ctk.CTkLabel(
            typing_frame, text="", font=("Arial", 24, "bold"))
        self.word_label.pack(pady=5)

        self.textbox = tk.Text(typing_frame, height=2, width=80,
                               font=("Consolas", 18), wrap="word")
        self.textbox.pack(pady=5)
        self.textbox.bind("<KeyRelease>", self._on_typing)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=16, pady=(8, 16))

        self.pause_btn = ctk.CTkButton(
            button_frame, text="Pause", command=self._toggle_pause)
        self.pause_btn.grid(row=0, column=0, padx=10, sticky="nsew")

        self.quit_btn = ctk.CTkButton(
            button_frame, text="Quit Game", command=self._quit_game)
        self.quit_btn.grid(row=0, column=1, padx=10, sticky="nsew")

    def _start_game(self) -> None:
        """Start the game."""
        self.game_running = True
        self._spawn_enemy()
        self._game_loop()
        self._timer_loop()

    def _spawn_enemy(self) -> None:
        """Spawn a new enemy with a word."""
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
        """Main game loop for enemy movement."""
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
        """Timer loop for game duration."""
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
        """Handle typing events."""
        typed = self.textbox.get("1.0", "end-1c")

        # Check if typed word matches current word
        if typed == self.current_word:
            # Word defeated!
            self._defeat_enemy()

    def _defeat_enemy(self) -> None:
        """Handle defeating an enemy."""
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
        if self.master.sound_enabled and SOUND_CORRECT in self.master.sounds:
            self.master.sounds[SOUND_CORRECT].play()

        # Increase difficulty if enabled
        if self.difficulty_scaling and self.words_defeated % 5 == 0:
            self.enemy_speed += 0.5

        # Spawn new enemy
        self._spawn_enemy()

    def _enemy_reached_line(self) -> None:
        """Handle enemy reaching the defense line."""
        self.lives -= 1
        self.lives_label.configure(text=f"Lives: {self.lives}")

        # Remove enemy from canvas
        if hasattr(self, 'enemy_ids'):
            for enemy_id in self.enemy_ids:
                self.game_canvas.delete(enemy_id)

        # Play sound if available
        if self.master.sound_enabled and SOUND_WRONG in self.master.sounds:
            self.master.sounds[SOUND_WRONG].play()

        # Check if game over
        if self.lives <= 0:
            self._end_game()
            return

        # Spawn new enemy
        self._spawn_enemy()

    def _toggle_pause(self) -> None:
        """Toggle game pause state."""
        self.game_running = not self.game_running

        if self.game_running:
            self.pause_btn.configure(text="Pause")
            self._game_loop()
            self._timer_loop()
        else:
            self.pause_btn.configure(text="Resume")

    def _quit_game(self) -> None:
        """Quit the game early."""
        self.game_running = False
        self._end_game()

    def _end_game(self) -> None:
        """End the game and show results."""
        self.game_running = False

        # Play completion sound if available
        if self.master.sound_enabled and SOUND_COMPLETE in self.master.sounds:
            self.master.sounds[SOUND_COMPLETE].play()

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


# Add this new class after the TypeDefenseGame class
class MemoryMasterGame(ctk.CTkToplevel):
    """Memory Master mini-game - trains and tests brain memory."""

    def __init__(self, master, difficulty: str = "Medium"):
        super().__init__(master)
        self.title("Memory Master - Typing Game")

        # Make the window responsive
        self.update_idletasks()
        width = max(900, int(self.winfo_screenwidth() * 0.8))
        height = max(700, int(self.winfo_screenheight() * 0.8))
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(True, True)

        # Configure grid weights for responsive design
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.master = master
        self.difficulty = difficulty
        self.game_duration = GAMES["Memory Master"]["duration"]
        self.time_left = self.game_duration
        self.game_running = False
        self.game_phase = "memorize"  # "memorize" or "recall"
        self.current_text = ""
        self.memorize_time = 0
        self.recall_start_time = 0
        self.score = 0
        self.accuracy = 0

        # Build UI
        self._build_ui()
        self._start_game()

    def _build_ui(self) -> None:
        """Build the game UI with responsive design."""
        # Main container with responsive grid
        main_container = ctk.CTkFrame(self)
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(main_container)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(header, text="Memory Master - Train Your Brain Memory",
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text="Memorize the text, then type it from memory!",
                     font=("Arial", 16)).pack(pady=5)

        # Game stats
        stats_frame = ctk.CTkFrame(header)
        stats_frame.pack(fill="x", padx=20, pady=5)

        self.score_label = ctk.CTkLabel(stats_frame, text=f"Score: {self.score}",
                                        font=("Arial", 16))
        self.score_label.pack(side="left", padx=20)

        self.accuracy_label = ctk.CTkLabel(stats_frame, text=f"Accuracy: {self.accuracy:.1f}%",
                                           font=("Arial", 16))
        self.accuracy_label.pack(side="left", padx=20)

        self.timer_label = ctk.CTkLabel(stats_frame, text=f"Time: {format_time(self.time_left)}",
                                        font=("Arial", 16))
        self.timer_label.pack(side="left", padx=20)

        self.phase_label = ctk.CTkLabel(stats_frame, text=f"Phase: Memorize",
                                        font=("Arial", 16, "bold"))
        self.phase_label.pack(side="right", padx=20)

        # Game area with responsive sizing
        game_area = ctk.CTkFrame(main_container)
        game_area.grid(row=1, column=0, sticky="nsew")
        game_area.grid_rowconfigure(0, weight=1)
        game_area.grid_columnconfigure(0, weight=1)

        # Text display area with responsive font sizing
        self.text_frame = ctk.CTkFrame(game_area)
        self.text_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        # Create a scrollable text widget for displaying text
        self.text_display = tk.Text(
            self.text_frame,
            wrap="word",
            font=("Arial", 16),  # Base font size, will be adjusted dynamically
            state="disabled",
            bg="#2b2b2b",
            fg="white",
            padx=10,
            pady=10
        )
        self.text_display.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for text display
        scrollbar = ctk.CTkScrollbar(
            self.text_frame, command=self.text_display.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_display.configure(yscrollcommand=scrollbar.set)

        # Typing area (initially hidden)
        self.typing_frame = ctk.CTkFrame(game_area)
        self.typing_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.typing_frame.grid_remove()  # Hide initially

        self.typing_label = ctk.CTkLabel(self.typing_frame, text="Type the text from memory:",
                                         font=("Arial", 16))
        self.typing_label.pack(pady=5)

        self.textbox = tk.Text(
            self.typing_frame,
            height=8,
            font=("Consolas", 16),
            wrap="word"
        )
        self.textbox.pack(fill="x", padx=10, pady=5)
        self.textbox.bind("<KeyRelease>", self._on_typing)

        # Tags for coloring
        self.textbox.tag_configure("correct", foreground="lime")
        self.textbox.tag_configure("wrong", foreground="red")

        # Progress bar
        progress_frame = ctk.CTkFrame(main_container)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.progress = ctk.CTkProgressBar(progress_frame, height=10)
        self.progress.pack(fill="x", padx=20)
        self.progress.set(0)

        # Buttons
        button_frame = ctk.CTkFrame(main_container)
        button_frame.grid(row=3, column=0, sticky="ew", pady=10)

        self.pause_btn = ctk.CTkButton(
            button_frame, text="Pause", command=self._toggle_pause)
        self.pause_btn.pack(side="left", padx=20)

        self.skip_memorize_btn = ctk.CTkButton(button_frame, text="Skip to Recall",
                                               command=self._skip_to_recall, state="normal")
        self.skip_memorize_btn.pack(side="left", padx=20)

        self.quit_btn = ctk.CTkButton(
            button_frame, text="Quit Game", command=self._quit_game)
        self.quit_btn.pack(side="right", padx=20)

        # Adjust font sizes based on window size
        self._adjust_font_sizes()
        self.bind("<Configure>", self._on_window_resize)


# Add this new method to TypingMasterPro class
def _adjust_font_sizes(self) -> None:
    """Adjust font sizes based on window size for responsive design."""
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
                getattr(self, button_name).configure(
                    font=("Arial", button_font_size))

    except Exception as e:
        print(f"Error adjusting font sizes: {e}")

   # Add this new method to TypingMasterPro class
    def _on_window_resize(self, event) -> None:
        """Handle window resize events for responsive design."""
        if event.widget == self:
            # Debounce resize events
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(200, self._adjust_font_sizes)

    def _start_game(self) -> None:
        """Start the game."""
        self.game_running = True
        self._load_memory_text()
        self._show_memorize_phase()
        self._timer_loop()

    def _load_memory_text(self) -> None:
        """Load text for memory challenge based on difficulty."""
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
        """Show the memorize phase of the game."""
        self.game_phase = "memorize"
        self.phase_label.configure(text="Phase: Memorize")
        self.memorize_time = self.game_duration // 2  # Half the time for memorizing

        # Show text display, hide typing area
        self.text_frame.grid(sticky="nsew")
        self.typing_frame.grid_remove()

        # Enable skip button
        self.skip_memorize_btn.configure(state="normal")

    def _show_recall_phase(self) -> None:
        """Show the recall phase of the game."""
        self.game_phase = "recall"
        self.phase_label.configure(text="Phase: Recall")
        self.recall_start_time = time.time()

        # Hide text display, show typing area
        self.text_frame.grid_remove()
        self.typing_frame.grid(sticky="nsew")

        # Clear typing area
        self.textbox.delete("1.0", "end")

        # Focus on typing area
        self.textbox.focus_set()

        # Disable skip button
        self.skip_memorize_btn.configure(state="disabled")

    def _skip_to_recall(self) -> None:
        """Skip to the recall phase."""
        if self.game_phase == "memorize":
            self._show_recall_phase()

    def _timer_loop(self) -> None:
        """Timer loop for game duration."""
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
        """Handle typing events."""
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
        correct_chars = sum(1 for a, b in zip(
            typed, self.current_text) if a == b)
        self.accuracy = (
            correct_chars / max(1, len(self.current_text))) * 100.0
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
        """Toggle game pause state."""
        self.game_running = not self.game_running

        if self.game_running:
            self.pause_btn.configure(text="Pause")
            if self.game_phase == "recall":
                self.recall_start_time = time.time() - (len(self.textbox.get("1.0", "end-1c")) / 10)
            self._timer_loop()
        else:
            self.pause_btn.configure(text="Resume")

    def _quit_game(self) -> None:
        """Quit the game early."""
        self.game_running = False
        self._end_game()

    def _end_game(self) -> None:
        """End the game and show results."""
        self.game_running = False

        # Play completion sound if available
        if self.master.sound_enabled and SOUND_COMPLETE in self.master.sounds:
            self.master.sounds[SOUND_COMPLETE].play()

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


class HumanitarianChallenge(ctk.CTkToplevel):
    """Humanitarian typing challenges that make a real-world difference."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Type for Humanity")
        self.geometry("700x600")
        self.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(header, text="Type for a Cause",
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text="Your typing can make a difference in the world!",
                     font=("Arial", 16)).pack(pady=5)

        # Challenges
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=16, pady=8)

        challenges = [
            {
                "title": "Trees for Typing",
                "desc": "For every 1000 words you type correctly, we'll plant a tree through our partner organizations.",
                "icon": "🌳",
                "progress": 0,
                "goal": 1000000,  # 1 million words = 1000 trees
                "partner": "One Tree Planted"
            },
            {
                "title": "Meals for Words",
                "desc": "Every 500 words typed correctly provides a meal to someone in need.",
                "icon": "🍲",
                "progress": 0,
                "goal": 500000,  # 500,000 words = 1000 meals
                "partner": "World Food Programme"
            },
            {
                "title": "Books for Knowledge",
                "desc": "For every 2000 words, we donate a book to underprivileged schools.",
                "icon": "📚",
                "progress": 0,
                "goal": 1000000,  # 1 million words = 500 books
                "partner": "Room to Read"
            }
        ]

        # Display challenges
        for challenge in challenges:
            self._display_challenge(content, challenge)

        # Stats
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=16, pady=(8, 16))

        total_words = 0
        total_impact = 0
        # In a real implementation, these would be fetched from a server
        ctk.CTkLabel(stats_frame, text=f"Global Community Impact: {total_words:,} words typed",
                     font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(stats_frame, text=f"Total Contributions: {total_impact:,} lives touched",
                     font=("Arial", 16)).pack(pady=5)

        # Participate button
        ctk.CTkButton(self, text="Start Typing for a Cause",
                      command=self.start_challenge).pack(pady=10)

    def _display_challenge(self, parent, challenge):
        """Display a single humanitarian challenge."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)

        # Icon and title
        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header_frame, text=challenge["icon"], font=(
            "Arial", 24)).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text=challenge["title"], font=(
            "Arial", 18, "bold")).pack(side="left", padx=5)

        # Description
        ctk.CTkLabel(frame, text=challenge["desc"], font=("Arial", 14),
                     wraplength=600).pack(padx=10, pady=5)

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

    def start_challenge(self):
        """Start a humanitarian typing challenge."""
        # In a real implementation, this would start a special typing session
        # that tracks progress toward the humanitarian goal
        messagebox.showinfo("Type for Humanity",
                            "Thank you for making a difference! Your typing will now contribute to the cause.")
        self.destroy()


class InspirationalStories(ctk.CTkToplevel):
    """Showcase stories of people transformed by typing skills."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Inspirational Stories")
        self.geometry("800x600")
        self.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(header, text="Real People, Real Transformations",
                     font=("Arial", 24, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text="Discover how typing skills changed lives around the world",
                     font=("Arial", 16)).pack(pady=5)

        # Stories notebook
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=8)

        # Add story categories
        self._add_stories("Overcoming Adversity", [
            {
                "name": "Maria's Journey",
                "location": "Brazil",
                "story": "Born with limited mobility in her hands, Maria struggled with basic tasks. "
                         "After discovering adaptive typing techniques, she now works as a freelance "
                         "transcriptionist, earning 3x the average income in her community.",
                "quote": "Typing gave me wings when I thought I was grounded forever.",
                "achievement": "Increased income by 300%"
            },
            {
                "name": "Ahmed's Second Chance",
                "location": "Egypt",
                "story": "After losing his job in the tourism industry, Ahmed had to reinvent himself. "
                         "He dedicated 3 months to mastering typing and now runs a successful digital "
                         "marketing agency from his home.",
                "quote": "When one door closed, typing opened another I never knew existed.",
                "achievement": "Created 12 new jobs in his community"
            }
        ])

        self._add_stories("Career Transformations", [
            {
                "name": "Priya's Tech Dream",
                "location": "India",
                "story": "From a rural village with limited computer access, Priya taught herself typing "
                         "using a mobile app. Today, she's a senior software engineer at a global tech company.",
                "quote": "Every keystroke was a step toward a future I once only dreamed of.",
                "achievement": "From village to Silicon Valley in 5 years"
            },
            {
                "name": "James' Comeback",
                "location": "USA",
                "story": "After serving in the military, James struggled to transition to civilian life. "
                         "A typing course at a community college led him to a career in data analysis.",
                "quote": "Learning to type was learning to speak a new language of opportunity.",
                "achievement": "Now mentors other veterans in tech skills"
            }
        ])

        self._add_stories("Community Heroes", [
            {
                "name": "The Digital Elder",
                "location": "Japan",
                "story": "At 78, Kenji learned typing to preserve local history. He has now transcribed "
                         "over 10,000 pages of historical documents, creating a digital archive for future generations.",
                "quote": "Age is just a number when you have a keyboard and a purpose.",
                "achievement": "Preserved 200 years of local history"
            },
            {
                "name": "The Classroom Champion",
                "location": "Kenya",
                "story": "Teacher Amina started a typing club for girls in her village. "
                         "Three years later, 50 of her students have received scholarships to study computer science.",
                "quote": "I didn't just teach typing; I opened doors to the future.",
                "achievement": "50+ scholarships secured for her students"
            }
        ])

        # Contribute button
        ctk.CTkButton(self, text="Share Your Story",
                      command=self.share_story).pack(pady=10)

    def _add_stories(self, tab_name, stories):
        """Add a tab with stories."""
        tab = self.notebook.add(tab_name)

        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for story in stories:
            self._display_story(scroll_frame, story)

    def _display_story(self, parent, story):
        """Display a single story."""
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
        ctk.CTkLabel(frame, text=story["story"], font=("Arial", 14),
                     wraplength=700, justify="left").pack(padx=10, pady=5)

        # Quote
        quote_frame = ctk.CTkFrame(frame, fg_color=("gray90", "gray20"))
        quote_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(quote_frame, text=f'"{story["quote"]}"',
                     font=("Arial", 16, "italic")).pack(padx=10, pady=5)

        # Achievement
        ctk.CTkLabel(frame, text=f"Achievement: {story['achievement']}",
                     font=("Arial", 14, "bold"), text_color="#4CAF50").pack(padx=10, pady=5)

    def share_story(self):
        """Open dialog to share a story."""
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
        ctk.CTkLabel(form_frame, text="Your Name:").pack(
            anchor="w", padx=5, pady=(5, 0))
        name_entry = ctk.CTkEntry(form_frame, width=400)
        name_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Location
        ctk.CTkLabel(form_frame, text="Location:").pack(
            anchor="w", padx=5, pady=(5, 0))
        location_entry = ctk.CTkEntry(form_frame, width=400)
        location_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Story
        ctk.CTkLabel(form_frame, text="Your Story:").pack(
            anchor="w", padx=5, pady=(5, 0))
        story_text = tk.Text(form_frame, height=10,
                             width=50, font=("Arial", 12))
        story_text.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        # Quote
        ctk.CTkLabel(form_frame, text="Inspirational Quote:").pack(
            anchor="w", padx=5, pady=(5, 0))
        quote_entry = ctk.CTkEntry(form_frame, width=400)
        quote_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Achievement
        ctk.CTkLabel(form_frame, text="Key Achievement:").pack(
            anchor="w", padx=5, pady=(5, 0))
        achievement_entry = ctk.CTkEntry(form_frame, width=400)
        achievement_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=20, pady=10)

        def submit_story():
            # In a real implementation, this would send the story to a server
            messagebox.showinfo("Thank You", "Your story has been submitted for review. "
                                "It may inspire thousands of others around the world!")
            dialog.destroy()

        ctk.CTkButton(button_frame, text="Submit Story",
                      command=submit_story).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel",
                      command=dialog.destroy).pack(side="right", padx=5)

# -----------------------------------
# World Typing Championship Integration
# -------------------------------------


class WorldChampionship(ctk.CTkToplevel):
    """World Typing Championship interface."""

    def __init__(self, master):
        super().__init__(master)
        self.title("World Typing Championship")
        self.geometry("900x700")
        self.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(header, text="🏆 World Typing Championship 🏆",
                     font=("Arial", 28, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text="Compete against the best typists in the world",
                     font=("Arial", 18)).pack(pady=5)

        # Championship info
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=16, pady=8)

        # Current championship details
        ctk.CTkLabel(info_frame, text="2023 Global Finals: December 15-17",
                     font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(info_frame, text="Prize Pool: $100,000 | Participants: 50,000+ from 120 countries",
                     font=("Arial", 14)).pack(pady=5)

        # Tabs
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=8)

        # Leaderboard tab
        self._add_leaderboard_tab()

        # Events tab
        self._add_events_tab()

        # Qualifiers tab
        self._add_qualifiers_tab()

        # Past champions tab
        self._add_champions_tab()

        # Participate button
        ctk.CTkButton(self, text="Join Championship",
                      command=self.join_championship).pack(pady=10)

    def _add_leaderboard_tab(self):
        """Add the global leaderboard tab."""
        tab = self.notebook.add("Global Leaderboard")

        # Filter options
        filter_frame = ctk.CTkFrame(tab)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(filter_frame, text="Filter by:").pack(side="left", padx=5)

        regions = ["All Regions", "Americas",
                   "Europe", "Asia", "Africa", "Oceania"]
        region_var = tk.StringVar(value="All Regions")
        region_menu = ctk.CTkOptionMenu(
            filter_frame, values=regions, variable=region_var)
        region_menu.pack(side="left", padx=5)

        age_groups = ["All Ages", "Under 18", "18-30", "31-45", "46-60", "60+"]
        age_var = tk.StringVar(value="All Ages")
        age_menu = ctk.CTkOptionMenu(
            filter_frame, values=age_groups, variable=age_var)
        age_menu.pack(side="left", padx=5)

        # Leaderboard
        leaderboard_frame = ctk.CTkFrame(tab)
        leaderboard_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create treeview for leaderboard
        columns = ("Rank", "Name", "Country", "WPM", "Accuracy", "Score")
        tree = ttk.Treeview(leaderboard_frame, columns=columns,
                            show="headings", height=20)

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
        scrollbar = ttk.Scrollbar(
            leaderboard_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def _add_events_tab(self):
        """Add the championship events tab."""
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
        """Display a single event."""
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
        ctk.CTkLabel(frame, text=event["description"], font=("Arial", 14),
                     wraplength=700, justify="left").pack(padx=10, pady=5)

        # Prize
        ctk.CTkLabel(frame, text=f"🏆 {event['prize']}",
                     font=("Arial", 14, "bold"), text_color="#FFD700").pack(anchor="w", padx=10, pady=2)

        # Register button
        ctk.CTkButton(frame, text="Register Now", width=120).pack(
            anchor="e", padx=10, pady=5)

    def _add_qualifiers_tab(self):
        """Add the qualifiers information tab."""
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
        """Add the past champions tab."""
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
                "story": "Elena, a concert pianist, applied her musical training to achieve "
                        "unprecedented typing rhythm and accuracy."
            },
            {
                "year": "2021",
                "name": "Marcus Johnson",
                "country": "USA",
                "wpm": 208.7,
                "accuracy": 98.9,
                "quote": "Champions are made when no one is watching.",
                "story": "Marcus practiced 4 hours daily for 3 years while working full-time "
                        "as a night security guard."
            },
            {
                "year": "2020",
                "name": "Sofia Rodriguez",
                "country": "Spain",
                "wpm": 205.3,
                "accuracy": 99.5,
                "quote": "Your fingers can fly when your mind is free.",
                "story": "A former journalist, Sofia developed her typing skills covering breaking "
                        "news under tight deadlines."
            }
        ]

        for champion in champions:
            self._display_champion(scroll_frame, champion)

    def _display_champion(self, parent, champion):
        """Display a single champion."""
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
        ctk.CTkLabel(frame, text=champion["story"], font=("Arial", 14),
                     wraplength=700, justify="left").pack(padx=10, pady=5)

    def join_championship(self):
        """Join the championship."""
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
        ctk.CTkLabel(form_frame, text="Full Name:").pack(
            anchor="w", padx=5, pady=(5, 0))
        name_entry = ctk.CTkEntry(form_frame, width=400)
        name_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Country
        ctk.CTkLabel(form_frame, text="Country:").pack(
            anchor="w", padx=5, pady=(5, 0))
        countries = ["USA", "Canada", "UK", "Germany", "France", "Spain", "Italy",
                     "Russia", "China", "Japan", "India", "Australia", "Brazil", "Other"]
        country_var = tk.StringVar()
        country_menu = ctk.CTkOptionMenu(
            form_frame, values=countries, variable=country_var)
        country_menu.pack(fill="x", padx=5, pady=(0, 10))

        # Age group
        ctk.CTkLabel(form_frame, text="Age Group:").pack(
            anchor="w", padx=5, pady=(5, 0))
        age_groups = ["Under 18", "18-30", "31-45", "46-60", "60+"]
        age_var = tk.StringVar()
        age_menu = ctk.CTkOptionMenu(
            form_frame, values=age_groups, variable=age_var)
        age_menu.pack(fill="x", padx=5, pady=(0, 10))

        # Experience
        ctk.CTkLabel(form_frame, text="Typing Experience:").pack(
            anchor="w", padx=5, pady=(5, 0))
        experience = ["Beginner", "Intermediate", "Advanced", "Professional"]
        exp_var = tk.StringVar()
        exp_menu = ctk.CTkOptionMenu(
            form_frame, values=experience, variable=exp_var)
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
        """Start championship training."""
        messagebox.showinfo("Championship Training",
                            "Championship training modules will be available soon. "
                            "Keep practicing to improve your skills!")
# ------------------------------
# Motivational & Inspirational Features
# =====================================
# Daily Inspiration System
# ------------------------


class DailyInspiration(ctk.CTkToplevel):
    """Daily inspiration and motivation system."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Daily Inspiration")
        self.geometry("600x500")
        self.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(header, text="✨ Daily Inspiration ✨",
                     font=("Arial", 24, "bold")).pack(pady=10)

        # Today's date
        today = datetime.now().strftime("%A, %B %d, %Y")
        ctk.CTkLabel(header, text=today, font=("Arial", 16)).pack(pady=5)

        # Content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=16, pady=8)

        # Quote of the day
        self._add_quote_of_the_day(content)

        # Success story of the day
        self._add_success_story(content)

        # Tip of the day
        self._add_tip_of_the_day(content)

        # Challenge of the day
        self._add_challenge_of_the_day(content)

        # Close button
        ctk.CTkButton(self, text="Start My Day",
                      command=self.destroy).pack(pady=10)

    def _add_quote_of_the_day(self, parent):
        """Add quote of the day section."""
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
        """Add success story of the day section."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)

        ctk.CTkLabel(frame, text="Success Story of the Day",
                     font=("Arial", 18, "bold")).pack(pady=5)

        # In a real implementation, stories would be fetched from a database
        stories = [
            {
                "name": "Raj from India",
                "story": "Raj, a rickshaw driver in Mumbai, learned typing using a mobile app. "
                        "After 6 months of practice, he got a job as a data entry clerk, "
                        "tripling his income and providing better education for his children."
            },
            {
                "name": "Maria from Brazil",
                "story": "Maria, a single mother of two, learned typing while her children slept. "
                        "She now works remotely as a transcriptionist, allowing her to be there "
                        "for her kids while supporting her family."
            },
            {
                "name": "Ahmed from Egypt",
                "story": "Ahmed lost his job during the pandemic. He dedicated himself to learning "
                        "typing and digital skills. Today, he runs a successful e-commerce business "
                        "and has hired 5 people from his community."
            }
        ]

        story = random.choice(stories)

        story_frame = ctk.CTkFrame(frame)
        story_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(story_frame, text=story["name"],
                     font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=2)
        ctk.CTkLabel(story_frame, text=story["story"], font=("Arial", 14),
                     wraplength=550, justify="left").pack(padx=5, pady=5)

    def _add_tip_of_the_day(self, parent):
        """Add tip of the day section."""
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
        """Add challenge of the day section."""
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
        ctk.CTkLabel(challenge_frame, text=challenge["description"], font=("Arial", 14),
                     wraplength=550, justify="left").pack(padx=5, pady=5)

        ctk.CTkButton(challenge_frame, text="Accept Challenge",
                      width=150).pack(anchor="e", padx=5, pady=5)

# ----------------------------------
# Integration with Main Application
# =================================
# Add these methods to the TypingMasterPro class


def show_humanitarian_challenges(self):
    """Show humanitarian challenges."""
    HumanitarianChallenge(self)



def show_world_championship(self):
    """Show world championship."""
    WorldChampionship(self)


def show_daily_inspiration(self):
    """Show daily inspiration."""
    DailyInspiration(self)


def _build_header(self):
    """Build the header section."""
    header = ctk.CTkFrame(self.main_container, fg_color="transparent")
    header.pack(fill="x", padx=16, pady=(16, 8))

    # Title
    title = ctk.CTkLabel(
        header, text="🔥 Typing Master Pro — Enhanced Edition 🔥", font=("Arial", 28, "bold"))
    title.grid(row=0, column=0, padx=10, pady=8, sticky="w")

    # Daily inspiration button
    self.inspiration_btn = ctk.CTkButton(
        header, text="✨ Daily Inspiration", command=self.show_daily_inspiration)
    self.inspiration_btn.grid(row=0, column=1, padx=10, pady=8, sticky="nsew")

    # Humanitarian challenges button
    self.humanitarian_btn = ctk.CTkButton(
        header, text="🌍 Type for Humanity", command=self.show_humanitarian_challenges)
    self.humanitarian_btn.grid(row=0, column=2, padx=10, pady=8, sticky="nsew")

    # World championship button
    self.championship_btn = ctk.CTkButton(
        header, text="🏆 World Championship", command=self.show_world_championship)
    self.championship_btn.grid(row=0, column=3, padx=10, pady=8, sticky="nsew")

    # User profile section
    profile_frame = ctk.CTkFrame(header, fg_color=("gray95", "gray25"))
    profile_frame.grid(row=0, column=4, padx=20, pady=8, sticky="ew")
    ctk.CTkLabel(profile_frame, text="Profile:", font=(
        "Arial", 14)).grid(row=0, column=0, padx=5, sticky="nsew")
    self.profile_var = tk.StringVar(value="Guest")
    self.profile_menu = ctk.CTkOptionMenu(
        profile_frame,
        values=["Guest"] + list(self.user_profile.profiles.keys()),
        variable=self.profile_var,
        command=self._on_profile_change
    )
    self.profile_menu.grid(row=0, column=1, padx=5, sticky="nsew")
    self.create_profile_btn = ctk.CTkButton(
        profile_frame, text="New", width=40, command=self._create_profile)
    self.create_profile_btn.grid(row=0, column=2, padx=5, sticky="nsew")

    # Theme selector
    theme_frame = ctk.CTkFrame(header, fg_color=("gray95", "gray25"))
    theme_frame.grid(row=0, column=5, padx=20, pady=8, sticky="nsew")
    ctk.CTkLabel(theme_frame, text="Theme:", font=(
        "Arial", 14)).grid(row=0, column=0, padx=5, sticky="nsew")
    self.theme_menu = ctk.CTkOptionMenu(
        theme_frame,
        values=["dark", "light", "system"],
        command=self._on_theme_change
    )
    self.theme_menu.set(self.current_theme)
    self.theme_menu.grid(row=0, column=1, padx=5, sticky="nsew")

    # Settings button
    self.settings_btn = ctk.CTkButton(
        header, text="⚙️ Settings", command=self._open_settings)
    self.settings_btn.grid(row=0, column=6, padx=10, pady=8, sticky="nsew")


def _build_footer(self):
    """Build the footer section."""
    footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
    footer.pack(fill="x", padx=16, pady=(8, 16))

    # Action buttons
    self.start_btn = ctk.CTkButton(
        footer, text="Start", command=self.start_round)
    self.start_btn.grid(row=0, column=0, padx=10, sticky="nsew")

    self.finish_btn = ctk.CTkButton(
        footer, text="Finish", command=self.finish_round)
    self.finish_btn.grid(row=0, column=1, padx=10, sticky="nsew")

    self.retry_btn = ctk.CTkButton(
        footer, text="Retry", command=self.retry_round)
    self.retry_btn.grid(row=0, column=2, padx=10, sticky="nsew")

    # Music toggle
    self.music_btn = ctk.CTkButton(
        footer, text="🎵 Music", command=self.toggle_music)
    self.music_btn.grid(row=0, column=3, padx=10, sticky="nsew")

    # Sound toggle
    self.sound_btn = ctk.CTkButton(
        footer, text="🔊 Sound", command=self.toggle_sound)
    self.sound_btn.grid(row=0, column=4, padx=10, sticky="nsew")

    # Stats button
    self.stats_btn = ctk.CTkButton(
        footer, text="📊 Stats", command=self.show_stats)
    self.stats_btn.grid(row=0, column=5, padx=10, sticky="nsew")

    # Leaderboard button
    self.lb_btn = ctk.CTkButton(
        footer, text="🏆 Leaderboard", command=self.show_leaderboard)
    self.lb_btn.grid(row=0, column=6, padx=10, sticky="nsew")

    # Heatmap button
    self.heatmap_btn = ctk.CTkButton(
        footer, text="🔥 Heatmap", command=self.show_heatmap)
    self.heatmap_btn.grid(row=0, column=7, padx=10, sticky="nsew")

    # Practice button
    self.practice_btn = ctk.CTkButton(
        footer, text="🎯 Practice", command=self.start_practice_mode)
    self.practice_btn.grid(row=0, column=8, padx=10, sticky="nsew")

    def show_inspirational_stories(self):
        """Show a random motivational message in a popup."""
        stories = [
            "🌟 Even the fastest typists once started at zero. Keep practicing!",
            "💡 Every keystroke you type makes you stronger.",
            "🚀 Progress is progress, no matter how small.",
            "🔥 Stay consistent and your speed will surprise you!",
            "🎯 Accuracy first, speed will follow.",
            "📖 Every mistake is a step closer to mastery."
        ]
        message = random.choice(stories)
        messagebox.showinfo("Inspirational Story", message)





class GlobalImpactDashboard(ctk.CTkToplevel):
    """Dashboard showing the global impact of Typing Master Pro."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Global Impact Dashboard")
        self.geometry("900x700")
        self.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(header, text="🌍 Global Impact Dashboard 🌍",
                     font=("Arial", 28, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text="Together, we're making a difference one keystroke at a time",
                     font=("Arial", 16)).pack(pady=5)

        # Impact stats
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=16, pady=8)

        # Create a grid for stats
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(pady=10)

        # Impact data (in a real implementation, this would be fetched from a server)
        impact_data = [
            ("Total Users", "2,450,000+"),
            ("Countries Reached", "187"),
            ("Words Typed", "125,000,000,000+"),
            ("Trees Planted", "125,000+"),
            ("Meals Provided", "250,000+"),
            ("Books Donated", "62,500+"),
            ("Lives Impacted", "500,000+"),
            ("Hours Trained", "15,000,000+")
        ]

        for i, (label, value) in enumerate(impact_data):
            row = i // 2
            col = i % 2
            ctk.CTkLabel(stats_grid, text=f"{label}:", font=("Arial", 14)).grid(
                row=row, column=col, sticky="w", padx=20, pady=5)
            ctk.CTkLabel(stats_grid, text=value, font=("Arial", 14, "bold")).grid(
                row=row, column=col+1, sticky="w", padx=20, pady=5)

        # Impact map placeholder
        map_frame = ctk.CTkFrame(self)
        map_frame.pack(fill="both", expand=True, padx=16, pady=8)

        ctk.CTkLabel(map_frame, text="Global Impact Map",
                     font=("Arial", 20, "bold")).pack(pady=10)

        # In a real implementation, this would be an interactive map
        map_placeholder = ctk.CTkLabel(map_frame, text="[Interactive World Map Showing Impact Areas]",
                                       font=("Arial", 16), height=300)
        map_placeholder.pack(pady=10)

        # Recent impact stories
        stories_frame = ctk.CTkFrame(self)
        stories_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(stories_frame, text="Recent Impact Stories",
                     font=("Arial", 20, "bold")).pack(pady=10)

        # Sample stories
        stories = [
            "School in Kenya receives 100 computers thanks to typing challenge participants",
            "Community garden project in Brazil funded by 'Type for Trees' initiative",
            "5000 meals provided to homeless shelters in India through 'Meals for Words'",
            "Library in rural Vietnam stocked with 1000 books from typing community"
        ]

        for story in stories:
            story_frame = ctk.CTkFrame(stories_frame)
            story_frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(story_frame, text=f"• {story}", font=(
                "Arial", 14)).pack(anchor="w", padx=5, pady=5)

        # Close button
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=10)

# Add this method to the TypingMasterPro class


def show_global_impact(self):
    """Show global impact dashboard."""
    GlobalImpactDashboard(self)


# -------------------------------
# Daily Challenge System
# -------------------------------
class DailyChallengeSystem:
    """Manage daily challenges."""

    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.current_challenge = get_daily_challenge()
        self.completed_today = self._check_completed_today()

    def _check_completed_today(self) -> bool:
        """Check if the daily challenge was already completed today."""
        if not self.user_profile.current_profile:
            return False

        profile = self.user_profile.profiles[self.user_profile.current_profile]
        last_challenge = profile.get("last_daily_challenge")

        if last_challenge:
            last_date = datetime.strptime(last_challenge, "%Y-%m-%d")
            today = datetime.now().date()
            return last_date.date() == today

        return False

    def check_challenge_completion(self, wpm: float, accuracy: float,
                                   difficulty: str, duration: int) -> bool:
        """Check if the daily challenge was completed."""
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
        """Mark the daily challenge as completed."""
        if not self.completed_today:
            self.user_profile.complete_daily_challenge()
            self.completed_today = True

# -------------------------------
# Enhanced Main Application
# -------------------------------


class TypingMasterPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Typing Master Pro — Enhanced Edition")
        self.geometry("1200x800")
        self.resizable(True, True)

        # Initialize systems
        self.user_profile = UserProfile()
        self.achievement_system = AchievementSystem()
        self.daily_challenge_system = DailyChallengeSystem(self.user_profile)

        # Runtime state variables
        self.player_name = "Guest"
        self.difficulty = "Easy"
        self.language = "English"
        self.current_sentence = ""
        self.start_time = None
        self.round_seconds = COUNTDOWN_DEFAULT
        self.time_left = COUNTDOWN_DEFAULT
        self.timer_running = False
        self.current_wpm = 0.0
        self.current_accuracy = 0.0
        self.current_mode = "Standard"  # Standard, Challenge, Custom, Game
        self.current_challenge = None
        self.sound_enabled = True
        self.blind_mode = False
        self.custom_text = ""

        # Theme settings
        self.current_theme = "dark"
        self.background_image = None
        self._bg_original_img = None

        # Initialize pygame mixer if available
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                if os.path.exists(BACKGROUND_MUSIC_FILE):
                    pygame.mixer.music.load(BACKGROUND_MUSIC_FILE)

                # Load sound effects
                self.sounds = {}
                for sound_file in [SOUND_CORRECT, SOUND_WRONG, SOUND_COMPLETE]:
                    if os.path.exists(sound_file):
                        self.sounds[sound_file] = pygame.mixer.Sound(
                            sound_file)
            except Exception as e:
                print("Audio init error:", e)
        else:
            print("pygame not available — audio disabled.")

        # Set initial appearance
        ctk.set_appearance_mode(self.current_theme)

        # Build UI
        self._build_ui()

        # Load background image
        self._load_background_image()

        # Bind resize event
        self.bind("<Configure>", self._resize_background)

        # Prepare first round
        self.load_new_sentence()

        # Show welcome dialog
        self._show_welcome_dialog()

        # Schedule ergonomics reminders
        self.after(1200000, self._schedule_ergonomics_reminder)  # 20 minutes

    def _build_ui(self) -> None:
        """Build the main application UI."""
        # Main container with transparent background
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # Header
        self._build_header()

        # Content
        self._build_content()

        # Footer
        self._build_footer()

    def _build_header(self) -> None:
        """Build the header section."""
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))

        # Title
        title = ctk.CTkLabel(
            header, text="🔥 Typing Master Pro — Enhanced Edition 🔥", font=("Arial", 28, "bold"))
        title.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        # Daily challenge indicator
        self.daily_challenge_btn = ctk.CTkButton(
            header, text="📅 Daily Challenge", command=self.show_daily_challenge)
        self.daily_challenge_btn.grid(
            row=0, column=1, padx=10, pady=8, sticky="nsew")

        # User profile section
        profile_frame = ctk.CTkFrame(header, fg_color=("gray95", "gray25"))
        profile_frame.grid(row=0, column=2, padx=20, pady=8, sticky="ew")
        ctk.CTkLabel(profile_frame, text="Profile:", font=(
            "Arial", 14)).grid(row=0, column=0, padx=5, sticky="nsew")
        self.profile_var = tk.StringVar(value="Guest")
        self.profile_menu = ctk.CTkOptionMenu(
            profile_frame,
            values=["Guest"] + list(self.user_profile.profiles.keys()),
            variable=self.profile_var,
            command=self._on_profile_change
        )
        self.profile_menu.grid(row=0, column=1, padx=5, sticky="nsew")
        self.create_profile_btn = ctk.CTkButton(
            profile_frame, text="New", width=40, command=self._create_profile)
        self.create_profile_btn.grid(row=0, column=2, padx=5, sticky="nsew")

        # Theme selector
        theme_frame = ctk.CTkFrame(header, fg_color=("gray95", "gray25"))
        theme_frame.grid(row=0, column=3, padx=20, pady=8, sticky="nsew")
        ctk.CTkLabel(theme_frame, text="Theme:", font=(
            "Arial", 14)).grid(row=0, column=0, padx=5, sticky="nsew")
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            command=self._on_theme_change
        )
        self.theme_menu.set(self.current_theme)
        self.theme_menu.grid(row=0, column=1, padx=5, sticky="nsew")

        # Settings button
        self.settings_btn = ctk.CTkButton(
            header, text="⚙️ Settings", command=self._open_settings)
        self.settings_btn.grid(row=0, column=4, padx=10, pady=8, sticky="nsew")

    def _build_content(self) -> None:
        """Build the main content area."""
        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=8)

        # Left panel - Typing area
        left_panel = ctk.CTkFrame(content, fg_color=("gray95", "gray25"))
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Mode selector
        mode_frame = ctk.CTkFrame(left_panel)
        mode_frame.pack(fill="x", pady=(10, 5))
        ctk.CTkLabel(mode_frame, text="Mode:", font=(
            "Arial", 14)).pack(side="left", padx=5)
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
        ctk.CTkLabel(lang_frame, text="Language:", font=(
            "Arial", 14)).pack(side="left", padx=5)
        self.lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=list(SENTENCES.keys()),
            command=self._on_language_change
        )
        self.lang_menu.set(self.language)
        self.lang_menu.pack(side="left", padx=5)

        # Challenge selector (initially hidden)
        self.challenge_frame = ctk.CTkFrame(left_panel)
        ctk.CTkLabel(self.challenge_frame, text="Challenge:",
                     font=("Arial", 14)).pack(side="left", padx=5)
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
        ctk.CTkLabel(self.game_frame, text="Game:",
                     font=("Arial", 14)).pack(side="left", padx=5)
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
        ctk.CTkLabel(diff_frame, text="Difficulty:", font=(
            "Arial", 14)).pack(side="left", padx=5)
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
        ctk.CTkLabel(self.custom_frame, text="Custom Text:",
                     font=("Arial", 14)).pack(side="left", padx=5)
        self.import_btn = ctk.CTkButton(
            self.custom_frame, text="Import Text", command=self._import_custom_text)
        self.import_btn.pack(side="left", padx=5)
        self.custom_frame.pack_forget()

        # Target sentence
        self.sentence_label = ctk.CTkLabel(
            left_panel, text="", wraplength=700, font=("Arial", 20))
        self.sentence_label.pack(pady=(18, 10))

        # Typing area
        typing_frame = ctk.CTkFrame(left_panel)
        typing_frame.pack(fill="x", pady=10)
        self.textbox = tk.Text(typing_frame, height=6,
                               width=80, font=("Consolas", 18), wrap="word")
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
            timer_frame, text=f"Time left: {self.time_left}s", font=("Arial", 16))
        self.timer_label.pack(side="left", padx=10)
        self.progress = ctk.CTkProgressBar(timer_frame, width=400)
        self.progress.pack(side="left", padx=10)
        self.progress.set(1)

        # Live stats
        self.stats_label = ctk.CTkLabel(
            left_panel, text="WPM: 0.00 | Accuracy: 0.00%", font=("Arial", 16))
        self.stats_label.pack(pady=5)

        # Motivation messages
        self.motivation_label = ctk.CTkLabel(
            left_panel, text="", font=("Arial", 18, "bold"))
        self.motivation_label.pack(pady=5)

        # Right panel - Stats and info
        right_panel = ctk.CTkFrame(content, fg_color=("gray95", "gray25"))
        right_panel.pack(side="right", fill="y", padx=(8, 0))
        right_panel.pack_propagate(False)

        # Profile stats
        profile_stats_frame = ctk.CTkFrame(right_panel)
        profile_stats_frame.pack(fill="x", pady=(10, 5))
        ctk.CTkLabel(profile_stats_frame, text="Your Stats",
                     font=("Arial", 18, "bold")).pack(pady=5)
        self.profile_stats_label = ctk.CTkLabel(
            profile_stats_frame, text="No profile selected", font=("Arial", 14))
        self.profile_stats_label.pack(pady=5)

        # Daily challenge
        daily_frame = ctk.CTkFrame(right_panel)
        daily_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(daily_frame, text="Daily Challenge",
                     font=("Arial", 18, "bold")).pack(pady=5)
        challenge = self.daily_challenge_system.current_challenge
        self.daily_label = ctk.CTkLabel(
            daily_frame, text=challenge["name"], font=("Arial", 14))
        self.daily_label.pack(pady=2)
        self.daily_desc_label = ctk.CTkLabel(
            daily_frame, text=challenge["desc"], font=("Arial", 12), wraplength=250)
        self.daily_desc_label.pack(pady=2)

        # Achievements
        achievements_frame = ctk.CTkFrame(right_panel)
        achievements_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(achievements_frame, text="Recent Achievements",
                     font=("Arial", 18, "bold")).pack(pady=5)
        self.achievements_label = ctk.CTkLabel(
            achievements_frame, text="None yet", font=("Arial", 14))
        self.achievements_label.pack(pady=5)

        # Leaderboard preview
        leaderboard_frame = ctk.CTkFrame(right_panel)
        leaderboard_frame.pack(fill="both", expand=True, pady=5)
        ctk.CTkLabel(leaderboard_frame, text="Top Players",
                     font=("Arial", 18, "bold")).pack(pady=5)
        self.leaderboard_text = tk.Text(
            leaderboard_frame, height=10, width=30, font=("Courier New", 10))
        self.leaderboard_text.pack(pady=5)
        self.leaderboard_text.configure(state="disabled")

        # Update leaderboard preview
        self._update_leaderboard_preview()

    # -------------------------------
    # FOOOTER
    # ==========
    def _build_footer(self):
        """Build the footer section."""
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=(8, 16))

        # Action buttons
        self.start_btn = ctk.CTkButton(
            footer, text="Start", command=self.start_round)
        self.start_btn.grid(row=0, column=0, padx=10, sticky="nsew")

        self.finish_btn = ctk.CTkButton(
            footer, text="Finish", command=self.finish_round)
        self.finish_btn.grid(row=0, column=1, padx=10, sticky="nsew")

        self.retry_btn = ctk.CTkButton(
            footer, text="Retry", command=self.retry_round)
        self.retry_btn.grid(row=0, column=2, padx=10, sticky="nsew")

        # Music toggle
        self.music_btn = ctk.CTkButton(
            footer, text="🎵 Music", command=self.toggle_music)
        self.music_btn.grid(row=0, column=3, padx=10, sticky="nsew")

        # Sound toggle
        self.sound_btn = ctk.CTkButton(
            footer, text="🔊 Sound", command=self.toggle_sound)
        self.sound_btn.grid(row=0, column=4, padx=10, sticky="nsew")

        # Stats button
        self.stats_btn = ctk.CTkButton(
            footer, text="📊 Stats", command=self.show_stats)
        self.stats_btn.grid(row=0, column=5, padx=10, sticky="nsew")

        # Leaderboard button
        self.lb_btn = ctk.CTkButton(
            footer, text="🏆 Leaderboard", command=self.show_leaderboard)
        self.lb_btn.grid(row=0, column=6, padx=10, sticky="nsew")

        # Heatmap button
        self.heatmap_btn = ctk.CTkButton(
            footer, text="🔥 Heatmap", command=self.show_heatmap)
        self.heatmap_btn.grid(row=0, column=7, padx=10, sticky="nsew")

        # Practice button
        self.practice_btn = ctk.CTkButton(
            footer, text="🎯 Practice", command=self.start_practice_mode)
        self.practice_btn.grid(row=0, column=8, padx=10, sticky="nsew")

        # Inspirational stories button
        self.stories_btn = ctk.CTkButton(
            footer, text="📖 Stories", command=self.show_inspirational_stories)
        self.stories_btn.grid(row=0, column=9, padx=10, sticky="nsew")

        # Global impact button
        self.impact_btn = ctk.CTkButton(
            footer, text="🌍 Impact", command=self.show_global_impact)
        self.impact_btn.grid(row=0, column=10, padx=10, sticky="nsew")


    def _show_welcome_dialog(self) -> None:
        """Show a welcome dialog for new users."""
        if not self.user_profile.profiles:
            dialog = ctk.CTkToplevel(self)
            dialog.title("Welcome to Typing Master Pro!")
            dialog.geometry("500x300")
            dialog.resizable(False, False)
            ctk.CTkLabel(dialog, text="Welcome to Typing Master Pro!",
                         font=("Arial", 24, "bold")).pack(pady=20)
            ctk.CTkLabel(dialog, text="Create a profile to track your progress and unlock achievements.", font=(
                "Arial", 14)).pack(pady=10)
            # Profile name entry
            name_frame = ctk.CTkFrame(dialog)
            name_frame.pack(pady=20)
            ctk.CTkLabel(name_frame, text="Your Name:").pack(
                side="left", padx=5)
            name_entry = ctk.CTkEntry(name_frame, width=200)
            name_entry.pack(side="left", padx=5)

            def create_profile():
                name = name_entry.get().strip()
                if name:
                    if self.user_profile.create_profile(name):
                        self.user_profile.load_profile(name)
                        self.profile_var.set(name)
                        self._update_profile_menu()
                        dialog.destroy()
                    else:
                        messagebox.showerror(
                            "Error", "Profile name already exists!")
            ctk.CTkButton(dialog, text="Create Profile",
                          command=create_profile).pack(pady=10)
            ctk.CTkButton(dialog, text="Continue as Guest",
                          command=dialog.destroy).pack(pady=5)

    def _create_profile(self) -> None:
        """Create a new user profile."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create Profile")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        ctk.CTkLabel(dialog, text="Create New Profile",
                     font=("Arial", 20, "bold")).pack(pady=20)
        # Profile name entry
        name_frame = ctk.CTkFrame(dialog)
        name_frame.pack(pady=20)
        ctk.CTkLabel(name_frame, text="Profile Name:").pack(
            side="left", padx=5)
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
                    messagebox.showerror(
                        "Error", "Profile name already exists!")
        ctk.CTkButton(dialog, text="Create", command=create).pack(pady=10)
        ctk.CTkButton(dialog, text="Cancel",
                      command=dialog.destroy).pack(pady=5)

    def _update_profile_menu(self) -> None:
        """Update the profile menu with current profiles."""
        profiles = ["Guest"] + list(self.user_profile.profiles.keys())
        self.profile_menu.configure(values=profiles)

    def _on_profile_change(self, value: str) -> None:
        """Handle profile selection change."""
        if value == "Guest":
            self.user_profile.current_profile = None
        else:
            self.user_profile.load_profile(value)
        self._update_profile_stats()

    def _on_theme_change(self, value: str) -> None:
        """Handle theme change."""
        self.current_theme = value
        ctk.set_appearance_mode(value)

    def _on_mode_change(self, value: str) -> None:
        """Handle mode change."""
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

    def _on_language_change(self, value: str) -> None:
        """Handle language change."""
        self.language = value

        # Update difficulty options
        difficulties = list(SENTENCES.get(value, {}).keys())
        self.diff_menu.configure(values=difficulties)

        if difficulties:
            self.difficulty = difficulties[0]
            self.diff_menu.set(self.difficulty)

        self.load_new_sentence()

    def _on_difficulty_change(self, value: str) -> None:
        """Handle difficulty change."""
        self.difficulty = value
        self.load_new_sentence()

    def _on_blind_mode_change(self) -> None:
        """Handle blind mode toggle."""
        self.blind_mode = self.blind_var.get()

        if self.blind_mode:
            messagebox.showinfo(
                "Blind Mode", "Blind mode activated! Try not to look at the keyboard while typing.")

    def _on_challenge_change(self, value: str) -> None:
        """Handle challenge selection."""
        self.current_challenge = value
        challenge = CHALLENGES[value]

        # Set round duration
        self.round_seconds = challenge["time_limit"]
        self.time_left = self.round_seconds
        self.timer_label.configure(text=f"Time left: {self.time_left}s")
        self.progress.set(1)

        # Update motivation label
        self.motivation_label.configure(
            text=f"Challenge: {value} - {challenge['reward']}")

        # Special handling for blind mode challenge
        if challenge.get("blind_mode"):
            self.blind_var.set(True)
            self._on_blind_mode_change()

    def _on_game_change(self, value: str) -> None:
        """Handle game selection."""
        game = GAMES[value]

        # Update motivation label
        self.motivation_label.configure(
            text=f"Game: {value} - {game['description']}")

        # Special handling for Memory Master game
        if value == "Memory Master":
            self.motivation_label.configure(
                text=f"Game: {value} - Train your brain memory!")

    def _import_custom_text(self) -> None:
        """Import custom text for typing practice."""
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

                messagebox.showinfo(
                    "Success", "Custom text imported successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to import text: {str(e)}")

    def _update_profile_stats(self) -> None:
        """Update the profile stats display."""
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
                ach = next(
                    (a for a in ACHIEVEMENTS if a["id"] == latest), None)
                if ach:
                    self.achievements_label.configure(
                        text=f"{ach['icon']} {ach['name']}")
        else:
            self.profile_stats_label.configure(text="No profile selected")
            self.achievements_label.configure(text="None yet")

    def _update_leaderboard_preview(self) -> None:
        """Update the leaderboard preview."""
        board = load_leaderboard()
        if board:
            sorted_board = sorted(
                board, key=lambda x: x.get("wpm", 0.0), reverse=True)
            top5 = sorted_board[:5]
            self.leaderboard_text.configure(state="normal")
            self.leaderboard_text.delete("1.0", "end")
            for i, entry in enumerate(top5, start=1):
                self.leaderboard_text.insert("end", f"{i}. {entry['name']}\n")
                self.leaderboard_text.insert(
                    "end", f"   {entry['wpm']:.1f} WPM\n")
            self.leaderboard_text.configure(state="disabled")

    def _open_settings(self) -> None:
        """Open the settings dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Settings")
        dialog.geometry("500x500")
        dialog.resizable(False, False)

        # Theme settings
        theme_frame = ctk.CTkFrame(dialog)
        theme_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(theme_frame, text="Theme Settings",
                     font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(theme_frame, text="Current Theme:").pack(
            anchor="w", padx=10)
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
        ctk.CTkLabel(bg_frame, text="Current: " + (BACKGROUND_IMAGE if os.path.exists(
            BACKGROUND_IMAGE) else "None")).pack(anchor="w", padx=10)

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

        # Ergonomics settings
        ergo_frame = ctk.CTkFrame(dialog)
        ergo_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(ergo_frame, text="Ergonomics Settings",
                     font=("Arial", 18, "bold")).pack(pady=10)
        ergo_var = tk.BooleanVar(value=True)
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

    def _load_background_image(self) -> None:
        """Load and set the background image if available."""
        if not PIL_AVAILABLE:
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
                    self, text="", image=self.background_image)
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

    def _resize_background(self, event) -> None:
        """Resize background dynamically when window size changes."""
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

    def _schedule_ergonomics_reminder(self) -> None:
        """Schedule ergonomics reminders."""
        if hasattr(self, 'ergonomics_enabled') and self.ergonomics_enabled:
            if self.user_profile.show_ergonomics_reminder():
                tip = random.choice(ERGONOMICS_TIPS)
                ErgonomicsReminder(self, tip)

        # Schedule next reminder
        self.after(1200000, self._schedule_ergonomics_reminder)  # 20 minutes

    def load_new_sentence(self) -> None:
        """Load a new random sentence based on difficulty and language."""
        if self.current_mode == "Custom" and self.custom_text:
            # Use custom text if available
            sentences = self.custom_text.split('.')
            if sentences:
                self.current_sentence = random.choice(sentences).strip() + '.'
            else:
                self.current_sentence = self.custom_text[:100] + "..."
        else:
            # Use predefined sentences
            pool = SENTENCES.get(self.language, {}).get(
                self.difficulty, SENTENCES["English"]["Easy"])
            self.current_sentence = random.choice(pool)

        self.sentence_label.configure(text=self.current_sentence)
        self.reset_typing_area()

    def reset_typing_area(self) -> None:
        """Reset the typing area and stats."""
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

    def start_round(self) -> None:
        """Start a new typing round."""
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
        if PYGAME_AVAILABLE and os.path.exists(BACKGROUND_MUSIC_FILE):
            try:
                pygame.mixer.music.play(-1)
                self.music_btn.configure(text="🔇 Music")
            except Exception:
                pass

    def finish_round(self) -> None:
        """Finish the current round early."""
        if not self.start_time:
            messagebox.showinfo("Info", "Click Start to begin the round.")
            return

        self.timer_running = False
        self._finalize_round()

    def retry_round(self) -> None:
        """Retry with a new sentence."""
        self.load_new_sentence()

    def toggle_music(self) -> None:
        """Toggle background music."""
        if not PYGAME_AVAILABLE:
            messagebox.showinfo(
                "Music", "pygame not available. Install with: pip install pygame")
            return

        if not os.path.exists(BACKGROUND_MUSIC_FILE):
            messagebox.showinfo(
                "Music", f"Missing {BACKGROUND_MUSIC_FILE}. Place an mp3 next to the script.")
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

    def toggle_sound(self) -> None:
        """Toggle sound effects."""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.configure(text="🔊 Sound")
        else:
            self.sound_btn.configure(text="🔇 Sound")

    def show_stats(self) -> None:
        """Show the statistics dashboard."""
        if self.user_profile.current_profile:
            profile = self.user_profile.profiles[self.user_profile.current_profile]
            StatsDashboard(self, profile)
        else:
            messagebox.showinfo(
                "Stats", "Please create or select a profile to view statistics.")

    def show_heatmap(self) -> None:
        """Show the typing heatmap."""
        if self.user_profile.current_profile:
            accuracy_data = self.user_profile.get_key_accuracy()
            if accuracy_data:
                TypingHeatmap(self, accuracy_data)
            else:
                messagebox.showinfo(
                    "Heatmap", "Not enough data to generate heatmap. Complete more typing tests.")
        else:
            messagebox.showinfo(
                "Heatmap", "Please create or select a profile to view heatmap.")

    def start_practice_mode(self) -> None:
        """Start practice mode for weak keys."""
        if self.user_profile.current_profile:
            weak_keys = self.user_profile.get_weak_keys(5)
            if weak_keys:
                PracticeMode(self, weak_keys, self.user_profile)
            else:
                messagebox.showinfo(
                    "Practice", "No weak keys identified yet. Complete more typing tests.")
        else:
            messagebox.showinfo(
                "Practice", "Please create or select a profile to use practice mode.")

    def show_daily_challenge(self) -> None:
        """Show the daily challenge details."""
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

    def share_achievement(self, achievement_id: str) -> None:
        """Share an achievement on social media."""
        if not self.user_profile.current_profile:
            messagebox.showinfo(
                "Share", "Please log in to share achievements.")
            return

        # Get achievement details
        achievement = next(
            (a for a in ACHIEVEMENTS if a["id"] == achievement_id), None)
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
                messagebox.showinfo(
                    "Success", "Achievement shared successfully!")

                # Unlock social butterfly achievement if not already unlocked
                if self.user_profile.unlock_achievement("social"):
                    self.achievement_system.show_achievement_popup(
                        self, "social")
            else:
                messagebox.showinfo(
                    "Share", f"Share message copied to clipboard: {message}")
        except:
            # Fallback to clipboard
            self.clipboard_clear()
            self.clipboard_append(message)
            messagebox.showinfo(
                "Share", f"Share message copied to clipboard: {message}")

    def _tick_timer(self) -> None:
        """Timer scheduler."""
        if not self.timer_running:
            return

        elapsed = int(time.time() - self.start_time)
        self.time_left = max(self.round_seconds - elapsed, 0)
        self.timer_label.configure(text=f"Time left: {self.time_left}s")

        # Update progress bar
        self.progress.set(
            self.time_left / self.round_seconds if self.round_seconds else 0)

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

    def _on_typing(self, event=None) -> None:
        """Handle typing events with sound effects."""
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
            correct_chars = sum(1 for a, b in zip(
                typed, self.current_sentence) if a == b)
            accuracy = (correct_chars /
                        max(1, len(self.current_sentence))) * 100.0

            self.current_wpm = round(wpm, 2)
            self.current_accuracy = round(accuracy, 2)
            self.stats_label.configure(
                text=f"WPM: {self.current_wpm:.2f} | Accuracy: {self.current_accuracy:.2f}%")

    def _apply_pending_tags(self) -> None:
        """Apply pending tags to all characters."""
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("wrong", "1.0", "end")
        self.textbox.tag_remove("pending", "1.0", "end")

        for i, _ in enumerate(self.current_sentence):
            self.textbox.tag_add("pending", f"1.{i}", f"1.{i+1}")

    def _finalize_round(self) -> None:
        """Finalize the round and save results."""
        # Stop music
        if PYGAME_AVAILABLE:
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
        correct_chars = sum(1 for a, b in zip(
            typed, self.current_sentence) if a == b)
        accuracy = (correct_chars / max(1, len(self.current_sentence))) * 100.0

        self.current_wpm = round(wpm, 2)
        self.current_accuracy = round(accuracy, 2)
        self.stats_label.configure(
            text=f"WPM: {self.current_wpm:.2f} | Accuracy: {self.current_accuracy:.2f}%")

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
                messagebox.showinfo("Challenge Complete!",
                                    f"You've earned the {reward}!")

        # Check daily challenge completion
        if self.daily_challenge_system.check_challenge_completion(
                wpm, accuracy, self.difficulty, self.round_seconds):
            self.daily_challenge_system.complete_challenge()
            DailyChallengePopup(
                self, self.daily_challenge_system.current_challenge, "XP Boost")

        # Save to leaderboard
        entry = {
            "name": self.player_name,
            "wpm": self.current_wpm,
            "accuracy": round(self.current_accuracy, 2),
            "difficulty": self.difficulty,
            "language": self.language,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        board = load_leaderboard()
        board.append(entry)
        save_json_file(LEADERBOARD_FILE, board)

        # Update user profile if logged in
        if self.user_profile.current_profile:
            self.user_profile.update_profile(
                self.current_wpm,
                self.current_accuracy,
                self.difficulty,
                typed,
                self.current_sentence,
                self.language
            )

            # Check achievements
            profile = self.user_profile.profiles[self.user_profile.current_profile]
            newly_unlocked = self.achievement_system.check_achievements(
                profile, self.current_wpm, self.current_accuracy, self.difficulty, self.language
            )

            for ach_id in newly_unlocked:
                if self.user_profile.unlock_achievement(ach_id):
                    self.achievement_system.show_achievement_popup(
                        self, ach_id)

            # Update profile stats display
            self._update_profile_stats()

        # Evaluate rankings
        self._evaluate_rewards(entry, board)

        # Update leaderboard preview
        self._update_leaderboard_preview()

    def _evaluate_rewards(self, entry: Dict, board: List) -> None:
        """Evaluate rewards and show popups."""
        # Overall sorted by WPM (desc)
        overall_sorted = sorted(
            board, key=lambda x: x.get("wpm", 0.0), reverse=True)
        # Rank of current entry among overall
        overall_rank = next(
            (i+1 for i, e in enumerate(overall_sorted) if e is entry or e == entry), None)

        # If the player is #1 overall, show celebration
        if overall_rank == 1:
            # Play victory sound
            if PYGAME_AVAILABLE and os.path.exists(VICTORY_SOUND_FILE):
                try:
                    sfx = pygame.mixer.Sound(VICTORY_SOUND_FILE)
                    sfx.play()
                except Exception:
                    pass

            ConfettiPopup(self)

            # Unlock champion achievement if logged in
            if self.user_profile.current_profile:
                if self.user_profile.unlock_achievement("champion"):
                    self.achievement_system.show_achievement_popup(
                        self, "champion")

        # Rank within difficulty
        same_diff = [e for e in board if e.get(
            "difficulty") == entry.get("difficulty")]
        diff_sorted = sorted(
            same_diff, key=lambda x: x.get("wpm", 0.0), reverse=True)
        diff_rank = next((i+1 for i, e in enumerate(diff_sorted)
                         if e is entry or e == entry), None)

        if diff_rank is not None and diff_rank <= 3:
            MedalPopup(self, place=diff_rank, difficulty=entry.get(
                "difficulty", ""), wpm=entry.get("wpm", 0.0))
        else:
            # Encouragement for others
            messagebox.showinfo(
                "Nice Run!", "Good effort! Keep practicing to climb the ranks.")

    def show_leaderboard(self) -> None:
        """Show the full leaderboard."""
        board = load_leaderboard()
        if not board:
            messagebox.showinfo(
                "Leaderboard", "No scores yet! Play a round first.")
            return

        # Sort by WPM desc
        sorted_board = sorted(
            board, key=lambda x: x.get("wpm", 0.0), reverse=True)
        top50 = sorted_board[:50]
        bottom10 = sorted_board[-10:] if len(
            sorted_board) >= 10 else sorted_board[-len(sorted_board):]

        # Create popup window
        win = ctk.CTkToplevel(self)
        win.title("Leaderboard — Top 50 & Bottom 10")
        win.geometry("900x620")

        # Top section
        section_top = ctk.CTkFrame(win)
        section_top.pack(fill="both", expand=True, padx=10, pady=(10, 6))
        lbl_top = ctk.CTkLabel(
            section_top, text="🏆 Top 50 Overall (by WPM)", font=("Arial", 22, "bold"))
        lbl_top.pack(pady=8)
        txt_top = tk.Text(section_top, height=16, width=110,
                          font=("Courier New", 12))
        txt_top.pack(padx=8, pady=6)

        # Header line
        txt_top.insert(
            "end", f"{'#':<4}{'Name':<18}{'WPM':>8}{'Acc%':>8}{'Difficulty':>14}{'Language':>10}{'Date':>16}\n")
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
            section_bottom, text="😬 Bottom 10 Overall (by WPM)", font=("Arial", 20, "bold"))
        lbl_bottom.pack(pady=8)
        txt_bottom = tk.Text(section_bottom, height=10,
                             width=110, font=("Courier New", 12))
        txt_bottom.pack(padx=8, pady=6)

        txt_bottom.insert(
            "end", f"{'#':<4}{'Name':<18}{'WPM':>8}{'Acc%':>8}{'Difficulty':>14}{'Language':>10}{'Date':>16}\n")
        txt_bottom.insert("end", "-" * 90 + "\n")

        for i, e in enumerate(bottom10, start=1):
            txt_bottom.insert(
                "end",
                f"{i:<4}{e.get('name', ''):<18}{e.get('wpm', 0):>8.2f}{e.get('accuracy', 0):>8.2f}{e.get('difficulty', ''):>14}{e.get('language', ''):>10}{e.get('date', ''):>16}\n"
            )
        txt_bottom.configure(state="disabled")

# -------------------------------
# App entrypoint
# -------------------------------
if __name__ == "__main__":
    app = TypingMasterPro()
    app.mainloop()
