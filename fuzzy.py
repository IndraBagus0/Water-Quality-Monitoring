import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Variabel input
ph = ctrl.Antecedent(np.arange(0, 14.1, 0.1), 'pH')
tds = ctrl.Antecedent(np.arange(0, 1001, 1), 'TDS')
kekeruhan = ctrl.Antecedent(np.arange(0, 26, 1), 'kekeruhan')

kelayakan = ctrl.Consequent(np.arange(50, 101, 1), 'kelayakan')

# Fungsi keanggotaan trapesium
ph['asam'] = fuzz.trapmf(ph.universe, [0, 0, 5, 7])
ph['netral'] = fuzz.trapmf(ph.universe, [6.5, 7, 8, 8.5])
ph['basa'] = fuzz.trapmf(ph.universe, [8, 9, 14, 14])

tds['baik'] = fuzz.trapmf(tds.universe, [0, 0, 200, 500])
tds['cukup'] = fuzz.trapmf(tds.universe, [300, 500, 700, 1000])
tds['tidak_baik'] = fuzz.trapmf(tds.universe, [900, 1000, 1000, 1000])

kekeruhan['jernih'] = fuzz.trapmf(kekeruhan.universe, [0, 0, 2, 5])
kekeruhan['cukup_jernih'] = fuzz.trapmf(kekeruhan.universe, [4, 10, 15, 25])
kekeruhan['keruh'] = fuzz.trapmf(kekeruhan.universe, [24, 25, 25, 25])

# Fungsi keanggotaan Sugeno untuk output
kelayakan['layak'] = fuzz.trimf(kelayakan.universe, [100, 100, 100])
kelayakan['tidak_layak'] = fuzz.trimf(kelayakan.universe, [50, 50, 50])

# Aturan Fuzzy
rules = [
    ctrl.Rule(ph['asam'] & tds['baik'] & kekeruhan['jernih'],
              kelayakan['tidak_layak']),  # 1
    ctrl.Rule(ph['asam'] & tds['baik'] & kekeruhan['cukup_jernih'],
              kelayakan['tidak_layak']),  # 2
    ctrl.Rule(ph['asam'] & tds['baik'] & kekeruhan['keruh'],
              kelayakan['tidak_layak']),  # 3

    ctrl.Rule(ph['asam'] & tds['cukup'] & kekeruhan['jernih'],
              kelayakan['tidak_layak']),  # 4
    ctrl.Rule(ph['asam'] & tds['cukup'] &
              kekeruhan['cukup_jernih'], kelayakan['tidak_layak']),  # 5
    ctrl.Rule(ph['asam'] & tds['cukup'] & kekeruhan['keruh'],
              kelayakan['tidak_layak']),  # 6

    ctrl.Rule(ph['asam'] & tds['tidak_baik'] &
              kekeruhan['jernih'], kelayakan['tidak_layak']),  # 7
    ctrl.Rule(ph['asam'] & tds['tidak_baik'] &
              kekeruhan['cukup_jernih'], kelayakan['tidak_layak']),  # 8
    ctrl.Rule(ph['asam'] & tds['tidak_baik'] &
              kekeruhan['keruh'], kelayakan['tidak_layak']),  # 9

    ctrl.Rule(ph['netral'] & tds['baik'] &
              kekeruhan['jernih'], kelayakan['layak']),  # 10
    ctrl.Rule(ph['netral'] & tds['baik'] &
              kekeruhan['cukup_jernih'], kelayakan['layak']),  # 11
    ctrl.Rule(ph['netral'] & tds['baik'] & kekeruhan['keruh'],
              kelayakan['tidak_layak']),  # 12

    ctrl.Rule(ph['netral'] & tds['cukup'] &
              kekeruhan['jernih'], kelayakan['layak']),  # 13
    ctrl.Rule(ph['netral'] & tds['cukup'] &
              kekeruhan['cukup_jernih'], kelayakan['layak']),  # 14
    ctrl.Rule(ph['netral'] & tds['cukup'] & kekeruhan['keruh'],
              kelayakan['tidak_layak']),  # 15

    ctrl.Rule(ph['netral'] & tds['tidak_baik'] &
              kekeruhan['jernih'], kelayakan['tidak_layak']),  # 16
    ctrl.Rule(ph['netral'] & tds['tidak_baik'] &
              kekeruhan['cukup_jernih'], kelayakan['tidak_layak']),  # 17
    ctrl.Rule(ph['netral'] & tds['tidak_baik'] &
              kekeruhan['keruh'], kelayakan['tidak_layak']),  # 18

    ctrl.Rule(ph['basa'] & tds['baik'] & kekeruhan['jernih'],
              kelayakan['tidak_layak']),  # 19
    ctrl.Rule(ph['basa'] & tds['baik'] & kekeruhan['cukup_jernih'],
              kelayakan['tidak_layak']),  # 20
    ctrl.Rule(ph['basa'] & tds['baik'] & kekeruhan['keruh'],
              kelayakan['tidak_layak']),  # 21

    ctrl.Rule(ph['basa'] & tds['cukup'] & kekeruhan['jernih'],
              kelayakan['tidak_layak']),  # 22
    ctrl.Rule(ph['basa'] & tds['cukup'] & kekeruhan['cukup_jernih'],
              kelayakan['tidak_layak']),  # 23
    ctrl.Rule(ph['basa'] & tds['cukup'] & kekeruhan['keruh'],
              kelayakan['tidak_layak']),  # 24

    ctrl.Rule(ph['basa'] & tds['tidak_baik'] &
              kekeruhan['jernih'], kelayakan['tidak_layak']),  # 25
    ctrl.Rule(ph['basa'] & tds['tidak_baik'] &
              kekeruhan['cukup_jernih'], kelayakan['tidak_layak']),  # 26
    ctrl.Rule(ph['basa'] & tds['tidak_baik'] &
              kekeruhan['keruh'], kelayakan['tidak_layak']),  # 27

]

# Sistem kontrol fuzzy
kelayakan_ctrl = ctrl.ControlSystem(rules)
kelayakan_sim = ctrl.ControlSystemSimulation(kelayakan_ctrl)

# Contoh input
data_ph = 12.2
data_tds = 400
data_kekeruhan = 19

kelayakan_sim.input['pH'] = data_ph
kelayakan_sim.input['TDS'] = data_tds
kelayakan_sim.input['kekeruhan'] = data_kekeruhan

kelayakan_sim.compute()

print(f"Hasil defuzzifikasi: {kelayakan_sim.output['kelayakan']}")
