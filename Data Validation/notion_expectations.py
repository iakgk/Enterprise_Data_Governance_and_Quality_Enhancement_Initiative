import os
import great_expectations as ge
from Notion.NotionAPI import NotionAPI

def main():
    # Set your environment variables
    NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
    dbid = "https://www.notion.so/29965940ff704020b78b7ec20dc063c6?v=f7f9dce03b6447278ebb7b2453143c43"
    expectation_suite_name = "example_3_columns_and_2_languages"

    # Initialize NotionAPI and query the database
    notion = NotionAPI(NOTION_API_KEY)
    notion_df = notion.query_db(dbid, return_type="dataframe")

    # Initialize Great Expectations context and convert DataFrame
    context = ge.get_context()
    df = ge.from_pandas(notion_df)

    # Display the first 5 rows
    df.head(5)

    # Column expectations
    df.expect_column_values_to_not_be_null('Name')
    df.expect_column_values_to_not_be_null('Phone')
    df.expect_column_values_to_not_be_null('Languages')

    df.expect_column_values_to_match_regex('Languages', 
                                           r'(?:.+\,){1,}.+',
                                           meta={"notes": "At least 2 or more entries. Using Regex"})

    # Save the expectation suite
    context.save_expectation_suite(discard_failed_expectations=False,
                                   expectation_suite=df._expectation_suite,
                                   expectation_suite_name=expectation_suite_name)

if __name__ == "__main__":
    main()
