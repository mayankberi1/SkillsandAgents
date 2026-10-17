#!/usr/bin/env bash
# Universal installer — detects installed agent runtimes and installs skills.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$PROJECT_DIR/skills"

if [[ ! -d "$SKILLS_DIR" ]]; then
    echo "Error: skills/ directory not found." >&2
    exit 1
fi

echo "=== Skills & Agents — Universal Installer ==="
echo "Project: $PROJECT_DIR"
echo ""

# --- Helper functions ---

install_to() {
    local dest="$1"
    local name="$2"
    echo "Installing skills to $name: $dest"
    mkdir -p "$dest"
    for skill_dir in "$SKILLS_DIR"/*/; do
        local skill_name
        skill_name="$(basename "$skill_dir")"
        if [[ -f "$skill_dir/SKILL.md" ]]; then
            cp -r "$skill_dir" "$dest/$skill_name/" 2>/dev/null || true
            echo "  ✓ $skill_name"
        fi
    done
}

detect_platform() {
    local platforms=()

    # Check for OpenCode
    if [[ -d "$HOME/.config/opencode" ]] || command -v opencode &>/dev/null; then
        platforms+=("opencode")
    fi

    # Check for Claude Code (anthropic-cli)
    if command -v claude &>/dev/null; then
        platforms+=("claude-code")
    fi

    # Check for Codex (openai-codex / CLI)
    if command -v codex &>/dev/null || [ -d "$HOME/.agents" ]; then
        platforms+=("codex")
    fi

    # Check for Cursor
    if [[ -d "$HOME/.config/comursor" ]] || [[ -f "$HOME/.cursor/CLAUDE.md" ]]; then
        platforms+=("cursor")
    fi

    echo "${platforms[*]:-none}"
}

# --- Main logic ---

PLATFORMS=$(detect_platform)
echo "Detected platform(s): ${PLATFORMS:-none}"

if [[ "$PLATFORMS" == *"opencode"* ]]; then
    echo ""
    read -rp "Install to OpenCode? [y/N] " reply
    if [[ "${reply,,}" == "y" ]]; then
        for config_dir in "$HOME/.config/opencode/skills" "$HOME/.claude/skills"; do
            if [[ -d "$config_dir" ]] || [[ -d "$(dirname "$config_dir")" ]]; then
                install_to "$config_dir" "OpenCode ($config_dir)"
            fi
        done
    fi
fi

if [[ "$PLATFORMS" == *"claude-code"* ]]; then
    echo ""
    read -rp "Install to Claude Code? [y/N] " reply
    if [[ "${reply,,}" == "y" ]]; then
        install_to "$HOME/.claude/skills" "Claude Code (global)"
    fi
fi

if [[ "$PLATFORMS" == *"codex"* ]]; then
    echo ""
    read -rp "Install to OpenAI Codex? [y/N] " reply
    if [[ "${reply,,}" == "y" ]]; then
        install_to "$HOME/.agents/skills" "Codex (global)"
    fi

    # Offer project-local install for current directory
    echo ""
    read -rp "Install project-local (.agents/skills/)? [y/N] " reply
    if [[ "${reply,,}" == "y" ]]; then
        mkdir -p "$PROJECT_DIR/.agents/skills"
        install_to "$PROJECT_DIR/.agents/skills" "Codex (project-local)"
    fi
fi

if [[ "$PLATFORMS" == *"cursor"* ]] || true; then
    echo ""
    read -rp "Install to Cursor? [y/N] " reply
    if [[ "${reply,,}" == "y" ]]; then
        install_to "$HOME/.agents/skills" "Cursor (global)"
    fi
fi

if [[ "$PLATFORMS" == *"none"* ]]; then
    echo ""
    echo "No known agent runtimes detected."
    echo "You can still run the per-platform installer scripts directly:"
    echo ""
    for script in "$SCRIPT_DIR"/install-*.sh; do
        [[ -f "$script" ]] && echo "  bash $script"
    done
fi

echo ""
echo "=== Done ==="
