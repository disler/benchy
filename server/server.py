from flask import Flask, request, jsonify
from time import time
import yaml
import concurrent.futures
from modules.data_types import ThoughtResponse
from modules.data_types import (
    ExecEvalBenchmarkReport,
    ModelAlias,
    PromptResponse,
    PromptWithToolCalls,
    ToolCallResponse,
    ExecEvalBenchmarkFile,
    ExecEvalBenchmarkCompleteResult,
)
import modules.llm_models as llm_models
from modules.exbench_module import (
    run_benchmark_for_model,
    generate_report,
    save_report_to_file,
)

app = Flask(__name__)


@app.route("/prompt", methods=["POST"])
def handle_prompt():
    """Handle a prompt request and return the model's response."""
    data = request.get_json()
    prompt = data["prompt"]
    model = data["model"]  # store as string

    start_time = time()
    prompt_response = llm_models.simple_prompt(prompt, model)
    run_time_ms = int((time() - start_time) * 1000)

    # Update the runtime in the response
    prompt_response.runTimeMs = run_time_ms

    return jsonify(
        {
            "response": prompt_response.response,
            "runTimeMs": prompt_response.runTimeMs,
            "inputAndOutputCost": prompt_response.inputAndOutputCost,
        }
    )


@app.route("/tool-prompt", methods=["POST"])
def handle_tool_prompt():
    """Handle a tool prompt request and return the tool calls."""
    data = request.get_json()
    prompt_with_tools = PromptWithToolCalls(prompt=data["prompt"], model=data["model"])

    start_time = time()
    tool_response = llm_models.tool_prompt(prompt_with_tools)
    run_time_ms = int((time() - start_time) * 1000)

    # Update the runtime in the response
    tool_response.runTimeMs = run_time_ms

    print(f"tool_response.tool_calls: {tool_response.tool_calls}")

    return jsonify(
        {
            "tool_calls": [
                {"tool_name": tc.tool_name, "params": tc.params}
                for tc in tool_response.tool_calls
            ],
            "runTimeMs": tool_response.runTimeMs,
            "inputAndOutputCost": tool_response.inputAndOutputCost,
        }
    )


@app.route("/thought-prompt", methods=["POST"])
def handle_thought_bench():
    """Handle a thought bench request and return the model's response."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    prompt = data.get("prompt")
    model = data.get("model")

    if not prompt or not model:
        return jsonify({"error": "Missing 'prompt' or 'model' in request"}), 400

    try:
        response = llm_models.thought_prompt(prompt, model)
        result = {
            "model": model,
            "thoughts": response.thoughts,
            "response": response.response,
            "error": response.error,
        }
    except Exception as e:
        result = {
            "model": model,
            "thoughts": "",
            "response": f"Error: {str(e)}",
            "error": str(e),
        }

    return jsonify(result), 200


@app.route("/iso-speed-bench", methods=["POST"])
def handle_iso_speed_bench():
    """Handle an ISO speed benchmark request with YAML input."""
    # Validate content type
    if not request.content_type == "application/yaml":
        return (
            jsonify({"error": "Invalid content type. Expected application/yaml"}),
            415,
        )

    try:
        # Parse YAML
        try:
            yaml_data = yaml.safe_load(request.data)
            if not yaml_data:
                raise ValueError("Empty YAML file")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {str(e)}")
            return jsonify({"error": f"Invalid YAML format: {str(e)}"}), 400

        # Validate structure
        try:
            benchmark_file = ExecEvalBenchmarkFile(**yaml_data)
        except ValueError as e:
            print(f"Error validating benchmark structure: {str(e)}")
            return jsonify({"error": f"Invalid benchmark structure: {str(e)}"}), 400

        # Validate models
        if not benchmark_file.models:
            print("No models specified in benchmark file")
            return jsonify({"error": "No models specified in benchmark file"}), 400

        # Validate prompts
        if not benchmark_file.prompts:
            print("No prompts specified in benchmark file")
            return jsonify({"error": "No prompts specified in benchmark file"}), 400

        # Run benchmarks
        complete_result = ExecEvalBenchmarkCompleteResult(
            benchmark_file=benchmark_file, results=[]
        )

        for model in benchmark_file.models:
            try:
                print(f"Running benchmark for model {model}")
                results = run_benchmark_for_model(model, benchmark_file)
                complete_result.results.extend(results)
            except Exception as e:
                print(f"Error running benchmark for model {model}: {str(e)}")
                return (
                    jsonify(
                        {
                            "error": f"Error running benchmark for model {model}: {str(e)}"
                        }
                    ),
                    500,
                )

        # Generate report
        try:
            print(f"Generating report for {benchmark_file.benchmark_name}")
            report: ExecEvalBenchmarkReport = generate_report(complete_result)

            # Save report using the new function
            report_path = save_report_to_file(report)
            print(f"Benchmark report saved to: {report_path}")

            return report.model_dump_json(), 200, {"Content-Type": "application/json"}
        except Exception as e:
            return jsonify({"error": f"Error generating report: {str(e)}"}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


def main():
    """Run the Flask application."""
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
