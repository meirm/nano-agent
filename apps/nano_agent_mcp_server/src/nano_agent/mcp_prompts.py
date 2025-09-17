"""
MCP Prompts for Nano Agent Server.

These prompts provide reusable templates for common agent tasks.
They can be used by MCP clients to quickly execute complex operations.
"""
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

# Define functions that will be decorated as prompts in __main__.py

def code_review_prompt(
    file_path: str,
    focus_areas: Optional[List[str]] = None
) -> str:
    """Generate a prompt for comprehensive code review."""
    focus_str = ""
    if focus_areas:
        focus_str = f"\nPay special attention to: {', '.join(focus_areas)}"

    return f"""Please perform a comprehensive code review of {file_path}.

Analyze the following aspects:
1. Code Quality: Check for readability, maintainability, and adherence to best practices
2. Potential Bugs: Identify any logical errors, edge cases, or potential runtime issues
3. Performance: Look for inefficiencies or optimization opportunities
4. Security: Identify any security vulnerabilities or unsafe practices
5. Documentation: Assess inline comments and docstrings{focus_str}

Provide specific suggestions for improvement with code examples where applicable.
"""


def refactor_prompt(
    file_path: str,
    refactor_goals: Optional[List[str]] = None
) -> str:
    """Generate a prompt for code refactoring."""
    goals_str = "general code quality improvements"
    if refactor_goals:
        goals_str = ", ".join(refactor_goals)

    return f"""Refactor the code in {file_path} to achieve the following goals: {goals_str}.

Guidelines:
1. Preserve all existing functionality - no behavior should change
2. Improve code structure and organization
3. Extract reusable functions where appropriate
4. Improve naming conventions for clarity
5. Add or improve type hints where applicable
6. Ensure the refactored code passes all existing tests

Make the changes incrementally and explain your reasoning for each modification.
"""


def test_generation_prompt(
    file_path: str,
    test_framework: str = "pytest",
    coverage_target: int = 80
) -> str:
    """Generate a prompt for creating unit tests."""
    return f"""Create comprehensive unit tests for {file_path} using {test_framework}.

Requirements:
1. Aim for at least {coverage_target}% code coverage
2. Test all public functions and methods
3. Include edge cases and error conditions
4. Test both happy path and failure scenarios
5. Use meaningful test names that describe what is being tested
6. Add appropriate fixtures or setup/teardown as needed
7. Include docstrings for complex test cases

Organize tests logically and ensure they are independent and repeatable.
"""


def documentation_prompt(
    directory: str,
    doc_type: str = "README",
    include_examples: bool = True
) -> str:
    """Generate a prompt for creating documentation."""
    examples_str = "Include usage examples for key functions." if include_examples else ""

    return f"""Create comprehensive {doc_type} documentation for the code in {directory}.

The documentation should include:
1. Overview: Brief description of what the code does and its purpose
2. Installation: How to set up and install dependencies
3. Architecture: High-level structure and design patterns used
4. API Reference: Document all public functions, classes, and methods
5. Configuration: Explain any configuration options or environment variables
{examples_str}

Use clear, concise language and follow markdown best practices.
Format the documentation to be both human-readable and suitable for automated documentation generators.
"""


def security_audit_prompt(
    directory: str,
    security_focus: Optional[List[str]] = None
) -> str:
    """Generate a prompt for security analysis."""
    focus_areas = security_focus or ["input validation", "authentication", "data exposure", "dependencies"]

    return f"""Perform a thorough security audit of the code in {directory}.

Focus on identifying vulnerabilities in these areas:
{chr(10).join(f'- {area}' for area in focus_areas)}

For each issue found:
1. Describe the vulnerability and its potential impact
2. Provide a CVSS score estimate if applicable
3. Show the vulnerable code location
4. Suggest a secure fix with code example
5. Reference relevant security standards (OWASP, CWE, etc.)

Prioritize findings by severity (Critical, High, Medium, Low).
"""


def api_design_prompt(
    spec_type: str = "REST",
    resource_name: str = "resource",
    operations: Optional[List[str]] = None
) -> str:
    """Generate a prompt for API design."""
    ops = operations or ["create", "read", "update", "delete", "list"]

    return f"""Design a complete {spec_type} API for managing {resource_name}.

Include the following operations: {', '.join(ops)}

For each endpoint, specify:
1. HTTP method and path
2. Request parameters (query, path, body)
3. Request/response schemas with examples
4. Status codes and error responses
5. Authentication/authorization requirements
6. Rate limiting considerations

Follow {spec_type} best practices and ensure the API is:
- Consistent and predictable
- Well-documented
- Versioned appropriately
- Secure by default

Provide the specification in OpenAPI 3.0 format if applicable.
"""


def bug_fix_prompt(
    error_message: str,
    file_path: Optional[str] = None,
    context: Optional[str] = None
) -> str:
    """Generate a prompt for debugging and fixing errors."""
    file_str = f" in {file_path}" if file_path else ""
    context_str = f"\n\nAdditional context: {context}" if context else ""

    return f"""Debug and fix the following error{file_str}:

Error message:
```
{error_message}
```{context_str}

Please:
1. Identify the root cause of the error
2. Explain why this error occurs
3. Provide a fix for the issue
4. Add error handling to prevent similar issues
5. Suggest any tests that should be added to catch this in the future

Ensure the fix doesn't introduce new bugs or break existing functionality.
"""


def code_migration_prompt(
    source_version: str,
    target_version: str,
    file_or_directory: str
) -> str:
    """Generate a prompt for code migration between versions."""
    return f"""Migrate the code in {file_or_directory} from {source_version} to {target_version}.

Migration tasks:
1. Identify all deprecated features and replace with modern equivalents
2. Update syntax to match the target version's standards
3. Upgrade dependencies to compatible versions
4. Modify configuration files as needed
5. Update type hints or annotations if applicable
6. Ensure all tests pass after migration

Document any breaking changes and provide migration notes for:
- API changes
- Configuration changes
- Behavioral differences
- Performance implications

Create a migration checklist for manual verification steps if needed.
"""


def performance_optimization_prompt(
    file_path: str,
    performance_targets: Optional[dict] = None
) -> str:
    """Generate a prompt for performance optimization."""
    targets = performance_targets or {"execution_time": "50% faster", "memory": "30% less"}
    targets_str = "\n".join(f"- {k}: {v}" for k, v in targets.items())

    return f"""Optimize the performance of {file_path} to achieve these targets:
{targets_str}

Optimization approach:
1. Profile the current code to identify bottlenecks
2. Analyze algorithmic complexity (time and space)
3. Identify inefficient operations:
   - Unnecessary loops or iterations
   - Redundant computations
   - Inefficient data structures
   - I/O operations that can be optimized
4. Apply optimizations while maintaining readability
5. Measure improvements and document changes

For each optimization:
- Explain what was changed and why
- Show before/after performance metrics
- Note any trade-offs made

Ensure optimizations don't break functionality or significantly reduce code maintainability.
"""


def project_setup_prompt(
    project_name: str,
    project_type: str,
    features: Optional[List[str]] = None
) -> str:
    """Generate a prompt for setting up a new project."""
    features_list = features or ["testing", "linting", "CI/CD", "documentation"]

    return f"""Set up a new {project_type} project called '{project_name}'.

Project requirements:
1. Initialize project structure following best practices for {project_type}
2. Set up dependency management (requirements.txt, package.json, etc.)
3. Configure the following features:
{chr(10).join(f'   - {feature}' for feature in features_list)}
4. Create initial project files:
   - README.md with project overview
   - .gitignore appropriate for {project_type}
   - License file (MIT unless specified)
   - Configuration files for tools and frameworks
5. Set up development environment:
   - Virtual environment or container setup
   - Pre-commit hooks if applicable
   - Development vs production configurations

Include clear instructions for:
- Getting started with development
- Running tests
- Building and deploying

Make the project structure scalable and maintainable.
"""