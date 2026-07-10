#!/bin/sh
# Generic pre-commit hook for non-JS projects

# Check for debug code
if git diff --cached --diff-filter=ACMR | grep -E 'console\.log|print\(|fmt\.Print|dbg!' > /dev/null 2>&1; then
  echo "Warning: Debug code detected in staged files"
  echo "Please review before committing"
fi
