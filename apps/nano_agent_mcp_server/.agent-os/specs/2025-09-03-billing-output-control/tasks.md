# Spec Tasks

These are the tasks to be completed for the spec detailed in @.agent-os/specs/2025-09-03-billing-output-control/spec.md

> Created: 2025-09-03
> Status: Ready for Implementation

## Tasks

### Phase 1: Infrastructure Setup (Estimated: 4-6 hours)

- [ ] **TASK-001: Define Output Format Enum**
  - [ ] 1.1.1 Create OutputFormat enum with values: SIMPLE, JSON, RICH
  - [ ] 1.1.2 Add to constants.py or new output_formats.py module
  - [ ] 1.1.3 Include enum in CLI imports
  - [ ] 1.1.4 Add type hints and documentation

- [ ] **TASK-002: Standardize Response Data Structure**
  - [ ] 1.2.1 Create AgentResponse dataclass with success, message, data, metadata fields
  - [ ] 1.2.2 Create BillingInfo dataclass for token/cost tracking
  - [ ] 1.2.3 Update existing response handling to use new structure
  - [ ] 1.2.4 Ensure backward compatibility with existing code

- [ ] **TASK-003: Implement Formatter Base Class and Interface**
  - [ ] 1.3.1 Create abstract OutputFormatter base class
  - [ ] 1.3.2 Define format_response method signature
  - [ ] 1.3.3 Create formatter factory function
  - [ ] 1.3.4 Add error handling for unknown formats

### Phase 2: Formatter Implementation (Estimated: 6-8 hours)

- [ ] **TASK-004: Implement Simple Text Formatter**
  - [ ] 2.1.1 Create SimpleFormatter class
  - [ ] 2.1.2 Handle plain text output without Rich formatting
  - [ ] 2.1.3 Include optional billing information formatting
  - [ ] 2.1.4 Test with various response types
  - [ ] 2.1.5 Handle multiline text properly

- [ ] **TASK-005: Implement JSON Formatter**
  - [ ] 2.2.1 Create JSONFormatter class
  - [ ] 2.2.2 Handle JSON serialization with proper error handling
  - [ ] 2.2.3 Ensure datetime and complex objects serialize correctly
  - [ ] 2.2.4 Include schema validation
  - [ ] 2.2.5 Add pretty-print option for readability

- [ ] **TASK-006: Refactor Decorated Formatter**
  - [ ] 2.3.1 Extract current Rich formatting logic into DecoratedFormatter class
  - [ ] 2.3.2 Maintain existing visual presentation
  - [ ] 2.3.3 Ensure billing information integration
  - [ ] 2.3.4 Preserve all current formatting features
  - [ ] 2.3.5 Test against existing output expectations

### Phase 3: CLI Integration (Estimated: 3-4 hours)

- [ ] **TASK-007: Add CLI Arguments**
  - [ ] 3.1.1 Add --billing flag to run and interactive commands
  - [ ] 3.1.2 Add --output-format/-f option with enum validation
  - [ ] 3.1.3 Update command signatures and help text
  - [ ] 3.1.4 Ensure Typer integration works correctly
  - [ ] 3.1.5 Add argument validation and error messages

- [ ] **TASK-008: Wire Formatters into Command Flow**
  - [ ] 3.2.1 Modify command execution to use selected formatter
  - [ ] 3.2.2 Pass billing flag to formatters
  - [ ] 3.2.3 Handle formatter selection logic
  - [ ] 3.2.4 Integrate with existing console output
  - [ ] 3.2.5 Update interactive mode to respect format settings

### Phase 4: Billing Control Implementation (Estimated: 2-3 hours)

- [ ] **TASK-009: Update Token Tracking Integration**
  - [ ] 4.1.1 Modify token tracking to be conditionally included
  - [ ] 4.1.2 Ensure billing information is collected but not displayed by default
  - [ ] 4.1.3 Update BillingInfo population in agent execution
  - [ ] 4.1.4 Test with various providers and models

- [ ] **TASK-010: Implement Billing Display Control**
  - [ ] 4.2.1 Hide billing information by default in all formatters
  - [ ] 4.2.2 Show billing information only when --billing flag is present
  - [ ] 4.2.3 Ensure consistent behavior across all output formats
  - [ ] 4.2.4 Update metadata section to exclude costs when not requested

### Phase 5: Testing and Validation (Estimated: 4-5 hours)

- [ ] **TASK-011: Unit Tests for Formatters**
  - [ ] 5.1.1 Test each formatter with various response types
  - [ ] 5.1.2 Test billing information display/hiding
  - [ ] 5.1.3 Test error handling and edge cases
  - [ ] 5.1.4 Mock external dependencies as needed
  - [ ] 5.1.5 Achieve >90% test coverage

- [ ] **TASK-012: CLI Integration Tests**
  - [ ] 5.2.1 Test all command combinations with new flags
  - [ ] 5.2.2 Verify backward compatibility
  - [ ] 5.2.3 Test error scenarios and validation
  - [ ] 5.2.4 Ensure help text is accurate
  - [ ] 5.2.5 Test flag interactions and precedence

- [ ] **TASK-013: End-to-End Testing**
  - [ ] 5.3.1 Test with different providers and models
  - [ ] 5.3.2 Verify JSON schema consistency
  - [ ] 5.3.3 Test interactive mode with new formats
  - [ ] 5.3.4 Performance testing for format overhead
  - [ ] 5.3.5 Test with real API calls and responses

### Phase 6: Documentation and Polish (Estimated: 2-3 hours)

- [ ] **TASK-014: Update Help Text and Documentation**
  - [ ] 6.1.1 Ensure CLI help text accurately describes new options
  - [ ] 6.1.2 Update README examples if needed
  - [ ] 6.1.3 Add usage examples for each output format
  - [ ] 6.1.4 Document backward compatibility guarantees
  - [ ] 6.1.5 Create migration guide for existing users

- [ ] **TASK-015: Code Review and Cleanup**
  - [ ] 6.2.1 Review all code changes for consistency
  - [ ] 6.2.2 Ensure proper error handling throughout
  - [ ] 6.2.3 Validate type hints and docstrings
  - [ ] 6.2.4 Clean up any temporary code or comments
  - [ ] 6.2.5 Run linters and formatters

### Acceptance Criteria

**Must Have**:
- [ ] Billing information hidden by default, shown with --billing flag
- [ ] Three output formats working: simple, json, rich (default)
- [ ] Full backward compatibility maintained
- [ ] All existing tests pass
- [ ] New functionality has comprehensive test coverage

**Should Have**:
- [ ] Performance impact < 5% for any format
- [ ] Clear error messages for invalid inputs
- [ ] Consistent information across all formats
- [ ] Help text accurately describes new features

**Nice to Have**:
- [ ] JSON schema documentation
- [ ] Example outputs in documentation
- [ ] Integration with existing verbose flag logic