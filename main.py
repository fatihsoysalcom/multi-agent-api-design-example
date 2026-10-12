import time

# Base class for all agents, providing basic communication capabilities
class Agent:
    def __init__(self, name):
        self.name = name
        self.messages = [] # Simplified message box for received messages

    def receive_message(self, sender_name, content):
        # Simulate receiving a message and adding it to the agent's inbox
        self.messages.append(f"[{sender_name} -> {self.name}]: {content}")
        print(f"[{self.name} received]: {content}")

    def send_message(self, recipient_agent, content):
        # Simulate sending a message to another agent
        recipient_agent.receive_message(self.name, content)

# Specialized agent responsible for high-level planning and architecture
class ArchitectAgent(Agent):
    def __init__(self):
        super().__init__("Architect")

    def design_plan(self, project_request):
        print(f"\n[{self.name}]: Analyzing request: '{project_request}'...")
        time.sleep(0.5)
        # The architect breaks down the complex request into manageable sub-tasks
        if "API endpoint" in project_request:
            plan = [
                "Define API endpoint path and HTTP method.",
                "Define request body parameters.",
                "Define response body structure."
            ]
            print(f"[{self.name}]: Designed plan: {plan}")
            return plan
        else:
            print(f"[{self.name}]: Cannot design plan for this request.")
            return []

# Specialized agent responsible for implementing specific tasks
class DeveloperAgent(Agent):
    def __init__(self, skills):
        super().__init__("Developer")
        self.skills = skills

    def implement_task(self, task_description):
        print(f"\n[{self.name}]: Working on task: '{task_description}'...")
        time.sleep(1)
        # The developer provides a 'solution' based on the task description
        if "path and method" in task_description:
            solution = "Endpoint: /api/register, Method: POST"
        elif "request body parameters" in task_description:
            solution = "Request Body: { 'username': 'string', 'password': 'string', 'email': 'string' }"
        elif "response body structure" in task_description:
            solution = "Response Body: { 'success': 'boolean', 'message': 'string' }"
        else:
            solution = f"// Unable to implement: {task_description}"
        print(f"[{self.name}]: Implemented: {solution}")
        return solution

# Specialized agent responsible for verifying implementations
class TesterAgent(Agent):
    def __init__(self):
        super().__init__("Tester")

    def test_solution(self, solution, task_description):
        print(f"\n[{self.name}]: Testing solution for '{task_description}': '{solution}'...")
        time.sleep(0.7)
        feedback = ""
        passed = True

        # The tester checks the solution against the task requirements
        if "path and method" in task_description:
            if not ("Endpoint:" in solution and "Method:" in solution):
                feedback = "Missing 'Endpoint' or 'Method' in solution."
                passed = False
        elif "request body parameters" in task_description:
            if not ("Request Body:" in solution and "username" in solution and "password" in solution):
                feedback = "Missing 'Request Body' or essential parameters."
                passed = False
        elif "response body structure" in task_description:
            if not ("Response Body:" in solution and "success" in solution and "message" in solution):
                feedback = "Missing 'Response Body' or essential fields."
                passed = False

        if passed:
            print(f"[{self.name}]: Test PASSED for '{task_description}'.")
            return True, "Looks good!"
        else:
            print(f"[{self.name}]: Test FAILED for '{task_description}'. Feedback: {feedback}")
            return False, feedback

# Orchestrator agent that manages the workflow and communication between other agents
class ProjectManagerAgent(Agent):
    def __init__(self, architect, developer, tester):
        super().__init__("ProjectManager")
        self.architect = architect
        self.developer = developer
        self.tester = tester
        self.project_status = {}

    def start_project(self, project_request):
        print(f"\n--- {self.name}: Starting new project: '{project_request}' ---")
        # Project Manager sends the initial request to the Architect
        self.send_message(self.architect, f"Please design a plan for: '{project_request}'")
        plan = self.architect.design_plan(project_request) # Architect directly returns plan for simplicity

        if not plan:
            print(f"[{self.name}]: Project failed: Architect could not create a plan.")
            return

        self.project_status['plan'] = plan
        self.project_status['tasks'] = []

        for i, task in enumerate(plan):
            print(f"\n--- {self.name}: Assigning Task {i+1}: '{task}' ---")
            # Project Manager assigns task to Developer
            self.send_message(self.developer, f"Implement the following task: '{task}'")
            solution = self.developer.implement_task(task) # Developer directly returns solution

            # Project Manager assigns solution to Tester for verification
            self.send_message(self.tester, f"Test the solution '{solution}' for task: '{task}'")
            passed, feedback = self.tester.test_solution(solution, task) # Tester directly returns result

            self.project_status['tasks'].append({
                'task': task,
                'solution': solution,
                'test_result': 'PASSED' if passed else 'FAILED',
                'feedback': feedback
            })

            if not passed:
                print(f"[{self.name}]: Task '{task}' FAILED testing. Feedback: {feedback}. In a real system, this would trigger a retry or escalation.")
            else:
                print(f"[{self.name}]: Task '{task}' completed successfully.")

        print(f"\n--- {self.name}: Project '{project_request}' Finished ---")
        print("\nProject Summary:")
        for task_info in self.project_status['tasks']:
            print(f"  - Task: {task_info['task']}")
            print(f"    Solution: {task_info['solution']}")
            print(f"    Status: {task_info['test_result']} ({task_info['feedback']})")
        print("\nAll agents collaborated to complete the project!")

# Main execution block
if __name__ == "__main__":
    # 1. Initialize specialized agents, each with a distinct role
    architect = ArchitectAgent()
    developer = DeveloperAgent(skills=["Python", "API Design"])
    tester = TesterAgent()

    # 2. Initialize the orchestrator (Project Manager) with references to the specialized agents
    project_manager = ProjectManagerAgent(architect, developer, tester)

    # 3. Start a project with a high-level request, demonstrating multi-agent collaboration
    project_manager.start_project("Design an API endpoint for user registration.")

    print("\n=======================================================")
    print("--- Demonstrating another project (simple failure case) ---")
    # This request will fail early as the Architect is not specialized for it,
    # showing how agents operate within their defined capabilities.
    project_manager.start_project("Write a poem about a cat.")
