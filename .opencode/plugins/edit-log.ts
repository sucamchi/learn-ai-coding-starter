import { Plugin } from "@opencode/plugin"
import { mkdir, appendFile } from "node:fs/promises"
import { dirname } from "node:path"

const LOG_PATH = "logs/plugin-tools.log"
const FILE_CHANGING_TOOLS = new Set(["edit", "write", "patch"])

export default Plugin.define({
  id: "edit-log",
  async setup(ctx) {
    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return
      if (!FILE_CHANGING_TOOLS.has(event.tool)) return

      const path = `${ctx.location.directory}/${LOG_PATH}`
      await mkdir(dirname(path), { recursive: true })
      await appendFile(
        path,
        `${JSON.stringify({ tool: event.tool, status: event.status })}\n`,
      )
    })
  },
})
