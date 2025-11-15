from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import tiktoken
import uvicorn
from datetime import datetime
from models import CompressionResult, CostAnalysis, ComprehensiveReport
from enums import CURRENT_LLM_PRICING
from utils import (count_tokens,
                   remove_extra_whitespace,
                   remove_redundant_punctuation,
                   remove_common_stopwords,
                   remove_code_comments,
                   deduplicate_repeated_content,
                   compress_text,
                   calculate_costs,
                   )



app = FastAPI(title="AI Cost Analysis Service", version="1.0.0")


def run_cost_analysis_pipeline(text):
    try:
        
        # raise excep for empty files
        if not text.strip():
            raise HTTPException(status_code=400, detail="File is empty")

        # calculate original text stats
        original_tokens = count_tokens(text)
        # char count
        char_count = len(text)
        # word count
        word_count = len(text.split())
        # line count
        line_count = len(text.split('\n'))

        # Perform compression
        compression_result = compress_text(text)
        
        # calculate costs for original text
        original_cost_analysis = calculate_costs(original_tokens)
        
        # calculate costs for compressed text
        compressed_cost_analysis = calculate_costs(compression_result.compressed_tokens)
        
        # find cheapest and most expensive models
        original_costs_1k = [(ca.llm_name, ca.provider, ca.total_cost_1k_output) 
                             for ca in original_cost_analysis if ca.fits_in_context]
        cheapest = min(original_costs_1k, key=lambda x: x[2])
        most_expensive = max(original_costs_1k, key=lambda x: x[2])
        
        # compression strategies
        strategies = ["1. Whitespace Normalization: Remove extra spaces, tabs, and newlines (5-15% reduction)",
                      "2. Punctuation Optimization: Remove redundant punctuation marks (1-3% reduction)",
                      "3. Deduplication: Remove repeated sentences and paragraphs (5-20% reduction)",
                      "4. Stopword Removal: Remove common words like 'the', 'a', 'is' (10-25% reduction for long texts)",
                      "5. Code Comment Removal: Strip comments from code files (10-30% reduction)",
                      "6. Abbreviation: Use common abbreviations (e.g., 'w/' for 'with', 'info' for 'information')",
                      "7. Sentence Compression: Remove filler phrases and redundant expressions",
                      "8. Smart Truncation: Remove less important sections while preserving core meaning",
                      "9. Format Optimization: Convert verbose formats to concise structures (JSON, bullet points)",
                      "10. Semantic Compression: Use AI-based methods like LLMLingua for intelligent compression (60-80% reduction)"
                      ]
        # package
        report = ComprehensiveReport(timestamp=datetime.now().isoformat(),
                                     original_text_stats=dict(characters=char_count,
                                                            words=word_count,
                                                            lines=line_count,
                                                            tokens=original_tokens,
                                                            estimated_reading_time_minutes=round(word_count / 200, 1)
                                                            ),
                                     compression_result=compression_result,
                                     cost_analysis=original_cost_analysis,
                                     cheapest_model=dict(model=f"{cheapest[1]} - {cheapest[0]}",
                                                        cost_1k_output=cheapest[2],
                                                        savings_vs_expensive=round(most_expensive[2] - cheapest[2], 6)
                                                        ),
                                     most_expensive_model=dict(model=f"{most_expensive[1]} - {most_expensive[0]}",
                                                            cost_1k_output=most_expensive[2]
                                                            ),
                                     compression_strategies=strategies
                                     )
        # deliver
        return report

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error processing file contents: {str(e)}")





# Endpoints


@app.post("/batch/", response_model=ComprehensiveReport)
async def batch_analyze(file: UploadFile = File(...)):
    """Run jobs processing all files in a folder"""
    pass


@app.post("/analyze/", response_model=ComprehensiveReport)
async def analyze(file: UploadFile = File(...)):
    """
    Upload a text file to analyze AI processing costs
    
    Returns comprehensive report including:
    - Token count breakdown
    - Cost analysis for all major LLM models
    - Text compression results
    - Cost-saving recommendations
    """
    try:
        # read file content
        content = await file.read()
        text = content.decode('utf-8')

        # run pipeline
        report = run_cost_analysis_pipeline(text)
        return report

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, 
                            detail="File must be a valid UTF-8 text file")


@app.get("/test/", response_model=ComprehensiveReport)
async def test():
    """test endpoint"""
    file_path = "./PROMPT.md"
    text = ""

    try:
        # open the file and read the text
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # run pipeline
        report = run_cost_analysis_pipeline(text)
        return report

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, 
                            detail="File must be a valid UTF-8 text file")



@app.get("/")
async def root():
    return dict(message="AI Cost Analysis Service",
                version="1.0.0",
                endpoints={"/analyze-costs/": "POST - Upload a text file for comprehensive cost analysis",
                            "/docs": "Interactive API documentation"
                            }
                )


@app.get("/models/")
async def list_models():
    """Get list of all supported LLM models and their pricing"""
    return {"models": CURRENT_LLM_PRICING}

# Endpoints



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

