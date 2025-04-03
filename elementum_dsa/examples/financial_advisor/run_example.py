"""Financial Advisor Example Runner

Scripts for running the Financial Advisor agent example.
"""

from elementum_dsa.examples.financial_advisor.financial_advisor_agent import FinancialAdvisorAgent
from elementum_dsa.core.monitoring import MonitoringSystem


def run_financial_advisor_example():
    """Run the Financial Advisor agent example."""
    # Create monitoring system
    monitoring = MonitoringSystem()

    # Create agent instance
    agent = FinancialAdvisorAgent(version=1.0)
    print(f"Created agent: {agent}\n")

    # Process investment recommendation query
    print("Generating investment recommendations...")
    monitoring.start_timing()
    investment_response = agent.process_query("What investment strategies do you recommend for a balanced portfolio?")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {investment_response['response']}\n")

    # Process retirement planning query
    print("Generating retirement planning recommendations...")
    monitoring.start_timing()
    retirement_response = agent.process_query("How should I plan for retirement?")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {retirement_response['response']}\n")

    # Process tax strategy query
    print("Generating tax strategy recommendations...")
    monitoring.start_timing()
    tax_response = agent.process_query("What tax strategies can help minimize my tax burden?")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {tax_response['response']}\n")
    
    # Process estate planning query
    print("Generating estate planning recommendations...")
    monitoring.start_timing()
    estate_response = agent.process_query("What should I include in my estate plan?")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {estate_response['response']}\n")
    
    # Process college planning query
    print("Generating college planning recommendations...")
    monitoring.start_timing()
    college_response = agent.process_query("How should I save for my child's college education?")
    response_time = monitoring.stop_timing()
    print(f"Response time: {response_time:.4f} seconds")
    print(f"Response: {college_response['response']}\n")

    # Get metrics summary
    metrics = monitoring.get_metrics_summary()
    print(f"Performance metrics: {metrics}")


if __name__ == "__main__":
    run_financial_advisor_example()
