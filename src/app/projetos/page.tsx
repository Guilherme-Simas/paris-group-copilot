import { apiClient } from "@/lib/api/client";
import { ProjetoList } from "@/components/projetos/ProjetoList";

export const dynamic = "force-dynamic";

export default async function ProjetosPage() {
  const { data, error } = await apiClient.GET("/projetos");

  return (
    <main className="mx-auto max-w-3xl px-4 py-12">
      <header className="mb-8">
        <p className="text-xs font-medium uppercase tracking-widest text-black/40 dark:text-white/40">
          Paris Group Copilot
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Projetos</h1>
        <p className="mt-2 text-sm text-black/60 dark:text-white/60">
          Produtos do studio, carregados da API via contrato OpenAPI tipado.
        </p>
      </header>

      {error ? (
        <p className="rounded-lg border border-red-500/30 bg-red-500/5 p-4 text-sm text-red-700 dark:text-red-400">
          Não foi possível carregar os projetos. Verifique se a API está no ar em{" "}
          <code>{process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}</code>.
        </p>
      ) : (
        <ProjetoList projetos={data ?? []} />
      )}
    </main>
  );
}
