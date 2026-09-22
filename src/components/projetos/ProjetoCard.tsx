import type { Projeto } from "@/lib/api/client";

export interface ProjetoCardProps {
  projeto: Projeto;
}

export function ProjetoCard({ projeto }: ProjetoCardProps) {
  const criadoEm = new Date(projeto.criado_em).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  return (
    <article className="rounded-lg border border-black/10 bg-white p-5 shadow-sm dark:border-white/10 dark:bg-white/5">
      <div className="flex items-baseline justify-between gap-4">
        <h2 className="text-lg font-semibold tracking-tight">{projeto.nome}</h2>
        <span className="shrink-0 text-xs text-black/50 dark:text-white/50">
          {criadoEm}
        </span>
      </div>

      <dl className="mt-4 space-y-3 text-sm">
        <div>
          <dt className="text-xs font-medium uppercase tracking-wider text-black/40 dark:text-white/40">
            Contexto
          </dt>
          <dd className="mt-1 text-black/70 dark:text-white/70">{projeto.contexto}</dd>
        </div>
        <div>
          <dt className="text-xs font-medium uppercase tracking-wider text-black/40 dark:text-white/40">
            Dor do usuário
          </dt>
          <dd className="mt-1 text-black/70 dark:text-white/70">{projeto.dor_usuario}</dd>
        </div>
      </dl>
    </article>
  );
}
