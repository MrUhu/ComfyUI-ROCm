# Graph Report - ComfyUI-ROCm  (2026-10-03)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 145 nodes · 162 edges · 15 communities (9 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 1,432 input · 2,272 output

## Graph Freshness
- Built from commit: `54c85a22`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Graphify Knowledge Graph Tool
- workspace/download_models.py
- ComfyUI ROCm Docker Project
- Architecture Documentation
- Usage Guide
- download_models.py
- build.sh
- Setup Instructions
- ComfyUI ROCm - Project Overview
- Python ROCm Requirements
- Key Components
- Model Management
- urllib_parse
- startup.sh
- Model Download Configuration

## God Nodes (most connected - your core abstractions)
1. `Architecture Documentation` - 10 edges
2. `Usage Guide` - 10 edges
3. `Setup Instructions` - 10 edges
4. `ComfyUI ROCm - Project Overview` - 9 edges
5. `download_model_set()` - 7 edges
6. `download_model_set()` - 7 edges
7. `Key Components` - 7 edges
8. `log()` - 5 edges
9. `log()` - 5 edges
10. `Container Management` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Graphify Extraction & Query Pipeline** — roo_skills_knowledge_graphify_skill, roo_skills_knowledge_graphify_references_extraction_spec, roo_skills_knowledge_graphify_references_query [EXTRACTED 1.00]

## Communities (15 total, 6 thin omitted)

### Community 1 - "workspace/download_models.py"
Cohesion: 0.27
Nodes (11): download_file(), download_model_set(), load_models_config(), log(), main(), Smart model downloader for ComfyUI, Download file with progress bar and validation, Load models configuration from YAML (+3 more)

### Community 2 - "ComfyUI ROCm Docker Project"
Cohesion: 0.33
Nodes (3): AMD ROCm GPU Support, ComfyUI ROCm Docker Project, Docker Compose Service Configuration

### Community 3 - "Architecture Documentation"
Cohesion: 0.11
Nodes (18): Adding Custom Models, Adding Custom Nodes, Architecture Documentation, Component Interaction, Container Architecture, Customizing the Build, Data Flow, Dependency Chain (+10 more)

### Community 4 - "Usage Guide"
Cohesion: 0.08
Nodes (25): Access the Interface, Common Issues, Container Management, Debug Mode, Docker Compose, Docker Run, Environment Variables, Execute Commands Inside Container (+17 more)

### Community 5 - "download_models.py"
Cohesion: 0.18
Nodes (14): download_file(), download_model_set(), load_models_config(), log(), main(), Smart model downloader for ComfyUI, Download file with progress bar and validation, Load models configuration from YAML (+6 more)

### Community 7 - "Setup Instructions"
Cohesion: 0.08
Nodes (24): Access ComfyUI, Build Fails on Dependencies, Build Time Expectations, Container Cannot Access GPU, Direct Docker Build, Docker Compose (Recommended for production), Docker GPU Support Not Working, Hardware Requirements (+16 more)

### Community 8 - "ComfyUI ROCm - Project Overview"
Cohesion: 0.19
Nodes (9): ComfyUI ROCm - Project Overview, Key Features, License, Project Structure, Supported Hardware, Third-Party Components, Version Information, What is this project? (+1 more)

### Community 10 - "Key Components"
Cohesion: 0.29
Nodes (7): [`artifacts/workspace/download_models.py`](../artifacts/workspace/download_models.py), [`artifacts/workspace/models.yaml`](../artifacts/workspace/models.yaml), [`artifacts/workspace/requirements_rocm.txt`](../artifacts/workspace/requirements_rocm.txt), [`artifacts/workspace/startup.sh`](../artifacts/workspace/startup.sh), [`docker-compose.yaml`](../docker-compose.yaml), [`Dockerfile`](../Dockerfile), Key Components

### Community 11 - "Model Management"
Cohesion: 0.50
Nodes (4): Custom Model Downloads, Model Directory Structure, Model Download Modes, Model Management

## Knowledge Gaps
- **66 isolated node(s):** `[`artifacts/workspace/download_models.py`](../artifacts/workspace/download_models.py)`, `[`artifacts/workspace/models.yaml`](../artifacts/workspace/models.yaml)`, `[`artifacts/workspace/requirements_rocm.txt`](../artifacts/workspace/requirements_rocm.txt)`, `[`artifacts/workspace/startup.sh`](../artifacts/workspace/startup.sh)`, `[`docker-compose.yaml`](../docker-compose.yaml)` (+61 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 94 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Usage Guide` connect `Usage Guide` to `ComfyUI ROCm - Project Overview`, `Model Management`?**
  _High betweenness centrality (0.202) - this node is a cross-community bridge._
- **Why does `Architecture Documentation` connect `Architecture Documentation` to `ComfyUI ROCm - Project Overview`, `Key Components`?**
  _High betweenness centrality (0.177) - this node is a cross-community bridge._
- **Why does `Setup Instructions` connect `Setup Instructions` to `ComfyUI ROCm - Project Overview`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **What connects `[`artifacts/workspace/download_models.py`](../artifacts/workspace/download_models.py)`, `[`artifacts/workspace/models.yaml`](../artifacts/workspace/models.yaml)`, `[`artifacts/workspace/requirements_rocm.txt`](../artifacts/workspace/requirements_rocm.txt)` to the rest of the system?**
  _66 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Architecture Documentation` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `Usage Guide` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Setup Instructions` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._