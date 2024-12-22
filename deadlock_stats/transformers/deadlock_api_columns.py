from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame
import ast
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# requires df_columns global variable
@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:

    df_columns = ast.literal_eval(kwargs['df_columns'])
    if not df_columns:
        raise ValueError("The 'df_columns' argument must be provided and cannot be empty.")

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
            print(f"Column '{col}' contains unhashable types.")
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)
    """
    Execute Transformer Action: ActionType.SELECT

    Docs: https://docs.mage.ai/guides/transformer-blocks#select-columns
    """
    print(df_columns)
    action = build_transformer_action(
        df,
        action_type=ActionType.SELECT,
        arguments=df_columns,  # Specify columns to select
        axis=Axis.COLUMN,
    )

    return BaseAction(action).execute(df)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
