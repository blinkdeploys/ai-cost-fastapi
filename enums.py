TOKEN_LIMIT = 5000

# stopword list similar to set used in NLTK or SpaCy
STOPWORDS = {'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
             'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
             'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
             'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
             'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
             'will', 'just', 'don', 'should', 'now', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'would', 'could', 'should',
             'might', 'must', 'shall', 'may', 'ought', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
             'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
             'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
             'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
             'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
             'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
             'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
             'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
             'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
             'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn',
             'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan',
             'shouldn', 'wasn', 'weren', 'won', 'wouldn'
             }

# Current LLM Pricing (November 2025) - per 1M tokens
CURRENT_LLM_PRICING = {
    "OpenAI": {
        "GPT-5": {"input": 3.00, "output": 12.00, "context": 200000},
        "GPT-4.5": {"input": 75.00, "output": 150.00, "context": 128000},
        "GPT-4o": {"input": 5.00, "output": 20.00, "context": 128000},
        "GPT-4.1": {"input": 12.00, "output": 48.00, "context": 128000},
        "GPT-3.5-Turbo": {"input": 3.00, "output": 6.00, "context": 16000},
        "o3": {"input": 10.00, "output": 40.00, "context": 128000},
        "o4-mini": {"input": 1.00, "output": 4.00, "context": 128000},
    },
    "Anthropic": {
        "Claude-Opus-4.1": {"input": 15.00, "output": 75.00, "context": 200000},
        "Claude-Sonnet-4.5": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Sonnet-4": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Sonnet-3.7": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Sonnet-3.5": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Haiku-4.5": {"input": 0.80, "output": 4.00, "context": 200000},
        "Claude-Haiku-3.5": {"input": 0.80, "output": 4.00, "context": 200000},
        "Claude-Haiku-3": {"input": 0.25, "output": 1.25, "context": 200000},
    },
    "Google": {
        "Gemini-2.5-Pro": {"input": 2.50, "output": 10.00, "context": 1000000},
        "Gemini-2.5-Flash": {"input": 0.15, "output": 0.60, "context": 1000000},
        "Gemini-1.5-Pro-128k": {"input": 1.25, "output": 5.00, "context": 128000},
        "Gemini-1.5-Pro-1M": {"input": 2.50, "output": 10.00, "context": 1000000},
        "Gemini-1.5-Flash": {"input": 0.075, "output": 0.30, "context": 1000000},
    },
    "xAI": {
        "Grok-3": {"input": 2.00, "output": 10.00, "context": 128000},
        "Grok-4": {"input": 5.00, "output": 15.00, "context": 128000},
        "Grok-Mini": {"input": 0.50, "output": 1.50, "context": 32000},
    },
    "DeepSeek": {
        "DeepSeek-V3.2": {"input": 0.27, "output": 1.10, "context": 128000},
        "DeepSeek-Chat": {"input": 0.14, "output": 0.28, "context": 64000},
    },
    "Mistral": {
        "Mistral-Large": {"input": 2.00, "output": 6.00, "context": 128000},
        "Mistral-Medium": {"input": 2.70, "output": 8.10, "context": 32000},
    },
    "Meta": {
        "Llama-3.1-405B": {"input": 0.80, "output": 0.80, "context": 128000},
        "Llama-3.1-70B": {"input": 0.35, "output": 0.40, "context": 128000},
        "Llama-4-70B": {"input": 0.50, "output": 0.60, "context": 200000},
    }
}

