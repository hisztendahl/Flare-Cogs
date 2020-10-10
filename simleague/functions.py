import random

WEATHER = [
    "rainy",
    "thunderstorms",
    "sunny",
    "dusk",
    "dawn",
    "night",
    "snowy",
    "hazy rain",
    "windy",
    "partly cloudy",
    "overcast",
    "cloudy",
]

COMMENT_TYPES = ["CHANCE!", "FOUL!"]

FOULS = [
    "Foul by {} ({}).",
    "Late tackle from {} ({}).",
    "{} ({}) concedes a free kick in the attacking half.",
    "{} ({}) concedes a free kick in the defensive half.",
    "{} ({}) concedes a free kick on the left wing.",
    "{} ({}) concedes a free kick on the right wing.",
]


YELLOW_CARDS = "{} ({}) with a {} on {}, {} was issued a {}."
YC_FOULS = ["bad tackle", "missed side tackle", "flying elbow"]
YELLOW_CARDS2 = "{} ({}) was shown a {} for {}"
YC_OFFENSES = [
    "timewasting.",
    "simulation.",
    "diving.",
    "handball.",
    "dissent.",
    random.choice(["Pushing", "Pulling"]) + " an opponent.",
]

RED_CARDS = "{} ({}) was caught {} {}! Red card!!"
RC_FOULS = [
    "biting",
    "kicking",
    "stamping on",
    "punching",
    "spitting at",
    "with a violent tackle on",
    "with a studs up challenge on",
]
RED_CARDS2 = "{} ({}) was shown a red card for {}!"
RC_OFFENSES = [
    "violent conduct",
    "offensive language",
    "insulting the ref",
    "flipping off the coach",
    "denying a clear goal scoring opportunity",
]
CHANCE_TYPE = ["saved", "missed", "blocked"]
GOAL = "from {} in the {} {} of the goal."
SAVED_CHANCE = "Attempt saved. {} ({}) from {} is saved in the {} {} of the goal."
MISSED_CHANCE = "Attempt missed. {} ({}) from {} {}."
MISSED_DIST = [
    "goes wide",
    "is close, but misses to the right",
    "is close, but misses to the left",
    "is too high",
]
BLOCKED_CHANCE = "Attempt blocked. {} ({}) from {} is blocked."

DISTANCE = ["outside the box", "the center of the box", "the edge of the box", "distance"]
HEIGHT = ["top", "center", "bottom"]
SIDE = ["left", "middle", "right"]
