#Due to Jupyter issue, isolate rendering function from sdk
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import json
from vertexai._genai import types
import vertexai._genai._evals_visualization as sdk
from typing import Optional
from pydantic import errors
import base64
def display_evaluation_dataset(eval_dataset_obj: types.EvaluationDataset) -> None:
    """Displays an evaluation dataset in an IPython environment."""
    from IPython import display

    processed_rows = []
    df = eval_dataset_obj.eval_dataset_df

    for _, row in df.iterrows():
        processed_row = {}
        for col_name, cell_value in row.items():
            if col_name in ["prompt", "request", "response"]:
                processed_row[col_name] = sdk._extract_text_and_raw_json(cell_value)
            elif col_name == "rubric_groups":
                # Special handling for rubric_groups to keep it as a dict
                if isinstance(cell_value, dict):
                    processed_row[col_name] = {
                        k: [
                            (
                                v_item.model_dump(mode="json")
                                if hasattr(v_item, "model_dump")
                                else v_item
                            )
                            for v_item in v
                        ]
                        for k, v in cell_value.items()
                    }
                else:
                    processed_row[col_name] = cell_value
            else:
                if isinstance(cell_value, (dict, list)):
                    processed_row[col_name] = json.dumps(
                        cell_value, ensure_ascii=False, default=sdk._pydantic_serializer
                    )
                else:
                    processed_row[col_name] = cell_value
        processed_rows.append(processed_row)

    dataframe_json_string = json.dumps(processed_rows, ensure_ascii=False, default=str)
    html_content = sdk._get_inference_html(dataframe_json_string)
    b64_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    data_uri = f"data:text/html;charset=utf-8;base64,{b64_html}"
    display.display(display.IFrame(data_uri, width="100%", height="800px"))

def display_evaluation_result(eval_result_obj: types.EvaluationResult, candidate_names: Optional[list[str]] = None) -> None:
    """Displays evaluation result in an IPython environment."""
    from IPython import display

    try:
        result_dump = eval_result_obj.model_dump(
            mode="json", exclude_none=True, exclude={"evaluation_dataset"}
        )
    except errors.PydanticSerializationError as e:
        print(
            "Serialization Error: %s\nCould not display the evaluation "
            "result due to a data serialization issue. Please check the "
            "content of the EvaluationResult object.",
            e,
        )
        return
    except Exception as e:
        print("Failed to serialize EvaluationResult: %s", e, exc_info=True)
        raise

    input_dataset_list = eval_result_obj.evaluation_dataset
    is_comparison = input_dataset_list and len(input_dataset_list) > 1

    metadata_payload = result_dump.get("metadata", {})
    metadata_payload["candidate_names"] = candidate_names or metadata_payload.get(
        "candidate_names"
    )

    if is_comparison and input_dataset_list:
        if input_dataset_list[0]:
            metadata_payload["dataset"] = sdk._extract_dataset_rows(input_dataset_list[0])

        if "eval_case_results" in result_dump:
            for case_res in result_dump["eval_case_results"]:
                for resp_idx, cand_res in enumerate(
                    case_res.get("response_candidate_results", [])
                ):
                    if (
                        input_dataset_list is not None
                        and resp_idx < len(input_dataset_list)
                        and input_dataset_list[resp_idx]
                    ):
                        rows = sdk._extract_dataset_rows(input_dataset_list[resp_idx])
                        case_idx = case_res.get("eval_case_index")
                        if case_idx is not None and case_idx < len(rows):
                            original_case = rows[case_idx]
                            cand_res["display_text"] = original_case[
                                "response_display_text"
                            ]
                            cand_res["raw_json"] = original_case["response_raw_json"]

        win_rates = eval_result_obj.win_rates if eval_result_obj.win_rates else {}
        if "summary_metrics" in result_dump:
            for summary in result_dump["summary_metrics"]:
                if summary.get("metric_name") in win_rates:
                    summary.update(win_rates[summary["metric_name"]])

        result_dump["metadata"] = metadata_payload
        html_content = sdk._get_comparison_html(json.dumps(result_dump))
    else:
        single_dataset = input_dataset_list[0] if input_dataset_list else None
        processed_rows = []
        if single_dataset is not None:
            processed_rows = sdk._extract_dataset_rows(single_dataset)
            metadata_payload["dataset"] = processed_rows

            if "eval_case_results" in result_dump and processed_rows:
                for case_res in result_dump["eval_case_results"]:
                    case_idx = case_res.get("eval_case_index")
                    if (
                        case_idx is not None
                        and case_idx < len(processed_rows)
                        and case_res.get("response_candidate_results")
                    ):
                        original_case = processed_rows[case_idx]
                        cand_res = case_res["response_candidate_results"][0]
                        cand_res["display_text"] = original_case[
                            "response_display_text"
                        ]
                        cand_res["raw_json"] = original_case["response_raw_json"]

        result_dump["metadata"] = metadata_payload
        html_content = sdk._get_evaluation_html(json.dumps(result_dump))

    b64_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    data_uri = f"data:text/html;charset=utf-8;base64,{b64_html}"
    display.display(display.IFrame(data_uri, width="100%", height="800px"))

import base64
from google.cloud import storage
from IPython.display import HTML

storage_client = storage.Client()

def path_to_image_html(path):
    try:
        if isinstance(path, dict):
            uri = path['parts'][0]['file_data']['file_uri']
        else:
            uri = str(path)

        if uri.startswith("gs://"):
            path_parts = uri.replace("gs://", "").split("/", 1)
            bucket_name = path_parts[0]
            blob_name = path_parts[1]

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            if not blob.exists():
                return f"Not Found: {blob_name}"

            content = blob.download_as_bytes()
            encoded = base64.b64encode(content).decode('utf-8')

            mime_type = "image/png"
            if blob_name.lower().endswith(".jpg") or blob_name.lower().endswith(".jpeg"):
                mime_type = "image/jpeg"

            return f'<img src="data:{mime_type};base64,{encoded}" width="200">'

    except Exception as e:
        return f"Error: {str(e)[:50]}"

    return "No Image"