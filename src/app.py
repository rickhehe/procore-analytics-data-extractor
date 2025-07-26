import re
import os
import pandas as pd
from dotenv import load_dotenv
from colorama import Back, Fore, Style

import delta_sharing  # Still need this for delta_sharing functions


#from df_to_sql_server import df_to_sql_server

# Load environment variables from .env file
load_dotenv()
CONFIG_PATH = os.getenv('CONFIG_PATH')
CLIENT = delta_sharing.SharingClient(CONFIG_PATH)

# It may happen that the list is greater than 1.
SHARED_NAME = CLIENT.list_shares()[0]


def get_tables(table_pattern):
    """
    Get tables from the Delta Sharing client that match a specific pattern.
    
    Args:
        client (delta_sharing.SharingClient): The Delta Sharing client.
        table_pattern (str): The regex pattern to match table names.
    Returns:
        list: A list of tables that match the pattern.
    """
    tables = CLIENT.list_all_tables()

    tables = [
        table
        for table in tables
        if re.search(table_pattern, table.name)
    ]

    if tables:
        print(
            Fore.CYAN
            + f"\nFound {len(tables)} tables:"
            + Style.RESET_ALL
        )
        for table in tables:
            print(f"- {table.schema}.{table.name}")
        return tables

def get_df_table(table):

    table_url = f"{CONFIG_PATH}#{SHARED_NAME.name}.{table.schema}.{table.name}"
    # print(table_url)
    # print(f"reading {table.schema}.{table.name}...")
    try:
        df = delta_sharing.load_as_pandas(table_url)

        if df.empty:
            print(Fore.YELLOW + f"- {table.schema}.{table.name} is empty." + Style.RESET_ALL)
            return pd.DataFrame()

        else:
            print(f"- {table.schema}.{table.name}")
            return df

    except Exception as e:
        
        print(Fore.RED + f"Error loading table {table.name}: {e}" + Style.RESET_ALL)


def df_table_to_csv(schema, name, df_table):

    df_table.to_csv(
        f"data/processed/{schema}.{name}.csv",
        index=False
    )


def main():
    # Define a pattern to match tables of interest
    # Learn some regex..
    table_pattern = '^companies|^projects'
    tables = get_tables(table_pattern)

    if not tables:
        print(Fore.RED + f"No tables found for this pattern: {table_pattern}" + Style.RESET_ALL)
        return

    print(Fore.CYAN + "\nProcessing tables..." + Style.RESET_ALL)
    for table in tables:
        df_table = get_df_table(table)
        # output the table to CSV if it is not empty
        # @todo: add a function to output to SQL Server
        if not df_table.empty:
            df_table_to_csv(table.schema, table.name, df_table)


if __name__ == "__main__":
    main()