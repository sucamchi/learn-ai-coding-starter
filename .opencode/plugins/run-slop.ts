import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "run-slop",
  async setup(ctx) {
    await ctx.tool.transform((editor) => {
      editor.add({
        name: "run_slop",
        description: "Run a SlopLang program with Sloperator and return stdout, stderr, and exitCode as JSON.",
        options: { codemode: false },
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, relative to the project root.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        execute: async (input, context) => {
          const { path } = input as { path: string }
          const proc = Bun.spawn(["uv", "run", "--no-active", "sloperator.py", path], {
            cwd: ctx.location.directory,
            stdout: "pipe",
            stderr: "pipe",
          })

          const [stdout, stderr, exitCode] = await Promise.all([
            new Response(proc.stdout).text(),
            new Response(proc.stderr).text(),
            proc.exited,
          ])

          if (context.signal.aborted) proc.kill()

          return { content: JSON.stringify({ stdout, stderr, exitCode }) }
        },
      })
    })
  },
})
