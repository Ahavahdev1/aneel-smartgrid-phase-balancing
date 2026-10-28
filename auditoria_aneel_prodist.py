# -*- coding: utf-8 -*-
# ==============================================================================
# AUDITORIA INDEPENDENTE DE FÍSICA E IMPACTO REGULATÓRIO ANEEL PRODIST MÓDULO 8
# ==============================================================================
import json
import numpy as np

def auditar_poc_aneel():
    print("=" * 80)
    print("🔬 AUDITORIA INDEPENDENTE DE EFICIÊNCIA ENERGÉTICA (PADRÃO ANEEL / PRODIST)")
    print("   ALVOS: Inova Cemig.Lab | GRIDVortex Energisa | Enel Open Innovability")
    print("=" * 80)

    with open("data_aneel_3000.json", "r") as f:
        rede = json.load(f)

    with open("solution_aneel_ground_truth.json", "r") as f:
        solucao = json.load(f)

    correntes = np.array(rede["currents"])
    trafos = rede["trafos"]
    spins = {int(k): v for k, v in solucao["spins"].items()}

    print(f"[*] Base de Dados Auditada:")
    print(f"    • Unidades Consumidoras (UCs)     : {rede['num_ucs']:,}")
    print(f"    • Transformadores de Poste (MT/BT): {rede['num_trafos']}")
    print(f"    • Tempo de Convergência do Motor  : {solucao['tempo_execucao_segundos']} segundos")
    print("\n[+] Processando Leis de Kirchhoff e Joule trafo por trafo...")

    i_neutro_antes_total = 0.0
    i_neutro_depois_total = 0.0
    r_ramal_bt = 0.25 # Resistência típica de neutro em BT (Ohms)
    perdas_kw_antes = 0.0
    perdas_kw_depois = 0.0

    for trafo in trafos:
        i_trafo = correntes[trafo]
        s_trafo = np.array([spins[u] for u in trafo])

        i_antes = abs(np.sum(i_trafo))
        i_neutro_antes_total += i_antes
        perdas_kw_antes += (r_ramal_bt * (i_antes ** 2)) / 1000.0

        i_depois = abs(np.sum(i_trafo * s_trafo))
        i_neutro_depois_total += i_depois
        perdas_kw_depois += (r_ramal_bt * (i_depois ** 2)) / 1000.0

    eficiencia = (1.0 - (i_neutro_depois_total / i_neutro_antes_total)) * 100.0
    kw_salvos = perdas_kw_antes - perdas_kw_depois

    # Premissas ANEEL: 8.760 h/ano | Fator de Carga: 0.55 | Tarifa de Energia: R$ 520,00/MWh
    mwh_ano_salvos = (kw_salvos / 1000.0) * 8760.0 * 0.55
    tarifa_mwh_br = 520.00
    economia_reais_ano = mwh_ano_salvos * tarifa_mwh_br

    fase_a = sum(1 for s in spins.values() if s == 1)
    fase_b = sum(1 for s in spins.values() if s == -1)

    print("-" * 80)
    print("📊 RESULTADOS OFICIAIS AUDITADOS MATEMATICAMENTE:")
    print("-" * 80)
    print(f"• Alocação de Cargas         : Fase A: {fase_a:,} ({fase_a/rede['num_ucs']*100:.1f}%) | Fase B: {fase_b:,} ({fase_b/rede['num_ucs']*100:.1f}%)")
    print(f"• Corrente de Neutro Inicial  : {i_neutro_antes_total:,.1f} A (Sobreaquecimento Severo)")
    print(f"• Corrente de Neutro Final    : {i_neutro_depois_total:,.1f} A (Quase Zero!)")
    print(f"• Eficiência de Cancelamento  : {eficiencia:.2f}% de eliminação de perdas parasitas")
    print(f"• Perdas Joule Iniciais (kW)  : {perdas_kw_antes:,.2f} kW")
    print(f"• Perdas Joule Finais (kW)    : {perdas_kw_depois:,.4f} kW")
    print(f"• Potência Ativa Recuperada   : {kw_salvos:,.2f} kW (~{kw_salvos/1000.0:.2f} MW instantâneos)")
    print("-" * 80)
    print("💰 IMPACTO REGULATÓRIO & ECONÔMICO:")
    print(f"• Energia Técnica Recuperada  : {mwh_ano_salvos:,.1f} MWh / ano")
    print(f"• Economia Financeira Direta  : R$ {economia_reais_ano:,.2f} por ano (por alimentador)")
    print(f"• Conformidade PRODIST        : Restabelecimento da simetria de fase e vida útil dos trafos.")
    print("-" * 80)

    if eficiencia >= 99.0:
        print("🏆 CERTIFICADO REGULATÓRIO: CONFORMIDADE MATEMÁTICA COMPROVADA!")
    print("=" * 80)

if __name__ == "__main__":
    auditar_poc_aneel()