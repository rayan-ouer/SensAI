/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** App
*/

import './App.css'

function App() {
  const activeAgent = "Wu"
  const agents = ["Wu", "Euclid"]
  const listAgents = agents.map(agent => <li key={agent}>{agent}</li>)

  return (
    <main>
      <h1>SensAI</h1>
      <h2>Profiles</h2>
      <ul>
        {listAgents}
      </ul>
      <p>Active agent: {activeAgent}</p>
        <p>Your project assistant.</p>
    </main>
  )
}

export default App
