import type { Operadora } from '@/types/operadora'

export async function searchOperadoras(query: string): Promise<Operadora[]> {
  const response = await fetch(`http://localhost:8000/operadoras/?query=${encodeURIComponent(query)}`)
  if (!response.ok) throw new Error('Erro ao buscar operadoras')
  return response.json()
}