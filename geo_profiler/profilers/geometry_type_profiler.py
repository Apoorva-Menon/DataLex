import re
from typing import Literal
from ..models import DatasetSemanticProfile

GeometryType = Literal["point", "polygon", "polyline", "multi", "unknown"]
POINT_KEYWORDS = ["latitude", "longitude", "lat", "lon", "coordinates"]
POLYGON_KEYWORDS = ["polygon", "boundary"]
LINE_KEYWORDS = ["line", "linestring", "route", "segment", "road_segment"]
MULTI_KEYWORDS = ["multipolygon", "multilinestring", "multipoint"]

# Regex patterns for detecting geometry in values (WKT / GeoJSON)
POINT_REGEX = re.compile(r'\bPOINT\b', re.IGNORECASE)
POLYGON_REGEX = re.compile(r'\bPOLYGON\b', re.IGNORECASE)
LINESTRING_REGEX = re.compile(r'\bLINESTRING\b', re.IGNORECASE)
MULTI_REGEX = re.compile(r'\bMULTI(POLYGON|LINESTRING|POINT)\b', re.IGNORECASE)

class GeometryTypeProfiler:

    @staticmethod
    def infer_geometry_type(profile: DatasetSemanticProfile) -> GeometryType:    
        cols = profile.columns    
        col_names = [c.name.lower() for c in cols]    
        
        # 0. Check sample values    
        for c in cols:        
            if c.sample_values:            
                joined = " ".join(c.sample_values)            
                if MULTI_REGEX.search(joined):                
                    return "multi"            
                if POLYGON_REGEX.search(joined):                
                    return "polygon"            
                if LINESTRING_REGEX.search(joined):                
                    return "polyline"            
                if POINT_REGEX.search(joined):                
                    return "point"    
                
        # 1. Check raw_type (Data Profiler output)    
        for c in cols:        
            if c.raw_type:            
                rt = c.raw_type.lower()            
                if "multipolygon" in rt or "multiline" in rt:                
                    return "multi"            
                if "polygon" in rt:                
                    return "polygon"            
                if "line" in rt:                
                    return "polyline"            
                if "geo" in rt or "coordinate" in rt:                
                    # Could still be point or something else.                
                    # But coordinates → usually point.                
                    return "point"    
                
                
        # 2. Check semantic profiler spatial_resolution    
        #    - Coordinates -> point    
        #    - Borough/ZIP/etc -> region -> might be boundary but geometry_type we still treat separately.    
        resolutions = [c.spatial_resolution.lower() for c in cols if c.spatial_resolution]    
        if "coordinates" in resolutions:        
            return "point"    
        
        # 3. Column name heuristics    
        if any(k in name for name in col_names for k in MULTI_KEYWORDS):        
            return "multi"    
        if any(k in name for name in col_names for k in POLYGON_KEYWORDS):        
            return "polygon"    
        if any(k in name for name in col_names for k in LINE_KEYWORDS):        
            return "polyline"    
        if any(k in name for name in col_names for k in POINT_KEYWORDS):        
            return "point"    
        
        # 4. Fallback    
        return "unknown"