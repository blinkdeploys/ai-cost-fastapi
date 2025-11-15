# Compression Techniques
import tiktoken
from typing import Optional, Dict, List

# Basic stopwords that can often be removed without losing context
STOPWORDS = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'very', 'really', 'quite', 'just', 'actually', 'basically'
             }
    


def count_tokens():
    """Count tokens using tiktoken library"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    return len(tokens)



def remove_extra_whitespace():
    """Remove extra whitespace and normalize spacing"""
    # replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # replace multiple newlines with single newline
    text = re.sub(r'\n+', '\n', text)
    # remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(lines)


def remove_redundant_punctuation();
    """Remove redundant punctuation"""
    # remove multiple consecutive punctuation marks
    text = re.sub(r'([!?.]){2,}', r'\1', text)
    # remove spaces before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return text


def remove_common_stopwords():
    """Remove common English stopwords while preserving meaning"""
    words = text.split()
    # only remove stopwords that don't start sentences
    result = []
    for i, word in enumerate(words):
        # keep word if it starts a sentence or isn't a stopword
        if i == 0 or word.lower() not in stopwords:
            result.append(word)
        elif word.lower() in stopwords:
            # skip common stopwords in the middle of sentences
            continue
        else:
            result.append(word)
    
    return ' '.join(result)



def remove_code_comments():
    """Remove programming comments if text contains code"""

    # remove single-line comments
    text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)
    text = re.sub(r'#.*?$', '', text, flags=re.MULTILINE)

    # remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

    return text


# NOTE: Exclude for code string processing
# this method removes duplicated lines
# may not be ideal for processing code as it will remove needed code
def deduplicate_repeated_content(text: str) -> str:
    """Remove repeated sentences or paragraphs"""

    # break into lines
    lines = text.split('\n')
    seen = set()
    unique_lines = []

    for line in lines:
        line_stripped = line.strip()
        if line_stripped and line_stripped not in seen:
            seen.add(line_stripped)
            unique_lines.append(line)
        elif not line_stripped:
            unique_lines.append(line)
    
    return '\n'.join(unique_lines)


def compress_text(text: str):
    """Compression pipeline: Apply multiple compression techniques to reduce token count"""


def calculate_costs():
    """Calculate costs for all LLM models"""
    pass


# Compression Techniques