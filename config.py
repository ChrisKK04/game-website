"""File for the global variables of the website."""

SECRET_KEY = "d751a7b727f62a1c45aa32e611eddbb2" # session key
GAMES_PER_PAGE = 10 # amount of games per homepage
TIME = '+3 hours'

IMAGE_FORM = {
    "MAX_IMAGE_SIZE": 100 * 1024, # maximum size of images
    "STR_IMAGE_SIZE": "100 kB" # string for the image size
}

REVIEW_FORM = {
    "MAX_LENGTH": 5000, # maximum review length
    "MIN_SCORE": 1, # minimum review score
    "MAX_SCORE": 5 # maximum review score
}

GAME_FORM = {
    "MAX_TITLE_LENGTH": 50, # maximum game title length
    "MAX_DESCRIPTION_LENGTH": 5000 # maximum game description length
}

USER_FORM = {
    "MAX_USERNAME_LENGTH": 50, # maximum username length
    "MAX_PASSWORD_LENGTH": 100 # maximum password length
}
