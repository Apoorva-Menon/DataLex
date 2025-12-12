# DataLex

**Automatic detection and analysis of spatial characteristics in tabular datasets**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

## Overview

This project extends the [AutoDDG framework](https://github.com/VIDA-NYU/AutoDDG) with a comprehensive geospatial profiling module. It automatically detects and analyzes spatial characteristics in tabular datasets, enhancing dataset descriptions with rich spatial context.

AutoDDG: LLM-Powered Dataset Description Generation
[README.md](https://github.com/user-attachments/files/24067865/README.md)

**Key Capabilities:**
- **Geometry Type Detection** - Identifies point, polygon, and polyline geometries
- **Spatial Role Classification** - Determines if data represents events, boundaries, infrastructure, or observations
- **Spatial Resolution Analysis** - Detects granularity from coordinates to city-level
- **Multi-Format Support** - Handles lat/lon columns, WKT, GeoJSON, and location tuples
- **Seamless AutoDDG Integration** - Enriches semantic profiles with spatial metadata

---

## Installation

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

## Requirements

All dependencies are automatically installed via `pip install -r requirements.txt`.

---

## Citation

If you use this geospatial profiler in your research, please cite:

```bibtex
@misc{datalex-geo-profiler,
  title={Geospatial Profiler for AutoDDG},
  author={Apoorva, Anuhiya, Pavan},
  year={2025},
  url={https://github.com/Apoorva-Menon/DataLex}
}
```

The original AutoDDG framework:

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
