import os
import re

import gym

import miniworld


# From python docs
def trim(docstring):
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = 232323
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < 232323:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return "\n".join(trimmed)


LAYOUT = "env"

pattern = re.compile(r"(?<!^)(?=[A-Z])")

miniworld_env_ids = sorted(list(miniworld.envs.env_ids))

previous_env_name = None

for env_id in miniworld_env_ids:
    res_env_md = "---\nautogenerated:\n---"
    print(env_id)
    env_spec = gym.spec(env_id)

    split = env_spec.entry_point.split(":")
    mod = __import__(split[0], fromlist=[split[1]])
    env_class = getattr(mod, split[1])
    docstring = trim(env_class.__doc__)

    # MiniWorld-Hallway -> Hallway
    env_name = env_spec.name.split("-")[1]

    # We are not adding sub envs like YMazeLeft
    if previous_env_name is None or previous_env_name not in env_name:
        previous_env_name = env_name
        env_name_snake_case = "_".join(env_id.lower().split("-")[1:-1])

        # Title
        res_env_md += f"\n# {env_name}\n\n"
        # Figure
        res_env_md += (
            "```{figure}"
            + f" ../_static/environments/{env_name_snake_case}.jpg"
            + f" \n:width: 300px\n:alt: {env_name}\n```\n\n"
        )
        # Docstring
        res_env_md += f"{docstring}\n"

        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "environments",
            f"{env_name_snake_case}.md",
        )

        file = open(file_path, "w+", encoding="utf-8")
        file.write(res_env_md)
        file.close()