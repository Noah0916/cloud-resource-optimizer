# Cloud Resource Optimizer

Cloud Resource Optimizer is een Python command-line tool voor het analyseren en optimaliseren van cloud resource kosten.
Het project is opgezet als een realistische cloud engineering opdracht met focus op structuur, deploybaarheid en cloud integratie.

De businesslogica is bewust eenvoudig gehouden; de nadruk ligt op tooling, packaging, containerization en infrastructuur.

---

## Functionaliteit

De CLI ondersteunt de volgende commando’s:

* `simulate`
  Geeft een kostenoverzicht op basis van inputdata.

* `optimize`
  Genereert een optimalisatierapport op basis van usage percentages.

* `stats`
  Toont statistieken per cloud provider.

De input en output worden verwerkt als CSV-bestanden.

---

## Technologieën

* Python 3.10+
* argparse (CLI met subcommands)
* Docker
* Git & GitHub
* Azure Container Registry
* Azure Container Apps Jobs
* Azure Blob Storage
* Azure Managed Identity
* Terraform (Infrastructure as Code)

---

## Projectstructuur

```
.
├── src/
│   ├── cloudopt_cli/
│   │   ├── cli.py
│   │   └── __main__.py
│   └── cloudopt/
│       ├── data_models.py
│       └── rules_engine.py
├── data/
│   └── resources.csv
├── infra/
│   └── terraform/
│       ├── main.tf
│       └── variables.tf
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Lokaal gebruik

Installatie in editable mode:

```bash
pip install -e .
```

Voorbeelden:

```bash
cloudopt simulate --input data/resources.csv
cloudopt optimize --input data/resources.csv --output optimization_report.csv
cloudopt stats --input optimization_report.csv
```

---

## Docker

Build en run lokaal:

```bash
docker build -t cloudopt:local .
docker run --rm cloudopt:local simulate --input data/resources.csv
```

---

## Azure uitvoering

Het project kan worden uitgevoerd als een batch job in Azure:

1. Infrastructure provisioning via Terraform
2. Docker image push naar Azure Container Registry
3. Execution via Azure Container Apps Jobs
4. Input en output via Azure Blob Storage
5. Authenticatie via Managed Identity (geen secrets in code)

Deze setup bootst een realistische productie-omgeving na voor batchverwerking.

---

## Security en best practices

* Geen secrets in Git
* Geen credentials in Docker images
* Terraform state uitgesloten van versiebeheer
* Gebruik van Azure RBAC en Managed Identity

---

## Doel van het project

Dit project is bedoeld om cloud engineering vaardigheden te demonstreren, waaronder:

* Python packaging en CLI ontwerp
* Containerization
* Infrastructure as Code
* Cloud deployment en debugging
* Werken met managed identities en storage

---

## Mogelijke uitbreidingen

* Scheduling van jobs
* CI/CD pipeline voor build en deploy
* Ondersteuning voor meerdere inputformaten
* Uitbreiding naar multi-cloud scenario’s

---

## Auteur

Noah
Cloud / Platform Engineer (in ontwikkeling)
