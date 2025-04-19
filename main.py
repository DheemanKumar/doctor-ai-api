from flask import Flask, request, jsonify
from fastapi.middleware.cors import CORSMiddleware
from doctor_ai.crew import AIDoctorAssistant
from datetime import datetime
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
import browser_use
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or limit it to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/run-diagnosis", methods=["POST"])
def run_diagnosis():
    try:
        data = request.json
        required_fields = ["user_name", "age", "city", "symptoms", "allergies", "chronic_conditions", "dietary_restrictions"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields in input"}), 400

        # Prepare inputs
        inputs = {
            "user_name": data["user_name"],
            "age": data["age"],
            "city": data["city"],
            "date": f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}",
            "symptoms": data["symptoms"],
            "allergies": data["allergies"],
            "chronic_conditions": data["chronic_conditions"],
            "dietary_restrictions": data["dietary_restrictions"]
        }

        AIDoctorAssistant().crew().kickoff(inputs=inputs)

        # Read outputs
        with open("output/first_aid_recommendation.md", "r", encoding="utf-8") as f1, \
             open("output/nearby_hospitals.md", "r", encoding="utf-8") as f2, \
             open("output/dietary_plan.md", "r", encoding="utf-8") as f3:
            result = {
                "first_aid": f1.read(),
                "hospitals": f2.read(),
                "dietary_plan": f3.read()
            }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/browser-agent", methods=["POST"])
def get_browser_agent():
    try:
        task_text = request.json.get("task")
        if not task_text:
            return jsonify({"error": "Missing task"}), 400

        async def main(task_text):
            agent = browser_use.Agent(
                task=task_text,
                llm=ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    api_key=GEMINI_API_KEY,
                ),
            )
            result = await agent.run()
            return result

        result = asyncio.run(main(task_text))
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
