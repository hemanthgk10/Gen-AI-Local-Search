import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class GenerativeAI:
    def __init__(self):
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api")
        self.model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

    def generate_response(self, query, search_results):
        """
        Generate a response using Generative AI with search results as context.

        Args:
            query (str): User's query.
            search_results (list[dict]): List of search results, where each result is a dict containing 'id', 'content', and 'score'.

        Returns:
            str: AI-generated response.
        """

        if search_results != '':
            # Create context from search results
            context = "\n".join(
                [f"Document [{result['id']}]: {result['content']}" for result in search_results]
            )

            # Construct the prompt with the context and the query
            prompt = f"""Answer the user's question using the documents given in the context.
        In the context are documents that should contain an answer.
        Please always reference the document ID (in square brackets, for example [0],[1]) of the document that was used to make a claim.
        Use as many citations and documents as necessary to answer the question based on the context provided.

        Context:
        {context}

        Question: {query}

        Answer:"""
        else:
            prompt = query

        payload = {"model": self.model_name, "prompt": prompt}
        response = requests.post(f"{self.api_url}/api/generate", json=payload)

        if response.status_code == 200:
            # Collect all the chunks and combine them into a complete response
            full_response = ""
            try:
                # Stream response and process each chunk as a separate JSON object
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk:  # Ignore empty lines
                        # Parse each chunk into a JSON object
                        chunk_data = json.loads(chunk)  # Use json.loads for parsing each chunk
                        if chunk_data.get("done"):
                            break
                        full_response += chunk_data.get("response", "")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from chunk: {e}")
                return "Error: Failed to parse response."

            return full_response if full_response else "No response generated."
        else:
            return f"Error: {response.status_code} - {response.text}"

