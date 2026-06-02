#!/bin/bash
source .venv/bin/activate
echo "Running v0..."
python3 run_eval.py --provider gemini --version v0 --suite base --eval-cases data/eval_base.json > run_v0.log 2>&1
echo "Running v1..."
python3 run_eval.py --provider gemini --version v1 --suite base --eval-cases data/eval_base.json > run_v1.log 2>&1
echo "Running v2..."
python3 run_eval.py --provider gemini --version v2 --suite base --eval-cases data/eval_base.json > run_v2.log 2>&1
echo "Running v3 base..."
python3 run_eval.py --provider gemini --version v3 --suite base --eval-cases data/eval_base.json > run_v3.log 2>&1
echo "Running v3 group..."
python3 run_eval.py --provider gemini --version v3 --suite group --eval-cases data/eval_group.json > run_v3_group.log 2>&1
echo "Done"
