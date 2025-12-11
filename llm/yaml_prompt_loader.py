from pathlib import Path
import yaml

class YamlPromptLoader:
    def __init__(self, yaml_path: str):
        base_dir = Path(__file__).resolve().parent  # llm/
        full_path = base_dir / yaml_path             # llm/prompts.yaml

        if not full_path.exists():
            raise FileNotFoundError(f"Prompt file not found at: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            self.prompts = yaml.safe_load(f)

    def get(self, key: str):
        return self.prompts.get(key)