import re

def replace_dollar_amount(text):
    # Further refined regular expression to handle amounts with commas and ensure proper spacing
    dollar_pattern = r"\$(\d{1,3}(?:,\d{3})*)(?:\.(\d+))?\s*(million|billion|thousand|trillion|Million|Billion|Thousand|Trillion)?\b"

    # Function to replace the matched pattern
    def replace_with_dollers(match):
        whole, fraction, unit = match.groups()
        # Format the string with a space between amount and unit or just after amount if no unit
        amount = whole + ('.' + fraction if fraction else '')
        return f"{amount}{(' ' + unit) if unit else ''} dollers "

    # Replace all occurrences of the pattern in the text
    return re.sub(dollar_pattern, replace_with_dollers, text).replace('  ',' ').replace(' .','.')


if __name__ == "__main__":

    test_cases = [
        "The city owes $300 in fees.",
        "A new startup raised $2.5 million in funding.",
        "She inherited a fortune of $50 thousand.",
        "The project cost is estimated to be around $10 billion.",
        "His salary is $5000 per month.",
        "GM claims to have only sold about $677,000 worth of goods in San Francisco in 2022." ,
        "The budget for the project was $1,234,567.",
        "20231229-1205_News_Google Settles $5 Billion Consumer Privacy Lawsuit"

    ]

    # Apply the final refined function to each test case
    final_refined_test_results = [replace_dollar_amount(tc) for tc in test_cases]
    [print(x) for x in final_refined_test_results]

