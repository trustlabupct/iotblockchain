import subprocess, os

os.makedirs("logs", exist_ok=True)

# Sólo semihonest por ahora
configs = [
  "configs/burst_500.ini","configs/burst_1000.ini","configs/burst_1500.ini","configs/burst_2000.ini"
]

seeds = open("seeds.txt").read().splitlines()

for cfg in configs:
    for seed in seeds:
        out = f"logs/{os.path.basename(cfg).replace('.ini','')}_{seed}.csv"
        subprocess.run([
            "python", "simulation_multi_agent.py",
            "--config", cfg,
            "--seed",   seed
        ], stdout=open(out, "w"))

