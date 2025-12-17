# Cloud Resource Optimizer (Python CLI)

Dit project is een command-line tool geschreven in Python voor het analyseren en optimaliseren
van cloud resource kosten.

De focus van dit project ligt op **structuur, tooling, debugging en deploybaarheid**,
niet op complexe businesslogica.

## Functionaliteit

- `simulate` – geeft een kostenoverzicht van cloud resources
- `optimize` – genereert een optimalisatierapport op basis van usage-percentages
- `stats` – toont statistieken per cloud provider

## Technologieën

- Python 3
- argparse (CLI met subcommando’s)
- CSV-verwerking
- logging (console + file)
- Docker
- Git & GitHub
- PowerShell en Linux/WSL

## Voorbeeldgebruik

```bash
python -m src.cloudopt_cli simulate --input data/resources.csv
python -m src.cloudopt_cli optimize --input data/resources.csv --output optimization_report.csv
python -m src.cloudopt_cli stats --input optimization_report.csv
