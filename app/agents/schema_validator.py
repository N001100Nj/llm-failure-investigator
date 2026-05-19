"""Schema validation failure detector."""

from __future__ import annotations

import json
from typing import Any

from app.models.graph_state import GraphState
from app.models.report import NodeFinding


def _validate_required_fields(payload: Any, schema: dict[str, Any] | None) -> list[str]:
    if not schema or not isinstance(payload, dict):
        return []
    missing = [field for field in schema.get("required", []) if field not in payload]
    properties = schema.get("properties", {})
    type_errors: list[str] = []
    type_map = {"string": str, "number": (int, float), "integer": int, "boolean": bool, "object": dict, "array": list}
    for name, spec in properties.items():
        if name in payload and isinstance(spec, dict) and "type" in spec:
            expected = type_map.get(spec["type"])
            if expected and not isinstance(payload[name], expected):
                type_errors.append(f"{name} expected {spec['type']}")
    return [*(f"missing required field {field}" for field in missing), *type_errors]


def analyze_schema(state: GraphState) -> GraphState:
    """Check JSON parsing and simple JSON-schema required/type conformance."""

    trace = state["trace"]
    payload = trace.structured_output
    evidence: list[str] = []

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as exc:
            evidence.append(f"invalid JSON: {exc.msg}")

    if not evidence:
        evidence.extend(_validate_required_fields(payload, trace.expected_schema))

    if evidence:
        return {
            "findings": [
                NodeFinding(
                    node_name="schema_validator",
                    failure_type="schema_validation_failure",
                    severity="high",
                    confidence=0.95,
                    evidence=evidence,
                    root_cause_hint="The model returned malformed or schema-incompatible structured output.",
                    recommendation_hint="Constrain generation with JSON mode/function calling and retry with schema-aware validation.",
                )
            ]
        }
    return {}
