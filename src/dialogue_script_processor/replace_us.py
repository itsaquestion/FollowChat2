import re

def replace_us(text):
    # Using regular expression to find instances of 'US' that are not part of another word
    # Handling the punctuation and end of sentence scenarios manually

    def replacement(match):
        # Get the position of the match
        start, end = match.span()

        # Check if 'US' is at the end of the sentence or followed by punctuation
        if end == len(text) or text[end] in ".,!?":
            return 'U.S.'
        else:
            return 'U.S.'

    return re.sub(r'\bUS\b', replacement, text).replace('..','.')

if __name__ == "__main__":
    test_cases = [
        ("I live in the US.", "I live in the U.S."), # End of sentence
        ("Is this the US question?", "Is this the U.S. question?"), # Middle of sentence
        ("US-based companies are thriving.", "U.S.-based companies are thriving."), # Hyphenated
        ("Visit the US! It's wonderful.", "Visit the U.S.! It's wonderful."), # Before exclamation mark
        ("Do you know about the US?", "Do you know about the U.S.?"), # Before question mark
        ("The symbol US$ represents US currency.", "The symbol U.S.$ represents U.S. currency."), # Inside other text
        ("US, UK, and Canada", "U.S., UK, and Canada"), # In a list
        ("She said, 'I am going to the US'", "She said, 'I am going to the U.S.'"), # Inside quotes
        ("The abbreviation for United States is US", "The abbreviation for United States is U.S.") # End of sentence without punctuation
    ]

    # Re-testing with the improved test cases
    test_result_final = [replace_us(x[0]) for x in test_cases]

    [print(x) for x in test_result_final]