"""
处理对话文本，对对话进行断句，每个句子加上正确的说话者名称。

见 process_chat()
"""
import re


def split_sentences(text):
    """
    Split a given text into sentences based on common sentence delimiters.

    Parameters:
        text (str): The input text to be split into sentences.

    Returns:
        List[str]: A list of sentences extracted from the input text.
    """
    # Use regular expression to split sentences by common delimiters ('.', '!', '?') followed by a space.
    
    # sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # 匹配 . ! ? ."(逗号双引号)
    sentences = re.split(r'(?<=[.!?])\s+|(?<=\."\s)', text)


    # Remove any empty strings that may have been added to the list
    sentences = [s for s in sentences if s]

    return sentences


def split_by_comma(sentences):
    """
    Further split each sentence from the list into comma-separated phrases.
    Do not split phrases that contain three words or fewer. If the last split contains three words
    or fewer, it should be merged with the previous split.
    Retain commas at the end of each split, except for the last one.

    Parameters:
        sentences (List[str]): The list of sentences to be split by commas.

    Returns:
        List[str]: A list of phrases after splitting by commas.
    """
    result = []

    for sentence in sentences:
        # Remove leading and trailing whitespace from each sentence
        sentence = sentence.strip()

        # Split the sentence by commas, but keep the commas
        comma_splits = re.split(r'(, )', sentence)

        # Initialize an empty string to hold the current phrase
        current_phrase = ""

        for i in range(0, len(comma_splits), 2):  # Step of 2 to skip commas
            # Merge the part with its following comma
            part = "".join(comma_splits[i:i+2])
            # Temporary holder for combining the current and next part
            temp_phrase = current_phrase + part

            # Count the number of words in the temporary phrase (excluding commas)
            word_count = len(re.split(r'\s+', temp_phrase.strip(", ")))

            # If the current phrase has more than 3 words or is the last part, append it to the result list
            if word_count > 3 or (i >= len(comma_splits) - 2 and temp_phrase):
                if i >= len(comma_splits) - 2 and word_count <= 3 and result:
                    # Merge with the last entry in result if the last part has 3 or fewer words
                    result[-1] = result[-1] + part
                else:
                    result.append(temp_phrase.strip())
                current_phrase = ""
            else:
                current_phrase = temp_phrase

    return result


def process_chat(chat_content):
    """
    对话脚本重新断句，返回一个新对话脚本。

    范例：
    
    输入：[字符串]
        'Aria: Really? Considering how adept you usually are, I wouldn't have anticipated that.'
    输出：[字符串]
         'Aria: Really?
          Aria: Considering how adept you usually are,
          Aria: I wouldn't have anticipated that.'
    """
    processed_lines = []
    lines = chat_content.split("\n")

    for line in lines:
        if line.strip() == "":
            continue

        name, sentence = line.split(": ", 1)
        sentences = split_by_comma(split_sentences(sentence))

        processed_lines += [name + ": " + sen for sen in sentences]

    return '\n'.join(processed_lines)


if __name__ == "__main__":
    def read_sample_chat():
        with open('./tests/test_data/script.txt', 'r') as f:
            return f.read()

    chat_script = read_sample_chat()
    print(process_chat(chat_script))
