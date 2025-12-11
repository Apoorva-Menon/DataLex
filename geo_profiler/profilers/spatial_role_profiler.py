import re
from typing import Literal
from ..models import DatasetSemanticProfile

SpatialRole = Literal["event", "boundary", "infrastructure", "observation", "unknown"]
EVENT_KEYWORDS = ["complaint", "incident", "request", "service", "violation", "call", "ticket", "case", "report", "inspection"]
BOUNDARY_KEYWORDS = ["district", "tract", "zone", "boundary", "polygon", "shape_area", "shape_len", "borough_boundary", "precinct"]
INFRASTRUCTURE_KEYWORDS = ["station", "stop", "entrance", "facility", "subway","school", "hospital", "bridge", "tunnel", "park", "library"]

class SpatialRoleProfiler:
    """
    Infers the dataset-level spatial role:
    - event
    - observation
    - infrastructure
    - boundary
    """
    
    @staticmethod
    def infer_spatial_role(profile: DatasetSemanticProfile) -> SpatialRole:    
        cols = profile.columns
        
        # Helpers    
        spatial_cols = [c for c in cols if c.is_spatial]   
        temporal_cols = [c for c in cols if c.is_temporal]

        col_names_lower = [c.name.lower() for c in cols]   
        def any_name_matches(keywords):        
            return any(any(k in name for k in keywords) for name in col_names_lower)    
        
        # 1. Boundary: polygon / administrative units    
        has_polygon_semantics = any(
            (c.raw_type and "polygon" in c.raw_type.lower()) or
            (c.spatial_resolution and c.spatial_resolution.lower() in ("region", "area", "polygon")) or
            ("shape_area" in c.name.lower() or "shape_leng" in c.name.lower())
            for c in spatial_cols
        )

        if has_polygon_semantics:
            return "boundary"    
        
        # 2. Event: time + coordinates + event-like columns    
        has_temporal = len(temporal_cols) > 0 
        has_point_like_spatial = any((c.spatial_resolution and c.spatial_resolution.lower() in ("coordinates", "street", "zip", "borough")) for c in spatial_cols)    
        has_event_keywords = any_name_matches(EVENT_KEYWORDS)

        if has_temporal and has_point_like_spatial and has_event_keywords:       
            return "event"    

        # 3. Infrastructure: facilities / fixed infrastructure objects    
        if spatial_cols and any_name_matches(INFRASTRUCTURE_KEYWORDS):        
            return "infrastructure"    
        
        # 4. Observation: spatial but not clearly event/boundary/infrastructure    
        if spatial_cols:
            return "observation"    
        
        # 5. Fallback    
        return "unknown"