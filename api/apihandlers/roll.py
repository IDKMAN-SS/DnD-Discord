import random
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


def roll_dice(dice):
    if "d" not in dice:
        logger.debug("d is not in string")
        raise ValueError("Invalid format.")
    parts = dice.lower().split("d")
    if parts[1] == "":
        logger.debug("second number is invalid")
        raise ValueError("Ivalid format.")
    try:
        num_to_roll = int(parts[0])
        roll_to_make = int(parts[1])
    except ValueError as e:
        logger.debug(e)
        return "invalid numbers"
    results = []
    for _ in range(num_to_roll):
        results.append(random.randint(1, roll_to_make))
    return results
