/**
 * Cliente HTTP tipado do Paris Group Copilot.
 *
 * Os tipos vêm de `src/types/api.d.ts`, gerado a partir do contrato OpenAPI
 * publicado pelo backend FastAPI em /openapi.json.
 *
 * Para regenerar depois de alterar o backend:
 *   npx openapi-typescript http://localhost:8000/openapi.json -o src/types/api.d.ts
 *
 * Nunca edite `src/types/api.d.ts` à mão — ele é sobrescrito a cada geração.
 */
import createClient from "openapi-fetch";
import type { paths, components } from "@/types/api";

const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const apiClient = createClient<paths>({ baseUrl });

/** Tipos de domínio derivados do contrato — sem redigitação. */
export type Projeto = components["schemas"]["ProjetoOut"];
export type Hipotese = components["schemas"]["HipoteseOut"];
