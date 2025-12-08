from dataclasses import dataclass, field
from typing import List, Optional, Dict

# Column-Level Semantics
@dataclass
class ColumnSemantic:
    name: str
    semantic_type: str                          # e.g., "location", "coordinate", "polygon"
    spatial_resolution: Optional[str] = None    # e.g., "Street", "ZIP", "Coordinates"
    domain_type: Optional[str] = None           # e.g., "geography", "gis"
    function_role: Optional[str] = None         # e.g., "measurement", "identifier"

# Dataset-Level Semantics
@dataclass
class DatasetSemanticProfile:
    dataset_name: str
    columns: List[ColumnSemantic] = field(default_factory=list)

    has_spatial: bool = False
    has_temporal: bool = False

    detected_spatial_columns: List[str] = field(default_factory=list)

# Geo-Level Enriched Profile
@dataclass
class GeoProfile:
    spatial_role: Optional[str] = None        # event | observation | infrastructure | boundary
    geometry_type: Optional[str] = None       # point | polygon | polyline
    spatial_resolution: Optional[str] = None  # street | zip | borough | multi-level
    spatial_use_cases: List[str] = field(default_factory=list)

# Full Enriched Dataset Object
@dataclass
class EnrichedDatasetProfile:
    dataset_semantics: DatasetSemanticProfile
    geo_profile: GeoProfile

    raw_metadata: Optional[Dict] = None
