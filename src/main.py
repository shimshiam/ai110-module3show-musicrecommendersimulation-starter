"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs, BalancedScorer, GenreFirstScorer, MoodFirstScorer, EnergyFocusedScorer
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, BalancedScorer, GenreFirstScorer, MoodFirstScorer, EnergyFocusedScorer


def format_bar(score: float, max_score: float = 4.5, width: int = 20) -> str:
    filled = int((score / max_score) * width)
    return "#" * filled + "-" * (width - filled)


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    strategy_name = user_prefs.get("strategy", "balanced")
    scorer_map = {
        "balanced": BalancedScorer(),
        "genre_first": GenreFirstScorer(),
        "mood_first": MoodFirstScorer(),
        "energy_focused": EnergyFocusedScorer(),
    }
    scorer = scorer_map.get(strategy_name, BalancedScorer())
    
    prefs_display = (
        f"Genre: {user_prefs.get('genre', '-'):12s} "
        f"Mood: {user_prefs.get('mood', '-'):12s} "
        f"Energy: {user_prefs.get('energy', '-'):<5} "
        f"Acoustic: {'yes' if user_prefs.get('likes_acoustic') else 'no'} "
        f"Strategy: {strategy_name}"
    )

    print()
    print("+" + "-" * 68 + "+")
    print(f"|  PROFILE: {name:56s}|")
    print("|  " + prefs_display.ljust(66) + "|")
    print("+" + "-" * 68 + "+")

    recommendations = recommend_songs(user_prefs, songs, k=k, scorer=scorer)

    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        bar = format_bar(score, max_score=6.0)  # Updated max score
        reasons = explanation.split("; ")

        print(f"|                                                                      |")
        print(f"|  #{rank}  {song['title']:<25s} {song['artist']:<18s}|")
        print(f"|       Genre: {song['genre']:<12s}  Mood: {song['mood']:<14s}   |")
        print(f"|       Score: {score:.2f} / 6.00  [{bar}]   |")

        for reason in reasons:
            print(f"|         {reason:<59s}|")

    print(f"|                                                                      |")
    print("+" + "-" * 68 + "+")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        # The upbeat pop listener — wants high energy, mainstream, and electronic
        "Party Mode": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "likes_acoustic": False,
            "strategy": "balanced",
        },
        # The late-night study session — low energy, chill, acoustic lofi
        "Study Session": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
            "strategy": "balanced",
        },
        # The workout grinder — max energy, intense, electronic production
        "Gym Grinder": {
            "genre": "metal",
            "mood": "aggressive",
            "energy": 0.95,
            "likes_acoustic": False,
            "strategy": "energy_focused",
        },
        # The mellow evening wind-down — mid-low energy, acoustic, soulful
        "Evening Wind-Down": {
            "genre": "blues",
            "mood": "soulful",
            "energy": 0.50,
            "likes_acoustic": True,
            "strategy": "balanced",
        },
        # The road trip vibe — mid-high energy, confident, electronic
        "Road Trip": {
            "genre": "hip-hop",
            "mood": "confident",
            "energy": 0.80,
            "likes_acoustic": False,
            "strategy": "genre_first",
        },
        # Conflicted Pop Fan — genre says pop, but mood and production contradict it
        "Conflicted Pop Fan": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.90,
            "likes_acoustic": True,
            "strategy": "mood_first",
        },
        # Low-Energy Happy Metal Listener — tests genre vs. low energy / happy mood
        "Low-Energy Happy Metal Listener": {
            "genre": "metal",
            "mood": "happy",
            "energy": 0.10,
            "likes_acoustic": True,
            "strategy": "balanced",
        },
        # Electronic Ballad Seeker — low energy but prefers non-acoustic sound
        "Electronic Ballad Seeker": {
            "genre": "r&b",
            "mood": "romantic",
            "energy": 0.20,
            "likes_acoustic": False,
            "strategy": "balanced",
        },
        # Impossible Energy — out-of-range energy to see whether scoring behaves safely
        "Impossible Energy": {
            "genre": "jazz",
            "mood": "mellow",
            "energy": 1.50,
            "likes_acoustic": True,
            "strategy": "balanced",
        },
        # No Good Match — likely no exact genre/mood pair in the dataset
        "No Good Match": {
            "genre": "classical",
            "mood": "nostalgic",
            "energy": 0.50,
            "likes_acoustic": True,
            "strategy": "balanced",
        },
    }

    for name, prefs in profiles.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
