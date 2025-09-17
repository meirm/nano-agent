#!/usr/bin/env python3
"""
Performance monitoring hook for nano-agent.

This hook tracks execution metrics, token usage, and performance statistics.
It runs after agent completion and logs performance data for analysis.

Usage:
    - Place in ~/.nano-cli/hooks/
    - Configure in hooks.json to run on post_agent_complete or agent_response events
    - Always returns 0 (non-blocking) as it's for monitoring only
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Main performance monitoring logic."""
    try:
        # Read event data from stdin
        input_data = sys.stdin.read()
        event_data = json.loads(input_data)

        # Extract performance metrics
        execution_time = event_data.get("execution_time", 0)
        token_usage = event_data.get("token_usage", {})
        model = event_data.get("model", "unknown")
        provider = event_data.get("provider", "unknown")
        context = event_data.get("context", "cli")
        event = event_data.get("event", "unknown")

        # Create metrics record
        metrics = {
            "timestamp": event_data.get("timestamp", datetime.now().isoformat()),
            "event": event,
            "context": context,
            "model": model,
            "provider": provider,
            "execution_time_seconds": execution_time,
            "token_usage": token_usage,
        }

        # Add event-specific metrics
        if event == "post_agent_complete":
            prompt = event_data.get("prompt", "")
            response = event_data.get("agent_response", "")
            metrics.update({
                "prompt_length": len(prompt),
                "response_length": len(response),
                "session_id": event_data.get("session_id"),
                "message_count": event_data.get("message_count"),
            })
        elif event == "post_tool_use":
            tool_name = event_data.get("tool_name", "")
            tool_result = event_data.get("tool_result", "")
            metrics.update({
                "tool_name": tool_name,
                "tool_result_length": len(str(tool_result)),
            })
        elif event == "agent_error" or event == "tool_error":
            error = event_data.get("error", "")
            metrics.update({
                "error": error[:200] if error else None,  # Truncate long errors
            })

        # Calculate token costs (example rates - adjust for your providers)
        cost = calculate_cost(token_usage, model, provider)
        if cost is not None:
            metrics["estimated_cost_usd"] = cost

        # Performance analysis
        performance_analysis = analyze_performance(metrics)
        metrics["performance_analysis"] = performance_analysis

        # Save metrics to file
        save_metrics(metrics)

        # Print summary to stdout
        print_summary(metrics)

        # Check for performance issues and emit warnings
        check_performance_thresholds(metrics)

        return 0  # Always return success (non-blocking)

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON input: {e}", file=sys.stderr)
        return 0  # Non-blocking
    except Exception as e:
        print(f"ERROR: Performance monitor failed: {e}", file=sys.stderr)
        return 0  # Non-blocking


def calculate_cost(token_usage, model, provider):
    """
    Calculate estimated cost based on token usage.

    These are example rates - update with actual provider pricing.
    """
    if not token_usage:
        return None

    input_tokens = token_usage.get("prompt_tokens", 0)
    output_tokens = token_usage.get("completion_tokens", 0)

    # Example pricing (per 1M tokens)
    pricing = {
        "openai": {
            "gpt-5-nano": {"input": 0.15, "output": 0.60},
            "gpt-5-mini": {"input": 0.30, "output": 1.20},
            "gpt-5": {"input": 2.50, "output": 10.00},
        },
        "anthropic": {
            "claude-3-haiku": {"input": 0.25, "output": 1.25},
            "claude-3-sonnet": {"input": 3.00, "output": 15.00},
            "claude-3-opus": {"input": 15.00, "output": 75.00},
        },
        "ollama": {
            "default": {"input": 0.00, "output": 0.00},  # Local models
        },
    }

    # Get pricing for model/provider
    provider_pricing = pricing.get(provider, {})
    model_pricing = provider_pricing.get(model, provider_pricing.get("default", {}))

    if not model_pricing:
        return None

    # Calculate cost
    input_cost = (input_tokens / 1_000_000) * model_pricing.get("input", 0)
    output_cost = (output_tokens / 1_000_000) * model_pricing.get("output", 0)

    return round(input_cost + output_cost, 6)


def analyze_performance(metrics):
    """
    Analyze performance metrics and generate insights.
    """
    analysis = {}

    execution_time = metrics.get("execution_time_seconds", 0)
    token_usage = metrics.get("token_usage", {})

    # Execution time analysis
    if execution_time > 0:
        if execution_time < 1:
            analysis["speed"] = "fast"
        elif execution_time < 5:
            analysis["speed"] = "normal"
        elif execution_time < 15:
            analysis["speed"] = "slow"
        else:
            analysis["speed"] = "very_slow"

        # Tokens per second (if available)
        total_tokens = token_usage.get("total_tokens", 0)
        if total_tokens > 0:
            tokens_per_second = total_tokens / execution_time
            analysis["tokens_per_second"] = round(tokens_per_second, 2)

    # Token efficiency
    if token_usage:
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)

        if prompt_tokens > 0 and completion_tokens > 0:
            efficiency = completion_tokens / prompt_tokens
            analysis["token_efficiency"] = round(efficiency, 2)

            if efficiency < 0.5:
                analysis["efficiency_rating"] = "low"
            elif efficiency < 2:
                analysis["efficiency_rating"] = "normal"
            else:
                analysis["efficiency_rating"] = "high"

    return analysis


def save_metrics(metrics):
    """
    Save metrics to a JSON lines file for later analysis.
    """
    metrics_dir = os.path.expanduser("~/.nano-cli/metrics")
    os.makedirs(metrics_dir, exist_ok=True)

    # Use date-based file naming for easy rotation
    date_str = datetime.now().strftime("%Y-%m-%d")
    metrics_file = os.path.join(metrics_dir, f"performance_{date_str}.jsonl")

    try:
        with open(metrics_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")
    except Exception as e:
        print(f"WARNING: Failed to save metrics: {e}", file=sys.stderr)


def print_summary(metrics):
    """
    Print a concise summary of performance metrics.
    """
    execution_time = metrics.get("execution_time_seconds", 0)
    token_usage = metrics.get("token_usage", {})
    cost = metrics.get("estimated_cost_usd")
    analysis = metrics.get("performance_analysis", {})

    summary_parts = [
        f"Performance: {execution_time:.2f}s",
    ]

    if token_usage:
        total_tokens = token_usage.get("total_tokens", 0)
        summary_parts.append(f"Tokens: {total_tokens}")

    if cost is not None:
        summary_parts.append(f"Cost: ${cost:.4f}")

    if analysis.get("tokens_per_second"):
        summary_parts.append(f"Speed: {analysis['tokens_per_second']:.1f} tok/s")

    if analysis.get("speed"):
        summary_parts.append(f"Rating: {analysis['speed']}")

    print(" | ".join(summary_parts), file=sys.stdout)


def check_performance_thresholds(metrics):
    """
    Check for performance issues and emit warnings.
    """
    # Define thresholds
    MAX_EXECUTION_TIME = 30  # seconds
    MAX_TOKENS = 8000
    MAX_COST = 0.50  # USD

    warnings = []

    execution_time = metrics.get("execution_time_seconds", 0)
    if execution_time > MAX_EXECUTION_TIME:
        warnings.append(f"Execution time ({execution_time:.1f}s) exceeds threshold ({MAX_EXECUTION_TIME}s)")

    token_usage = metrics.get("token_usage", {})
    total_tokens = token_usage.get("total_tokens", 0)
    if total_tokens > MAX_TOKENS:
        warnings.append(f"Token usage ({total_tokens}) exceeds threshold ({MAX_TOKENS})")

    cost = metrics.get("estimated_cost_usd")
    if cost is not None and cost > MAX_COST:
        warnings.append(f"Cost (${cost:.4f}) exceeds threshold (${MAX_COST:.2f})")

    # Print warnings
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())