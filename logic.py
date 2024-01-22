# Function to get suggestions from a file
def get_suggestions():
    suggestions = open("./static/data/suggestions.txt")
    content = suggestions.read()
    suggestions.close()
    all_suggestions = content.split("\n") 
    all_suggestions.pop()
    return all_suggestions

# Function to append a suggestion to the file
def append_suggestion(suggestion):
    suggestions = open("./static/data/suggestions.txt","a")
    suggestions.write(suggestion+"\n")
    suggestions.close()