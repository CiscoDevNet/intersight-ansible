"""
Script to map changed files in a PR to corresponding integration test targets.
This helps run only relevant tests instead of the full test suite.
"""

import os
import subprocess
from pathlib import Path


def get_changed_files():
    """Get list of changed files in the current PR/commit."""
    try:
        # For PR context, compare against the base branch
        if os.getenv('GITHUB_EVENT_NAME') == 'pull_request':
            base_ref = os.getenv('GITHUB_BASE_REF', 'main')
            result = subprocess.run(
                ['git', 'diff', '--name-only', f'origin/{base_ref}...HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
        else:
            # For push events, compare against previous commit
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1'],
                capture_output=True,
                text=True,
                check=True
            )

        changed_files = result.stdout.strip().split('\n')
        return [f for f in changed_files if f.strip()]

    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def map_files_to_test_targets(changed_files):
    """Map changed files to their corresponding integration test targets."""
    test_targets = set()

    # Get available test targets
    test_targets_dir = Path('tests/integration/targets')
    available_targets = {
        target.name for target in test_targets_dir.iterdir()
        if target.is_dir() and not target.name.startswith('__')
    }

    for file_path in changed_files:
        path = Path(file_path)

        # Skip non-relevant files
        if any(skip_pattern in str(path) for skip_pattern in [
            '.github/', 'README', '.gitignore', 'LICENSE',
            'CHANGELOG', 'requirements.txt', 'galaxy.yml'
        ]):
            continue

        # Handle module files
        if path.parts[0] == 'plugins' and len(path.parts) > 2 and path.parts[1] == 'modules':
            module_name = path.stem

            # Remove '_info' suffix if present (info modules use same test target)
            if module_name.endswith('_info'):
                module_name = module_name[:-5]

            if module_name in available_targets:
                test_targets.add(module_name)
                print(f"✓ Mapped {file_path} -> {module_name}")
            else:
                print(f"⚠ No test target found for module: {module_name}")
                print(f"  Available targets: {sorted(available_targets)}")

        # Handle module_utils changes - these affect multiple modules
        elif path.parts[0] == 'plugins' and 'module_utils' in path.parts:
            print(f"Module utils changed: {file_path}")
            # For module_utils changes, we could run core tests or all tests
            # Let's run a representative set of core tests
            core_tests = {'intersight_rest_api', 'intersight_info'} & available_targets
            test_targets.update(core_tests)
            print(f"Added core tests for module_utils change: {core_tests}")

        # Handle test files themselves
        elif path.parts[0] == 'tests' and 'integration' in path.parts:
            for part in path.parts:
                if part in available_targets:
                    test_targets.add(part)
                    print(f"Mapped test file {file_path} -> {part}")
                    break

        # Handle playbook changes
        elif path.parts[0] == 'playbooks':
            # Playbook changes might affect multiple modules
            # For now, let's run a basic set of tests
            basic_tests = {'intersight_info'} & available_targets
            test_targets.update(basic_tests)
            print(f"Added basic tests for playbook change: {file_path}")

    return sorted(list(test_targets))


def main():
    # For workflow_dispatch events, allow running all tests if no specific files changed
    event_name = os.getenv('GITHUB_EVENT_NAME')
    if event_name == 'workflow_dispatch':
        print("Manual workflow dispatch detected")
        # Check for special environment variable to force all tests
        if os.getenv('RUN_ALL_TESTS', '').lower() == 'true':
            test_targets_dir = Path('tests/integration/targets')
            available_targets = [
                target.name for target in test_targets_dir.iterdir()
                if target.is_dir() and not target.name.startswith('__')
            ]
            targets_string = ' '.join(available_targets)
            print(f"Running all available test targets: {available_targets}")
            github_output = os.getenv('GITHUB_OUTPUT')
            if github_output:
                with open(github_output, 'a') as f:
                    f.write(f"targets={targets_string}\n")
                    f.write("skip_tests=false\n")
            return

    # Get changed files
    changed_files = get_changed_files()

    if not changed_files:
        print("No changed files detected")
        # Use modern GitHub Actions output format
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write("targets=\n")
                f.write("skip_tests=true\n")
        return

    print(f"Changed files: {changed_files}")

    # Map to test targets
    test_targets = map_files_to_test_targets(changed_files)

    github_output = os.getenv('GITHUB_OUTPUT')
    if not test_targets:
        print("No integration tests needed for the changed files")
        if github_output:
            with open(github_output, 'a') as f:
                f.write("targets=\n")
                f.write("skip_tests=true\n")
    else:
        targets_string = ' '.join(test_targets)
        print(f"Test targets to run: {test_targets}")
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"targets={targets_string}\n")
                f.write("skip_tests=false\n")


if __name__ == '__main__':
    main()
