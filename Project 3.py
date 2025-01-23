#Project - 3
#Name of the project is "Timed Math Challenge"
#Description: This is a Math Quiz Game where users solve randomly generated arithmetic problems involving addition, subtraction, and multiplication. It tracks the user's performance and measures the total time taken to complete the quiz.

import random
import time

OPERATORS = ["+","-","*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10

# Function to generate a math problem
def generate_problem():
    left = random.randint(MIN_OPERAND, MAX_OPERAND)
    right = random.randint(MIN_OPERAND, MAX_OPERAND)
    operator = random.choice(OPERATORS)

    expr = str(left) + " " + operator + " " + str(right) # Create the problem as a string
    answer = eval(expr) # Evaluate the problem to get the answer
    return expr, answer

wrong = 0
input("Press enter to start!")
print("----------------------")

start_time = time.time()

# Generate and present problems to the user
for i in range(TOTAL_PROBLEMS):
    expr, answer = generate_problem()
    while True:
        guess = input("Problem #" + str(i+1) + ": " + expr + " = ")
        if guess == str(answer):
            break
        wrong += 1

end_time = time.time()
total_time = round(end_time - start_time, 2)# Calculate the total time taken

print("-------------------------")
print("Nice Work! You have finined in ", total_time, "seconds!")