"""Command-line interface for the Elementum DSA framework."""

import argparse
import json
import logging
from typing import Dict, Any, List

from core.mca import MasterControlAgent
from examples.powerpoint.powerpoint_agent import PowerPointAgent
from examples.data_analysis.data_analysis_agent import DataAnalysisAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("elementum_dsa")


def create_mca() -> MasterControlAgent:
    """Create and initialize the Master Control Agent.

    Returns:
        Initialized Master Control Agent
    """
    logger.info("Creating Master Control Agent")
    mca = MasterControlAgent()

    # Register example agents
    logger.info("Registering example agents")
    mca.register_agent(PowerPointAgent())
    mca.register_agent(DataAnalysisAgent())

    return mca


def process_query(mca: MasterControlAgent, query: str, agent_id: str = None, domain: str = None) -> Dict[str, Any]:
    """Process a query using the Master Control Agent.

    Args:
        mca: Master Control Agent
        query: The query to process
        agent_id: Optional agent ID to use
        domain: Optional domain to filter by

    Returns:
        Response from the agent
    """
    logger.info(f"Processing query: {query}")
    logger.info(f"Agent ID: {agent_id if agent_id else 'Not specified'}")
    logger.info(f"Domain: {domain if domain else 'Not specified'}")

    # Process the query
    response = mca.process_query(query, agent_id, domain)

    # Log the response status
    if "status" in response:
        logger.info(f"Response status: {response['status']}")
    else:
        logger.info("Response status not available")

    return response


def process_collaboration(mca: MasterControlAgent, query: str, primary_agent_id: str, support_agent_ids: List[str]) -> Dict[str, Any]:
    """Process a collaborative query using the Master Control Agent.

    Args:
        mca: Master Control Agent
        query: The query to process
        primary_agent_id: Primary agent ID
        support_agent_ids: Support agent IDs

    Returns:
        Response from the collaboration
    """
    logger.info(f"Processing collaborative query: {query}")
    logger.info(f"Primary agent ID: {primary_agent_id}")
    logger.info(f"Support agent IDs: {support_agent_ids}")

    # Process the collaborative query
    response = mca.collaborate(query, primary_agent_id, support_agent_ids)

    # Log the response status
    if "status" in response:
        logger.info(f"Response status: {response['status']}")
    else:
        logger.info("Response status not available")

    return response


def load_query_file(file_path: str) -> List[Dict[str, Any]]:
    """Load queries from a JSON file.

    Args:
        file_path: Path to the query file

    Returns:
        List of query objects
    """
    logger.info(f"Loading queries from file: {file_path}")
    with open(file_path, "r") as f:
        queries = json.load(f)
    logger.info(f"Loaded {len(queries)} queries")
    return queries


def process_query_file(mca: MasterControlAgent, file_path: str) -> List[Dict[str, Any]]:
    """Process queries from a file.

    Args:
        mca: Master Control Agent
        file_path: Path to the query file

    Returns:
        List of responses
    """
    # Load queries from file
    queries = load_query_file(file_path)

    # Process each query
    responses = []
    for i, query_obj in enumerate(queries):
        logger.info(f"Processing query {i + 1} of {len(queries)}")

        # Extract query parameters
        query = query_obj["query"]
        agent_id = query_obj.get("agent_id")
        domain = query_obj.get("domain")

        # Check if this is a collaborative query
        if "primary_agent_id" in query_obj and "support_agent_ids" in query_obj:
            primary_agent_id = query_obj["primary_agent_id"]
            support_agent_ids = query_obj["support_agent_ids"]
            response = process_collaboration(mca, query, primary_agent_id, support_agent_ids)
        else:
            response = process_query(mca, query, agent_id, domain)

        responses.append(response)

    return responses


def save_responses(responses: List[Dict[str, Any]], output_file: str):
    """Save responses to a JSON file.

    Args:
        responses: List of responses
        output_file: Path to the output file
    """
    logger.info(f"Saving responses to file: {output_file}")
    with open(output_file, "w") as f:
        json.dump(responses, f, indent=2)
    logger.info(f"Saved {len(responses)} responses")


def main():
    """Main CLI entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Elementum DSA Application")
    parser.add_argument("--query", type=str, help="Query to process")
    parser.add_argument("--agent-id", type=str, help="Agent ID to use")
    parser.add_argument("--domain", type=str, help="Domain to filter by")
    parser.add_argument("--query-file", type=str, help="Path to query file")
    parser.add_argument("--output-file", type=str, help="Path to output file")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))

    # Create and initialize the Master Control Agent
    mca = create_mca()

    # Process query file if specified
    if args.query_file:
        responses = process_query_file(mca, args.query_file)
        if args.output_file:
            save_responses(responses, args.output_file)
        else:
            print(json.dumps(responses, indent=2))
    # Process single query if specified
    elif args.query:
        response = process_query(mca, args.query, args.agent_id, args.domain)
        print(json.dumps(response, indent=2))
    # Display usage information if no query specified
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
