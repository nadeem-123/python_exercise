#Project - 2
#Name of the project is "Madlibs Generator"
#Description: This is a Mad Libs Game, which reads a story template from a file, identifies placeholders enclosed in < and >, asks the user to provide replacements for these placeholders, and then displays the completed story. 

#Open the story file in read mode and read its content
with open("/Users/mdnadeem/Documents/Python/Projects/story.txt","r") as f:
    story = f.read()

words = set()
start_of_word = -1

target_start = "<"
target_end = ">"

#Extract placeholders from the story
for i, char in enumerate(story):
    if char == target_start:
        start_of_word = i # Mark the start of a placeholder

    if char == target_end and start_of_word != -1:
        word = story[start_of_word: i+1] #slice of str, Extract placeholder including <>
        words.add(word)
        start_of_word = -1 # Reset the start marker

answers = {}

# Prompt the user to enter replacements for each placeholder
for word in words:
    answer = input("Enter a word for " + word + ": ")
    answers[word] = answer

# Replace placeholders in the story with user-provided replacements
for word in words:
    story = story.replace(word, answers[word])

print(story)
