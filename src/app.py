import re
import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from colorama import Fore, Style

import delta_sharing

# Load environment variables from .env file
load_dotenv()

# Get the configuration path for Delta Sharing connection
CONFIG_PATH = os.getenv('CONFIG_PATH')

# Initialize the Delta Sharing client with the configuration
CLIENT = delta_sharing.SharingClient(CONFIG_PATH)

# Get the first shared dataset (assuming there's at least one available)
# Note: It may happen that the list is greater than 1, but we use the first one
SHARED_NAME = CLIENT.list_shares()[0]


def get_matching_tables(table_pattern):
    """
    Find all tables that match the given regex pattern.
    
    Args:
        table_pattern (str): Regex pattern to match table names
        
    Returns:
        list: List of matching table objects, or None if no matches found
    """
    # Get all available tables from the Delta Sharing client
    all_tables = CLIENT.list_all_tables()

    # Filter tables based on the regex pattern
    matching_tables = [
        table
        for table in all_tables
        if re.search(table_pattern, table.name)
    ]

    # Print results and return matching tables
    if matching_tables:
        print(
            Fore.CYAN
            + f"\nFound {len(matching_tables)} matching tables:"
            + Style.RESET_ALL
        )
        for table in matching_tables:
            print(f"- {table.schema}.{table.name}")
        return matching_tables


async def process_table(table):
    """
    Asynchronously process a single table by loading it from Delta Sharing
    and saving it as a CSV file.
    
    Args:
        table: Delta Sharing table object containing schema and name
    """
    # Construct the table URL for Delta Sharing
    table_url = f"{CONFIG_PATH}#{SHARED_NAME.name}.{table.schema}.{table.name}"
    
    try:
        # Load table data asynchronously using delta sharing
        df_table = await asyncio.to_thread(
             delta_sharing.load_as_pandas,
             table_url
        )

        # Check if the table is empty
        if df_table.empty:
            print(Fore.YELLOW + f"- {table.schema}.{table.name} is empty." + Style.RESET_ALL)
            return pd.DataFrame()
        else:
            # Save non-empty table to CSV
            df_table_to_csv(table.schema, table.name, df_table)
            print(f"- {table.schema}.{table.name} saved as csv")

    except Exception as e:
        # Handle any errors during table processing
        print(Fore.RED + f"Error loading table {table.name}: {e}" + Style.RESET_ALL)


def df_table_to_csv(schema, name, df_table):
    """
    Save a DataFrame to CSV file in the processed data directory.
    
    Args:
        schema (str): Database schema name
        name (str): Table name
        df_table (pd.DataFrame): DataFrame to save
    """
    df_table.to_csv(
        f"data/processed/{schema}.{name}.csv",
        index=False
    )


async def main():
    """
    Main function that orchestrates the table extraction process.
    
    Finds tables matching a specific pattern, processes them asynchronously,
    and saves them as CSV files in the processed data directory.
    """
    # Define a pattern to match tables of interest
    # This regex matches table names starting with 'companies' or 'projects'
    table_pattern = '^companies|^projects'
    
    # Find all tables that match our pattern
    matching_tables = get_matching_tables(table_pattern)

    # Exit early if no matching tables found
    if not matching_tables:
        print(Fore.RED + f"No tables found for pattern: {table_pattern}" + Style.RESET_ALL)
        return

    print(Fore.CYAN + "\nProcessing tables..." + Style.RESET_ALL)

    # Process all matching tables concurrently using asyncio.gather
    # This allows multiple tables to be downloaded and processed simultaneously
    await asyncio.gather(
        *(process_table(table) for table in matching_tables)
    )

if __name__ == "__main__":
    asyncio.run(main())