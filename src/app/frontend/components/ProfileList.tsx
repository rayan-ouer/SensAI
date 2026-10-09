/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ProfileList
*/

type ProfileListProps = {
    agents: string[]
    activeAgent: string
}

function ProfileList({agents, activeAgent}: ProfileListProps) {
    const listAgents = agents.map((agent) => <li key={agent}>{agent === activeAgent ? "-> " : ""}{agent}</li>)
    return (
        <ul>
            {listAgents}
        </ul>
    )
}

export default ProfileList
