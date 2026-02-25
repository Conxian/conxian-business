# Conxian Labs: Root Makefile
# Orchestrates development across the ecosystem.

.PHONY: init auth start stop update-all logs bench deploy help

help:
	@echo "Conxian Business Repository - Root Management Commands:"
	@echo "  make init        - Initialize and update all submodules"
	@echo "  make auth        - Provision local .env with secrets (via conxius-platform)"
	@echo "  make start       - Build and start the entire stack (via conxius-platform)"
	@echo "  make stop        - Stop and remove the stack"
	@echo "  make update-all  - Pull the latest main branches for all submodules"
	@echo "  make logs        - Tail logs for all services"
	@echo "  make bench       - Run automated performance benchmarks"
	@echo "  make deploy      - Run deployment workflows"

init:
	@echo "Initializing all submodules..."
	git submodule update --init --recursive

auth:
	@echo "Delegating auth to conxius-platform..."
	$(MAKE) -C conxius-platform auth

start:
	@echo "Delegating start to conxius-platform..."
	$(MAKE) -C conxius-platform start

stop:
	@echo "Delegating stop to conxius-platform..."
	$(MAKE) -C conxius-platform stop

update-all:
	@echo "Updating all submodules to main..."
	git submodule foreach 'git fetch origin && git checkout main && git pull'

logs:
	@echo "Delegating logs to conxius-platform..."
	$(MAKE) -C conxius-platform logs

bench:
	@echo "Delegating benchmarks to conxius-platform..."
	$(MAKE) -C conxius-platform bench

deploy:
	@echo "Delegating deployment to conxius-platform..."
	$(MAKE) -C conxius-platform deploy
