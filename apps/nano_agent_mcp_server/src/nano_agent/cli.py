#!/usr/bin/env python
"""
Nano Agent CLI - Direct command-line interface for testing the nano agent.

This provides a simple command-line interface to test the nano agent functionality
with various commands and interactive modes.
"""

import asyncio
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from pathlib import Path
import os
import sys
import json

# Enable flexible configuration system
try:
    from .modules.config_integration import enable_flexible_configuration
    enable_flexible_configuration()
except ImportError:
    # Fallback if config_integration is not available
    pass

from .modules.nano_agent import prompt_nano_agent, _execute_nano_agent
from .modules.data_types import PromptNanoAgentRequest, ChatMessage
from .modules.constants import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    ERROR_NO_API_KEY,
    DEMO_PROMPTS,
    DEFAULT_TEMPERATURE,
    MAX_TOKENS
)
from .modules.command_loader import CommandLoader, parse_command_syntax
from .modules.session_manager import SessionManager
from .modules.output_formats import (
    OutputFormat,
    OutputFormatter,
    AgentResponse,
    BillingInfo,
    create_formatter
)

app = typer.Typer()
console = Console()
console_stderr = Console(stderr=True)

def get_log_console(verbose: bool = False) -> Console:
    """Get the appropriate console for logging messages.
    
    Args:
        verbose: If True, returns stderr console. If False, returns stdout console.
        
    Returns:
        Console instance for logging output
    """
    return console_stderr if verbose else console

def check_api_key(provider: str = None):
    """Check if required API key is set based on provider."""
    # If no provider specified, try to determine from context
    if provider is None:
        provider = DEFAULT_PROVIDER
    
    # Only check API keys for providers that require them
    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            console_stderr.print(f"[red]Error: OPENAI_API_KEY environment variable is not set[/red]")
            console_stderr.print("Please set it with: export OPENAI_API_KEY=your-api-key")
            sys.exit(1)
    elif provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            console_stderr.print(f"[red]Error: ANTHROPIC_API_KEY environment variable is not set[/red]")
            console_stderr.print("Please set it with: export ANTHROPIC_API_KEY=your-api-key")
            sys.exit(1)
    # Ollama, ollama-native, and lmstudio don't require API keys by default
    # They may use them for authentication but it's optional

@app.command()
def test_tools():
    """Test individual tool functions."""
    # Import the raw tool functions from nano_agent_tools
    from .modules.nano_agent_tools import (
        read_file_raw,
        list_directory_raw,
        write_file_raw,
        get_file_info_raw,
        edit_file_raw
    )
    
    console.print(Panel("[cyan]Testing Nano Agent Tools[/cyan]", expand=False))
    
    # Test list_directory (call the raw function, not the FunctionTool)
    console.print("\n[yellow]1. Testing list_directory:[/yellow]")
    result = list_directory_raw(".")
    console.print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test write_file
    console.print("\n[yellow]2. Testing write_file:[/yellow]")
    test_file = "test_nano_agent.txt"
    result = write_file_raw(test_file, "Hello from Nano Agent CLI!\nThis is line 2\nThis is line 3")
    console.print(result)
    
    # Test read_file
    console.print("\n[yellow]3. Testing read_file:[/yellow]")
    result = read_file_raw(test_file)
    console.print(f"Content: {result}")
    
    # Test edit_file
    console.print("\n[yellow]4. Testing edit_file:[/yellow]")
    result = edit_file_raw(test_file, "This is line 2", "This is the EDITED line 2")
    console.print(f"Edit result: {result}")
    result = read_file_raw(test_file)
    console.print(f"Content after edit: {result}")
    
    # Test get_file_info
    console.print("\n[yellow]5. Testing get_file_info:[/yellow]")
    result = get_file_info_raw(test_file)
    info = json.loads(result)
    console.print(json.dumps(info, indent=2))
    
    # Clean up
    Path(test_file).unlink(missing_ok=True)
    console.print("\n[green]✓ All tool tests completed successfully![/green]")

@app.command()
def run(
    prompt: str,
    model: str = typer.Option(None, help="Model to use"),
    provider: str = typer.Option(None, help="Provider to use"),
    agent: str = typer.Option(None, help="Agent personality to use"),
    api_base: str = typer.Option(None, help="API base URL (overrides environment variables)"),
    api_key: str = typer.Option(None, help="API key (overrides environment variables)"),
    verbose: bool = typer.Option(False, help="Show detailed output"),
    # Claude-inspired options
    continue_session: bool = typer.Option(False, "--continue", "-c", help="Continue the last session"),
    session: str = typer.Option(None, "--session", "-s", help="Use a specific session ID"),
    new_session: bool = typer.Option(False, "--new", "-n", help="Force a new session"),
    temperature: float = typer.Option(None, "--temperature", "-t", help="Model temperature (0.0-2.0)"),
    max_tokens: int = typer.Option(None, "--max-tokens", help="Maximum response tokens"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save conversation to session history"),
    enable_trace: bool = typer.Option(False, "--enable-trace", help="Enable OpenAI agent tracing"),
    # New output control options
    billing: bool = typer.Option(False, "--billing", help="Show token usage and cost information"),
    output_format: str = typer.Option("rich", "--output-format", "-f", 
                                      help="Output format: simple, json, or rich (default)"),
    output_thinking: bool = typer.Option(False, "--output-thinking", help="Show agent thinking and reasoning text"),
    panel_width: Optional[int] = typer.Option(None, "--panel-width", help="Maximum width for rich output panels (default: auto-detect)")
):
    """Run the nano agent with a prompt. Supports /command syntax for command files."""
    # Determine provider first before checking API key
    if provider is None:
        config_file = Path.home() / ".nano-cli" / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    provider = config.get('default_provider', DEFAULT_PROVIDER)
            except Exception:
                provider = DEFAULT_PROVIDER
        else:
            provider = DEFAULT_PROVIDER
    
    check_api_key(provider)
    
    # Load config defaults if not specified
    config_file = Path.home() / ".nano-cli" / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if model is None:
                    model = config.get('default_model', DEFAULT_MODEL)
                if provider is None:
                    provider = config.get('default_provider', DEFAULT_PROVIDER)
                if agent is None:
                    agent = config.get('default_agent')
        except Exception:
            pass
    
    # Final fallbacks
    if model is None:
        model = DEFAULT_MODEL
    if provider is None:
        provider = DEFAULT_PROVIDER
    
    # Session management (Claude-inspired feature)
    session_manager = SessionManager()
    chat_history = []
    
    if continue_session and not new_session:
        # Continue the last session
        last_session = session_manager.get_last_session()
        if last_session:
            get_log_console(verbose).print(f"[dim]Continuing session: {last_session.session_id}[/dim]")
            chat_history = session_manager.get_conversation_context()
            # Use session's model/provider if not overridden
            if model == DEFAULT_MODEL:
                model = last_session.model
            if provider == DEFAULT_PROVIDER:
                provider = last_session.provider
    elif session and not new_session:
        # Load specific session
        loaded_session = session_manager.load_session(session)
        if loaded_session:
            get_log_console(verbose).print(f"[dim]Loaded session: {session}[/dim]")
            chat_history = session_manager.get_conversation_context()
            # Use session's model/provider if not overridden
            if model == DEFAULT_MODEL:
                model = loaded_session.model
            if provider == DEFAULT_PROVIDER:
                provider = loaded_session.provider
        else:
            get_log_console(verbose).print(f"[yellow]Warning: Session '{session}' not found, starting new session[/yellow]")
    
    if save and session_manager.current_session is None:
        # Create new session if saving and no session loaded
        session_manager.create_session(provider, model)
    
    # Parse output format early to control all output
    format_type = OutputFormat.from_string(output_format)
    
    # Check if this is a command syntax
    command_name, arguments = parse_command_syntax(prompt)
    
    if command_name:
        # Load and execute command
        loader = CommandLoader()
        final_prompt = loader.execute_command(command_name, arguments)
        
        if final_prompt is None:
            if format_type == OutputFormat.JSON:
                console.print(json.dumps({"success": False, "error": f"Command '/{command_name}' not found"}))
            else:
                get_log_console(verbose).print(f"[red]Command '/{command_name}' not found.[/red]")
                get_log_console(verbose).print(f"[dim]Available commands can be listed with: nano-cli commands list[/dim]")
            sys.exit(1)
        
        # Only show panel in rich mode and verbose
        if format_type == OutputFormat.RICH and verbose:
            get_log_console(verbose).print(Panel(
                f"[cyan]Running Command: /{command_name}[/cyan]\n"
                f"Arguments: {arguments if arguments else '(none)'}\n"
                f"Model: {model}\n"
                f"Provider: {provider}", 
                expand=False
            ))
    else:
        final_prompt = prompt
        # Only show panel in rich mode and verbose
        if format_type == OutputFormat.RICH and verbose:
            get_log_console(verbose).print(Panel(f"[cyan]Running Nano Agent[/cyan]\nModel: {model}\nProvider: {provider}", expand=False))
    
    # Only show prompt in rich mode and verbose
    if format_type == OutputFormat.RICH and verbose:
        get_log_console(verbose).print(f"\n[yellow]Prompt:[/yellow] {final_prompt}\n")
    
    # Create request with the final prompt (either direct or from command)
    request = PromptNanoAgentRequest(
        agentic_prompt=final_prompt,
        model=model,
        provider=provider,
        agent_name=agent,
        api_base=api_base,
        api_key=api_key,
        chat_history=chat_history if chat_history else None,
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
        max_tokens=max_tokens if max_tokens is not None else MAX_TOKENS,
        enable_trace=enable_trace
    )
    
    # Disable rich logging for simple/json formats
    enable_rich = format_type == OutputFormat.RICH
    
    # Execute agent without progress spinner (rich logging will show progress)
    response = _execute_nano_agent(request, enable_rich_logging=enable_rich, verbose=verbose)
    
    # Create console with specified width if provided
    output_console = Console(width=panel_width) if panel_width else console
    
    # Create formatter based on output format
    formatter = create_formatter(format_type, show_billing=billing, verbose=verbose, show_thinking=output_thinking, console=output_console)
    
    # Convert response to AgentResponse format
    agent_response = AgentResponse(
        success=response.success,
        message="Agent completed successfully" if response.success else "Agent failed",
        data=response.result if response.success else None,
        error=response.error if not response.success else None,
        metadata=response.metadata,
        execution_time=response.execution_time_seconds,
        session_id=session_manager.current_session.session_id if session_manager.current_session else None
    )
    
    # Extract billing information if available
    if response.metadata and "token_usage" in response.metadata:
        usage = response.metadata["token_usage"]
        agent_response.billing = BillingInfo(
            total_tokens=usage.get("total_tokens", 0),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            cached_tokens=usage.get("cached_tokens", 0),
            total_cost=usage.get("total_cost", 0.0),
            input_cost=usage.get("input_cost", 0.0),
            output_cost=usage.get("output_cost", 0.0),
            cached_savings=usage.get("cached_savings", 0.0)
        )
    
    # Format and display the response
    output = formatter.format_response(agent_response)
    if output:  # SimpleFormatter and JSONFormatter return strings
        console.print(output)
    
    # Save to session if enabled
    if response.success and save and session_manager.current_session:
        session_manager.add_exchange(
            final_prompt,
            response.result,
            response.metadata
        )
        if format_type == OutputFormat.RICH and verbose:  # Only show session info in rich mode and verbose
            get_log_console(verbose).print(f"[dim]Session saved: {session_manager.current_session.session_id}[/dim]")
    
    # Only show additional metadata panel if verbose AND using rich format
    if verbose and format_type == OutputFormat.RICH:
        # Format metadata as a single JSON object
        metadata_display = response.metadata.copy() if response.metadata else {}
        
        # Remove token usage from metadata if already shown via billing
        if "token_usage" in metadata_display and billing:
            del metadata_display["token_usage"]
            
        # Only show metadata panel if there's something to show
        if metadata_display:
            # Pretty print the combined metadata
            metadata_json = json.dumps(metadata_display, indent=2)
            
            get_log_console(verbose).print(Panel(
                Syntax(metadata_json, "json", theme="monokai", line_numbers=False),
                title="🔍 Additional Metadata",
                border_style="dim",
                expand=False
            ))

@app.command()
def sessions(
    action: str = typer.Argument("list", help="Action to perform: list, show, clear"),
    session_id: str = typer.Option(None, "--id", help="Session ID for 'show' action"),
    days: int = typer.Option(30, "--days", help="Days to keep for 'clear' action")
):
    """Manage conversation sessions (Claude-inspired feature)."""
    session_manager = SessionManager()
    
    if action == "list":
        # List recent sessions
        sessions = session_manager.get_recent_sessions(limit=20)
        if not sessions:
            console.print("[yellow]No sessions found.[/yellow]")
            return
            
        table = Table(title="Recent Sessions")
        table.add_column("Session ID", style="cyan")
        table.add_column("Created", style="green")
        table.add_column("Last Updated", style="yellow")
        table.add_column("Provider/Model", style="magenta")
        table.add_column("Messages", style="blue")
        
        for session in sessions:
            created = session["created_at"].split("T")[0] if "T" in session["created_at"] else session["created_at"]
            updated = session["last_updated"].split("T")[0] if "T" in session["last_updated"] else session["last_updated"]
            model_info = f"{session['provider']}/{session['model']}"
            table.add_row(
                session["session_id"],
                created,
                updated,
                model_info,
                str(session.get("message_count", 0))
            )
        
        console.print(table)
        console.print(f"\n[dim]Use 'nano-cli run --continue' to resume the last session[/dim]")
        console.print(f"[dim]Use 'nano-cli sessions show --id <session_id>' to view a specific session[/dim]")
        
    elif action == "show":
        # Show a specific session
        if not session_id:
            console.print("[red]Error: --id required for 'show' action[/red]")
            return
            
        session = session_manager.load_session(session_id)
        if not session:
            console.print(f"[red]Session '{session_id}' not found[/red]")
            return
            
        console.print(Panel(
            f"[cyan]Session: {session.session_id}[/cyan]\n"
            f"Created: {session.created_at}\n"
            f"Provider: {session.provider} | Model: {session.model}\n"
            f"Messages: {len(session.conversation)}",
            title="Session Details",
            expand=False
        ))
        
        # Display conversation history
        for i, msg in enumerate(session.conversation):
            if msg.role == "user":
                console.print(f"\n[blue]👤 User:[/blue]")
                console.print(msg.content[:500] + "..." if len(msg.content) > 500 else msg.content)
            elif msg.role == "assistant":
                console.print(f"\n[green]🤖 Assistant:[/green]")
                console.print(msg.content[:500] + "..." if len(msg.content) > 500 else msg.content)
                
    elif action == "clear":
        # Clear old sessions
        deleted = session_manager.clear_old_sessions(days=days)
        console.print(f"[green]Cleared {deleted} sessions older than {days} days[/green]")
        
    else:
        console_stderr.print(f"[red]Unknown action: {action}[/red]")
        console_stderr.print("Available actions: list, show, clear")

@app.command()
def demo():
    """Run a demo showing various agent capabilities."""
    check_api_key(DEFAULT_PROVIDER)
    
    console.print(Panel("[cyan]Nano Agent Demo[/cyan]", expand=False))
    
    for i, (prompt, model) in enumerate(DEMO_PROMPTS, 1):
        console.print(f"\n[yellow]Demo {i}:[/yellow] {prompt}")
        
        request = PromptNanoAgentRequest(
            agentic_prompt=prompt,
            model=model,
            provider=DEFAULT_PROVIDER
        )
        
        # Execute without progress spinner
        response = _execute_nano_agent(request)
        
        if response.success:
            console.print(f"[green]✓[/green] {response.result[:200]}...")
        else:
            console.print(f"[red]✗[/red] {response.error}")
    
    # Clean up
    Path("demo.txt").unlink(missing_ok=True)
    console.print("\n[green]✓ Demo completed![/green]")

@app.command()
def interactive(
    model: str = typer.Option(None, help="Initial model to use"),
    provider: str = typer.Option(None, help="Initial provider to use"),
    agent: str = typer.Option(None, help="Initial agent personality to use"),
    api_base: str = typer.Option(None, help="API base URL (overrides environment variables)"),
    api_key: str = typer.Option(None, help="API key (overrides environment variables)"),
    simple: bool = typer.Option(False, help="Use simple mode without autocompletion"),
    enable_trace: bool = typer.Option(False, "--enable-trace", help="Enable OpenAI agent tracing"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Run the agent in enhanced interactive mode with autocompletion."""
    # Determine provider first before checking API key
    if provider is None:
        config_file = Path.home() / ".nano-cli" / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    provider = config.get('default_provider', DEFAULT_PROVIDER)
            except Exception:
                provider = DEFAULT_PROVIDER
        else:
            provider = DEFAULT_PROVIDER
    
    check_api_key(provider)
    
    # Load config defaults if not specified
    config_file = Path.home() / ".nano-cli" / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if model is None:
                    model = config.get('default_model', DEFAULT_MODEL)
                if provider is None:
                    provider = config.get('default_provider', DEFAULT_PROVIDER)
                if agent is None:
                    agent = config.get('default_agent')
        except Exception:
            pass
    
    # Final fallbacks
    if model is None:
        model = DEFAULT_MODEL
    if provider is None:
        provider = DEFAULT_PROVIDER
    
    # Use simple mode if requested or if prompt_toolkit is not available
    if simple:
        _run_simple_interactive(model, provider, api_base, api_key)
    else:
        try:
            from .modules.interactive_mode import InteractiveSession
            session = InteractiveSession(initial_model=model, initial_provider=provider, initial_agent=agent, 
                                        api_base=api_base, api_key=api_key, enable_trace=enable_trace)
            session.run()
        except ImportError:
            (console_stderr if verbose else console).print("[yellow]Enhanced interactive mode not available. Install with: uv sync[/yellow]")
            (console_stderr if verbose else console).print("[dim]Falling back to simple mode...[/dim]\n")
            _run_simple_interactive(model, provider, verbose, api_base, api_key)

def _run_simple_interactive(model: str, provider: str, verbose: bool = False, api_base: str = None, api_key: str = None):
    """Run simple interactive mode without autocompletion."""
    (console_stderr if verbose else console).print(Panel("[cyan]Nano Agent Interactive Mode (Simple)[/cyan]\nType 'exit' to quit", expand=False))
    
    loader = CommandLoader()
    
    while True:
        try:
            prompt = typer.prompt("\n[yellow]Enter prompt[/yellow]")
            
            if prompt.lower() in ["exit", "quit", "q"]:
                (console_stderr if verbose else console).print("[dim]Goodbye![/dim]")
                break
            
            # Handle special commands (both slash and non-slash)
            if prompt.lower() in ["help", "/help"]:
                (console_stderr if verbose else console).print("[cyan]Built-in Commands:[/cyan]")
                (console_stderr if verbose else console).print("  /help           - Show this help")
                (console_stderr if verbose else console).print("  /commands       - List available command files")
                (console_stderr if verbose else console).print("  /clear          - Clear the screen")
                (console_stderr if verbose else console).print("  /<command> args - Run a command file")
                (console_stderr if verbose else console).print("")
                (console_stderr if verbose else console).print("[cyan]Shell Commands:[/cyan]")
                (console_stderr if verbose else console).print("  !<command>      - Execute shell command (e.g., !ls)")
                (console_stderr if verbose else console).print("")
                (console_stderr if verbose else console).print("[cyan]Other Commands:[/cyan]")
                (console_stderr if verbose else console).print("  exit/quit/q     - Exit interactive mode")
                (console_stderr if verbose else console).print("")
                (console_stderr if verbose else console).print("[dim]Type any text to send directly to the agent[/dim]")
                continue
            
            if prompt.lower() in ["commands", "/commands"]:
                loader.display_commands_table()
                continue
            
            # Handle /commands show
            if prompt.lower().startswith("/commands show ") or prompt.lower().startswith("commands show "):
                parts = prompt.split()
                if len(parts) >= 3:
                    cmd_to_show = parts[2]
                    if cmd_to_show.startswith('/'):
                        cmd_to_show = cmd_to_show[1:]
                    
                    command = loader.load_command(cmd_to_show)
                    if command:
                        try:
                            content = command.path.read_text()
                            console.print(Panel(
                                content,
                                title=f"📋 Command File: /{command.name}",
                                subtitle=str(command.path),
                                border_style="cyan",
                                expand=False
                            ))
                        except Exception as e:
                            console.print(f"[red]Error reading command file: {e}[/red]")
                    else:
                        console.print(f"[red]Command '{cmd_to_show}' not found.[/red]")
                else:
                    console.print("[yellow]Usage: /commands show <command_name>[/yellow]")
                continue
            
            if prompt.lower() in ["clear", "/clear"]:
                console.clear()
                continue
            
            # Handle shell commands with ! prefix
            if prompt.startswith('!'):
                shell_cmd = prompt[1:].strip()
                if shell_cmd:
                    user_shell = os.environ.get('SHELL', '/bin/bash')
                    (console_stderr if verbose else console).print(f"[dim]Executing: {shell_cmd} (using {user_shell})[/dim]")
                    try:
                        import subprocess
                        result = subprocess.run(
                            [user_shell, '-c', shell_cmd],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if result.stdout:
                            console.print("[green]Output:[/green]")
                            console.print(result.stdout)
                        if result.stderr:
                            console.print("[yellow]Error output:[/yellow]")
                            console.print(result.stderr)
                        (console_stderr if verbose else console).print(f"[dim]Exit code: {result.returncode}[/dim]")
                    except subprocess.TimeoutExpired:
                        (console_stderr if verbose else console).print("[red]Command timed out after 30 seconds[/red]")
                    except Exception as e:
                        (console_stderr if verbose else console).print(f"[red]Error: {e}[/red]")
                else:
                    (console_stderr if verbose else console).print("[yellow]Usage: !<shell command>[/yellow]")
                continue
            
            # Check for /command syntax
            command_name, arguments = parse_command_syntax(prompt)
            
            if command_name:
                final_prompt = loader.execute_command(command_name, arguments)
                if final_prompt is None:
                    (console_stderr if verbose else console).print(f"[red]Command '/{command_name}' not found.[/red]")
                    continue
                (console_stderr if verbose else console).print(f"[dim]Using command: /{command_name}[/dim]")
            else:
                final_prompt = prompt
            
            request = PromptNanoAgentRequest(
                agentic_prompt=final_prompt,
                model=model,
                provider=provider,
                api_base=api_base,
                api_key=api_key
            )
            
            # Execute without progress spinner
            response = _execute_nano_agent(request)
            
            if response.success:
                console.print(Panel(
                    response.result,
                    title="💬 Agent Response",
                    border_style="cyan",
                    expand=False
                ))
            else:
                console.print(Panel(
                    response.error,
                    title="❌ Error",
                    border_style="red",
                    expand=False
                ))
                
        except KeyboardInterrupt:
            (console_stderr if verbose else console).print("\n[dim]Interrupted. Type 'exit' to quit.[/dim]")
        except Exception as e:
            (console_stderr if verbose else console).print(f"\n[red]Error:[/red] {str(e)}")

@app.command("list-models")
def list_models(
    provider: str = typer.Option(None, "--provider", "-p", help="List models from a specific provider"),
    all_providers: bool = typer.Option(False, "--all", "-a", help="List models from all providers"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format: table or json"),
    capability: str = typer.Option(None, "--capability", "-c", help="Filter models by capability"),
    show_deprecated: bool = typer.Option(False, "--show-deprecated", help="Include deprecated models"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information")
):
    """List available models from AI providers."""
    from .modules.model_providers import ProviderRegistry
    from .modules.provider_implementations import initialize_providers
    from rich.table import Table
    import json
    
    # Initialize providers
    initialize_providers()
    
    # Get registry instance
    registry = ProviderRegistry()
    
    async def fetch_models():
        """Fetch models based on parameters."""
        if all_providers:
            return await registry.list_all_models()
        elif provider:
            return await registry.list_provider_models(provider)
        else:
            # Default to listing from all providers
            return await registry.list_all_models()
    
    try:
        # Fetch models
        models = asyncio.run(fetch_models())
        
        # Filter by capability if specified
        if capability:
            models = [m for m in models if capability in m.capabilities]
        
        # Filter out deprecated models unless requested
        if not show_deprecated:
            models = [m for m in models if not m.deprecated]
        
        # Format output
        if format_type == "json":
            # JSON output
            output = [
                {
                    "id": m.id,
                    "name": m.name,
                    "provider": m.provider,
                    "context_length": m.context_length,
                    "capabilities": m.capabilities,
                    "deprecated": m.deprecated,
                    "replacement_model": m.replacement_model
                }
                for m in models
            ]
            console.print(json.dumps(output, indent=2))
        else:
            # Table output
            if not models:
                console.print("[yellow]No models found matching the criteria.[/yellow]")
                return
            
            table = Table(title="Available Models")
            table.add_column("Provider", style="cyan")
            table.add_column("Model ID", style="green")
            table.add_column("Name", style="white")
            
            if verbose:
                table.add_column("Context", style="yellow")
                table.add_column("Capabilities", style="blue")
            
            if show_deprecated:
                table.add_column("Status", style="red")
            
            for model in models:
                row = [
                    model.provider,
                    model.id,
                    model.name or model.id
                ]
                
                if verbose:
                    context = f"{model.context_length:,}" if model.context_length else "N/A"
                    capabilities = ", ".join(model.capabilities) if model.capabilities else "N/A"
                    row.extend([context, capabilities])
                
                if show_deprecated:
                    status = "DEPRECATED" if model.deprecated else "Active"
                    row.append(status)
                
                table.add_row(*row)
            
            console.print(table)
            
            # Show summary
            provider_counts = {}
            for m in models:
                provider_counts[m.provider] = provider_counts.get(m.provider, 0) + 1
            
            if verbose:
                console.print(f"\n[dim]Total models: {len(models)}[/dim]")
                for p, count in provider_counts.items():
                    console.print(f"[dim]  {p}: {count} models[/dim]")
    
    except Exception as e:
        from .modules.model_providers import (
            ProviderNotFoundError,
            ProviderConnectionError,
            ProviderAuthenticationError
        )
        
        if isinstance(e, ProviderNotFoundError):
            console.print(f"[red]Error: Provider '{e.provider_name}' not found[/red]")
            console.print("[dim]Available providers: openai, anthropic, ollama, lmstudio[/dim]")
        elif isinstance(e, ProviderConnectionError):
            console.print(f"[red]Error: Could not connect to {e.provider}[/red]")
            console.print(f"[dim]{str(e)}[/dim]")
        elif isinstance(e, ProviderAuthenticationError):
            console.print(f"[red]Error: Authentication failed for {e.provider}[/red]")
            console.print(f"[dim]{str(e)}[/dim]")
        else:
            console.print(f"[red]Error: {str(e)}[/red]")
            if verbose:
                import traceback
                console.print(f"[dim]{traceback.format_exc()}[/dim]")
        
        sys.exit(1)

# Create a sub-app for command management
commands_app = typer.Typer()
app.add_typer(commands_app, name="commands", help="Manage nano-cli command files")

@commands_app.command("list")
def list_commands():
    """List all available command files."""
    loader = CommandLoader()
    loader.display_commands_table()

@commands_app.command("create")
def create_command(
    name: str = typer.Argument(..., help="Name of the command to create"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing command")
):
    """Create a new command template file."""
    loader = CommandLoader()
    success = loader.create_command_template(name, overwrite)
    if not success:
        sys.exit(1)

@commands_app.command("show")
def show_command(
    name: str = typer.Argument(..., help="Name of the command to show")
):
    """Show the content of a command file."""
    loader = CommandLoader()
    command = loader.load_command(name)
    
    if command is None:
        console.print(f"[red]Command '{name}' not found.[/red]")
        sys.exit(1)
    
    console.print(Panel(
        f"[green]{command.description}[/green]",
        title=f"📋 Command: /{command.name}",
        border_style="cyan"
    ))
    
    console.print("\n[yellow]Prompt Template:[/yellow]")
    console.print(Panel(command.prompt_template, border_style="dim"))
    
    if command.metadata:
        console.print("\n[yellow]Metadata:[/yellow]")
        for key, value in command.metadata.items():
            console.print(f"  {key}: {value}")
    
    console.print(f"\n[dim]File: {command.path}[/dim]")
    console.print(f"[dim]Usage: nano-cli /{command.name} \"arguments\"[/dim]")

@commands_app.command("edit")
def edit_command(
    name: str = typer.Argument(..., help="Name of the command to edit")
):
    """Open a command file in the default editor."""
    loader = CommandLoader()
    command = loader.load_command(name)
    
    if command is None:
        console.print(f"[red]Command '{name}' not found.[/red]")
        console.print(f"[dim]Create it with: nano-cli commands create {name}[/dim]")
        sys.exit(1)
    
    # Try to open in default editor
    import subprocess
    import platform
    
    if platform.system() == "Windows":
        os.startfile(command.path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", command.path])
    else:  # Linux and others
        # Try common editors in order of preference
        editors = ["nano", "vim", "vi", "emacs"]
        editor = os.environ.get("EDITOR")
        
        if editor:
            subprocess.call([editor, command.path])
        else:
            for ed in editors:
                if subprocess.call(["which", ed], stdout=subprocess.DEVNULL) == 0:
                    subprocess.call([ed, command.path])
                    break
            else:
                console.print(f"[yellow]No editor found. Please edit manually: {command.path}[/yellow]")

def main():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    main()