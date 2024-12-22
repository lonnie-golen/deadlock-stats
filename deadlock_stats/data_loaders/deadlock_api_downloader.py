import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# requires api_url global variable
@data_loader
def load_data_from_api(*args, **kwargs) -> pd.DataFrame:
    if not kwargs['api_url']:
        raise ValueError("URL must be provided to fetch data.")
    else:
        url = kwargs['api_url']

    response = requests.get(url)

    # Raise an error for unsuccessful responses
    response.raise_for_status()

    # Assume JSON response can be directly converted to a DataFrame
    return pd.read_json(response.text)


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