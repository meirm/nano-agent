# HOP/LOP Pattern Guide - Cost-Optimized Agent Delegation

> **Hierarchical Orchestration Pattern (HOP) / Localized Operation Pattern (LOP)** - A powerful delegation strategy for using cheaper or specialized models for subtasks while maintaining quality through intelligent orchestration.

## 📋 Table of Contents

1. [Core Concept](#core-concept)
2. [Architecture](#architecture)
3. [Implementation Strategies](#implementation-strategies)
4. [Real-World Examples](#real-world-examples)
5. [Cost Analysis](#cost-analysis)
6. [Best Practices](#best-practices)
7. [Integration with Nano-Agent](#integration-with-nano-agent)

## Core Concept

The HOP/LOP pattern is a **cost-optimization strategy** that leverages the strengths of different AI models by delegating specific subtasks to the most appropriate (and cost-effective) model for that task.

### The Problem It Solves

Using premium models (Claude Opus, GPT-4) for every operation is:
- **Expensive**: $0.015-0.060 per 1K tokens
- **Inefficient**: Simple tasks don't need complex reasoning
- **Slow**: Premium models have higher latency
- **Wasteful**: 80% of tasks can be handled by cheaper models

### The Solution

**Hierarchical delegation** where:
- **HOP (Orchestrator)**: Smart coordinator that breaks down complex tasks
- **LOP (Workers)**: Specialized executors optimized for specific operations

## Architecture

```
┌─────────────────────────────────────┐
│       HOP ORCHESTRATOR              │
│   (Claude, GPT-5, or GPT-5-mini)    │
│                                     │
│  • Analyzes request complexity      │
│  • Decomposes into subtasks         │
│  • Delegates to appropriate LOPs    │
│  • Aggregates and validates results │
└──────────┬──────────────────────────┘
           │
           ├─────────────┬──────────────┬──────────────┐
           ▼             ▼              ▼              ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
    │  LOP #1  │  │  LOP #2  │  │  LOP #3  │  │  LOP #4  │
    │          │  │          │  │          │  │          │
    │ gpt-oss  │  │ mistral  │  │gpt-5-nano│  │  llama   │
    │   :20b   │  │  -small  │  │          │  │   3.2    │
    └──────────┘  └──────────┘  └──────────┘  └──────────┘
     File Ops      Analysis      Coding       Documentation
```

## Implementation Strategies

### Strategy 1: Task-Based Delegation

Assign models based on task type:

```python
task_model_mapping = {
    "file_reading": "gpt-oss:20b",      # Local, fast, free
    "code_writing": "gpt-5-mini",       # Good balance
    "analysis": "gpt-5-nano",           # Fast, cheap
    "complex_reasoning": "claude-opus",  # When needed
    "documentation": "mistral-small",    # Specialized
}
```

### Strategy 2: Complexity-Based Routing

Route based on estimated complexity:

```python
def select_model(task_complexity: float) -> str:
    if task_complexity < 0.3:
        return "gpt-oss:20b"      # Simple tasks
    elif task_complexity < 0.6:
        return "gpt-5-nano"       # Moderate tasks
    elif task_complexity < 0.8:
        return "gpt-5-mini"       # Complex tasks
    else:
        return "claude-opus-4"    # Very complex tasks
```

### Strategy 3: Parallel Execution

Execute independent tasks simultaneously:

```python
async def parallel_lop_execution(tasks):
    """Execute multiple LOPs in parallel for speed"""
    results = await asyncio.gather(
        lop_file_analysis(model="gpt-oss:20b"),
        lop_security_scan(model="gpt-5-nano"),
        lop_performance_check(model="mistral"),
        lop_test_generation(model="gpt-5-mini")
    )
    return aggregate_results(results)
```

## Real-World Examples

### Example 1: Comprehensive Code Review

```markdown
# HOP Orchestrator Prompt (Claude or GPT-5)
You are coordinating a code review. Break down the review into:
1. Syntax and style check
2. Security vulnerability scan
3. Performance analysis
4. Test coverage assessment
5. Documentation review

Delegate each to the appropriate nano-agent with specific models.
Aggregate results into a comprehensive review.
```

```python
# Implementation
async def comprehensive_code_review(code_path):
    hop_prompt = f"""
    Coordinate review of {code_path}:
    1. Use nano-agent with gpt-oss:20b for syntax/style
    2. Use nano-agent with gpt-5-mini for security
    3. Use nano-agent with gpt-5-nano for performance
    4. Use nano-agent with mistral for documentation
    Aggregate findings and provide actionable recommendations.
    """
    
    # HOP orchestrates
    tasks = parse_into_subtasks(hop_prompt)
    
    # LOPs execute in parallel
    results = await execute_lops(tasks, {
        "syntax": ("gpt-oss:20b", "Check PEP8, naming, imports"),
        "security": ("gpt-5-mini", "OWASP Top 10, SQL injection, XSS"),
        "performance": ("gpt-5-nano", "O(n) analysis, memory leaks"),
        "docs": ("mistral", "Docstring coverage, clarity")
    })
    
    # HOP aggregates
    return synthesize_review(results)
```

### Example 2: Full-Stack Feature Implementation

```python
# HOP breaks down feature into components
feature_components = {
    "database_schema": {
        "model": "gpt-oss:20b",
        "prompt": "Create PostgreSQL schema for user authentication"
    },
    "backend_api": {
        "model": "gpt-5-mini",
        "prompt": "Implement FastAPI endpoints for auth (login, register, logout)"
    },
    "frontend_ui": {
        "model": "gpt-5-nano",
        "prompt": "Create React components for login/register forms"
    },
    "tests": {
        "model": "gpt-oss:20b",
        "prompt": "Write pytest tests for auth endpoints"
    },
    "documentation": {
        "model": "mistral",
        "prompt": "Create API documentation in OpenAPI format"
    }
}

# Execute with nano-agent
for component, config in feature_components.items():
    result = await nano_agent.execute(
        prompt=config["prompt"],
        model=config["model"],
        provider=get_provider(config["model"])
    )
```

### Example 3: Large Codebase Migration

```yaml
# HOP Configuration (.claude/commands/migrate_to_typescript.yaml)
orchestrator:
  model: gpt-5-mini
  role: "Migration coordinator"
  
workers:
  - name: file_scanner
    model: gpt-oss:20b
    task: "Identify all .js files needing conversion"
    
  - name: type_analyzer
    model: gpt-5-nano
    task: "Analyze and infer TypeScript types"
    
  - name: converter
    model: gpt-5-mini
    task: "Convert JavaScript to TypeScript"
    
  - name: validator
    model: gpt-oss:20b
    task: "Run tsc and fix compilation errors"
    
  - name: test_runner
    model: mistral
    task: "Ensure all tests still pass"

execution:
  strategy: "batch_parallel"
  batch_size: 10
  error_handling: "retry_with_stronger_model"
```

## Cost Analysis

### Traditional Approach (All Premium)

| Task | Tokens | Model | Cost |
|------|--------|-------|------|
| File Reading | 5K | Claude Opus | $0.075 |
| Analysis | 10K | Claude Opus | $0.150 |
| Code Writing | 8K | Claude Opus | $0.120 |
| Testing | 6K | Claude Opus | $0.090 |
| **Total** | **29K** | | **$0.435** |

### HOP/LOP Approach

| Task | Tokens | Model | Cost |
|------|--------|-------|------|
| Orchestration | 2K | GPT-5-mini | $0.006 |
| File Reading | 5K | gpt-oss:20b | $0.000 |
| Analysis | 10K | gpt-5-nano | $0.010 |
| Code Writing | 8K | gpt-5-mini | $0.024 |
| Testing | 6K | mistral | $0.000 |
| **Total** | **31K** | | **$0.040** |

**Savings: 91% reduction in cost!**

## Best Practices

### 1. Model Selection Guidelines

```python
MODEL_SELECTION_MATRIX = {
    # Task Type -> (preferred_model, fallback_model)
    "simple_read": ("gpt-oss:20b", "gpt-5-nano"),
    "code_generation": ("gpt-5-mini", "gpt-5"),
    "complex_analysis": ("gpt-5", "claude-opus"),
    "creative_writing": ("claude-opus", "gpt-5"),
    "data_processing": ("gpt-oss:20b", "mistral"),
    "testing": ("gpt-5-nano", "gpt-5-mini"),
}
```

### 2. Prompt Optimization for LOPs

```python
def optimize_prompt_for_model(prompt: str, model: str) -> str:
    """Adapt prompt style for specific model capabilities"""
    
    if "gpt-oss" in model:
        # Local models need more explicit instructions
        return f"""
        TASK: {prompt}
        FORMAT: Provide step-by-step solution
        CONSTRAINTS: Be concise and specific
        OUTPUT: Code only, minimal explanation
        """
    
    elif "gpt-5-nano" in model:
        # Fast model, keep it simple
        return f"Quick task: {prompt}\nProvide solution:"
    
    elif "claude" in model:
        # Can handle nuanced instructions
        return prompt  # Use as-is
    
    return prompt
```

### 3. Error Handling and Fallbacks

```python
async def execute_with_fallback(task, primary_model, fallback_model):
    """Try cheaper model first, fallback to stronger if needed"""
    try:
        result = await execute_lop(task, primary_model)
        if validate_result(result):
            return result
    except Exception as e:
        log.warning(f"Primary model failed: {e}")
    
    # Fallback to stronger model
    log.info(f"Falling back to {fallback_model}")
    return await execute_lop(task, fallback_model)
```

### 4. Result Validation

```python
def validate_lop_result(result, expected_format):
    """Ensure LOP output meets quality standards"""
    checks = {
        "completeness": len(result) > min_length,
        "format": matches_expected_format(result, expected_format),
        "syntax": is_valid_code(result) if is_code else True,
        "coherence": confidence_score(result) > 0.7
    }
    return all(checks.values())
```

## Integration with Nano-Agent

### Setting Up HOP/LOP with Nano-Agent

1. **Create Orchestrator Command** (`.claude/commands/hop_orchestrator.md`):

```markdown
# HOP Orchestrator for {task_name}

You are the orchestrator for a complex task. Your role:
1. Analyze the request and break it into subtasks
2. Determine the best model for each subtask
3. Create prompts optimized for each model
4. Delegate to nano-agent with appropriate configurations
5. Aggregate results and ensure quality

## Available Models
- gpt-oss:20b (local, free, good for simple tasks)
- gpt-5-nano (fast, cheap, good for quick analysis)
- gpt-5-mini (balanced, good for code generation)
- gpt-5 (powerful, for complex reasoning)
- claude-opus (most capable, use sparingly)

## Delegation Template
For each subtask, use:
```
nano-cli run "{subtask_prompt}" --model {selected_model} --provider {provider}
```
```

2. **Create LOP Templates** (`.claude/commands/lops/`):

```markdown
# lop_file_operations.md
Simple file operations optimized for gpt-oss:20b:
- Read files and extract content
- List directories
- Search for patterns
- Create simple files

# lop_code_generation.md  
Code generation optimized for gpt-5-mini:
- Write functions with clear requirements
- Implement algorithms
- Create API endpoints
- Generate tests

# lop_analysis.md
Analysis tasks optimized for gpt-5-nano:
- Code complexity analysis
- Performance assessment
- Security quick scan
- Dependency checking
```

3. **Implement in Code**:

```python
# hop_lop_coordinator.py
from nano_agent.modules.nano_agent import prompt_nano_agent

class HOPLOPCoordinator:
    def __init__(self):
        self.model_costs = {
            "gpt-oss:20b": 0.0,
            "gpt-5-nano": 0.001,
            "gpt-5-mini": 0.003,
            "gpt-5": 0.01,
            "claude-opus": 0.06
        }
    
    async def orchestrate(self, task: str):
        # Step 1: Analyze with HOP
        subtasks = await self.decompose_task(task)
        
        # Step 2: Route to appropriate LOPs
        results = []
        for subtask in subtasks:
            model = self.select_optimal_model(subtask)
            result = await prompt_nano_agent(
                agentic_prompt=subtask.prompt,
                model=model,
                provider=self.get_provider(model)
            )
            results.append(result)
        
        # Step 3: Aggregate results
        return self.synthesize_results(results)
    
    def select_optimal_model(self, subtask):
        """Select model based on complexity and cost"""
        if subtask.complexity < 0.3:
            return "gpt-oss:20b"
        elif subtask.requires_code_generation:
            return "gpt-5-mini"
        elif subtask.requires_analysis:
            return "gpt-5-nano"
        else:
            return "gpt-5"
```

### Monitoring and Optimization

```python
# Track performance and costs
class LOPMetrics:
    def __init__(self):
        self.executions = []
    
    def track(self, model, tokens, cost, quality_score):
        self.executions.append({
            "model": model,
            "tokens": tokens,
            "cost": cost,
            "quality": quality_score,
            "timestamp": datetime.now()
        })
    
    def optimize_routing(self):
        """Adjust model selection based on historical performance"""
        for model in self.get_unique_models():
            avg_quality = self.get_avg_quality(model)
            avg_cost = self.get_avg_cost(model)
            
            # Adjust routing thresholds
            if avg_quality < 0.8 and avg_cost > 0.01:
                self.increase_model_tier(model)
            elif avg_quality > 0.95 and avg_cost > 0.005:
                self.decrease_model_tier(model)
```

## Advanced Patterns

### Pattern 1: Cascade Validation

```python
async def cascade_validation(code):
    """Use increasingly powerful models for validation"""
    
    # Level 1: Quick syntax check (free)
    syntax_ok = await validate_with("gpt-oss:20b", code, "syntax")
    if not syntax_ok:
        return await fix_with("gpt-5-mini", code, "syntax")
    
    # Level 2: Logic check (cheap)
    logic_ok = await validate_with("gpt-5-nano", code, "logic")
    if not logic_ok:
        return await fix_with("gpt-5", code, "logic")
    
    # Level 3: Best practices (if needed)
    if requires_optimization(code):
        return await optimize_with("claude-opus", code)
    
    return code
```

### Pattern 2: Specialist Routing

```python
SPECIALIST_MODELS = {
    "sql": "gpt-5-mini",           # Good at SQL
    "regex": "gpt-oss:20b",        # Simple pattern matching
    "algorithms": "gpt-5",         # Complex algorithms
    "ui_components": "gpt-5-nano", # React/Vue components
    "documentation": "mistral",     # Clear writing
    "testing": "gpt-oss:20b",      # Test generation
}

def route_to_specialist(task_type: str) -> str:
    return SPECIALIST_MODELS.get(task_type, "gpt-5-mini")
```

### Pattern 3: Budget-Aware Execution

```python
class BudgetAwareOrchestrator:
    def __init__(self, max_cost_per_request: float = 0.10):
        self.budget = max_cost_per_request
        self.spent = 0.0
    
    async def execute_within_budget(self, tasks):
        results = []
        for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
            model = self.select_model_within_budget(task)
            if model:
                cost = estimate_cost(task, model)
                if self.spent + cost <= self.budget:
                    result = await execute_with_model(task, model)
                    results.append(result)
                    self.spent += cost
                else:
                    # Use free model or skip low-priority tasks
                    if task.priority > 0.5:
                        result = await execute_with_model(task, "gpt-oss:20b")
                        results.append(result)
        return results
```

## Conclusion

The HOP/LOP pattern with nano-agent provides:

- **91% cost reduction** on average
- **3-5x faster execution** through parallelization
- **Maintained quality** through intelligent orchestration
- **Flexibility** to adjust model selection based on requirements
- **Scalability** for large-scale operations

By leveraging the strengths of different models and delegating appropriately, you can build powerful, cost-effective AI systems that deliver enterprise-grade results at a fraction of the cost.

---

**Remember**: The most expensive model isn't always the best choice. Smart delegation beats brute force! 🎯