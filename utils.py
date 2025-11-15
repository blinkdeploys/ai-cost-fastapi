# Compression Techniques
import tiktoken
from typing import Optional, Dict, List
from models import CompressionResult, CostAnalysis, ComprehensiveReport


# Basic stopwords that can often be removed without losing context
TOKEN_LIMIT = 5000
STOPWORDS = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'very', 'really', 'quite', 'just', 'actually', 'basically'
             }
    


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens using tiktoken library"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    return len(tokens)


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
    return text


def remove_common_stopwords(text: str) -> str:
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

    for provider, models in LLM_PRICING.items():
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