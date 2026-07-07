# Demo & recording guide

Three ways to show this project working — pick based on how much time you have.

## Option 1 — Terminal demo (fastest, zero setup)

```bash
python demo.py
```

Plays a full AI-agent conversation where every tool result is real. Screenshot
the output or record the terminal. Great for a LinkedIn post or a README GIF.

## Option 2 — Web dashboard (best for a screen recording)

```bash
python web_app.py     # then open http://localhost:8000
```

A clickable dashboard. Suggested ~60-second recording flow:

1. **Employee lookup** → pick `E1005` → click **Predict attrition risk**.
   Narrate: *"An explainable model — it shows exactly why Diego is high-risk."*
2. **US compliance** → pick `DC` → **Min wage**, then pick `MS` → **I-9 / E-Verify**.
   Narrate: *"Full coverage across all 50 states plus DC."*
3. **Pay-equity** → role `Senior Software Engineer` → **Analyze pay equity**.
   Narrate: *"It surfaces a 12% gender pay gap — a real US compliance concern."*
4. **Ask HR policy** → type *"do unused vacation days carry over?"* → **Search**.
   Narrate: *"Semantic search over policy documents, no ML libraries."*
5. **Approval workflow** → submit a `$6,000` expense → **Act on request** (approve).
   Narrate: *"A big expense auto-routes Manager → Finance → HR/VP."*

## Option 3 — Real AI in Claude Desktop (most impressive)

This shows a real AI assistant using your server live.

1. Install [Claude Desktop](https://claude.ai/download).
2. Open its MCP config file and add:

   ```json
   {
     "mcpServers": {
       "hr-super-agent": {
         "command": "/full/path/to/.venv/bin/python",
         "args": ["/full/path/to/server.py"]
       }
     }
   }
   ```

3. Restart Claude Desktop. You'll see the HR tools appear.
4. Ask natural questions and record the conversation:
   - *"I'm relocating from California to Texas — does my paycheck change?"*
   - *"Which of my reports is most likely to quit, and why?"*
   - *"Run a pay-equity check on our senior engineers."*
   - *"Submit a $6,000 travel expense for approval."*

A 30–60 second recording of Claude actually calling your tools is the single
most convincing artifact for a recruiter.
