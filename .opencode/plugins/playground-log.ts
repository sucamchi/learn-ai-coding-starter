import { Plugin } from "@opencode/plugin"
import { mkdir, appendFile } from "node:fs/promises"
import { dirname } from "node:path"

const LOG_PATH = "logs/plugin-playground.log"

function commandFrom(input: unknown): string | undefined {
  if (typeof input !== "object" || input === null) return undefined
  const { command } = input as { command?: unknown }
  return typeof command === "string" ? command : undefined
}

export default Plugin.define({
  id: "playground-log",
  async setup(ctx) {
    await ctx.tool.hook("execute.before", async (event) => {
      if (event.tool !== "shell") return
      const command = commandFrom(event.input)
      if (!command?.includes("playground/server.py")) return

      const path = `${ctx.location.directory}/${LOG_PATH}`
      await mkdir(dirname(path), { recursive: true })
      await appendFile(path, "playground shell request\n")
    })
  },
})
