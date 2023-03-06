import HelloComponent from "../components/hello.svelte"
import { writable } from "svelte/store"

export const defaultComponent = writable(HelloComponent)

export const components = {
    HelloComponent
}
