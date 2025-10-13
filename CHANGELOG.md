## [2.1.1](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/compare/v2.1.0...v2.1.1) (2025-10-13)

## [2.1.0](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/compare/v2.0.0...v2.1.0) (2025-10-13)

### Features

* Implement MCP peer-to-peer chat functionality ([#17](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/issues/17)) ([c446d31](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/commit/c446d31a5ba0d8964ae7ca7194bf640f63ee4dc6))

## [2.0.0](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/compare/v1.2.1...v2.0.0) (2025-10-12)

### ⚠ BREAKING CHANGES

* Config format now uses 'type' field to specify transport type

* refactor(mcp): implement persistent HTTP/SSE session management

- Create HTTPMCPConnection dataclass to maintain active sessions
- Create HTTPMCPToolkit to wrap HTTP MCP tools as callable functions
- Refactor http_client.py to use persistent connections instead of context managers
- Update MCPManager to store HTTPMCPConnection objects for HTTP servers
- Implement proper HTTP session cleanup in _close_server()
- Update type signatures to support both MCPToolkit and HTTPMCPToolkit

This fixes the issue where HTTP MCP servers showed 0 functions because
connections were being closed immediately after initialization.

Note: Known issue with task group lifecycle management causing occasional
RuntimeError - will be fixed in next commit.

* fix(mcp): use Agno Function wrapper for HTTP MCP toolkit

- Replace plain async function with Agno Function object in HTTPMCPToolkit
- Add Function.parameters attribute using tool.inputSchema
- Store client_context reference in HTTPMCPConnection for proper cleanup
- Fix AttributeError: 'function' object has no attribute 'parameters'

* refactor(mcp): improve HTTP transport type safety and error handling

**Type Safety Improvements:**
- Replace all `Any` type hints in HTTPMCPConnection with proper types
- Add TYPE_CHECKING guard to avoid circular imports
- Create AuthType Enum for type-safe authentication configuration

**Error Handling Enhancement:**
- Add 4 new structured exception classes (MCPConnectionError, MCPConnectionTimeoutError, MCPInvalidConfigError, MCPToolExecutionError)
- Replace generic exception handling with specific exception types
- Ensure all exceptions provide proper context and retry information

**Code Quality:**
- Extract magic values to named constants (_HTTP_CLIENT_TERMINATE_ON_CLOSE, _HTTP_CLIENT_DEFAULT_TIMEOUT)
- Move auth header building logic to HTTPAuthConfig.build_header() method
- Update docstring Raises sections to reflect actual exceptions
- Add validation in HTTPAuthConfig.__post_init__()

These changes improve code maintainability, type safety, and debugging experience without altering functionality.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

* refactor(mcp): remove redundant exception handling in initialization flow

**Problem:**
- Defensive `except Exception` blocks were catching and logging errors without re-raising
- This could lead to silent failures where toolkits appear initialized but lack functions
- Redundant error logging (same errors logged multiple times)

**Changes:**
1. **manager.py (_initialise_http_server)**
   - Remove try-except wrapper around create_http_mcp_connection
   - Exceptions (MCPConnectionError, MCPConnectionTimeoutError, MCPInvalidConfigError)
     now bubble up directly to _handle_initialization_error
   - Eliminates duplicate error logging

2. **toolkit.py (_load_functions)**
   - Remove try-except that swallowed all exceptions
   - If function loading fails, exception now propagates to caller
   - Prevents silent failures in MCPToolkit initialization

3. **http_toolkit.py (_load_functions)**
   - Remove try-except that swallowed all exceptions
   - If tool wrapper creation fails, exception now propagates to caller
   - Prevents silent failures in HTTPMCPToolkit initialization

**Impact:**
- Errors are now handled at the appropriate level (asyncio.gather in initialize_from_configs)
- Cleaner error propagation following the "throw early, catch late" principle
- Better visibility into initialization failures
- No functional change - all exceptions still caught at the appropriate layer

**Note:**
Cleanup operations (close, shutdown) still use defensive exception handling,
which is correct as they should not fail due to cleanup errors.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

* test: add HTTP MCP transport unit tests (49 tests)

- Add test_server_params_http.py (22 tests)
- Add test_http_client.py (11 tests)
- Add test_http_toolkit.py (16 tests)

All tests follow international naming standards:
- Pattern: test_<function>_with_<scenario>_expects_<result>
- FIRST principles (Fast, Isolated, Repeatable, Self-validating, Timely)
- AAA pattern (Arrange, Act, Assert)

Test coverage for:
- HTTPAuthConfig validation and bearer/API key authentication
- HTTP MCP connection creation with various scenarios
- HTTP transport detection and config parsing
- HTTPMCPToolkit functionality and connection management

* test: achieve 85% coverage with comprehensive boundary tests

- Increase overall coverage from 78% to 85%
- toolkit.py: 69% → 100% (8 new boundary tests)
- server_params.py: 55% → 74% (17 new parsing/validation tests)
- manager.py: maintained at 86%

New test files:
- test_toolkit_boundaries.py (8 tests)
  * Empty function handling
  * Allowed function filtering with whitespace
  * Function reload mechanisms
  * Missing attributes edge cases

- test_server_params_boundaries.py (28 total tests)
  * STDIO command/args parsing
  * Environment variable handling
  * Config parsing edge cases (enabled/disabled, timeout, description)
  * Invalid config detection and skipping
  * Missing field validation

All tests follow international naming standards:
- Pattern: test_<function>_with_<scenario>_expects_<result>
- FIRST principles applied
- AAA pattern consistently used
- Meaningful boundary and edge case testing

Total: 114 tests passing in 1.25s

### Features

* http mcp transport ([#16](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/issues/16)) ([abb80e7](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/commit/abb80e74ab16dbad9b15ac995c95df5abcc19908))

## [1.2.1](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/compare/v1.2.0...v1.2.1) (2025-10-11)

## [1.2.0](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/compare/v1.1.0...v1.2.0) (2025-10-11)

### Features

* UI/UX redesign for chat interface and components ([#13](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/issues/13)) ([ba7ac29](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/commit/ba7ac293ccd40e4db4c6b2c040104aba327a3062))

## [1.1.0](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/compare/v1.0.0...v1.1.0) (2025-10-10)

### Features

* add Docker Compose deployment with environment configuration ([#10](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/issues/10)) ([03ac6b5](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/commit/03ac6b591b99b8d6ee11d90f75d79fc38e84c1c9))

## 1.0.0 (2025-09-15)

### Features

* add initial project infrastructure ([034143b](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/commit/034143b860e4567aa03c65b646f55330a8ae0edb))
* initialize monorepo with Next.js 15 and FastAPI ([a63806b](https://github.com/Mapleeeeeeeeeee/hwdc-2025-mcp-league-starter/commit/a63806b3164ad1a92ab61b503dabc3063208de41))
