from fastapi import APIRouter
import toml
from agentic_security.config import get_or_create_config

router = APIRouter()

def load_llm_configs():
    with open("configs/llm_specs.toml", "r") as f:
        return toml.load(f)


@router.get("/v1/data-config")
def get_data_config():
    data = load_llm_configs()

    return [
        {
            "name": c["name"],
            "spec": c["spec"]
        }
        for c in data["configs"]
    ]

@router.get("/config")
def get_config():
    cfg = get_or_create_config()

    return {
        "enableChartDiagram": cfg.get_config_value("general.enableChartDiagram", False),
        "enableLogging": cfg.get_config_value("general.enableLogging", False),
        "enableConcurrency": cfg.get_config_value("general.enableConcurrency", False),
    }