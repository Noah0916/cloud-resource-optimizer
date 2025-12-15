#!/usr/bin/env python3
import argparse
import csv
import logging
import sys
import json
from collections import defaultdict
from typing import Optional

from src.data_models import Resource
from src.rules_engine import RuleEngine, Thresholds, StopIdleRule, DownsizeRule

# Exit codes
EXIT_OK = 0
EXIT_BAD_INPUT = 2
EXIT_NO_FINDINGS = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("cloudopt.log", encoding="utf-8"),
    ],
)


def open_csv_reader(path: str):
    # 1) Lees sample om delimiter te detecteren (bestand gaat daarna weer dicht)
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(2048)

    delimiter = ";" if sample.count(";") > sample.count(",") else ","

    # 2) Open het bestand opnieuw en geef het OPEN file-object terug
    f = open(path, "r", encoding="utf-8-sig", newline="")
    return f, csv.DictReader(f, delimiter=delimiter)



def load_thresholds(config_path: Optional[str]) -> Thresholds:
    if not config_path:
        return Thresholds()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return Thresholds(
            downsize_usage_lt=float(cfg.get("downsize_usage_lt", 30.0)),
            stop_usage_lt=float(cfg.get("stop_usage_lt", 5.0)),
        )
    except Exception as e:
        logging.error(f"Config fout: {e}")
        sys.exit(EXIT_BAD_INPUT)


def simulate(input_file: str) -> None:
    logging.info(f"Simulate run on {input_file}")

    total_cost = 0.0
    count = 0
    provider_costs = defaultdict(float)

    f, reader = open_csv_reader(input_file)
    with f:
        for row in reader:
            cost = float(row["cost_per_month"])
            provider = row["provider"]

            total_cost += cost
            count += 1
            provider_costs[provider] += cost

    print("=== SIMULATION REPORT ===")
    print(f"Aantal resources: {count}")
    print(f"Totaal maandelijkse kosten: €{total_cost:.2f}")
    print("\nKosten per provider:")
    for p, c in provider_costs.items():
        print(f"  {p}: €{c:.2f}")


def optimize(input_file: str, output_file: str, config_path: Optional[str], dry_run: bool) -> None:
    logging.info(f"Optimize run: {input_file} -> {output_file}")

    thresholds = load_thresholds(config_path)
    engine = RuleEngine([
        StopIdleRule(thresholds),
        DownsizeRule(thresholds),
    ])

    optimized_rows = []

    f, reader = open_csv_reader(input_file)
    with f:
        for row in reader:
            try:
                resource = Resource(
                    provider=row["provider"],
                    region=row.get("region", "unknown"),
                    resource_type=row.get("resource_type", "unknown"),
                    sku=row.get("sku", "unknown"),
                    cost_per_month=float(row["cost_per_month"]),
                    usage_percent=float(row["usage_percent"]),
                )
            except Exception:
                continue

            rec = engine.run(resource)

            row.update({
                "rule_id": rec.rule_id,
                "action": rec.action,
                "optimized_cost": rec.optimized_cost,
                "savings": rec.savings,
                "reason": rec.reason,
            })
            optimized_rows.append(row)

    if not optimized_rows:
        print("[OPTIMIZE] Geen optimalisaties gevonden.")
        sys.exit(EXIT_NO_FINDINGS)

    total_savings = sum(float(r["savings"]) for r in optimized_rows)
    print(f"[OPTIMIZE] Findings: {len(optimized_rows)} | Total savings: €{total_savings:.2f}")

    if dry_run:
        print("[OPTIMIZE] Dry-run: geen bestand geschreven.")
        sys.exit(EXIT_OK)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=optimized_rows[0].keys())
        writer.writeheader()
        writer.writerows(optimized_rows)

    print(f"[OPTIMIZE] Rapport opgeslagen in: {output_file}")


def stats(input_file: str, group_by: str) -> None:
    totals = defaultdict(float)

    f, reader = open_csv_reader(input_file)
    with f:
        for row in reader:
            key = row[group_by]
            totals[key] += float(row["cost_per_month"])

    print(f"=== STATS per {group_by} ===")
    for k, v in totals.items():
        print(f"  {k}: €{v:.2f}")


def build_parser():
    parser = argparse.ArgumentParser(description="Cloud cost optimization CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_sim = subparsers.add_parser("simulate")
    p_sim.add_argument("--input", required=True)

    p_opt = subparsers.add_parser("optimize")
    p_opt.add_argument("--input", required=True)
    p_opt.add_argument("--output", required=True)
    p_opt.add_argument("--config", required=False)
    p_opt.add_argument("--dry-run", action="store_true")

    p_stats = subparsers.add_parser("stats")
    p_stats.add_argument("--input", required=True)
    p_stats.add_argument("--group-by", required=True)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "simulate":
        simulate(args.input)
    elif args.command == "optimize":
        optimize(args.input, args.output, args.config, args.dry_run)
    elif args.command == "stats":
        stats(args.input, args.group_by)


if __name__ == "__main__":
    main()
