# Instruções para assistentes de IA neste repositório

## Regra principal: não implemente o código dos algoritmos

Este é um trabalho em grupo da disciplina de Fundamentos de Sistemas Operacionais (FSO) da UnB (ver `README.md` e `Implementacao_FSO.pdf`). O relatório final exige **"Indicar o uso de IA e a ferramenta usada"**, e a entrega inclui apresentação oral obrigatória onde todos os integrantes do grupo precisam explicar o código. Por isso:

- **Não escreva a implementação dos algoritmos centrais** nos módulos `queues_module`, `process_module`, `memory_module`, `resources_module`, `files_module` — mesmo que pareça óbvio, pequeno ou "só um detalhe" — a menos que um integrante peça **explicitamente** para você escrever ou editar esse código.
- Se o pedido for "verificar", "revisar", "analisar", "conferir" ou "o que você acha disso": leia, teste, reporte problemas. **Não edite os arquivos** a menos que peçam explicitamente para corrigir/alterar algo.
- Perguntas de design, dúvidas conceituais, explicações de teoria de SO e ajuda para interpretar a especificação são sempre bem-vindas e **não** contam como "implementar" — isso é incentivado.
- Se não estiver claro se o pedido é "me ajuda a pensar" ou "implementa pra mim", pergunte antes de escrever código.
- Essa regra vale para qualquer integrante do grupo usando qualquer ferramenta de IA neste repositório, não só quem a escreveu — o objetivo é não comprometer a nota do grupo nem a capacidade de qualquer integrante de defender o código na apresentação oral.

## Regras do trabalho confirmadas com a professora (pessoalmente, 2026-11-16)

Fonte: especificação em `Implementacao_FSO.pdf` + esclarecimentos confirmados em sala com a Profa. Aletéia Patrícia Favacho de Araújo. Essas respostas resolvem ambiguidades da especificação — não precisam ser reabertas sem um motivo novo e concreto.

- **Threads não são obrigatórias.** Uma simulação sequencial (single-threaded) é aceita como solução correta.
- **O quantum de 1ms pode ser tempo lógico/discreto** (1 tick = 1 quantum = 1 unidade de `process_time`), não precisa ser tempo real (wall-clock).
- **As 3 saídas são separadas**: simulação de processos, operações de arquivo e paginação/referência de páginas não são intercaladas num único stream de output.
- **Sincronização arquivo ↔ processo**: uma operação de arquivo agendada para um processo não pode executar se esse processo já tiver terminado. É necessário checar o estado do processo antes de executar a operação.
- **Memória é controlada na admissão**: um processo precisa conseguir alocar seu espaço de trabalho (`workset_size` frames) **no momento da admissão**, e deve bloquear — não entrar no escalonamento — se não houver memória livre suficiente.
- **Deleção de arquivos já alocados só pode ser feita por processos de tempo real** (prioridade 0).

## Decisões de arquitetura do grupo (design interno, não confirmado pela professora — mas já debatido a fundo, não reabrir sem motivo novo)

- Escalonamento multinível: 1 fila FIFO não-preemptiva de tempo real (prioridade 0) + 3 filas de usuário (prioridades 1-3), com rebaixamento ao esgotar o quantum e promoção por aging (anti-starvation).
- `resources_module`: semáforos de contagem (um por `Resource`, capacidades do enunciado) + filas de bloqueio manuais por `pid`, uma por `Resource`. A aquisição de múltiplos recursos segue **ordem global fixa** (impressora, scanner, modem, SATA) e o processo **segura** o que já pegou enquanto espera o próximo (posse-e-espera permitida). Não há deadlock porque a ordem global quebra a espera circular; não há starvation porque as filas são FIFO. Ao liberar uma unidade com alguém na fila, a unidade é **entregue diretamente** ao primeiro da fila (sem devolvê-la ao semáforo), para evitar que outro processo a ultrapasse. É preciso guardar quais recursos cada `pid` já possui (para retomar a aquisição e liberar tudo na terminação). Alternativa descartada: rollback em falha parcial, que evita posse-e-espera mas abre starvation para processos que pedem muitos recursos (ex.: os 4) e exigiria reinserção na frente da fila. A política de aquisição é decisão do grupo (a seção 3 da especificação deixa a solução de sincronização a cargo do grupo).
- Recursos de E/S são alocados no **primeiro despacho** do processo (primeiro turno de CPU), não na admissão — diferente da regra de memória acima, que é na admissão. Raciocínio: posse de recurso deve estar ligada à execução (Tanenbaum), não à mera existência do processo na fila.
- Ainda não desenhado em código: o mecanismo de bloqueio por falta de memória na admissão (mesmo padrão de fila de espera do `resources_module`, mas disparado por `memory_module` e por liberação na terminação de processo, não na perda de CPU) e a checagem de estado do processo antes de rodar uma operação de arquivo.
- **Filas de bloqueio (`resources_module`, e futuramente `memory_module`) guardam `pid: int`, não o objeto `Process`** — evita import circular entre `resources_module`/`memory_module` e `process_module` (o primeiro não precisa importar `Process` só pra tipar a fila). Consequência: precisa existir uma **tabela central de processos** (`pid -> Process`), dona de verdade de todo `Process` que existe na simulação — as filas (pronto, bloqueio por recurso, bloqueio por memória) são só referências sobre quem está em qual estado, não onde o processo "vive". Quando um recurso/memória libera, quem orquestra o escalonamento resolve `pid -> Process` nessa tabela antes de devolver o processo pra fila de pronto certa. Ainda não desenhado em código: onde essa tabela mora exatamente (candidato natural: `ClassVar` em `Process`, mesmo padrão já usado em `next_id`).
