from pydantic import BaseModel
from typing import Optional, Dict, List



class CompressionResult(BaseModel):
    original_tokens: int
    compressed_tokens: int
    reduction_percentage: float
    compression_techniques_applied: List[str]
    compressed_text: str


class CostAnalysis(BaseModel):
    llm_name: str
    provider: str
    input_cost: float
    output_cost_1k: float
    output_cost_5k: float
    total_cost_1k_output: float
    total_cost_5k_output: float
    context_window: int
    fits_in_context: bool


class ComprehensiveReport(BaseModel):
    timestamp: str
    original_text_stats: Dict
    compression_result: CompressionResult
    cost_analysis: List[CostAnalysis]
    cheapest_model: Dict
    most_expensive_model: Dict
    compression_strategies: List[str]
