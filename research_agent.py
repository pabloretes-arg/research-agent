from dotenv import load_dotenv
load_dotenv()
from smolagents import tool, LiteLLMModel, CodeAgent, FinalAnswerTool, GradioUI, DuckDuckGoSearchTool, VisitWebpageTool
import datetime
import pytz
import requests
from io import BytesIO
from urllib.parse import quote
from PIL import Image


# ---------- HERRAMIENTAS ----------

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


@tool
def generate_image(prompt: str) -> Image.Image:
    """A tool that generates an image from a text description.
    Args:
        prompt: A detailed description of the image, in English. Add details to improve the result (e.g., 'a red apple on a wooden table, photorealistic, high-res').
    """
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=768&height=768&nologo=true"
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


web_search = DuckDuckGoSearchTool()
visit_webpage = VisitWebpageTool()
final_answer = FinalAnswerTool()


# ---------- MODELO (el "cerebro") ----------

model = LiteLLMModel(
    model_id="gemini/gemini-flash-lite-latest",
    max_tokens=4096,
)


# ---------- AGENTE ----------

agent = CodeAgent(
    model=model,
    tools=[final_answer, get_current_time_in_timezone, generate_image, web_search, visit_webpage],
    max_steps=8,
    verbosity_level=1,
    instructions=(
	"If the user says 'today' or 'now', first call get_current_time_in_timezone "
        "with 'America/Argentina/Buenos_Aires' to get the current date. "
        "When searching the web, keep only results from that date and discard results from other days. "
        "Always think and answer in English."
        "Write your thoughts as plain sentences. Never start a line of your thoughts with '#'."
    ),
)


# ---------- INTERFAZ ----------

GradioUI(agent).launch(share=False)