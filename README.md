# Otimização Autônoma Sub-Minuto de Perdas Técnicas e Desbalanço de Fases em Redes com Alta GD Solar

[![Norma ANEEL](https://img.shields.io/badge/Regulação-ANEEL%20PRODIST%20Módulo%208-green)](https://www.gov.br/aneel)
[![ODS 7](https://img.shields.io/badge/ONU%20ODS-7%20Energia%20Limpa-orange)](https://brasil.un.org/pt-br/sdgs/7)
[![ODS 13](https://img.shields.io/badge/ONU%20ODS-13%20Ação%20Climática-blue)](https://brasil.un.org/pt-br/sdgs/13)
[![Status de PI](https://img.shields.io/badge/Propriedade%20Intelectual-Patente%20Pendente-red)](#-aviso-de-propriedade-intelectual--patente-pendente)

**Alvo Regulatório:** ANEEL PRODIST Módulo 8 (Qualidade da Energia Elétrica & Perdas Técnicas)  
**Casos de Aplicação:** Chamadas de P&D ANEEL (Inova Cemig.Lab, GRIDVortex Energisa, Enel Open Innovability)  
**Arquiteto Principal & Pesquisador:** Bruno Loureiro Desidera  
**Framework Algorítmico:** MEA v14.5 "Quantum Core" Architecture  

---

## 🔒 Aviso de Propriedade Intelectual & Patente Pendente

> **AVISO DE SALVAGUARDA DE PROPRIEDADE INDUSTRIAL:**  
> O algoritmo do motor de otimização (**MEA v14.5 Concave Annealing Engine**), seu agendamento de recozimento côncavo subcrítico (gamma = 1.45), o kernel compilado nativamente em LLVM/SIMD e as rotinas de quench são propriedade intelectual protegida por depósitos formais de patentes internacionais (**Patent Pending**).
>
> Para viabilizar a auditoria regulatória por comitês de inovação de distribuidoras de energia (CEMIG, Energisa, Enel) e pela ANEEL **sem comprometer a novidade dos pedidos de patente**:
> 1. A topologia completa do alimentador com 3.000 UCs e 60 transformadores está aberta no arquivo `data_aneel_3000.json`.
> 2. O vetor de comutação de fases encontrado pelo motor em 14,86 segundos está publicado integralmente no arquivo `solution_aneel_ground_truth.json`.
> 3. O script público de auditoria independente (`auditoria_aneel_prodist.py`) permite que qualquer engenheiro recalcule as Leis de Kirchhoff e Joule em menos de 0,2 segundo.
> 4. Testes de Prova de Conceito (PoC) em campo e acesso ao código compilado sob acordo de confidencialidade (NDA) podem ser solicitados diretamente ao autor.

---

## 1. O Desafio Operacional no Brasil: A Lei 14.300/2022 e a GD Solar

A expansão recorde da micro e minigeração distribuída solar fotovoltaica no Brasil (GD Solar) sobrecarregou os alimentadores de baixa tensão. A injeção assimétrica de potência ativa provoca:
* **Sobreaquecimento Crítico de Transformadores:** Transformadores de distribuição (MT/BT de 75 kVA e 112,5 kVA) sofrem queima prematura de enrolamento devido ao desbalanço entre fases.
* **Perdas Técnicas no Condutor de Neutro:** Correntes de retorno de neutro elevadas geram perdas por Efeito Joule (P = R * I²), pesando na tarifa regulatória da ANEEL.
* **O Limite da Computação Clássica:** Solvers comerciais de programação inteira não-linear (MINLP) levam mais de 30 minutos para calcular o balanceamento de um alimentador regional de 3.000 UCs, inviabilizando a atuação em tempo real diante da intermitência de nuvens.

---

## 2. A Solução: Formulação em Vidro de Spins Antiferromagnético

A minimização quadrática da corrente de neutro em cada transformador com variáveis de fase discretas s_i in {-1, +1} reduz-se estritamente a um **Vidro de Spins de Ising Antiferromagnético puro sem campo linear (h_i = 0)**:

H_Ising = sum_{t=1}^{60} sum_{i < j} J_ij * s_i * s_j,  onde J_ij = 2 * (I_i / I_max) * (I_j / I_max)

* **Carga com Carga (I_i > 0, I_j > 0 => J_ij > 0):** Os consumidores repelem-se mutuamente para fases opostas de forma natural.
* **GD Solar com Carga (I_i < 0, I_j > 0 => J_ij < 0):** O gerador solar atrai cargas locais para a sua fase, anulando a corrente na raiz do transformador.

---

## 3. Resultados Auditados da Prova de Conceito (3.000 UCs | 60 Trafos)

| Métrica Avaliada | Situação Inicial (Sem Otimização) | Pós-Otimização (Motor MEA v14.5) | Impacto Regulatório / Operacional |
| :--- | :--- | :--- | :--- |
| **Tempo de Convergência** | >1.800 s (Estimado MINLP) | **14,86 segundos** | **Atuação em Tempo Real (< 30s)** |
| **Alocação de Fases** | 3.000 Fase A (100%) | **1.469 Fase A / 1.531 Fase B** | **Simetria Quase Perfeita (49,0% / 51,0%)** |
| **Corrente Agregada de Neutro** | 33.255,5 A | **53,5 A** | **Queda Residual de -33.202,0 A** |
| **Eficiência de Cancelamento** | 0,00% | **99,84%** | **Quase Extinção da Corrente Parasita** |
| **Perdas Joule no Neutro** | 4.828,92 kW | **0,0210 kW** | **4.828,89 kW Instantâneos Salvos** |
| **Energia Anual Recuperada** | — | **23.265,6 MWh / ano** | **Alívio da Matriz Elétrica** |
| **Economia Financeira Direta** | — | **R$ 12.098.119,93 / ano** | **Retorno Imediato para a Distribuidora** |

---

## 4. Como Executar a Auditoria Independente

Para verificar a física das leis de Kirchhoff e os cálculos econômicos sem necessidade de instalar compiladores:

```bash
# 1. Clonar o repositório
git clone https://github.com/Ahavahdev1/aneel-smartgrid-phase-balancing.git
cd aneel-smartgrid-phase-balancing

# 2. Executar o auditor regulatório
python auditoria_aneel_prodist.py

5. Proposta para Chamadas de Inovação Aberta (CEMIG / Energisa / Enel)
Estamos à disposição para estruturar projetos de P&D (regulados pela ANEEL) em regime de Prova de Conceito (PoC) em campo:
Hardware-in-the-Loop (HIL): Validação em bancada com chaves estáticas de transferência de fase (solid-state switches).
Piloto Operacional: Desdobramento em alimentador crítico com alta penetração de GD fotovoltaica.
📬 Contato do Proponente
Bruno Loureiro Desidera
Arquiteto de Software & Pesquisador Principal
Aberto para reuniões técnicas com equipes de Operação, Planejamento e Inovação de Concessionárias de Energia.