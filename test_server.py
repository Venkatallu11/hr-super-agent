"""Quick smoke test: list the server's tools and call each one."""
import asyncio
from server import mcp


async def main():
    tools = await mcp.list_tools()
    print(f"Server exposes {len(tools)} tools:")
    for t in tools:
        print(f"  - {t.name}: {t.description.splitlines()[0]}")
    print("\n--- Calling each tool ---\n")

    async def call(name, args):
        result = await mcp.call_tool(name, args)
        # call_tool returns (content_list, ...) in newer SDKs; handle both.
        content = result[0] if isinstance(result, tuple) else result
        text = content[0].text if content else "(no output)"
        print(f"> {name}({args})\n{text}\n")

    await call("get_leave_balance", {"employee_id": "E1002"})
    await call("get_onboarding_checklist", {"employee_id": "E1002"})
    await call("check_state_tax_compliance", {"employee_id": "E1002", "new_state": "TX"})
    await call("notify_manager", {"employee_id": "E1002", "message": "Please approve John's leave request."})


asyncio.run(main())
