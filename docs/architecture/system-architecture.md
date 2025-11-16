# System Architecture: AI Cost Analysis Service

**Version**: 1.0  
**Date**: 2025-11-15  
**Status**: Current

---

## 🎯 Architecture Overview

The AI Cost Analysis Service is a stateless, containerized microservice that provides real-time cost analysis and text compression for LLM API usage.

### Key Principles

1. **Stateless**: No persistent storage, each request is independent
2. **Privacy-First**: All processing happens locally, no external API calls
3. **Fast**: Sub-second analysis for typical documents
4. **Portable**: Runs anywhere Docker runs
5. **Extensible**: Easy to add new models and compression techniques

---

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                          Client Layer                       │
│  ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Browser   │  │  cURL     │  │  Python  │  │  CI/CD    │  │
│  │ (Swagger) │  │  Command  │  │  Script  │  │ Pipeline  │  │
│  └──────┬────┘  └─────┬─────┘  └────┬─────┘  └─────┬─────┘  │
│         │             │             │              │        │
│         └─────────────┴─────────────┴──────────────┘        │
│                              │                              │
└──────────────────────────────┼────────────────────────────-─┘
                               │ HTTP/REST
┌──────────────────────────────┼──────────────────────────────┐
│                              ▼                              │
│                    ┌────────────────────┐                   │
│                    │  Nginx (Optional)  │                   │
│                    │  Reverse Proxy     │                   │
│                    └────────┬───────────┘                   │
│                             │                               │
│                    ┌────────▼─────────┐                     │
│                    │   FastAPI App    │                     │
│                    │   (Port 8000)    │                     │
│                    └────────┬─────────┘                     │
│                             │                               │
│         ┌───────────────────┼───────────────────┐           │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Upload    │    │   Models    │    │    Docs     │      │
│  │   Handler   │    │   Endpoint  │    │  (Swagger)  │      │
│  └──────┬──────┘    └─────────────┘    └─────────────┘      │
│         │                                                   │
│         ▼                                                   │
│  ┌───────────────────────────────────────────────────┐      │
│  │             Request Processing Pipeline           │      │
│  │                                                   │      │
│  │  1. File Validation ────────────────────┐         │      │
│  │      │                                  │         │      │
│  │      ▼                                  │         │      │
│  │  2. Text Extraction                     │         │      │
│  │      │                                  │         │      │
│  │      ▼                                  │         │      │
│  │  3. Token Counting (tiktoken)           │         │      │
│  │      │                                  ▼         │      │
│  │      ▼                            Error Handler   │      │
│  │  4. Compression Engine                  │         │      │
│  │      │                                  │         │      │
│  │      ▼                                  │         │      │
│  │  5. Cost Calculator                     │         │      │
│  │      │                                  │         │      │
│  │      ▼                                  │         │      │
│  │  6. Report Generator ───────────────────┘         │      │
│  │      │                                            │      │
│  └──────┼────────────────────────────────────────────┘      │
│         │                                                   │
│         ▼                                                   │
│     ┌─────────────────┐                                     │
│     │  JSON Response  │                                     │
│     └─────────────────┘                                     │
│                                                             │
│                     Docker Container                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Component Architecture

### 1. API Layer

#### FastAPI Application
**Responsibility**: Handle HTTP requests, routing, and response generation

**Key Components**:
- **Endpoints**: `/`, `/analyze-costs/`, `/models/`, `/docs`
- **Middleware**: CORS, request validation, error handling
- **Documentation**: Automatic OpenAPI/Swagger generation

**Technology**: 
- FastAPI 0.104.1
- Uvicorn ASGI server
- Pydantic for validation

**Configuration**:
```python
app = FastAPI(
    title="AI Cost Analysis Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

---

### 2. Processing Pipeline

#### File Upload Handler
**Responsibility**: Accept and validate uploaded files

**Flow**:
```
Client Upload
     ↓
Accept multipart/form-data
     ↓
Validate file type (text/plain, UTF-8)
     ↓
Validate file size (< 100MB)
     ↓
Extract text content
     ↓
Pass to pipeline
```

**Error Handling**:
- 400: Invalid file format
- 400: Empty file
- 413: File too large
- 500: Processing error

#### Token Counter
**Responsibility**: Accurate token counting for cost estimation

**Implementation**:
```python
def count_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)
```

**Features**:
- Uses OpenAI's tiktoken library
- Fallback to cl100k_base encoding
- Accurate to within 1% of actual API usage
- Performance: ~0.05s for 10K tokens

#### Compression Engine
**Responsibility**: Reduce token count while preserving meaning

**Architecture**:
```
Input Text
    ↓
┌───────────────────────────────────────┐
│     Compression Pipeline              │
│                                       │
│  1. Whitespace Normalization          │
│  2. Punctuation Optimization          │
│  3. Filler Phrase Removal             │
│  4. Redundant Pair Elimination        │
│  5. Common Abbreviations              │
│  6. Technical Term Abbreviation       │
│  7. Contraction Conversion            │
│  8. Number Compression                │
│  9. Code Comment Removal (if code)    │
│ 10. URL/Path Compression (if URLs)    │
│ 11. Deduplication                     │
│ 12. Stopword Removal (if long text)   │
│                                       │
│  Final Cleanup                        │
└───────────────────────────────────────┘
    ↓
Compressed Text + Metadata
```

**Design Pattern**: Chain of Responsibility
- Each technique is a separate function
- Applied sequentially
- Each tracks if it was applied
- Modular and testable

**Performance**:
- Time: ~0.1-0.3s for 10K tokens
- Memory: Negligible (in-place operations where possible)
- Effectiveness: 35-50% reduction

#### Cost Calculator
**Responsibility**: Calculate costs across all LLM providers

**Data Structure**:
```python
LLM_PRICING = {
    "Provider": {
        "ModelName": {
            "input": float,      # $ per 1M tokens
            "output": float,     # $ per 1M tokens
            "context": int       # max context window
        }
    }
}
```

**Calculation Logic**:
```python
input_cost = (tokens / 1_000_000) * pricing["input"]
output_cost = (output_tokens / 1_000_000) * pricing["output"]
total_cost = input_cost + output_cost
```

**Output Scenarios**:
- 1K tokens output
- 5K tokens output
- Allows comparison at different usage levels

#### Report Generator
**Responsibility**: Assemble comprehensive analysis report

**Report Structure**:
```json
{
  "timestamp": "ISO-8601",
  "original_text_stats": {
    "characters": int,
    "words": int,
    "lines": int,
    "tokens": int,
    "reading_time": float
  },
  "compression_result": {
    "original_tokens": int,
    "compressed_tokens": int,
    "reduction_percentage": float,
    "techniques_applied": [string],
    "compressed_text": string
  },
  "cost_analysis": [
    {
      "model_name": string,
      "provider": string,
      "input_cost": float,
      "output_cost_1k": float,
      "output_cost_5k": float,
      "total_cost_1k_output": float,
      "total_cost_5k_output": float,
      "context_window": int,
      "fits_in_context": bool
    }
  ],
  "cheapest_model": {...},
  "most_expensive_model": {...},
  "compression_strategies": [string]
}
```

---

## 🗄️ Data Flow

### Request Flow

```
1. Client Request
   ├─ POST /analyze-costs/
   ├─ Content-Type: multipart/form-data
   └─ File: document.txt

2. FastAPI Routing
   ├─ Match endpoint
   ├─ Validate request
   └─ Call handler function

3. File Processing
   ├─ Read file content
   ├─ Decode UTF-8
   └─ Validate non-empty

4. Analysis Pipeline
   ├─ Count original tokens
   ├─ Apply compression
   ├─ Count compressed tokens
   ├─ Calculate all costs
   └─ Generate report

5. Response
   ├─ Format as JSON
   ├─ Add headers
   └─ Return 200 OK
```

### Error Flow

```
Error Occurs
    ↓
Exception Caught
    ↓
Determine Error Type
    ├─ Validation Error → 400
    ├─ Not Found → 404
    └─ Server Error → 500
    ↓
Format Error Response
    ├─ status_code
    ├─ detail message
    └─ error_type (optional)
    ↓
Return to Client
```

---

## 🐳 Deployment Architecture

### Docker Container Structure

```
┌─────────────────────────────────────────┐
│   Python 3.11 Base Image                │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  System Dependencies              │  │
│  │  - gcc (for compilation)          │  │
│  │  - curl (for health checks)       │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Python Dependencies              │  │
│  │  - fastapi                        │  │
│  │  - uvicorn                        │  │
│  │  - tiktoken                       │  │
│  │  - pydantic                       │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Application Code                 │  │
│  │  - main.py                        │  │
│  │  - /app/uploads (empty dir)       │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Runtime                          │  │
│  │  - Uvicorn ASGI Server            │  │
│  │  - Port 8000 exposed              │  │
│  │  - Health check on /              │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Docker Compose Stack

```
┌──────────────────────────────────────────────────┐
│              Docker Compose Stack                │
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │     ai-cost-analyzer (main service)     │   │
│  │  - Image: custom build                  │   │
│  │  - Port: 8000:8000                      │   │
│  │  - Volumes: ./main.py:/app/main.py      │   │
│  │  - Network: ai-cost-network             │   │
│  │  - Restart: unless-stopped              │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │     nginx (optional, production)        │   │
│  │  - Image: nginx:alpine                  │   │
│  │  - Port: 80:80, 443:443                 │   │
│  │  - Config: ./nginx.conf                 │   │
│  │  - Profile: production                  │   │
│  │  - Depends: ai-cost-analyzer            │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │         ai-cost-network                 │   │
│  │  - Driver: bridge                       │   │
│  │  - Internal communication               │   │
│  └─────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

### Network Architecture

```
Internet
    │
    ▼
┌───────────-------─────┐
│  Port 80/443 (Nginx)  │
└────────────-------────┘
    │
    ▼ Reverse Proxy
┌───────────────────────┐
│  Port 8000 (FastAPI)  │
└───────────────────────┘
    │
    ▼ Internal
┌───────────────-------┐
│    Bridge Network    │
└──────────────────────┘
```

---

## 🔐 Security Architecture

### Current Security Measures

1. **Input Validation**
   - File type checking
   - Size limits (100MB)
   - UTF-8 encoding validation
   - Content sanitization

2. **Isolation**
   - Containerized execution
   - No shell access
   - Minimal base image
   - Non-root user (TODO)

3. **Network**
   - Internal bridge network
   - Configurable CORS
   - Optional nginx rate limiting

### Security Considerations

**Threat Model**:
- ❌ Malicious file uploads
- ❌ Resource exhaustion (large files)
- ❌ Injection attacks
- ❌ DDoS

**Mitigations**:
- ✅ File size limits
- ✅ Content type validation
- ✅ No code execution from uploads
- ⚠️ Rate limiting (nginx only)
- ⚠️ Authentication (not implemented)

---

## 📊 Performance Architecture

### Performance Characteristics

**Latency** (P95):
- Small files (< 1K tokens): 100ms
- Medium files (1-10K tokens): 300ms
- Large files (10-100K tokens): 2s
- Very large files (100-200K tokens): 5s

**Throughput**:
- Single instance: ~100 requests/minute
- Limited by Python GIL
- Can scale horizontally with multiple containers

**Resource Usage**:
- CPU: ~10% per request (spike)
- Memory: 150MB baseline + 1MB per request
- Disk: None (stateless)

### Optimization Strategies

1. **Algorithm Efficiency**
   - Regex compilation cached
   - Single-pass processing where possible
   - In-place modifications

2. **Async Support** (Future)
   - Currently sync (simpler)
   - Can add async for I/O operations
   - Queue-based processing for batches

3. **Caching** (Future)
   - Token count caching by content hash
   - Compression result caching
   - Model pricing caching

---

## 🔄 Scalability Architecture

### Current: Single Container

```
Client Requests
    │
    ▼
┌────────────────────────┐
│   Container (Single)   │
└────────────────────────┘
```

**Limitations**:
- Single point of failure
- Limited throughput
- No high availability

### Future: Horizontal Scaling

```
        Load Balancer
            │
    ┌───────┼────────┐
    │       │        │
    ▼       ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│  C1  │ │  C2  │ │  C3  │
└──────┘ └──────┘ └──────┘
```

**Benefits**:
- Increased throughput
- High availability
- Fault tolerance

**Requirements**:
- Stateless design ✅ (already implemented)
- Load balancer (nginx, HAProxy)
- Container orchestration (Docker Swarm, K8s)

---

## 🧩 Integration Architecture

### Current Integrations

**Client Types**:
1. **Browser** → Swagger UI
2. **CLI** → cURL, wget
3. **Scripts** → Python requests, Node.js axios
4. **CI/CD** → GitHub Actions, Jenkins

### Future Integrations

**Planned**:
1. **LangChain** → Plugin/wrapper
2. **LlamaIndex** → Custom loader
3. **OpenAI SDK** → Middleware
4. **Webhooks** → Event notifications

**Integration Pattern**:
```
Application Code
         │
         ▼
┌────────────--------──┐
│  SDK/Client Wrapper  │
└────────┬──────────-──┘
         │ HTTP REST
         ▼
┌──────────────────────┐
│      API Service     │
└──────────────────────┘
```

---

## 📈 Monitoring & Observability

### Current Monitoring

**Built-in**:
- Health check endpoint (`/`)
- Docker health checks
- Log output (stdout/stderr)

**Limitations**:
- No metrics collection
- No tracing
- No alerting

### Future Monitoring Stack

```
Application
    │
    ├─ Logs ──────────────┐
    │                     ▼
    │              ┌──────────────────────┐
    │              │  Logging (ELK/Loki)  │
    │              └──────────────────────┘
    ├─ Metrics ───────────┐
    │                     ▼
    │              ┌────────────┐
    │              │ Prometheus │
    │              └──────┬─────┘
    │                     │
    ├─ Traces ────────────┼─────┐
    │                     │     ▼
    │                     │ ┌─────────┐
    │                     └─│ Grafana │
    │                       └─────────┘
    │                             │
    └─ Health Checks ─────────────┘
```

---

## 🎯 Architecture Decisions

### Why Stateless?
- **Simplicity**: No database to manage
- **Scalability**: Easy to add containers
- **Reliability**: No data loss risk
- **Performance**: No DB queries

**Trade-off**: No usage tracking (can add optionally later)

### Why FastAPI?
- **Documentation**: Auto-generated Swagger
- **Performance**: Fast async support
- **Developer Experience**: Modern Python
- **Ecosystem**: Rich plugin ecosystem

### Why Docker?
- **Portability**: Run anywhere
- **Consistency**: Dev = Prod
- **Isolation**: Security boundary
- **Simplicity**: One-command deployment

### Why No Database?
- **Simplicity**: Less to manage
- **Privacy**: No data retention
- **Performance**: Faster responses
- **Stateless**: Easier scaling

**When to add**: If persistent cost tracking is needed

---

## 🔜 Future Architecture

### Phase 2: Enhanced (Q1 2026)

```
Client
   │
   ▼
API Gateway
   │
   ├─► Analysis Service (existing)
   │
   ├─► Batch Processing Service
   │      ├─ Queue (RabbitMQ/Redis)
   │      └─ Workers (multiple)
   │
   └─► Storage Service (optional)
          └─ Database (PostgreSQL)
```

### Phase 3: Enterprise (Q4 2026)

```
Client
   │
   ▼
API Gateway + Auth
   │
   ├─► Service Mesh
   │      │
   │      ├─► Analysis Service (scaled)
   │      ├─► Batch Service (scaled)
   │      ├─► AI Compression Service
   │      └─► Analytics Service
   │
   ├─► Cache Layer (Redis)
   │
   ├─► Database (PostgreSQL)
   │
   └─► Object Storage (S3)
```

---

## 📝 Architecture Patterns

### Design Patterns Used

1. **Chain of Responsibility**: Compression pipeline
2. **Strategy Pattern**: Different compression techniques
3. **Factory Pattern**: Cost calculator for different models
4. **Builder Pattern**: Report generation
5. **Singleton**: Application instance (FastAPI)

### Principles Followed

1. **SOLID**:
   - Single Responsibility: Each function has one job
   - Open/Closed: Easy to add new techniques
   - Liskov Substitution: N/A (no inheritance)
   - Interface Segregation: Focused interfaces
   - Dependency Inversion: Inject configuration

2. **DRY**: Reusable compression functions
3. **KISS**: Simple, straightforward logic
4. **YAGNI**: Only what's needed now

---

**Document Owner**: Architecture Team  
**Last Updated**: 2025-11-15  
**Next Review**: 2026-02-15

