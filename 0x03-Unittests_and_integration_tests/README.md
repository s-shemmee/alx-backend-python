# 0x03. Unittests and Integration Tests

This project focuses on unit testing and integration testing in Python using the `unittest` framework and `unittest.mock` for mocking external dependencies.

## Learning Objectives

- Understand the difference between unit and integration tests
- Learn common testing patterns such as mocking, parametrizations and fixtures
- Practice writing comprehensive test suites for Python applications

## Requirements

- All files are interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All files end with a new line
- The first line of all files is exactly `#!/usr/bin/env python3`
- Code follows the pycodestyle style (version 2.5)
- All files are executable
- All modules, classes, and functions have proper documentation
- All functions and coroutines are type-annotated

## Files

- `utils.py` - Utility functions for GitHub organization client
- `client.py` - GitHub organization client implementation
- `fixtures.py` - Test fixtures containing sample data
- `test_utils.py` - Unit tests for utils module
- `test_client.py` - Unit and integration tests for client module

## Testing

Execute tests using:

```bash
python -m unittest path/to/test_file.py
```

For example:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

## Tasks

1. **Parameterize a unit test** - Test `access_nested_map` function with various inputs
2. **Parameterize a unit test** - Test exception handling in `access_nested_map`
3. **Mock HTTP calls** - Test `get_json` function with mocked HTTP requests
4. **Parameterize and patch** - Test `memoize` decorator functionality
5. **Parameterize and patch as decorators** - Test `GithubOrgClient.org` method
6. **Mocking a property** - Test `GithubOrgClient._public_repos_url` property
7. **More patching** - Test `GithubOrgClient.public_repos` method
8. **Parameterize** - Test `GithubOrgClient.has_license` static method
9. **Integration test: fixtures** - Integration tests using fixtures for end-to-end testing
