import io
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta
import pytz

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

# requires api_url global variable
@data_loader
def load_data_from_api(*args, **kwargs) -> pd.DataFrame:
    timezone = pytz.timezone('America/New_York')  # Replace with your desired timezone
    # Get the current time in the specified timezone
    _date = datetime.now(timezone)
    # Create a datetime object for midnight today
    _date = _date.replace(hour=0, minute=0, second=0, microsecond=0)
    # DataFrame to store all API results
    all_api_data = []

    # Make 7 API calls with decreasing timestamps
    for i in range(7):
        # Calculate the UNIX timestamp for each day
        min_timestamp = int(_date.timestamp())
        max_timestamp = min_timestamp + 86400 - 1  # 86400 seconds in a day
        
        # Update the API URL with the calculated timestamps
        url = (f'https://analytics.deadlock-api.com/v2/hero-win-loss-stats?min_unix_timestamp={min_timestamp}&max_unix_timestamp={max_timestamp}')

        # Make the API call
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the API response and add extra columns
            df = pd.read_json(response.text)
            df['min_timestamp'] = min_timestamp
            df['max_timestamp'] = max_timestamp

            #print(df)
            # Add to the main list
            all_api_data.append(df)
        else:
            print(f"Failed to fetch data for Timestamp Range {min_timestamp}-{max_timestamp}: {response.status_code}")
            
        # Move to the previous day
        _date -= timedelta(days=1)

    final_df = pd.concat(all_api_data, ignore_index=True)
    return final_df


@test
def test_output(output, *args, **kwargs) -> None:
    """
    Template code for testing the output of the block.
    
    Args:
        output: The output DataFrame to test.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'The output is not a DataFrame'
    assert not output.empty, 'The output DataFrame is empty'