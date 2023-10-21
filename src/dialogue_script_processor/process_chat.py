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

    abbreviations = ['Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Jr.', 'Sr.', 'U.S.', 'e.g.', 'i.e.', 'etc.', 'a.m.', 'p.m.']
    
    # Initialize the list to store the final sentences
    final_sentences = []

    # Loop through the initial list of sentences to refine them
    for i, sentence in enumerate(sentences):
        # If the sentence ends with an abbreviation, merge it with the next sentence
        if any(sentence.endswith(abbr) for abbr in abbreviations):
            try:
                sentences[i+1] = sentence + ' ' + sentences[i+1]
            except IndexError:
                # Handle the case where the abbreviation is at the end of the text
                final_sentences.append(sentence)
        else:
            final_sentences.append(sentence)

    # Remove any empty strings that may have been added to the list
    final_sentences = [s for s in final_sentences if s]
    
    return final_sentences


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
    # print(process_chat(chat_script))
    
    text = "So, there's this U.S. soldier, right? He was just released from North Korea, which is a big deal. But guess what? Now he's in trouble back home. Turns out, he's facing charges related to child pornography. Yeah, not good. The soldier, we don't know his name, was arrested as soon as he got back to the U.S. The charges are all about him having and sharing explicit pictures of kids. Yikes! His lawyer hasn't said anything about it yet. People are really concerned about how soldiers who were held captive in other countries are checked before they come back. Like, what if they're dangerous? This whole thing is putting a damper on the celebration of his release from North Korea. It was supposed to be a positive thing for the ongoing diplomatic efforts between the two countries. But now, these charges are stealing the spotlight. The soldier is gonna have a military trial, and if he's found guilty, he could be in big trouble. Like, prison and getting kicked out of the military kind of trouble."
    
    print(process_chat('Aria: '+ text))
