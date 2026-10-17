#!/usr/bin/env bash
# Installer for OpenCode — installs skills to OpenCode skill paths.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$PROJECT_DIR/skills"

if [[ ! -d "$SKILLS_DIR" ]]; then
    echo "Error: skills/ directory not found." >&2
    exit 1
fi

echo "=== OpenCode Skill Installer ==="

# Determine target directories (user may have multiple configured paths)
TARGET_DIRS=(
    "$HOME/.config/opencode/skills"
    "$PROJECT_DIR/.opencode/skills"
    "$PROJECT_DIR/.claude/skills"
    "$PROJECT_DIR/.agents/skills"
)

count=0
for target in "${TARGET_DIRS[@]}"; do
    # Check if the parent directory exists (config dir or project root)
    parent="$(dirname "$target")"
    [[ ! -d "$parent" ]] && continue

    echo "Installing to: $target"
    mkdir -p "$target"
    for skill_dir in "$SKILLS_DIR"/*/; do
        local_name="$(basename "$skill_dir")"
        if [[ -f "$skill_dir/SKILL.md" ]]; then
            cp -r "$skill_dir" "$target/$local_name/" 2>/dev/null || true
            echo "  ✓ $local_name"
        fi
    done
    count=$((count + 1))
done

if [[ $count -eq 0 ]]; then
    echo "No writable OpenCode config paths found." >&2
    echo "Create one of these directories manually and re-run:" >&2
    for target in "${TARGET_DIRS[@]}"; do
        echo "  mkdir -p $(dirname "$target")" >&2
    done
fi

echo ""
echo "=== Done — OpenCode skills installed ==="
