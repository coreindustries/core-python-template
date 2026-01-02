#!/bin/bash
# Security gate hook
# Warns about security-sensitive patterns in code changes

set -e

FILE="$1"
CONTENT="$2"

# Security patterns to check
declare -A PATTERNS=(
    ["password.*=.*['\"]"]="Potential hardcoded password"
    ["api[_-]?key.*=.*['\"]"]="Potential hardcoded API key"
    ["secret.*=.*['\"]"]="Potential hardcoded secret"
    ["token.*=.*['\"]"]="Potential hardcoded token"
    ["AKIA[A-Z0-9]{16}"]="AWS Access Key ID detected"
    ["-----BEGIN.*PRIVATE KEY-----"]="Private key detected"
    ["eval\("]="Dangerous eval() usage"
    ["exec\("]="Dangerous exec() usage"
    ["shell=True"]="Shell injection risk (shell=True)"
    ["subprocess.*shell"]="Shell injection risk in subprocess"
    ["os\.system"]="Command injection risk (os.system)"
    ["pickle\.load"]="Insecure deserialization (pickle)"
    ["yaml\.load\([^,]*\)"]="Insecure YAML loading (use safe_load)"
    ["SELECT.*\+.*\""]="SQL injection risk (string concatenation)"
    ["f\".*SELECT"]="SQL injection risk (f-string in query)"
)

WARNINGS=()

for pattern in "${!PATTERNS[@]}"; do
    if echo "$CONTENT" | grep -qE "$pattern"; then
        WARNINGS+=("⚠️  ${PATTERNS[$pattern]}: $pattern")
    fi
done

if [ ${#WARNINGS[@]} -gt 0 ]; then
    echo "🔒 Security Review Required for: $FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    for warning in "${WARNINGS[@]}"; do
        echo "$warning"
    done
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Please review these patterns and ensure they are:"
    echo "1. Using environment variables for secrets"
    echo "2. Properly sanitizing user input"
    echo "3. Using parameterized queries for SQL"
    echo ""
    echo "Run /security-scan for a comprehensive check."
fi
