# Software Dependency Manifest

## Overview
This document provides a comprehensive overview of all dependencies used in the Neo4j Graph Data Analysis project, including development environment configurations, runtime dependencies, and tooling.

## Development Environment

### VS Code Extensions
| Extension ID | Version | Purpose |
|-------------|---------|----------|
| ms-python.python | Latest | Python language support |
| ms-python.vscode-pylance | Latest | Python type checking and intelligence |
| ms-python.black-formatter | Latest | Code formatting |
| ms-python.flake8 | Latest | Linting |
| ms-python.isort | Latest | Import organization |
| neo4j.neo4j-vscode | Latest | Neo4j development support |

### Dev Container Configuration
| Component | Version | Purpose |
|-----------|---------|----------|
| Dev Containers | Latest | VS Code remote container development |
| Docker Desktop | Latest | Container runtime |
| Remote - SSH | Latest | Remote development |
| Remote - WSL | Latest | Windows Subsystem for Linux integration |

### Dev Container Features
```json
{
    "customizations": {
        "vscode": {
            "extensions": [...],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python",
                "python.formatting.provider": "black",
                "python.linting.enabled": true,
                "python.linting.flake8Enabled": true
            }
        }
    }
}
```

## System Dependencies

### Base Image
- **python:3.11-slim**
  - Purpose: Minimal Python runtime environment
  - Rationale: Provides a balance between size and functionality

### Linux System Libraries
| Package | Version | Purpose | Installation Method |
|---------|---------|---------|-------------------|
| git | Latest | Version control and package installation | apt-get |
| openssh-client | Latest | Secure communications | apt-get |
| build-essential | Latest | Compilation tools for Python packages | apt-get |
| libgraphviz-dev | Latest | Graph visualization support | apt-get |
| graphviz | Latest | Graph rendering and visualization | apt-get |
| curl | Latest | HTTP requests and downloads | apt-get |
| wget | Latest | File downloads | apt-get |
| ninja-build | Latest | Fast build system for PyTorch extensions | apt-get |
| cmake | Latest | Build system for C++ libraries | apt-get |

## Neo4j Dependencies

### Core Database
| Package | Version | Purpose |
|---------|---------|---------|
| neo4j | 5.14.1 | Core Neo4j Python driver |
| neo4j-driver | 5.14.1 | Official Neo4j Python driver |
| graphdatascience | 1.7 | Neo4j Graph Data Science library integration |
| py2neo | 2021.2.4 | Higher-level Neo4j Python integration |
| neomodel | 5.2.1 | Object Graph Mapper (OGM) for Neo4j |

### Neo4j Plugins
| Plugin | Purpose | Configuration |
|--------|---------|---------------|
| APOC | Extended Procedures Library | Enabled via NEO4J_PLUGINS |
| Graph Data Science | Graph Algorithms Library | Enabled via NEO4J_PLUGINS |

## Python Libraries

### Graph Neural Networks
| Package | Version | Purpose |
|---------|---------|---------|
| torch_geometric | 2.5.2 | Graph Neural Network library |
| torch_scatter | 2.1.0 | Scatter operations for GNNs |
| torch_sparse | 0.6.15 | Sparse tensor operations |
| torch | 2.1.2 | Deep learning framework |

### Graph Processing
| Package | Version | Purpose |
|---------|---------|---------|
| networkx | 3.2.1 | Graph algorithms and analysis |
| python-igraph | 0.11.3 | High-performance graph operations |
| networkit | 10.1 | Large-scale network analysis |
| pyvis | 0.3.2 | Interactive network visualizations |
| graphviz | 0.20.1 | Graph visualization |

### Machine Learning & AI
| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.1.0 | LLM workflow management |
| transformers | 4.36.2 | NLP transformers models |
| sentence-transformers | 2.2.2 | Text embeddings |
| faiss-cpu | 1.7.4 | Vector similarity search |
| chromadb | 0.4.22 | Vector database |
| openai | 1.6.1 | OpenAI API integration |
| tiktoken | 0.5.2 | Token counting for LLMs |

### Data Science & Visualization
| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.1.4 | Data manipulation and analysis |
| numpy | 1.26.3 | Numerical computations |
| scikit-learn | 1.3.2 | Machine learning algorithms |
| matplotlib | 3.8.2 | Static visualizations |
| seaborn | 0.13.1 | Statistical visualizations |
| plotly | 5.18.0 | Interactive visualizations |

### Development Tools
| Package | Version | Purpose |
|---------|---------|---------|
| jupyter | Latest | Interactive development environment |
| pylint | Latest | Code linting |
| black | Latest | Code formatting |
| flake8 | Latest | Code style enforcement |
| isort | Latest | Import sorting |
| pytest | Latest | Testing framework |
| pytest-cov | Latest | Test coverage reporting |

### Utilities
| Package | Version | Purpose |
|---------|---------|---------|
| tqdm | 4.66.1 | Progress bars |
| requests | 2.31.0 | HTTP client |
| beautifulsoup4 | 4.12.2 | HTML parsing |
| faker | 22.5.1 | Test data generation |
| python-dateutil | 2.8.2 | Date manipulation |
| python-dotenv | 1.0.0 | Environment variable management |

## Container Configuration

### Docker Compose Services
| Service | Base Image | Purpose |
|---------|------------|----------|
| neo4j | neo4j:5.15.0 | Graph database |
| data-generator | python:3.11-slim | Data generation and processing |

### Volume Mounts
| Volume | Purpose |
|--------|----------|
| neo4j_data | Persistent database storage |
| neo4j_logs | Log files |
| neo4j_import | Data import directory |
| neo4j_plugins | Neo4j plugins |
| vscode-extensions | VS Code extensions storage |

## Version Control
Changes to dependencies should be documented here with:
- Date of change
- Reason for update
- Impact assessment
- Testing results

## Security Considerations
- Regular security audits via `pip-audit`
- Vulnerability scanning
- License compliance checking
- Container security scanning
- Development environment isolation

## Maintenance Guidelines
1. Regular review of dependency versions
2. Security patch application process
3. Testing requirements for updates
4. Rollback procedures
5. Dev container rebuild process

## Usage Instructions
1. Development setup
   ```bash
   code .
   # Select "Reopen in Container"
   ```
2. Production deployment
3. Testing environment configuration
4. CI/CD pipeline integration

## Common Issues and Solutions
Document known issues, workarounds, and solutions related to specific dependency versions or combinations.

## Special Notes
- PyTorch Geometric libraries require specific CUDA versions for GPU support
- Dev container setup requires Docker Desktop with WSL2 on Windows
- Some extensions may need manual configuration in VS Code

---
Last Updated: 2024-01-04

Maintainer: @AJamal27891