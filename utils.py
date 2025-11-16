# Compression Techniques
import re
import tiktoken
from typing import Optional, Dict, List
from models import CompressionResult, CostAnalysis, ComprehensiveReport
from enums import (TOKEN_LIMIT,
                    CURRENT_LLM_PRICING,
                    STOPWORDS,
                    _COMPILED_REDUNDANT_PAIRS,
                    _COMPILED_ABBREVIATIONS,
                    _COMPILED_CONTRACTIONS,
                    NUM_WORDS, MULTIPLIERS,
                    WORD_NUMBER_PATTERN
                    )



    


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens using tiktoken library"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    return len(tokens)



# BASIC CONPRESSION



def remove_extra_whitespace(text: str) -> str:
    """Remove extra whitespace and normalize spacing"""
    # replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # replace multiple newlines with single newline
    text = re.sub(r'\n+', '\n', text)
    # remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(lines)


def remove_redundant_punctuation(text: str) -> str:
    """Remove redundant punctuation"""
    # remove multiple consecutive punctuation marks
    text = re.sub(r'([!?.]){2,}', r'\1', text)
    # remove spaces before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    # remove extra commas in the same place
    text = re.sub(r',{2,}', ',', text)
    return text


def remove_common_stopwords(text: str) -> str:
    """Remove common English stopwords while preserving meaning
    
    Remove common English stopwords but keep the first word of each sentence.
    Handles multiple sentences efficiently.
    """
    result = []
    # slipt text into sentences, keeping the punctuation intact
    sentences = re.split(r'([.!?]\s*)', text)

    # loop through the sentences : smaller loop sizes
    for i in range(0, len(sentences), 2):
        sentence = sentences[i].split()
        punctuation = sentences[i+1] if i+1 < len(sentences) else ''

        if not sentence:
            continue

        # keep the first word, filter out stopwords for the rest
        filtered = [sentence[0]] + [w for w in sentence[1:] if w.lower() not in STOPWORDS]
        result.append(' '.join(filtered) + punctuation)

    return ''.join(result)


def remove_code_comments(text: str) -> str:
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






# ADVANCED COMPRESSION

# Using English syntax rules to reduce prompt text further



def compress_filler_phrases(text: str) -> str:
    """Remove or compress common filler phrases and verbose expressions"""
    for pattern, replacement in _COMPILED_FILLER_PATTERNS:
        text = pattern.sub(replacement, text)

    # normalize spaces and punctuation spacing
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)

    return text


def compress_redundant_pairs(text: str) -> str:
    """Remove redundant word pairs where both words mean the same"""
    for pattern, replacement in _COMPILED_REDUNDANT_PAIRS:
        text = pattern.sub(replacement, text)

    # clean up extra spaces resulting from replacements
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def apply_common_abbreviations(text: str) -> str:
    """Replace common words with standard abbreviations

    Replace long technical/common words with short industry-standard abbreviations.
    Uses precompiled regex patterns for high performance.
    """
    for pattern, replacement in _COMPILED_ABBREVIATIONS:
        text = pattern.sub(replacement, text)

    # clean spacing
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compress_technical_terms(text: str) -> str:
    """Replace common technical terms with abbreviations"""
    pass


# TODO: to include a URL shortening service
# best for when analysing the links themseleves
# and NOT for providing additional web context
def compress_urls_and_paths(text: str) -> str:
    """Compress URLs and file paths"""
    pass


def expand_to_contractions(text: str) -> str:
    """Convert common phrases to contractions (saves tokens)"""
    for pattern, replacement in _COMPILED_CONTRACTIONS:
        text = pattern.sub(replacement, text)

    # clean spacing
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# cheaper trick -  converting words to numbers
# word to number converter v1
def words_to_number(text: str):
    """
    Convert numbers written in English words into digits and append '(in words)'.
    FAST implementation using token streaming.
    """
    # Normalize text
    clean = text.lower()
    clean = re.sub(r"[,/&-]", " ", clean)
    tokens = clean.split()

    total = 0
    current = 0
    found_words = False

    for token in tokens:
        if token in NUM_WORDS:
            found_words = True
            current += NUM_WORDS[token]
        elif token in MULTIPLIERS:
            found_words = True
            current = max(1, current) * MULTIPLIERS[token]
            total += current
            current = 0
        elif token == "and":
            continue
        else:
            # not a number word
            continue

    total += current

    if not found_words:
        return text  # no conversion

    return f"{total:,} (in words)"

# word to number converter v2
def convert_number_words_to_int(words: str) -> int:
    clean = words.lower()
    clean = re.sub(r"[,/&-]", " ", clean)
    tokens = clean.split()

    total = 0
    current = 0

    for token in tokens:
        if token in NUM_WORDS:
            current += NUM_WORDS[token]
        elif token in MULTIPLIERS:
            current = max(1, current) * MULTIPLIERS[token]
            total += current
            current = 0
        elif token == "and":
            continue

    return total + current


def convert_all_numbers_in_text(text: str) -> str:
    def repl(match):
        original = match.group()
        number = convert_number_words_to_int(original)
        return f"{number:,} (in words)"

    return WORD_NUMBER_PATTERN.sub(repl, text)


# TODO: to detect numbers like in convert_all_numbers_in_text() and append approprialtey
def compress_numbers_and_dates(text: str) -> str:
    """Compress numeric expressions and dates"""
    # convert written numbers to digits
    number_words = {
        r'\bone thousand\b': '1000',
        r'\btwo thousand\b': '2000',
        r'\bone hundred\b': '100',
        r'\bone million\b': '1M',
        r'\bone billion\b': '1B',
    }
    
    for pattern, replacement in number_words.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Compress percentage expressions
    text = re.sub(r'\b(\w+) percent\b', r'\1%', text)
    
    return text


def compress_text(text: str):
    """Compression pipeline: Apply multiple compression techniques to reduce token count"""
    original_tokens = count_tokens(text)
    compressed_text = text
    techniques_applied = []
    
    # 1. Remove extra whitespace
    compressed_text = remove_extra_whitespace(compressed_text)
    techniques_applied.append("Whitespace normalization")
    
    # 2. Remove redundant punctuation
    compressed_text = remove_redundant_punctuation(compressed_text)
    techniques_applied.append("Punctuation optimization")
    
    # 3. Remove code comments if present
    if '//' in text or '/*' in text or text.count('#') > 5:
        compressed_text = remove_code_comments(compressed_text)
        techniques_applied.append("Code comment removal")
    
    # 4. Deduplicate repeated content
    # TODO: file extension to be used to determine if text is code
    # compressed_text = deduplicate_repeated_content(compressed_text)
    # techniques_applied.append("Deduplication")
    
    # 5. Remove common stopwords (conservative approach)
    # Only apply if text is very long to avoid over-compression
    if original_tokens > TOKEN_LIMIT:
        compressed_text = remove_common_stopwords(compressed_text)
        techniques_applied.append("Stopword reduction")
    
    compressed_tokens = count_tokens(compressed_text)
    reduction = ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0
    
    return CompressionResult(original_tokens=original_tokens,
                             compressed_tokens=compressed_tokens,
                             reduction_percentage=round(reduction, 2),
                             compression_techniques_applied=techniques_applied,
                             compressed_text=compressed_text
                             )


def calculate_costs(token_count: int) -> List[CostAnalysis]:
    """Calculate costs for all LLM models"""
    cost_analyses = []
    QUOTA_SIZE = 1_000_000

    for provider, models in CURRENT_LLM_PRICING.items():
        for llm_name, pricing in models.items():
            input_cost = (token_count / QUOTA_SIZE) * pricing["input"]
            
            # calculate output costs for 1k and 5k tokens
            output_cost_1k = (1000 / QUOTA_SIZE) * pricing["output"]
            output_cost_5k = (5000 / QUOTA_SIZE) * pricing["output"]
            
            total_1k = input_cost + output_cost_1k
            total_5k = input_cost + output_cost_5k
            
            fits_in_context = token_count <= pricing["context"]
            
            cost_analyses.append(CostAnalysis(llm_name=llm_name,
                                              provider=provider,
                                              input_cost=round(input_cost, 6),
                                              output_cost_1k=round(output_cost_1k, 6),
                                              output_cost_5k=round(output_cost_5k, 6),
                                              total_cost_1k_output=round(total_1k, 6),
                                              total_cost_5k_output=round(total_5k, 6),
                                              context_window=pricing["context"],
                                              fits_in_context=fits_in_context
                                              ))
    
    return cost_analyses

# Compression Techniques