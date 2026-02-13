import pandas as pd, glob

def top10_share(df):
    c = df['approver_id'].value_counts()
    return c.iloc[:10].sum() / c.sum()

def metrics(pattern):
    files = glob.glob(pattern)
    dfs = []
    for f in files:
        try:
            # Leer con Latin-1 y saltar líneas erróneas
            df = pd.read_csv(
                f,
                encoding='latin-1',
                on_bad_lines='skip',    # descartará líneas que no encajen
                comment='#'             # si hay comentarios estilo bash
            )
            dfs.append(df)
        except Exception as e:
            print(f"⚠️  Skipping {f}: {e}")
    if not dfs:
        return None, None, None
    big = pd.concat(dfs, ignore_index=True)
    p95   = big['conf_time'].quantile(0.95)
    orphan = big.get('orphan_flag', pd.Series()).mean()*100
    t10   = top10_share(big)
    return p95, orphan, t10

names = [
    "burst_500",
    "collude_04",
    "collude_06",
    "collude_08",
    "collude_10",
]

for name in names:
    pat = f"logs/{name}_*.csv"
    p95, o, t10 = metrics(pat)
    if p95 is None:
        print(f"{name}: ¡no he podido leer ningún CSV!")
    else:
        print(f"{name}: p95={p95:.1f}s, orphans={o:.2f}%")
