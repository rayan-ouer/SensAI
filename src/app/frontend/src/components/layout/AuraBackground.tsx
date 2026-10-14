/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** AuraBackground
*/

// Gradient from Aura (Golden Dawn): https://auragradients.vercel.app/?gradient=nebula-golden-dawn
const BASE_COLOR = '#0f0800'

const LAYERS = [
  {
    background: 'radial-gradient(ellipse 45% 50% at 30% 40%, rgba(251,191,36,0.85) 0%, transparent 65%)',
    blur: 'blur-[138px] md:blur-[198px]',
  },
  {
    background: 'radial-gradient(ellipse 35% 40% at 70% 35%, rgba(234,179,8,0.7) 0%, transparent 60%)',
    blur: 'blur-[125px] md:blur-[180px]',
  },
  {
    background: 'radial-gradient(ellipse 30% 35% at 50% 75%, rgba(217,119,6,0.5) 0%, transparent 55%)',
    blur: 'blur-[113px] md:blur-[162px]',
  },
  {
    background: 'radial-gradient(ellipse 20% 25% at 80% 70%, rgba(180,83,9,0.35) 0%, transparent 60%)',
    blur: 'blur-[88px] md:blur-[126px]',
  },
]

function AuraBackground() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 isolate overflow-hidden"
      style={{ backgroundColor: BASE_COLOR }}
    >
      {LAYERS.map((layer) => (
        <div
          key={layer.background}
          className={`absolute inset-0 mix-blend-screen ${layer.blur}`}
          style={{ background: layer.background }}
        />
      ))}
    </div>
  )
}

export default AuraBackground
