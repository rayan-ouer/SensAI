/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** App
*/

import './App.css'
import ProfileList from './components/ProfileList'

function App() {
  const activeAgent = "Wu"
  const agents = ["Wu", "Euclid"]

  return (
    <main>
      <h1>SensAI</h1>
      <h2>Profiles</h2>
      <ProfileList agents={agents} activeAgent={activeAgent}/>
      <p>Active agent: {activeAgent}</p>
      <p>Your project assistant.</p>
    </main>
  )
}

export default App
