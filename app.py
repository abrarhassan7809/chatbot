from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket
from backend_funtions.scraper import search_duckduckgo, search_google, get_wikipedia_summary
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            question = await websocket.receive_text()

            # Combine results from different scrapers
            duckduckgo_results = search_duckduckgo(question)
            google_results = search_google(question)
            wikipedia_summary = get_wikipedia_summary(question)

            web_data = ""

            # Process DuckDuckGo results
            if duckduckgo_results:
                web_data += "<strong>DuckDuckGo Search Results:</strong><br>"
                for result in duckduckgo_results:
                    web_data += f"{result['title']}<br>"
                    web_data += f'<a href="{result["link"]}" style="cursor: pointer; color: #5365ef; text-decoration: none; font-size: 18px;" target="_blank">{result["link"]}</a><br>'
                web_data += "<br>"

            # Process Google results
            if google_results:
                web_data += "<strong>Google Search Results:</strong><br>"
                for result in google_results:
                    web_data += f"{result['title']}<br>"
                    web_data += f'<a href="{result["link"]}" style="cursor: pointer; color: #5365ef; text-decoration: none; font-size: 18px;" target="_blank">{result["link"]}</a><br>'
                web_data += "<br>"

            # Add Wikipedia summary if available
            if wikipedia_summary:
                web_data += "<strong>Wikipedia Summary:</strong><br>"
                web_data += f"{wikipedia_summary}<br>"

            # If no results were found
            if not web_data:
                web_data = "No relevant results found."

            # Send the combined results to the client
            await websocket.send_text(web_data)
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
