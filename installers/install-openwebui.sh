#!/usr/bin/env bash
# Installer/guide for Open WebUI / LibreChat — these platforms load skills
# differently from CLI agents. See docs/PLATFORMS.md for details.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$PROJECT_DIR/skills"

echo "=== Open WebUI / LibreChat Skill Setup ==="
echo ""

# These platforms do not load skills via ~/.agents/skills/ or similar.
# Instead, they use project-local skill loading:
#
#   Open WebUI — Computer agent reads from a local .agents/skills/ or
#                custom path configured in the Computer tool settings.
#   LibreChat  — Skills may be loaded via the Agent plugin's config
#                pointing at a directory of SKILL.md files.
#

echo "For Open WebUI:"
echo "  1. Copy skills to your Open WebUI project directory:"
echo "     cp -r $SKILLS_DIR/* /path/to/open-webui/.agents/skills/"
echo ""
echo "For LibreChat:"
echo "  1. Configure the Agent plugin to point at $SKILLS_DIR"
echo "  2. Or copy skills to your LibreChat config directory:"
echo "     cp -r $SKILLS_DIR/* /path/to/librechat/.agents/skills/"
echo ""

if [[ ! -d "$SKILLS_DIR" ]]; then
    echo "Error: skills/ directory not found." >&2
    exit 1
fi

# Offer project-local install for common deployment paths
DEPLOY_PATHS=(
    "/var/lib/open-webui"
    "/app/open-webui"
    "${HOME}/open-webui"
    "${HOME}/librechat"
)

echo "Searching for common deployment directories..."
found=0
for deploy in "${DEPLOY_PATHS[@]}"; do
    if [[ -d "$deploy" ]]; then
        echo "  Found: $deploy"
        found=$((found + 1))
    fi
done

if [[ $found -eq 0 ]]; then
    echo "  No common deployment directories detected."
    echo "  Update the paths above to match your setup."
fi

echo ""
echo "=== See docs/PLATFORMS.md for full platform details ==="
