
import datetime
import feather
import gc
import json
import pandas as pd
import numpy as np
import sys
import warnings

from utils import loadpkl, to_feature, to_json, save2pkl, line_notify

warnings.filterwarnings('ignore')

#==============================================================================
# Preprocessing Queries & Profiles
#==============================================================================

def main(num_rows=None):
    # load pkls
    queries = loadpkl('../features/queries.pkl')
    profiles = loadpkl('../features/profiles.pkl')

    profiles = profiles[['pid']+['profile_{}'.format(i) for i in range(0,66)]]

    # merge
    df = pd.merge(queries, profiles, on='pid', how='left')
    del queries, profiles
    gc.collect()

    # count features
    df['pid_count'] = df['pid'].map(df['pid'].value_counts())

    # drop columns
    df.drop(['pid','req_time'],axis=1,inplace=True)

    # save pkl
    save2pkl('../features/queries_profiles.pkl', df)

    # save configs
    configs = json.load(open('../configs/102_lgbm_queries_profiles.json'))
    configs['features'] = df.columns.to_list()
    to_json(configs,'../configs/102_lgbm_queries_profiles.json')

    line_notify('{} finished.'.format(sys.argv[0]))

if __name__ == '__main__':
    main()
