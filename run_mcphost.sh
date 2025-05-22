# Models can be specified using the --model (-m) flag:

# Anthropic Claude (default): anthropic:claude-3-5-sonnet-latest
# OpenAI or OpenAI-compatible: openai:gpt-4o
# Ollama models: ollama:granite3.3:8b
# Google: google:gemini-2.5-flash-preview-04-17 --google-api-key $GEMINI_API_KEY 

./mcphost -m ollama:granite3.3:8b --config ./mcp.json --system-prompt ./my-system-prompt.txt --message-window 0