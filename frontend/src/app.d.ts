// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface Platform {}
	}
}

import type { SvelteComponentTyped } from "svelte";
export type Props<T> = T extends SvelteComponentTyped<infer P, any, any> ? P : never;

// and a bonus:
export type Events<T> = T extends SvelteComponentTyped<any, infer E, any> ? E : never;
export type Slots<T> = T extends SvelteComponentTyped<any, any, infer S> ? S : never;

export {};


