import argparse
import logging
import os
import great_expectations as ge
from great_expectations.checkpoint import Checkpoint
from great_expectations.core.batch import RuntimeBatchRequest
from Notion.NotionAPI import NotionAPI

def setup_logging():
    log = logging.getLogger("notion")
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    return log

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db",
        type=str,
        help="Notion's database id",
    )
    parser.add_argument(
        "--data_source",
        type=str,
        help="Data source to use. Default: my_notion_pandas_data_source",
        default="my_notion_pandas_data_source",
    )
    parser.add_argument(
        "--data_connector",
        type=str,
        help="Data connector to use. Default: my_notion_pandas_data_connector",
        default="my_notion_pandas_data_connector",
    )
    parser.add_argument(
        "--expectation_suite",
        type=str,
        help="Expectation suite name to be used. Must be previously configured.",
    )
    parser.add_argument(
        "--run_name",
        type=str,
        help="Run name. This will appear on the Data Docs. Default is 'None'",
        default="None",
    )
    args = parser.parse_args()
    return args

def main():
    log = setup_logging()
    log.info("Starting the script...")

    args = parse_arguments()
    log.info("Parsed arguments: %s", args)

    notion = NotionAPI(os.environ.get("NOTION_API_KEY"))
    notion_df = notion.query_db(args.db, return_type="dataframe")
    context = ge.get_context()
    df = ge.from_pandas(notion_df)

    checkpoint = Checkpoint(
        context=context,
        datasource=args.data_source,
        data_connector_name=args.data_connector,
    )
    batch_request = RuntimeBatchRequest(
        datasource_name=args.data_source,
        data_connector_name=args.data_connector,
        data_asset_name=args.db,
    )
    checkpoint_result = checkpoint.run(batch_request=batch_request)

    log.info("Checkpoint result: %s", checkpoint_result)

if __name__ == "__main__":
    main()

def main():
    log = logging.getLogger("notion")
    logging.basicConfig()
    log.setLevel(logging.DEBUG)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db",
        type=str,
        help="Notion's database id",
    )
    parser.add_argument(
        "--data_source",
        type=str,
        help="Data source to use. Default: my_notion_pandas_data_source",
        default="my_notion_pandas_data_source",
    )
    parser.add_argument(
        "--data_connector",
        type=str,
        help="Data connector to use. Default: my_notion_pandas_data_connector",
        default="my_notion_pandas_data_connector",
    )
    parser.add_argument(
        "--expectation_suite",
        type=str,
        help="Expectation suite name to be used. Must be previously configured.",
    )
    parser.add_argument(
        "--run_name",
        type=str,
        help="Run name. This will appear on the Data Docs. Default is 'None'",
        default="None",
    )
    args = parser.parse_args()
    log.info("Successfully parsed arguments")

    # Loading and testing Notion API key
    log.info("Parsing Notion API key and testing connection")
    notion = NotionAPI(os.environ.get("NOTION_API_KEY"))

    # Query database
    log.info(f"Querying database: {args.db}")
    directory_df = notion.query_db(args.db, return_type="dataframe")
    db_title = notion.get_db_title(args.db)
    df = ge.from_pandas(directory_df)
    log.info("Queried Notion and got database as a pandas dataframe")

    # Great Expectations
    log.info("Reading Great Expectations' context")
    context = ge.get_context()

    checkpoint_name = "notion_checkpoint"
    action_list = [
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
    ]

    batch_request = RuntimeBatchRequest(
        datasource_name=args.data_source,
        data_connector_name=args.data_connector,
        data_asset_name=db_title,
        batch_identifiers={"default_identifier_name": "default_identifier"},
        runtime_parameters={"batch_data": df},
    )

    checkpoint_config = {
        "config_version": 1.0,
        "class_name": "Checkpoint",
        "validations": [
            {
                "batch_request": batch_request,
                "expectation_suite_name": args.expectation_suite,
                "action_list": action_list,
            }
        ],
    }

    checkpoint = Checkpoint(
        name=checkpoint_name, data_context=context, **checkpoint_config
    )

    log.info("Running validation")
    checkpoint.run(run_name=args.run_name)
    log.info("Done running validation. Check data docs to see result.")

if __name__ == "__main__":
    main()