# Set Vercel Environment Variable
# Run: python set_vercel_env.py

import subprocess
import os

api_key = "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"

print("Setting OPENAI_API_KEY...")
result = subprocess.run(
    ["vercel", "env", "add", "OPENAI_API_KEY", "production"],
    input=api_key,
    text=True,
    capture_output=True
)
print(result.stdout)
print(result.stderr)

print("\nDeploying...")
result = subprocess.run(["vercel", "--prod"], capture_output=True, text=True)
print(result.stdout)
