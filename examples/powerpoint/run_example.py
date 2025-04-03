"""PowerPoint Example Runner

Scripts for running the PowerPoint agent example.
"""

from examples.powerpoint.powerpoint_agent import PowerPointAgent
from core.monitoring import MonitoringSystem


def run_powerpoint_example():
    """Run the PowerPoint agent example."""
    # Create monitoring system
    monitoring = MonitoringSystem()

    # Create agent instance
    agent = PowerPointAgent(version=1.0)
    print(f"Created agent: {agent}\n")

    # Process structure query
    print("Generating presentation structure...")
    monitoring.start_timing()
    structure_response = agent.process_query("Generate presentation structure for technical overview")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {structure_response['response']}\n")

    # Process design query
    print("Generating design guidelines...")
    monitoring.start_timing()
    design_response = agent.process_query("Provide slide design guidelines for executive presentation")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {design_response['response']}\n")

    # Process guidelines query
    print("Generating delivery guidelines...")
    monitoring.start_timing()
    guidelines_response = agent.process_query("Give me delivery guidelines for a sales pitch")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {guidelines_response['response']}\n")

    # Get metrics summary
    metrics = monitoring.get_metrics_summary()
    print(f"Performance metrics: {metrics}")


if __name__ == "__main__":
    run_powerpoint_example()
