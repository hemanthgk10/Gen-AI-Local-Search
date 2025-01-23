import os
import threading
import webview

# HTML for the PyWebView UI
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Streamlit App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            margin-left: 10px;
            cursor: pointer;
        }
        #result {
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Search Tool</h1>
    <div>
        <input type="text" id="search-input" placeholder="Enter your search query...">
        <button onclick="performSearch()">Search</button>
    </div>
    <div id="result"></div>
    <script>
        async function performSearch() {
            const query = document.getElementById("search-input").value;
            const resultDiv = document.getElementById("result");
            if (!query) {
                resultDiv.textContent = "Please enter a search query.";
                return;
            }
            resultDiv.textContent = "Searching...";
            try {
                // Send query to Streamlit backend
                const response = await fetch("http://localhost:8501/api/search", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query })
                });
                const data = await response.json();
                resultDiv.textContent = data.result || "No results found.";
            } catch (error) {
                resultDiv.textContent = "Error connecting to the search service.";
            }
        }
    </script>
</body>
</html>
"""

# Start Streamlit in a separate thread
def start_streamlit():
    os.system("streamlit run app.py")

threading.Thread(target=start_streamlit, daemon=True).start()

# Open the HTML UI in a PyWebView window
webview.create_window("My Streamlit App", html=HTML_CONTENT)
webview.start()


