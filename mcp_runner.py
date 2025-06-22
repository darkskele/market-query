"""
mcp_runner.py — Minimal MCP-style YAML flow runner for NANDA agents.

This script loads a YAML flow file (e.g. `flows/mvp.yaml`),
dynamically imports agent functions, resolves templated arguments,
executes each step in sequence, and stores intermediate outputs.

Supports dot-access via DotDict for templated expressions like:
    ${{ inputs.idea_text }}
    ${{ steps.parse.output }}
"""

import importlib
import yaml

class DotDict(dict):
    """
    A dictionary that supports attribute-style access (dot notation).

    Example:
        d = DotDict({"foo": {"bar": 1}})
        d.foo.bar == 1
    """
    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
            self[key] = value  # cache it
        return value


def import_func(path: str):
    """
    Dynamically import a function from a dotted path.
    
    Example: "agents.idea_parser.idea_parser.parse_idea"
    """
    module_path, func_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def run_flow(yaml_path: str, inputs: dict):
    """
    Run a flow defined in a YAML file with the given inputs.

    Args:
        yaml_path (str): Path to the YAML flow definition.
        inputs (dict): Initial input variables.

    Returns:
        dict: Final context including all intermediate step outputs.
    """
    with open(yaml_path, "r") as f:
        flow = yaml.safe_load(f)

    # Context object passed to eval_template (inputs + step outputs)
    ctx = {
        "inputs": DotDict(inputs),
        "steps": DotDict(),
    }

    # Execute each step in order
    for step in flow["steps"]:
        step_id = step["id"]
        func = import_func(step["uses"])

        # Resolve templated arguments like "${{ steps.X.output }}"
        args = {
            k: eval_template(v, ctx)
            for k, v in step.get("args", {}).items()
        }

        output = func(**args)
        ctx["steps"][step_id] = {"output": output}

    return ctx["steps"]


def eval_template(val, ctx):
    """
    Resolve templated expressions using `eval` in the given context.

    Example:
        If val = "${{ inputs.idea_text }}", this evaluates
        ctx["inputs"].idea_text and returns the value.
    """
    if isinstance(val, str) and val.startswith("${{") and val.endswith("}}"):
        return eval(val[3:-2], {}, ctx)
    return val
