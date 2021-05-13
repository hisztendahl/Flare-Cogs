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
YC_FOULS = ["bad tackle", "missed sliding tackle", "flying elbow"]
YELLOW_CARDS2 = "{} ({}) was shown a {} for {}"
YC_OFFENSES = [
    "timewasting.",
    "simulation.",
    "diving.",
    "handball.",
    "dissent.",
    "bad sportsmanship.",
    "unsporting behavior.",
    "delaying the restart of play",
    "removing their shirt",
    random.choice(["Pushing", "Pulling"]) + " an opponent.",
]

RED_CARDS = "{} ({}) was caught {} {}! Red card!!"
RC_FOULS = [
    "biting",
    "kicking",
    "stamping on",
    "punching",
    "spitting at",
    "headbutting",
    "slaping",
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
GOAL2 = random.choice(
    [
        "Top bins!",
        "A great effort beats the keeper at the near post.",
        "Fluffed his shot, but it somehow rolled in...",
        "A quick shot had the keeper flat-footed",
        "Easy tap-in in the 6-yard box",
        "Hits the post on its way in!",
        "Deflected by the keeper, but it wasn't enough...",
    ]
)
FK_GOAL = random.choice(
    [
        "Top bins!",
        "A great effort beats the keeper at the near post.",
        "Hits the post on its way in!",
        "Deflected by the keeper, but it wasn't enough...",
        "Hit the wall and the deflection took it past the keeper...",
        "Great effort in the bottom left corner",
        "Great effort in the bottom right corner",
        "Great effort in the top left corner",
        "Great effort in the top right corner",
    ]
)
CORNER_GOAL = random.choice(
    [
        "Powerful header in the top right corner!",
        "Powerful header in the top left corner!",
        "Powerful header in the bottom left corner!",
        "Powerful header in the bottom right!",
        "Easy tap-in after the keeper missed his high claim...",
        "Strong header at the near post!",
        "Strong header at the far post!",
    ]
)
PEN_GOAL = random.choice(
    [
        "Cheeky panenka!",
        "Keeper dove the other way",
        "Straight down the middle!",
        "Keeper picked the correct side but could'nt get a glove to it",
        "Nice shot caught the keeper flat-footed",
        "Hits the post on its way in!",
        "The keeper got a hand to it, but it wasn't enough...",
        "Great effort in the bottom left corner",
        "Great effort in the bottom right corner",
        "Great effort in the top left corner",
        "Great effort in the top right corner",
    ]
)
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
