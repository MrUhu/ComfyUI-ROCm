# Graph Report - ComfyUI-ROCm  (2026-09-24)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 137 nodes · 145 edges · 13 communities (8 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 1,348 input · 2,128 output

## Graph Freshness
- Built from commit: `669c14be`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Graphify Knowledge Graph Tool
- download_models.py
- ComfyUI ROCm Docker Project
- Architecture Documentation
- Usage Guide
- startup.sh
- build.sh
- Setup Instructions
- ComfyUI ROCm - Project Overview
- architecture.md
- Key Components
- Container Management
- urllib_parse

## God Nodes (most connected - your core abstractions)
1. `Architecture Documentation` - 10 edges
2. `Usage Guide` - 10 edges
3. `Setup Instructions` - 10 edges
4. `ComfyUI ROCm - Project Overview` - 9 edges
5. `download_model_set()` - 7 edges
6. `Key Components` - 7 edges
7. `log()` - 5 edges
8. `Container Management` - 5 edges
9. `Troubleshooting Setup Issues` - 5 edges
10. `download_file()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `ComfyUI ROCm Docker Project` --shares_data_with--> `Python ROCm Requirements`  [EXTRACTED]
  None → None  _Bridges community 2 → community 9_

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **ComfyUI ROCm Deployment Stack** — docker_compose, docker_models, docker_requirements_rocm [EXTRACTED 1.00]
- **Graphify Extraction & Query Pipeline** — roo_skills_knowledge_graphify_skill, roo_skills_knowledge_graphify_references_extraction_spec, roo_skills_knowledge_graphify_references_query [EXTRACTED 1.00]

## Communities (13 total, 5 thin omitted)

### Community 1 - "download_models.py"
Cohesion: 0.15
Nodes (16): download_file(), download_model_set(), load_models_config(), log(), main(), Smart model downloader for ComfyUI, Download file with progress bar and validation, Load models configuration from YAML (+8 more)

### Community 2 - "ComfyUI ROCm Docker Project"
Cohesion: 0.25
Nodes (4): AMD ROCm GPU Support, ComfyUI ROCm Docker Project, Docker Compose Service Configuration, Model Download Configuration

### Community 3 - "Architecture Documentation"
Cohesion: 0.11
Nodes (18): Adding Custom Models, Adding Custom Nodes, Architecture Documentation, Component Interaction, Container Architecture, Customizing the Build, Data Flow, Dependency Chain (+10 more)

### Community 4 - "Usage Guide"
Cohesion: 0.08
Nodes (24): Access the Interface, Common Issues, Custom Model Downloads, Debug Mode, Docker Compose, Docker Run, Environment Variables, Health Check (+16 more)

### Community 7 - "Setup Instructions"
Cohesion: 0.08
Nodes (24): Access ComfyUI, Build Fails on Dependencies, Build Time Expectations, Container Cannot Access GPU, Direct Docker Build, Docker Compose (Recommended for production), Docker GPU Support Not Working, Hardware Requirements (+16 more)

### Community 8 - "ComfyUI ROCm - Project Overview"
Cohesion: 0.22
Nodes (9): ComfyUI ROCm - Project Overview, Key Features, License, Project Structure, Supported Hardware, Third-Party Components, Version Information, What is this project? (+1 more)

### Community 10 - "Key Components"
Cohesion: 0.29
Nodes (7): [`docker-compose.yaml`](../docker-compose.yaml), [`docker/Dockerfile`](../docker/Dockerfile), [`docker/download_models.py`](../docker/download_models.py), [`docker/models.yaml`](../docker/models.yaml), [`docker/requirements_rocm.txt`](../docker/requirements_rocm.txt), [`docker/startup.sh`](../docker/startup.sh), Key Components

### Community 11 - "Container Management"
Cohesion: 0.40
Nodes (5): Container Management, Execute Commands Inside Container, Remove Container, Start/Stop/Restart, View Logs

## Knowledge Gaps
- **66 isolated node(s):** `[`docker-compose.yaml`](../docker-compose.yaml)`, `[`docker/Dockerfile`](../docker/Dockerfile)`, `[`docker/download_models.py`](../docker/download_models.py)`, `[`docker/models.yaml`](../docker/models.yaml)`, `[`docker/requirements_rocm.txt`](../docker/requirements_rocm.txt)` (+61 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 92 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Usage Guide` connect `Usage Guide` to `architecture.md`, `Container Management`?**
  _High betweenness centrality (0.260) - this node is a cross-community bridge._
- **Why does `Architecture Documentation` connect `Architecture Documentation` to `architecture.md`, `Key Components`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **Why does `Setup Instructions` connect `Setup Instructions` to `architecture.md`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **What connects `[`docker-compose.yaml`](../docker-compose.yaml)`, `[`docker/Dockerfile`](../docker/Dockerfile)`, `[`docker/download_models.py`](../docker/download_models.py)` to the rest of the system?**
  _66 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Architecture Documentation` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `Usage Guide` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._
- **Should `Setup Instructions` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._
