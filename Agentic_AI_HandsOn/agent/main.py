import asyncio
from react_agent import ReActAgent


async def main():
    try:
        agent = ReActAgent()

        # Example query that requires both search and calculation
        # query = "What is the population density of Canada given its current population and total area?"
        query = input("Enter your Query : ")
        response = await agent.run(query)

        print("Thought Process:")
        for step in response.thought_process:
            print(f"\nThought: {step.thought}")
            if step.action:
                print(f"Action: {step.action.model_dump_json()}")
            if step.observation:
                print(f"Observation: {step.observation.result}")

        print(f"\nFinal Answer: {response.final_answer}")

    except Exception as e:
        print(f"Error running agent: {e}")


if __name__ == "__main__":
    asyncio.run(main())