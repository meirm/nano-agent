# Billing Display Control and Output Format Options - Lite Summary

Add user control over billing information display and flexible output format options to nano-agent CLI. Hide cost information by default, show only with `--billing` flag. Provide three output formats: simple text, JSON, and rich (current rich format as default).

## Key Points
- Hide billing/cost information by default, show only with `--billing` flag
- Add `--output-format` option with three choices: simple, json, rich (default)
- Maintain full backward compatibility with existing CLI behavior
- Enable programmatic integration with JSON output and script-friendly plain text
- Preserve current rich formatting as the default user experience