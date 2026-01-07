#!/usr/bin/env bash
# Worktree Management Script for Parallel AI Agent Development
#
# This script creates and manages git worktrees optimized for running
# multiple Claude Code or Cursor AI agents in parallel.
#
# Usage:
#   ./scripts/worktree.sh create <name> [base-branch]  # Create a new worktree
#   ./scripts/worktree.sh list                          # List all worktrees
#   ./scripts/worktree.sh remove <name>                 # Remove a worktree
#   ./scripts/worktree.sh clean                         # Remove all worktrees

set -euo pipefail

# Configuration
WORKTREE_DIR="../worktrees"  # Parent directory for worktrees (sibling to main repo)
MAIN_REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE=".env"
ENV_EXAMPLE_FILE=".env.example"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Ensure we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not a git repository. Run this from the project root."
        exit 1
    fi
}

# Create a new worktree for parallel development
create_worktree() {
    local name="${1:-}"
    local base_branch="${2:-HEAD}"

    if [[ -z "$name" ]]; then
        log_error "Usage: $0 create <name> [base-branch]"
        log_info "Example: $0 create feature-auth main"
        exit 1
    fi

    local worktree_path="${WORKTREE_DIR}/${name}"
    local branch_name="worktree/${name}"

    # Check if worktree already exists
    if [[ -d "$worktree_path" ]]; then
        log_error "Worktree '$name' already exists at $worktree_path"
        exit 1
    fi

    # Create parent directory if needed
    mkdir -p "$WORKTREE_DIR"

    log_info "Creating worktree '$name' from '$base_branch'..."

    # Create new branch and worktree
    cd "$MAIN_REPO_DIR"
    git worktree add -b "$branch_name" "$worktree_path" "$base_branch"

    log_success "Worktree created at: $worktree_path"

    # Copy .env file if it exists
    setup_env_file "$worktree_path"

    # Copy any local configuration files
    setup_local_configs "$worktree_path"

    # Install dependencies in the worktree
    setup_dependencies "$worktree_path"

    log_success "Worktree '$name' is ready for parallel development!"
    echo ""
    log_info "To start working:"
    echo "  cd $worktree_path"
    echo "  claude  # or cursor ."
    echo ""
    log_info "Branch: $branch_name"
}

# Set up .env file in worktree
setup_env_file() {
    local worktree_path="$1"

    if [[ -f "${MAIN_REPO_DIR}/${ENV_FILE}" ]]; then
        log_info "Copying .env file to worktree..."
        cp "${MAIN_REPO_DIR}/${ENV_FILE}" "${worktree_path}/${ENV_FILE}"

        # Optionally modify DATABASE_URL to use a different database for isolation
        # Uncomment the following to use a unique database per worktree:
        # local worktree_name=$(basename "$worktree_path")
        # sed -i "s|/app|/app_${worktree_name}|g" "${worktree_path}/${ENV_FILE}"

        log_success ".env file copied"
    elif [[ -f "${MAIN_REPO_DIR}/${ENV_EXAMPLE_FILE}" ]]; then
        log_warning "No .env file found. Copying .env.example..."
        cp "${MAIN_REPO_DIR}/${ENV_EXAMPLE_FILE}" "${worktree_path}/${ENV_FILE}"
        log_warning "Please update ${worktree_path}/${ENV_FILE} with your settings"
    else
        log_warning "No .env or .env.example found. Create one manually."
    fi
}

# Copy local configuration files that aren't in git
setup_local_configs() {
    local worktree_path="$1"

    # Copy .claude/settings.local.json if it exists
    if [[ -f "${MAIN_REPO_DIR}/.claude/settings.local.json" ]]; then
        log_info "Copying Claude local settings..."
        cp "${MAIN_REPO_DIR}/.claude/settings.local.json" "${worktree_path}/.claude/settings.local.json"
    fi

    # Copy any .secrets.baseline if it exists
    if [[ -f "${MAIN_REPO_DIR}/.secrets.baseline" ]]; then
        cp "${MAIN_REPO_DIR}/.secrets.baseline" "${worktree_path}/.secrets.baseline"
    fi
}

# Install dependencies in worktree
setup_dependencies() {
    local worktree_path="$1"

    if command -v uv &> /dev/null; then
        log_info "Installing dependencies with uv..."
        cd "$worktree_path"
        uv sync --quiet 2>/dev/null || log_warning "uv sync failed - run manually"
        cd "$MAIN_REPO_DIR"
    else
        log_warning "uv not found. Run 'uv sync' manually in the worktree."
    fi
}

# List all worktrees
list_worktrees() {
    log_info "Git worktrees:"
    echo ""
    git worktree list
    echo ""

    if [[ -d "$WORKTREE_DIR" ]]; then
        log_info "Parallel agent worktrees in ${WORKTREE_DIR}:"
        for dir in "$WORKTREE_DIR"/*/; do
            if [[ -d "$dir" ]]; then
                local name=$(basename "$dir")
                local branch=$(cd "$dir" && git branch --show-current 2>/dev/null || echo "unknown")
                echo "  - $name (branch: $branch)"
            fi
        done
    fi
}

# Remove a worktree
remove_worktree() {
    local name="${1:-}"

    if [[ -z "$name" ]]; then
        log_error "Usage: $0 remove <name>"
        exit 1
    fi

    local worktree_path="${WORKTREE_DIR}/${name}"
    local branch_name="worktree/${name}"

    if [[ ! -d "$worktree_path" ]]; then
        log_error "Worktree '$name' not found at $worktree_path"
        exit 1
    fi

    log_info "Removing worktree '$name'..."

    # Remove the worktree
    cd "$MAIN_REPO_DIR"
    git worktree remove "$worktree_path" --force 2>/dev/null || rm -rf "$worktree_path"

    # Optionally delete the branch
    read -p "Delete branch '$branch_name'? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -D "$branch_name" 2>/dev/null || log_warning "Branch not found or already deleted"
    fi

    log_success "Worktree '$name' removed"
}

# Remove all worktrees
clean_worktrees() {
    log_warning "This will remove ALL worktrees in ${WORKTREE_DIR}"
    read -p "Are you sure? [y/N] " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cancelled"
        exit 0
    fi

    cd "$MAIN_REPO_DIR"

    # Get list of worktrees (excluding main)
    local worktrees=$(git worktree list --porcelain | grep "^worktree" | grep -v "$MAIN_REPO_DIR" | cut -d' ' -f2)

    for wt in $worktrees; do
        log_info "Removing $wt..."
        git worktree remove "$wt" --force 2>/dev/null || rm -rf "$wt"
    done

    # Prune any stale worktree references
    git worktree prune

    log_success "All worktrees removed"
}

# Show help
show_help() {
    cat << EOF
Worktree Management for Parallel AI Agent Development

USAGE:
    $0 <command> [arguments]

COMMANDS:
    create <name> [base-branch]   Create a new worktree for parallel development
    list                          List all worktrees
    remove <name>                 Remove a worktree
    clean                         Remove all worktrees
    help                          Show this help message

EXAMPLES:
    # Create a worktree for a new feature
    $0 create auth-feature main

    # Create a worktree from current HEAD
    $0 create bugfix-123

    # List all worktrees
    $0 list

    # Remove a worktree when done
    $0 remove auth-feature

PARALLEL DEVELOPMENT WORKFLOW:
    1. Create worktrees for each task:
       $0 create task-a main
       $0 create task-b main

    2. Open each worktree in a separate terminal/Claude session:
       cd ../worktrees/task-a && claude
       cd ../worktrees/task-b && claude

    3. Each agent works independently on its own branch

    4. Merge completed work back to main:
       git checkout main
       git merge worktree/task-a
       git merge worktree/task-b

    5. Clean up:
       $0 remove task-a
       $0 remove task-b

EOF
}

# Main entry point
main() {
    check_git_repo

    local command="${1:-help}"
    shift || true

    case "$command" in
        create)
            create_worktree "$@"
            ;;
        list)
            list_worktrees
            ;;
        remove)
            remove_worktree "$@"
            ;;
        clean)
            clean_worktrees
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
