import re
from .models import ColumnSemantic, DatasetSemanticProfile
import pandas as pd

class SemanticParser:

    @staticmethod
    def parse_semantic_profile_text(text: str, df: pd.DataFrame) -> DatasetSemanticProfile:
        columns = []

        # Split per column block using '**ColumnName**:'
        blocks = re.split(r"\*\*(.*?)\*\*:", text)[1:]

        for i in range(0, len(blocks), 2):
            name = blocks[i].strip()
            content = blocks[i + 1]

            # Defaults
            is_spatial = False
            spatial_resolution = None
            domain_type = None
            function = None
            is_temporal = False
            raw_type = None

            #Spatial detection
            if "Contains spatial data" in content:
                is_spatial = True

                #Extract spatial resolution
                res_match = re.search(r"resolution:\s*([^)]+)", content)
                if res_match:
                    spatial_resolution = res_match.group(1).strip()

            #Temporal detection
            if "Contains temporal data" in content:
                is_temporal = True

            #Domain type
            dom_match = re.search(r"Domain-specific type:\s*([^.]+)", content)
            if dom_match:
                domain_type = dom_match.group(1).strip()

            func_match = re.search(r"Function/Usage context:\s*([^.]+)", content)
            if func_match:
                function = func_match.group(1).strip()

            raw_match = re.search(r"Represents\s+([^.]+)", content)
            if raw_match:
                raw_type = raw_match.group(1).strip()

            columns.append(
                ColumnSemantic(
                    name=name,
                    is_spatial=is_spatial,
                    spatial_resolution=spatial_resolution,
                    is_temporal=is_temporal,
                    domain_type=domain_type,
                    function=function,
                    raw_type=raw_type,
                    sample_values=df[name].dropna().astype(str).head(3).tolist())
            )

        return DatasetSemanticProfile(columns=columns)