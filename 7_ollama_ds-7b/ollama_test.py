import ollama

# Set the model to use
model = "deepseek-r1:latest"

# Get user input
prompt_input = input(f"Hi, I'm Ollama using model: {model} 😊!\n Enter your message: ")
if not prompt_input:
    exit()

# Send text to the AI model
response = ollama.chat(model, messages=[{"role": "user", "content": prompt_input}])

# Print AI's response
print(response["message"]["content"])
