import pytest
from src.dialogue_script_processor import process_chat


def read_sample_chat():
    with open('tests/test_data/sample_chat.txt', 'r') as f:
        return f.read()


def test_process_chat():
    sample_chat = read_sample_chat()
    result = process_chat(sample_chat)

    assert result[1] == 'Aria: Indeed, I have.'
    #assert result is not None  # 仅作为示例，您应根据实际需求编写断言
