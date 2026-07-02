import os
import gradio as gr
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPT_V1

# טעינת משתני סביבה
load_dotenv()

# מעקף SSL בשביל נטפרי
custom_http_client = httpx.Client(verify=False)

# אתחול הלקוח הרשמי של OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=custom_http_client
)

def generate_cli(user_text):
    if not user_text.strip():
        return "בבקשה הכניסי הוראה בשפה טבעית."
    
    formatted_prompt = PROMPT_V1.format(user_input=user_text)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"שגיאה בפנייה ל-LLM: {str(e)}"

# ממשק Gradio
with gr.Blocks(title="Natural Language to CLI") as demo:
    gr.Markdown("# 🔛 Prompt Engineering בפעולה: מטקסט לפקודת CLI")
    gr.Markdown("הכניסי הוראה בשפה טבעית וקבלי את פקודת הטרמינל המתאימה.")
    
    with gr.Row():
        input_text = gr.Textbox(label="הוראה בשפה טבעית (למשל: 'תראה לי את רשימת הקבצים')", placeholder="הקלידי כאן...")
        output_command = gr.Textbox(label="פקודת CLI שהופקה", interactive=False)
    
    submit_btn = gr.Button("המר לפקודה")
    submit_btn.click(fn=generate_cli, inputs=input_text, outputs=output_command)

if __name__ == "__main__":
    demo.launch()