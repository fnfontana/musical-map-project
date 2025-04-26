# Documentação de Migração

Este documento orienta sobre a migração de dados, código e estrutura do projeto Musical Map.

## Migração de Dados

- Como migrar dados antigos para o novo banco SQLite.
- Scripts de apoio: `migrate_to_sqlite.py`, `consolidate_database-migration.md`.

## Migração de Código

- Refatoração para a nova arquitetura modular.
- Separação de responsabilidades por módulos.

## Estrutura Recomendada

- Veja `project/refactoring-guide.md` para detalhes da arquitetura.

## Passos Gerais

1. Backup dos dados antigos.
2. Executar scripts de migração.
3. Validar integridade dos dados migrados.
4. Ajustar configurações conforme necessário.

---

> Atualize este documento conforme novas migrações forem necessárias.
