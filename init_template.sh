#!/usr/bin/env bash
set -euo pipefail

HYPHEN_TOKEN="software-project-template"
SNAKE_TOKEN="software_project_template"

usage() {
  cat <<'EOF'
Usage: ./init_template.sh <project-slug>
       ./init_template.sh --help

Initialize a repository from the software project template.

Arguments:
  project-slug   Lowercase letters, numbers, and hyphens only.
                 Must not start or end with a hyphen.

Options:
  -h, --help     Show this help message.
EOF
}

die() {
  echo "Error: $*" >&2
  echo >&2
  usage >&2
  exit 1
}

validate_slug() {
  local slug="$1"

  [[ "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] \
    || die "Invalid slug: $slug"
}

main() {
  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
  esac

  [[ $# -eq 1 ]] || die "Expected exactly one project slug."

  local project_slug_hyphen="$1"
  validate_slug "$project_slug_hyphen"

  local project_slug_snake="${project_slug_hyphen//-/_}"
  local current_date="$(date +%F)"

  local root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
  local decisions_file="$root_dir/docs/decisions.md"

  local -a files=()
  mapfile -d '' files < <(
    find "$root_dir" \
      \( -name .git -o -name .next -o -name .venv -o -name node_modules -o -name __pycache__ \) -prune -o \
      -type f \
      ! -name init_template.sh \
      -exec grep -IlZ -E "$HYPHEN_TOKEN|$SNAKE_TOKEN" {} +
  )

  if ((${#files[@]})); then
    perl -pi -e "
      s/\Q$HYPHEN_TOKEN\E/$project_slug_hyphen/g;
      s/\Q$SNAKE_TOKEN\E/$project_slug_snake/g;
    " "${files[@]}"
  fi

  if [[ -f "$decisions_file" ]]; then
    perl -pi -e "s/\[DATE\]/$current_date/g" "$decisions"
  fi

  cat > "$root_dir/README.md" <<EOF
## $project_slug_hyphen

This repository was created from [julienberman/software-project-template](https://github.com/julienberman/software-project-template) and by default shares its dependencies and prerequisites.
EOF

  echo "Updated ${#files[@]} template files"
  echo "Wrote README.md"
}

main "$@"
