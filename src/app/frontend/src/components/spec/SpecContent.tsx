/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** SpecContent
*/

type SpecContentProps = {
  text: string
}

function clean(line: string): string {
  return line.replace(/^_(.*)_$/, '$1')
}

function SpecLine({ line }: { line: string }) {
  if (line.startsWith('## '))
    return <h3 className="mt-4 mb-1 text-xs font-medium tracking-wide text-amber-200/80 uppercase">{line.slice(3)}</h3>
  if (line.startsWith('# '))
    return <h2 className="text-sm font-medium text-amber-50">{line.slice(2)}</h2>
  if (line.startsWith('- '))
    return <li className="ml-4 list-disc text-amber-50/80">{clean(line.slice(2))}</li>
  const text = clean(line)
  const empty = text === 'Nothing yet.'
  return <p className={empty ? 'text-amber-100/30 italic' : 'text-amber-50/80'}>{text}</p>
}

function SpecContent({ text }: SpecContentProps) {
  const lines = text.split('\n').map((line) => line.trim()).filter((line) => line !== '')
  return (
    <div className="space-y-1 text-[0.8rem] leading-relaxed">
      {lines.map((line, index) => (
        <SpecLine key={index} line={line} />
      ))}
    </div>
  )
}

export default SpecContent
