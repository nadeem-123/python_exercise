#Project - 1
#Name of the project is "Pig"
#Description: The Pig Game is a turn-based dice game for 2-4 players where players take turns rolling a six-sided die. Players accumulate points during their turn, but rolling a 1 resets their turn's score to zero and ends their turn. The first player to reach or exceed 50 points wins the game.

import random

#Function to simulate a dice roll
def roll():
    min_value = 1
    max_value = 6
    roll = random.randint(min_value, max_value)

    return roll

#Validate the number of players (2-4)
while True:
    players = input("Enter the number of players (2-4): ")
    if players.isdigit():
        players = int(players)
        if 2 <= players <= 4:
            break
        else:
            print("Must be between 2 - 4 Players.")
    else:
        print("Invalid Try Again.")

#game setting
max_score = 50
player_scores = [0 for _ in range(players)]

#Game loop: Continue until a player reaches or exceeds max_score
while max(player_scores) < max_score:
    for player_index in range(players):
        print("\nPlayer number", player_index + 1, "turn has just started!")
        print("Your total score is: ", player_scores[player_index],"\n")
        current_score = 0

        while True:
            should_roll = input("would you like to roll (y)? ")
            if should_roll.lower() != "y":
                break

            value = roll()
            if value == 1:
                print("You rolled a 1! Turn Done!")
                current_score = 0
                break
            else:
                current_score += value
                print("You rolled a:", value)
            
            print("Your current score is: ", current_score)

        player_scores[player_index] += current_score
        print("Your total score is: ", player_scores[player_index])

#Determine and announce the winner
max_score = max(player_scores)
winning_index = player_scores.index(max_score)
print("Player number", winning_index + 1, "is the winner with a score of", max_score)