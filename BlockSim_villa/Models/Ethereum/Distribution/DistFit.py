import os
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import RandomForestRegressor
from InputsConfig import InputsConfig as p
import pandas as pd

class DistFit:

    cgas = None
    cprice = None
    ctime = None
    egas = None
    eprice = None
    etime = None
    x = 0

    @staticmethod
    def fit():
        if DistFit.x < 1:
            # Obtén el directorio actual del archivo DistFit.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path_set1 = os.path.join(current_dir, "Data_sets.xlsx")
            file_path_set2 = os.path.join(current_dir, "Data_sets.xlsx")
            
            df = pd.read_excel(file_path_set1, sheet_name="Set1")
            df2 = pd.read_excel(file_path_set2, sheet_name="Set2")
            DistFit.cgas, DistFit.cprice, DistFit.ctime = DistFit.creation_fit(df)  # fitted models
            DistFit.egas, DistFit.eprice, DistFit.etime = DistFit.execution_fit(df2)
            DistFit.x += 1

    @staticmethod
    def creation_fit(df):
        K = 39
        g = GaussianMixture(n_components=K)
        data = np.log(df['b']).values.reshape(-1, 1)
        gmm = g.fit(data)  # fit model

        X = np.transpose([df['b']])  # used gas
        y = np.array(df['d'])  # cpu time

        depth = 30
        estimators = 10
        clf = RandomForestRegressor(max_depth=depth, n_estimators=estimators)  # RF instance
        clf.fit(X, y)  # fit model

        eps = 0.001  # correction param
        K = 35
        gg = GaussianMixture(n_components=K)
        data = np.log(df['c'] + eps).values.reshape(-1, 1)
        ggmm = gg.fit(data)  # fit model

        return gmm, ggmm, clf

    @staticmethod
    def execution_fit(df):
        K = 39
        g = GaussianMixture(n_components=K)
        data = np.log(df['b']).values.reshape(-1, 1)
        gmm = g.fit(data)  # fit model

        X = np.transpose([df['b']])  # used gas
        y = np.array(df['d'])  # cpu time

        depth = 300
        estimators = 100
        clf = RandomForestRegressor(max_depth=depth, n_estimators=estimators)  # RF instance
        clf.fit(X, y)  # fit model

        eps = 0.001  # correction param
        K = 65
        gg = GaussianMixture(n_components=K)
        data = np.log(df['c'] + eps).values.reshape(-1, 1)
        ggmm = gg.fit(data)  # fit model

        return gmm, ggmm, clf

    @staticmethod
    def sample_transactions(n):
        cN = max(1, round(n * 0.0121))  # rate of contract creation transactions, based on real data
        eN = max(1, round(n * 0.9879))  # rate of function execution transactions, based on real data

        # Sample contract creation transactions
        b_s = DistFit.cgas.sample(cN)[0]
        b_s = np.exp(b_s).flatten().round()
        b_s[b_s < 21000] = 21000
        b_s[b_s > 8000000] = 8000000

        b_s = b_s.reshape(-1, 1)
        d_s = DistFit.ctime.predict(b_s)
        c_s = np.exp(DistFit.cprice.sample(cN)[0])
        a_s = np.random.uniform(low=b_s.flatten(), high=8 * 10**6, size=cN)

        a_s = a_s.round()
        b_s = b_s.flatten().round()
        c_s = c_s.flatten()
        d_s = d_s.round()

        # Sample function execution transactions
        b_e = DistFit.egas.sample(eN)[0]
        b_e = np.exp(b_e).flatten().round()
        b_e[b_e < 21000] = 21000
        b_e[b_e > 8000000] = 8000000

        b_e = b_e.reshape(-1, 1)
        d_e = DistFit.etime.predict(b_e)
        c_e = np.exp(DistFit.eprice.sample(eN)[0])
        a_e = np.random.uniform(low=b_e.flatten(), high=8 * 10**6, size=eN)

        a_e = a_e.round()
        b_e = b_e.flatten().round()
        c_e = c_e.flatten()
        d_e = d_e.round()

        # Preparing samples
        gasLimit = np.concatenate((a_s, a_e), axis=None)
        usedGas = np.concatenate((b_s, b_e), axis=None)
        gasPrice = np.concatenate((c_s, c_e), axis=None)
        CPUTime = np.concatenate((d_s, d_e), axis=None)

        return gasLimit, usedGas, gasPrice, CPUTime

