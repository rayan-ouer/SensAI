##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## commands
##

from core.messages import SystemMessage


def switch_profile(config: dict, args: list[str]):
    if len(args) != 1:
        print("Usage: /profile <name>")
        return
    name = args[0]
    if name not in config["profiles"]:
        print(f"Unknown profile: '{name}'. Type /profiles to see available ones.")
        return
    config["active_profile"] = name
    note = f"The active agent has changed. From now on you are '{config['profiles'][name]['name']}'. Earlier assistant replies were written by a different agent."
    config["messages"].append(SystemMessage(content=note))
    print(f"Switched to '{name}' profile.")


def print_profiles(config: dict, _args: list[str]):
    for key, profile in config["profiles"].items():
        profile_name = profile["name"]
        marker = "-> " if key == config["active_profile"] else "   "
        print(f"{marker}{key:<12}{profile_name}")


COMMANDS = {
    "/profiles": print_profiles,
    "/profile": switch_profile,
}


def handle_command(config: dict, user_input: str):
    args = user_input.split()
    handler = COMMANDS.get(args[0])
    if handler is None:
        print("Unknown command.")
        return
    handler(config, args[1:])
