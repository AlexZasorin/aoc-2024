set shell := ["zsh", "-cu"]

fetch-input day:
  #!/usr/bin/env zsh
  day_str=$(printf "%02d" {{day}})

  print -P "%F{magenta}Geting day-$day_str inputs...%f"
  cookie=$(cat .session-cookie 2>/dev/null)
  curl -s -H "Cookie: session=$cookie" https://adventofcode.com/2024/day/{{day}}/input > inputs/day-$day_str.txt

setup day:
  #!/usr/bin/env zsh
  day_str=$(printf "%02d" {{day}})

  print -P "%F{magenta}Setting up day-$day_str package...%f"

  uv init puzzles/day-$day_str --package

  # Copy common code into __init__.py

  # Create a solution.py with an empty part1 and part2 function

  just fetch-input day={{day}}

  # Get day examples for part1 and part2

