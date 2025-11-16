# AI Cost Analysis FastAPI Service

A comprehensive FastAPI service that analyzes AI processing costs for text files across all major LLM providers and performs intelligent text compression to reduce token usage.

## Features

### 1. **Token Analysis**
- Accurate token counting using OpenAI's tiktoken library
- Character, word, and line count statistics
- Estimated reading time calculation

### 2. **Comprehensive Cost Calculation**
Includes current pricing (November 2025) for **40+ LLM models** from:
| Providers | LLM Models |
|-----------|------------|
| **OpenAI**: | GPT-5, GPT-4.5, GPT-4o, GPT-4.1, GPT-3.5-Turbo, o3, o4-mini |
| **Anthropic**: | Claude Opus 4.1, Sonnet 4.5/4/3.7/3.5, Haiku 4.5/3.5/3 |
| **Google**: | Gemini 2.5 Pro/Flash, Gemini 1.5 Pro/Flash |
| **xAI**: | Grok-3, Grok-4, Grok-Mini |
| **DeepSeek**: | V3.2, Chat |
| **Mistral**: | Large, Medium |
| **Meta**: | Llama 3.1 & 4 (405B, 70B) |

### 3. **Intelligent Text Compression**
Applies multiple heuristic (non-AI) compression techniques:
- ✅ Whitespace normalization (removes extra spaces, tabs, newlines)
- ✅ Punctuation optimization (removes redundant marks)
- ✅ Code comment removal (strips //, #, /* */ comments)
- ✅ Deduplication (removes repeated sentences/paragraphs)
- ✅ Conservative stopword removal (for very long texts)

### 4. **Cost Comparison**
- Identifies cheapest and most expensive models
- Shows potential savings from model selection
- Calculates costs with 1K and 5K token outputs
- Indicates which models fit within context windows

### 5. **Compression Strategies**
Provides 10 research-backed strategies for reducing tokens:
- Semantic compression techniques
- AI-based methods (LLMLingua, AutoCompressor)
- Format optimization approaches
- Advanced prompt compression methods

## Installation

### Option 1: Docker Compose (Recommended)

```bash
# Clone or download the service files
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The service will be available at `http://localhost:8000`

### Option 2: Local Python Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

The service will start on `http://localhost:8000`

## Docker Commands

### Basic Commands
```bash
# Build and start
docker-compose up -d

# Rebuild after code changes
docker-compose up -d --build

# View logs
docker-compose logs -f ai-cost-analyzer

# Stop service
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Check service status
docker-compose ps
```

### Production Setup with Nginx
```bash
# Start with nginx reverse proxy
docker-compose --profile production up -d

# This will start both the API service and nginx on port 80
```

### Development with Hot Reload
The docker-compose setup includes volume mounting for hot-reload:
- Edit `main.py` and changes will reflect automatically
- No need to rebuild the container during development

### API Endpoints

#### 1. **Analyze Costs** (Main Endpoint)
```bash
POST /analyze/
```

Upload a text file to get comprehensive cost analysis.

**Example using cURL:**

In terminal, run:

```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.txt"
```

A prompt document has been included for testing purposes:

```bash
curl -X POST "http://localhost:8000/analyze/" \
  -F "file=@./PROMPT.md"
```

**Example using Python:**
```python
import requests

with open('your_document.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze-costs/',
        files={'file': f}
    )
    
report = response.json()
print(f"Original tokens: {report['original_text_stats']['tokens']}")
print(f"Compressed tokens: {report['compression_result']['compressed_tokens']}")
print(f"Reduction: {report['compression_result']['reduction_percentage']}%")
```

**Node.js example using axios**
```js
import fs from "fs";
import FormData from "form-data";
import axios from "axios";

// Path to your file
const filePath = "./your_document.txt";

// Create form data
const form = new FormData();
form.append("file", fs.createReadStream(filePath));

// Send POST request
try {
  const response = await axios.post("http://localhost:8000/analyze/", form, {
    headers: form.getHeaders(),
  });

  const report = response.data;

  console.log(`Original tokens: ${report.original_text_stats.tokens}`);
  console.log(`Compressed tokens: ${report.compression_result.compressed_tokens}`);
  console.log(`Reduction: ${report.compression_result.reduction_percentage}%`);
} catch (error) {
  console.error(error.response?.data || error.message);
}
```

**✅ Notes:**

* `fs.createReadStream(filePath)` streams the file to the request.
* `form.getHeaders()` automatically sets the correct Content-Type including the multipart boundary.

If you are using CommonJS, replace the imports with:
```js
const fs = require("fs");
const FormData = require("form-data");
const axios = require("axios");
```


#### 2. **List Models**
```bash
GET /models/
```

Returns all supported models and their pricing.

#### 3. **API Documentation**
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Response Structure

The service returns a comprehensive JSON report:

```json
{
  "timestamp": "2025-11-14T10:30:00",
  "original_text_stats": {
    "characters": 15420,
    "words": 2315,
    "lines": 187,
    "tokens": 3842,
    "estimated_reading_time_minutes": 11.6
  },
  "compression_result": {
    "original_tokens": 3842,
    "compressed_tokens": 3156,
    "reduction_percentage": 17.86,
    "compression_techniques_applied": [
      "Whitespace normalization",
      "Punctuation optimization",
      "Deduplication"
    ],
    "compressed_text": "..."
  },
  "cost_analysis": [
    {
      "llm_name": "GPT-4o",
      "provider": "OpenAI",
      "input_cost": 0.01921,
      "output_cost_1k": 0.00002,
      "output_cost_5k": 0.0001,
      "total_cost_1k_output": 0.01923,
      "total_cost_5k_output": 0.02021,
      "context_window": 128000,
      "fits_in_context": true
    }
  ],
  "cheapest_model": {
    "model": "Google - Gemini-1.5-Flash",
    "cost_1k_output": 0.00029,
    "savings_vs_expensive": 0.28842
  },
  "most_expensive_model": {
    "model": "Anthropic - Claude-Opus-4.1",
    "cost_1k_output": 0.28871
  },
  "compression_strategies": [...]
}
```

## Text Compression Techniques Explained

### 1. **Whitespace Normalization** (5-15% reduction)
Removes unnecessary spaces, tabs, and multiple newlines while preserving structure.

### 2. **Punctuation Optimization** (1-3% reduction)
Removes redundant punctuation like multiple periods or exclamation marks.

### 3. **Deduplication** (5-20% reduction)
Identifies and removes repeated sentences or paragraphs that appear multiple times.

### 4. **Stopword Removal** (10-25% reduction)
Conservative removal of common words like "the", "a", "is" that don't affect meaning significantly. Only applied to very long texts (5000+ tokens).

### 5. **Code Comment Removal** (10-30% reduction)
Strips programming comments (//, #, /* */) if the text contains code.

### Advanced Strategies (Recommended for Implementation)

#### **AI-Based Compression**
- **LLMLingua**: Can achieve 60-80% compression while preserving key information
- **AutoCompressor**: Pre-trained models for semantic compression
- **Selective Context**: Uses perplexity scoring to keep only important content

#### **Prompt Engineering**
- Replace verbose instructions with concise directives
- Use abbreviations consistently
- Structure data as bullet points vs. prose

#### **Semantic Techniques**
- Hierarchical attention networks
- Token merging based on similarity
- Context-aware compression with shared mappings

## Cost Savings Examples

Based on current November 2025 pricing:

**Example: 10,000 token input + 1,000 token output**

| Model | Original Cost | After 20% Compression | Savings |
|-------|--------------|----------------------|---------|
| Claude Opus 4.1 | $0.225 | $0.195 | 13.3% |
| GPT-4o | $0.07 | $0.06 | 14.3% |
| Gemini Flash | $0.002 | $0.0016 | 20% |

**With LLMLingua (70% compression):**
| Model | Original Cost | After Compression | Savings |
|-------|--------------|-------------------|---------|
| Claude Opus 4.1 | $0.225 | $0.105 | 53.3% |
| GPT-4o | $0.07 | $0.035 | 50% |

## Research References

The compression strategies are based on recent research:

1. **Sparse Attention Mechanisms**: Longformer and BigBird reduce memory and token overhead by having only subsets of tokens interact during attention

2. **Contextual Summarization**: Periodically summarizing conversations reduces tokens required for historical context

3. **Encoding Methods**: Transform input texts into vectors, reducing prompt length without losing critical information

4. **Prompt Compression Goals**: Reduces costs, improves speed, and maintains quality through systematic optimization

5. **LongLLMLingua**: Achieves 6-7x compression while retaining key information, translating to ~80% cost savings

## Best Practices

1. **Always test compression**: Some texts may be over-compressed, losing critical context
2. **Use appropriate models**: Match model capability to task complexity
3. **Monitor token usage**: Track actual usage vs. estimates
4. **Consider caching**: Anthropic offers prompt caching discounts for repeated queries
5. **Batch processing**: Group similar requests to optimize costs

## Limitations

- Compression is heuristic-based; meaning preservation isn't guaranteed
- Token counting uses GPT-4 tokenizer; counts may vary slightly by model
- Pricing is current as of November 2025; verify with providers
- Very aggressive compression may impact LLM comprehension

## Future Enhancements

- [ ] Integration with LLMLingua for AI-based compression
- [ ] Support for PDF and document parsing
- [ ] Batch file processing
- [ ] Cost tracking over time
- [ ] Custom compression rules
- [ ] Multiple output token size scenarios
- [ ] Real-time pricing updates via API

## Contributing

Suggestions and improvements welcome! Key areas:
- Additional compression techniques
- More LLM providers
- Better semantic preservation methods
- Performance optimizations

## License

MIT License - Feel free to use and modify for your needs.

## Support

For issues or questions:
- Check `/docs` endpoint for API documentation
- Review compression strategies in the response
- Test with small files first to understand compression behavior
