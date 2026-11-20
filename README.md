# Pseudo OS - Grupo 7

## FSO 2026.2

Projeto de implementação da matéria de Fundamentos de Sistemas Operacionais com a Professora **Aletéia Patrícia Favacho de Araújo**

## Membros

| Nome Completo | Matrícula |
| :--- | ---: |
| Lucas Rocha dos Santos | 211055325 |
| Gabriela de Oliveira Henriques | 211055254 |
| Danilo Silveira da Silva | 222014142 |
| Lucas Lima | xxxxxxxxx |

## Uso de IA neste projeto

O relatório final exige declarar o uso de ferramentas de IA. Por isso, usamos IA (Claude Code) apenas para revisar, verificar, testar e explicar código — **não** para implementar os algoritmos principais (filas/escalonamento, memória/paginação, recursos de E/S, sistema de arquivos). Essas regras estão em `CLAUDE.md` e se aplicam a qualquer integrante usando qualquer ferramenta de IA no repositório, para que todo mundo consiga defender o próprio código na apresentação oral.

## Regras confirmadas com a professora (2026-11-16)

Esclarecimentos sobre pontos ambíguos da especificação (`Implementacao_FSO.pdf`), confirmados pessoalmente com a Profa. Aletéia:

- Threads não são obrigatórias — simulação sequencial é aceita.
- O quantum de 1ms pode ser tempo lógico/discreto (1 tick = 1 quantum), não precisa ser tempo real.
- As 3 saídas (processos, operações de arquivo, paginação) são separadas, não intercaladas.
- Uma operação de arquivo não pode executar se o processo associado já tiver terminado — precisa de sincronização entre os módulos.
- Memória é controlada na admissão: o processo precisa conseguir alocar seu `workset_size` ao entrar no sistema, e bloqueia se não houver memória livre suficiente.
- Deleção de arquivos já alocados só pode ser feita por processos de tempo real (prioridade 0).

Detalhes de arquitetura e decisões de design do grupo estão em `CLAUDE.md`.
