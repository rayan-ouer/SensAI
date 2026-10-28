##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## commands
##

from core.messages import SystemMessage
from interfaces.cli.cli_state import CliState


def switch_profile(state: CliState, args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: /profile <name>")
        return
    name = args[0]
    if name not in state.profiles:
        print(f"Unknown profile: '{name}'. Type /profiles to see available ones.")
        return
    state.active_profile = name
    note = f"The active agent has changed. From now on you are '{state.current_profile().name}'. Earlier assistant replies were written by a different agent."
    state.conversation.add_system_message(SystemMessage(content=note))
    print(f"Switched to '{name}' profile.")


def print_profiles(state: CliState, _args: list[str]) -> None:
    for key, profile in state.profiles.items():
        profile_name = profile.name
        marker = "-> " if key == state.active_profile else "   "
        print(f"{marker}{key:<16}{profile_name}")


COMMANDS = {
    "/profiles": print_profiles,
    "/profile": switch_profile,
}


def handle_command(state: CliState, user_input: str) -> None:
    args = user_input.split()
    handler = COMMANDS.get(args[0])
    if handler is None:
        print("Unknown command.")
        return
    handler(state, args[1:])
