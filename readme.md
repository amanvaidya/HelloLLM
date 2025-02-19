My First LLM using Ollama

Tried with OpenAI, but was getting quota expired, so downloaded Ollama to run prompts offline. 
Since it was my first LLM-based model, I was trying for a text-based model only.

Since Ollama installs locally, no API key is required.

## Installation

You can install Ollama using Homebrew or download it directly:

```sh
brew install ollama
```

Or download from: [https://ollama.com/download](https://ollama.com/download)

## Verify Installation

Check if Ollama is installed correctly:

```sh
ollama --version
```

## Downloading Models

Once installed, you can download models like:

```sh
ollama pull mistral  # (4.1 GB Download)
ollama pull llama2
```

## Running Ollama

Start the Ollama service in the background:

```sh
ollama serve
```

Verify if it's running:

```sh
ollama list
```

## Switching to a Lighter Model

Since Mistral was heavy (4.1 GB) and took **25.68 sec** to execute, I moved to a lighter model: **Gemma:2B**.

### Uninstall Mistral

```sh
ollama rm mistral
```

### Install Gemma:2B

```sh
ollama pull gemma:2b
```

Using **Gemma:2B**, I received a response in **0.50 sec**.
