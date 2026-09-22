import type { Projeto } from "@/lib/api/client";
import { ProjetoCard } from "./ProjetoCard";

export interface ProjetoListProps {
  projetos: Projeto[];
  vazioLabel?: string;
}

export function ProjetoList({
  projetos,
  vazioLabel = "Nenhum projeto cadastrado ainda.",
}: ProjetoListProps) {
  if (projetos.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-black/15 p-8 text-center text-sm text-black/50 dark:border-white/15 dark:text-white/50">
        {vazioLabel}
      </p>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {projetos.map((projeto) => (
        <ProjetoCard key={projeto.id} projeto={projeto} />
      ))}
    </div>
  );
}
