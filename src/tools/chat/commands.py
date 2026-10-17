##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## commands
##

from core.messages import SystemMessage
from interfaces.cli.session_data import Session


def switch_profile(session: Session, args: list[str]):
    if len(args) != 1:
        print("Usage: /profile <name>")
        return
    name = args[0]
    if name not in session.profiles:
        print(f"Unknown profile: '{name}'. Type /profiles to see available ones.")
        return
    session.active_profile = name
    note = f"The active agent has changed. From now on you are '{session.current_profile().name}'. Earlier assistant replies were written by a different agent."
    session.messages.append(SystemMessage(content=note))
    print(f"Switched to '{name}' profile.")


def print_profiles(session: Session, _args: list[str]):
    for key, profile in session.profiles.items():
        profile_name = profile.name
        marker = "-> " if key == session.active_profile else "   "
        print(f"{marker}{key:<12}{profile_name}")


COMMANDS = {
    "/profiles": print_profiles,
    "/profile": switch_profile,
}


def handle_command(session: Session, user_input: str):
    args = user_input.split()
    handler = COMMANDS.get(args[0])
    if handler is None:
        print("Unknown command.")
        return
    handler(session, args[1:])
