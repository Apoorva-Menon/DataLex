# DataLex
AutoDDG: LLM-Powered Dataset Description Generation
[README.md](https://github.com/user-attachments/files/24067865/README.md)
# Geospatial Profiler for AutoDDG

**Automatic detection and analysis of spatial characteristics in tabular datasets**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

## Overview

This project extends the [AutoDDG framework](https://github.com/VIDA-NYU/AutoDDG) with a comprehensive geospatial profiling module. It automatically detects and analyzes spatial characteristics in tabular datasets, enhancing dataset descriptions with rich spatial context.

**Key Capabilities:**
- **Geometry Type Detection** - Identifies point, polygon, and polyline geometries
- **Spatial Role Classification** - Determines if data represents events, boundaries, infrastructure, or observations
- **Spatial Resolution Analysis** - Detects granularity from coordinates to city-level
- **Multi-Format Support** - Handles lat/lon columns, WKT, GeoJSON, and location tuples
- **Seamless AutoDDG Integration** - Enriches semantic profiles with spatial metadata

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- Git

### Setup

**1. Clone the repository:**

```bash
git clone https://github.com/Apoorva-Menon/DataLex.git
cd DataLex
```

**2. Install AutoDDG framework:**

```bash
pip install git+https://github.com/VIDA-NYU/AutoDDG@main
```

**Note for macOS users:** Add `--break-system-packages` flag if needed:
```bash
pip install --break-system-packages git+https://github.com/VIDA-NYU/AutoDDG@main
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

### Using Conda (Recommended)

```bash
# Clone repository
git clone https://github.com/Apoorva-Menon/DataLex.git
cd DataLex

# Create environment
conda create -n geo_profiler python=3.11
conda activate geo_profiler

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

### Basic Usage

```python
from geo_profiler.geo_profiler import profile_dataset
import pandas as pd

# Load your dataset
df = pd.read_csv('your_dataset.csv')

# Generate complete geospatial profile
profile = profile_dataset(df, dataset_name="NYC WiFi Hotspots")

# Access results
print(f"Geometry Type: {profile.geo_profile.geometry_type}")
print(f"Spatial Role: {profile.geo_profile.spatial_role}")
print(f"Resolution: {profile.geo_profile.spatial_resolution}")
print(f"Use Cases: {profile.geo_profile.spatial_use_cases}")
```

### With AutoDDG Integration

```python
from openai import OpenAI
from autoddg import AutoDDG
from geo_profiler.geo_profiler import profile_dataset

# Initialize AutoDDG
client = OpenAI(api_key="your_api_key")
autoddg = AutoDDG(client=client, model_name="gpt-4o-mini")

# Load data
df = pd.read_csv('nyc_parks.csv')

# Get geospatial profile
geo_profile = profile_dataset(df, "NYC Parks")

# Generate AutoDDG profiles
data_profile, _ = autoddg.profile_dataframe(df)
semantic_profile = autoddg.analyze_semantics(df)

# Enhance with geospatial information
enhanced_semantic = f"""{semantic_profile}

**Geospatial Profile:**
- Geometry Type: {geo_profile.geo_profile.geometry_type}
- Spatial Role: {geo_profile.geo_profile.spatial_role}
- Resolution: {geo_profile.geo_profile.spatial_resolution}
- Use Cases: {', '.join(geo_profile.geo_profile.spatial_use_cases)}
"""

# Generate enhanced description
prompt, description = autoddg.describe_dataset(
    dataset_sample=df.to_csv(index=False),
    dataset_profile=data_profile,
    use_profile=True,
    semantic_profile=enhanced_semantic,
    use_semantic_profile=True
)

print(description)
```

---

## Project Structure

```
DataLex/
├── geo_profiler/
│   ├── __init__.py
│   ├── geo_profiler.py          # Main profiling orchestration
│   ├── geometry_type.py         # Geometry detection (point/polygon/polyline)
│   ├── spatial_role.py          # Role classification (event/boundary/etc)
│   ├── spatial_resolution.py    # Resolution analysis (street/zip/borough)
│   ├── spatial_use_cases.py     # Use case generation
│   ├── semantic_parser.py       # Parse AutoDDG semantic output
│   └── models.py                # Data models and types
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## Components

### 1. Geometry Type Detection

Identifies the geometric representation in datasets:

**Supported Types:**
- **Point** - Individual coordinate locations
  - Lat/lon columns (`latitude`, `longitude`)
  - Coordinate tuples (`(40.7, -73.9)`)
  - WKT: `POINT(-73.9 40.7)`
  - GeoJSON: `{"type": "Point", "coordinates": [...]}`

- **Polygon** - Area boundaries
  - WKT: `POLYGON((...))` or `MULTIPOLYGON(...)`
  - GeoJSON: `{"type": "Polygon", "coordinates": [...]}`
  - Keywords: `shape_area`, `boundary`, `the_geom`

- **Polyline** - Linear paths
  - WKT: `LINESTRING(...)`
  - GeoJSON: `{"type": "LineString", "coordinates": [...]}`
  - Keywords: `route`, `segment`, `road_segment`

**Detection Methods:**
1. Sample value pattern matching (WKT/GeoJSON)
2. Column data type analysis
3. Semantic profiler resolution values
4. Column name keyword matching

### 2. Spatial Role Classification

Categorizes the dataset's spatial purpose:

- **Event** - Time-stamped occurrences at locations
  - Examples: 311 complaints, incident reports, service requests
  - Requires: temporal columns + point locations + event keywords

- **Boundary** - Administrative or geographic regions
  - Examples: Census tracts, districts, zones
  - Indicators: polygon geometry, area-based resolutions

- **Infrastructure** - Fixed facilities and structures
  - Examples: Subway stations, schools, parks, hospitals
  - Indicators: infrastructure keywords + spatial columns

- **Observation** - General spatial measurements
  - Examples: Environmental sensors, survey points
  - Fallback for spatial data not fitting above categories

### 3. Spatial Resolution Analysis

Determines the geographic granularity:

**Resolution Levels (finest to coarsest):**
1. **Coordinates** - Exact lat/lon points
2. **Street** - Street address level
3. **ZIP** - Postal code areas
4. **Neighborhood** - Named local areas
5. **District** - Administrative districts
6. **Borough** - NYC borough level
7. **City** - City-wide
8. **Multi-level** - Multiple granularities present

### 4. Use Case Generation

Automatically suggests applications based on spatial characteristics:

**Generated for:**
- Specific geometry types (mapping, route analysis, coverage)
- Spatial roles (event monitoring, boundary analysis, facility access)
- Resolution levels (micro vs macro analysis)

---

## API Reference

### Main Entry Point

```python
from geo_profiler.geo_profiler import profile_dataset

profile = profile_dataset(
    df: pd.DataFrame,
    dataset_name: str = "Dataset"
) -> EnrichedDatasetProfile
```

**Returns:**
```python
EnrichedDatasetProfile(
    dataset_semantics=DatasetSemanticProfile(...),
    geo_profile=GeoProfile(
        geometry_type='point',
        spatial_role='event',
        spatial_resolution='street-level',
        spatial_use_cases=['Event monitoring', 'Heatmap generation', ...]
    )
)
```

### Individual Components

```python
from geo_profiler.geometry_type import infer_geometry_type
from geo_profiler.spatial_role import infer_spatial_role
from geo_profiler.spatial_resolution import infer_spatial_resolution

# Use individually
geometry = infer_geometry_type(semantic_profile)
role = infer_spatial_role(semantic_profile)
resolution = infer_spatial_resolution(semantic_profile)
```

---

## Data Models

### ColumnSemantic
```python
@dataclass
class ColumnSemantic:
    name: str
    semantic_type: str
    spatial_resolution: Optional[str] = None
    domain_type: Optional[str] = None
    function_role: Optional[str] = None
```

### GeoProfile
```python
@dataclass
class GeoProfile:
    spatial_role: Optional[str] = None
    geometry_type: Optional[str] = None
    spatial_resolution: Optional[str] = None
    spatial_use_cases: List[str] = field(default_factory=list)
```

### EnrichedDatasetProfile
```python
@dataclass
class EnrichedDatasetProfile:
    dataset_semantics: DatasetSemanticProfile
    geo_profile: GeoProfile
    raw_metadata: Optional[Dict] = None
```

---

## Requirements

```
autoddg @ git+https://github.com/VIDA-NYU/AutoDDG@main
pandas>=2.0.0
numpy>=1.24.0
```

All dependencies are automatically installed via `pip install -r requirements.txt`.

---

## Examples

### Example 1: 311 Service Requests (Event Data)

```python
df = pd.read_csv('311_requests.csv')
profile = profile_dataset(df, "NYC 311 Service Requests")

# Output:
# geometry_type: 'point'
# spatial_role: 'event'
# spatial_resolution: 'street-level'
# use_cases: ['Event monitoring', 'Temporal-spatial analysis', 'Heatmap generation']
```

### Example 2: NYC Parks (Boundary Data)

```python
df = pd.read_csv('parks.csv')
profile = profile_dataset(df, "NYC Parks")

# Output:
# geometry_type: 'polygon'
# spatial_role: 'boundary'
# spatial_resolution: 'district-level'
# use_cases: ['Area analysis', 'Coverage mapping', 'Boundary visualization']
```

### Example 3: Bike Routes (Polyline Data)

```python
df = pd.read_csv('bike_routes.csv')
profile = profile_dataset(df, "NYC Bike Routes")

# Output:
# geometry_type: 'polyline'
# spatial_role: 'infrastructure'
# spatial_resolution: 'street-level'
# use_cases: ['Route analysis', 'Network mapping', 'Path optimization']
```

---

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'autoddg'`

**Solution:**
```bash
pip install git+https://github.com/VIDA-NYU/AutoDDG@main
```

---

**Issue:** `ModuleNotFoundError: No module named 'geo_profiler'`

**Solution:** Ensure you're in the project root directory:
```bash
cd DataLex
python3 -c "from geo_profiler.geo_profiler import profile_dataset"
```

---

**Issue:** `This environment is externally managed` (macOS)

**Solutions:**
1. Use flag: `pip install --break-system-packages package_name`
2. Use conda: `conda create -n geo_profiler python=3.11`
3. Use venv: `python3 -m venv venv && source venv/bin/activate`

---

## Testing

Verify installation:

```bash
python3 -c "from geo_profiler.geo_profiler import profile_dataset; print('Installation successful')"
```

---

## Citation

If you use this geospatial profiler in your research, please cite:

```bibtex
@misc{datalex-geo-profiler,
  title={Geospatial Profiler for AutoDDG},
  author={Apoorva, Anuhiya, Pavan},
  year={2024},
  url={https://github.com/Apoorva-Menon/DataLex}
}
```

Also cite the original AutoDDG framework:

```bibtex
@misc{zhang2025autoddg,
  title={AutoDDG: Automated Dataset Description Generation using Large Language Models},
  author={Zhang, Haoxiang and Liu, Yurong and Hung, Wei-Lun and Santos, Aécio and Freire, Juliana},
  year={2025},
  eprint={2502.01050},
  archivePrefix={arXiv},
  primaryClass={cs.DB}
}
```

---

## License

This project extends [AutoDDG](https://github.com/VIDA-NYU/AutoDDG), which is released under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

## Acknowledgments

- VIDA Lab at NYU for the AutoDDG framework
- NYC Open Data for test datasets
