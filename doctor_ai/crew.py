from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class AIDoctorAssistant:
    """AI Doctor Assistant crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def first_aid_prescriber_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["first_aid_prescriber_agent"],
            verbose=True,
        )

    @agent
    def hospital_locator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["hospital_locator_agent"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def dietary_plan_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["dietary_plan_agent"],
            verbose=True,
        )
    


    @task
    def first_aid_prescriber_task(self) -> Task:
        return Task(
            config=self.tasks_config["first_aid_prescriber_task"],
            output_file="output/first_aid_recommendation.md",
        )

    @task
    def hospital_locator_task(self) -> Task:
        return Task(
            config=self.tasks_config["hospital_locator_task"],
            output_file="output/nearby_hospitals.md",
        )

    @task
    def dietary_plan_creator_task(self) -> Task:
        return Task(
            config=self.tasks_config["dietary_plan_task"],
            output_file="output/dietary_plan.md",
        )
    


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

