#!/usr/bin/env bash
set -e
mkdir -p graph_data/backups
cp instance/knowledge_graph.db graph_data/backups/knowledge_graph_$(date +%Y%m%d_%H%M%S).db 2>/dev/null || true
