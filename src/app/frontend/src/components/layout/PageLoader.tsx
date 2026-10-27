/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** PageLoader
*/

function PageLoader() {
  return (
    <div className="flex h-dvh items-center justify-center" role="status" aria-label="Loading page">
      <img src="/logo.svg" alt="" className="size-14 animate-pulse motion-reduce:animate-none" />
    </div>
  )
}

export default PageLoader
