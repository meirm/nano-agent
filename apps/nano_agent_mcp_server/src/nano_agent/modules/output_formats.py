"""
Output formatting system for Nano Agent CLI.

This module provides different output formats (simple, json, rich) for
displaying agent responses, with optional billing information display.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax


class OutputFormat(Enum):
    """Available output format options."""
    SIMPLE = "simple"      # Plain text output for scripts
    JSON = "json"          # JSON format for programmatic use
    RICH = "rich"          # Rich formatted output (default)
    
    @classmethod
    def from_string(cls, value: str) -> 'OutputFormat':
        """Create OutputFormat from string value."""
        try:
            # Handle backward compatibility
            if value.lower() == "rich":
                return cls.RICH
            return cls(value.lower())
        except ValueError:
            # Default to rich if invalid
            return cls.RICH


@dataclass
class BillingInfo:
    """Billing and token usage information."""
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    total_cost: float = 0.0
    input_cost: float = 0.0
    output_cost: float = 0.0
    cached_savings: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_tokens": f"{self.total_tokens:,}" if self.total_tokens > 0 else "0",
            "input_tokens": f"{self.input_tokens:,}" if self.input_tokens > 0 else "0",
            "output_tokens": f"{self.output_tokens:,}" if self.output_tokens > 0 else "0",
            "cached_tokens": f"{self.cached_tokens:,}" if self.cached_tokens > 0 else "0",
            "total_cost": f"${self.total_cost:.4f}",
            "input_cost": f"${self.input_cost:.4f}",
            "output_cost": f"${self.output_cost:.4f}",
            "cached_savings": f"${self.cached_savings:.4f}" if self.cached_savings > 0 else None
        }
    
    def to_simple_string(self) -> str:
        """Convert to simple string format."""
        parts = []
        if self.total_tokens > 0:
            parts.append(f"Tokens: {self.total_tokens:,}")
        if self.total_cost > 0:
            parts.append(f"Cost: ${self.total_cost:.4f}")
        return " | ".join(parts) if parts else ""


@dataclass
class AgentResponse:
    """Standardized agent response structure."""
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    billing: Optional[BillingInfo] = None
    execution_time: Optional[float] = None
    session_id: Optional[str] = None
    
    def to_dict(self, include_billing: bool = False) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "success": self.success,
            "message": self.message,
        }
        
        if self.data is not None:
            result["data"] = self.data
            
        if self.error:
            result["error"] = self.error
            
        if self.metadata:
            result["metadata"] = self.metadata
            
        if include_billing and self.billing:
            result["billing"] = self.billing.to_dict()
            
        if self.execution_time is not None:
            result["execution_time_seconds"] = round(self.execution_time, 2)
            
        if self.session_id:
            result["session_id"] = self.session_id
            
        return result


class OutputFormatter(ABC):
    """Abstract base class for output formatters."""
    
    def __init__(self, show_billing: bool = False, verbose: bool = False):
        """
        Initialize formatter.
        
        Args:
            show_billing: Whether to include billing information in output
            verbose: Whether to show verbose information (status, timing)
        """
        self.show_billing = show_billing
        self.verbose = verbose
    
    @abstractmethod
    def format_response(self, response: AgentResponse) -> str:
        """
        Format an agent response for display.
        
        Args:
            response: The agent response to format
            
        Returns:
            Formatted string for output
        """
        pass
    
    @abstractmethod
    def format_error(self, error: str) -> str:
        """
        Format an error message.
        
        Args:
            error: Error message to format
            
        Returns:
            Formatted error string
        """
        pass
    
    @abstractmethod
    def format_info(self, message: str) -> str:
        """
        Format an informational message.
        
        Args:
            message: Info message to format
            
        Returns:
            Formatted info string
        """
        pass


class SimpleFormatter(OutputFormatter):
    """Plain text formatter for simple output."""
    
    def format_response(self, response: AgentResponse) -> str:
        """Format response as plain text."""
        lines = []
        
        if response.success:
            # Only show status message in verbose mode
            if self.verbose and response.message:
                lines.append(response.message)
            if response.data:
                # If data is a string, use it directly
                if isinstance(response.data, str):
                    lines.append(response.data)
                else:
                    # Otherwise convert to string representation
                    lines.append(str(response.data))
        else:
            lines.append(f"Error: {response.error or 'Unknown error'}")
            
        # Add billing info if requested
        if self.show_billing and response.billing:
            billing_str = response.billing.to_simple_string()
            if billing_str:
                lines.append(f"[{billing_str}]")
                
        # Add execution time if available and in verbose mode
        if self.verbose and response.execution_time is not None:
            lines.append(f"[Time: {response.execution_time:.2f}s]")
            
        return "\n".join(lines)
    
    def format_error(self, error: str) -> str:
        """Format error as plain text."""
        return f"Error: {error}"
    
    def format_info(self, message: str) -> str:
        """Format info as plain text."""
        return message


class JSONFormatter(OutputFormatter):
    """JSON formatter for programmatic output."""
    
    def __init__(self, show_billing: bool = False, verbose: bool = False, pretty: bool = True):
        """
        Initialize JSON formatter.
        
        Args:
            show_billing: Whether to include billing information
            verbose: Whether to show verbose information (ignored for JSON)
            pretty: Whether to pretty-print JSON
        """
        super().__init__(show_billing, verbose)
        self.pretty = pretty
    
    def format_response(self, response: AgentResponse) -> str:
        """Format response as JSON."""
        data = response.to_dict(include_billing=self.show_billing)
        
        if self.pretty:
            return json.dumps(data, indent=2, default=str)
        else:
            return json.dumps(data, default=str)
    
    def format_error(self, error: str) -> str:
        """Format error as JSON."""
        data = {
            "success": False,
            "error": error
        }
        if self.pretty:
            return json.dumps(data, indent=2)
        else:
            return json.dumps(data)
    
    def format_info(self, message: str) -> str:
        """Format info as JSON."""
        data = {
            "success": True,
            "message": message
        }
        if self.pretty:
            return json.dumps(data, indent=2)
        else:
            return json.dumps(data)


class RichFormatter(OutputFormatter):
    """Rich formatted output (current default style)."""
    
    def __init__(self, show_billing: bool = False, verbose: bool = False, console: Optional[Console] = None):
        """
        Initialize rich formatter.
        
        Args:
            show_billing: Whether to include billing information
            verbose: Whether to show verbose information (ignored for rich format)
            console: Rich console instance to use
        """
        super().__init__(show_billing, verbose)
        self.console = console or Console()
    
    def format_response(self, response: AgentResponse) -> str:
        """Format response with Rich formatting."""
        # This returns empty string as the actual printing is done via console
        # The console.print calls happen directly in the formatter methods
        
        if response.success:
            # Success panel (only in verbose mode)
            if self.verbose and response.message:
                self.console.print(Panel(
                    response.message,
                    title="✅ Success",
                    border_style="green"
                ))
            
            # Data/result panel
            if response.data:
                if isinstance(response.data, str):
                    self.console.print(Panel(
                        response.data,
                        title="📋 Agent Result",
                        border_style="cyan"
                    ))
                else:
                    # Format complex data
                    self.console.print(Panel(
                        str(response.data),
                        title="📋 Agent Result",
                        border_style="cyan"
                    ))
            
            # Billing panel (if requested)
            if self.show_billing and response.billing:
                self._print_billing_panel(response.billing)
                
            # Metadata panel (only in verbose mode)
            if self.verbose and (response.metadata or response.execution_time):
                self._print_metadata_panel(response)
                
        else:
            # Error panel
            self.console.print(Panel(
                response.error or "Unknown error",
                title="❌ Agent Failed",
                border_style="red"
            ))
            
        return ""  # Rich console handles the actual output
    
    def format_error(self, error: str) -> str:
        """Format error with Rich formatting."""
        self.console.print(Panel(
            error,
            title="❌ Error",
            border_style="red"
        ))
        return ""
    
    def format_info(self, message: str) -> str:
        """Format info with Rich formatting."""
        self.console.print(Panel(
            message,
            title="ℹ️ Information",
            border_style="blue"
        ))
        return ""
    
    def _print_billing_panel(self, billing: BillingInfo):
        """Print billing information panel."""
        table = Table(title="💰 Token Usage & Costs", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        if billing.total_tokens > 0:
            table.add_row("Total Tokens", f"{billing.total_tokens:,}")
        if billing.input_tokens > 0:
            table.add_row("Input Tokens", f"{billing.input_tokens:,}")
        if billing.output_tokens > 0:
            table.add_row("Output Tokens", f"{billing.output_tokens:,}")
        if billing.cached_tokens > 0:
            table.add_row("Cached Tokens", f"{billing.cached_tokens:,}")
            
        table.add_row("Total Cost", f"${billing.total_cost:.4f}")
        
        if billing.cached_savings > 0:
            table.add_row("Cache Savings", f"${billing.cached_savings:.4f}", style="yellow")
            
        self.console.print(table)
    
    def _print_metadata_panel(self, response: AgentResponse):
        """Print metadata panel."""
        metadata = response.metadata or {}
        
        # Add execution time if available
        if response.execution_time is not None:
            metadata["execution_time_seconds"] = round(response.execution_time, 2)
            
        # Add session ID if available
        if response.session_id:
            metadata["session_id"] = response.session_id
            
        if metadata:
            # Format as JSON for readability
            metadata_str = json.dumps(metadata, indent=2, default=str)
            
            self.console.print(Panel(
                Syntax(metadata_str, "json", theme="monokai"),
                title="🔍 Metadata",
                border_style="dim"
            ))


def create_formatter(
    format_type: OutputFormat,
    show_billing: bool = False,
    verbose: bool = False,
    console: Optional[Console] = None
) -> OutputFormatter:
    """
    Factory function to create appropriate formatter.
    
    Args:
        format_type: The output format to use
        show_billing: Whether to show billing information
        verbose: Whether to show verbose information
        console: Rich console instance (for rich format)
        
    Returns:
        Appropriate OutputFormatter instance
    """
    if format_type == OutputFormat.SIMPLE:
        return SimpleFormatter(show_billing=show_billing, verbose=verbose)
    elif format_type == OutputFormat.JSON:
        return JSONFormatter(show_billing=show_billing, verbose=verbose)
    elif format_type == OutputFormat.RICH:
        return RichFormatter(show_billing=show_billing, verbose=verbose, console=console)
    else:
        # Default to rich
        return RichFormatter(show_billing=show_billing, verbose=verbose, console=console)