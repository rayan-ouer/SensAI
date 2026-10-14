/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** PageLoader
*/

// Loader from Dot Matrix: https://dotmatrix.zzzzshawn.cloud/

import { DotmSquare3 } from '@/components/ui/dotm-square-3'

function PageLoader() {
  return (
    <div className="flex h-dvh items-center justify-center" role="status">
      <DotmSquare3 size={44} dotSize={6} color="#fbbf24" ariaLabel="Loading page" />
    </div>
  )
}

export default PageLoader
