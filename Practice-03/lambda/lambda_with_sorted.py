# Here is a list of words with different lengths
words = ["apple", "pie", "banana", "cat"]

# Here is how to use sorted() with a lambda key to sort words by their length
sorted_by_length = sorted(words, key=lambda word: len(word))
print(sorted_by_length)  # ['pie', 'cat', 'apple', 'banana']