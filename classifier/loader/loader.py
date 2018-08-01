import pickle
import sys,os
model_path = '../models/ml_models/'
saved_model_path = '../saved_model/{}/main_flow/{}.pkl'
saved_model_path = os.path.join(os.path.dirname(__file__), saved_model_path)
sys.path.append(os.path.join(os.path.dirname(__file__), model_path))
from ml import *
log_path = '../lib/'
sys.path.append(os.path.join(os.path.dirname(__file__), log_path))
from log import Logger
env_path = '../env/'
sys.path.append(os.path.join(os.path.dirname(__file__), env_path))
from env import ENV

model_list = ['IDClassifier', 
                  'CutDebt', 
                  'WillingToPay',
                  'IfKnowDebtor',
                  'Installment',
                  'ConfirmLoan']

def load_all():
    logger = Logger(load_all.__name__).logger
    model_dict = {}
    for model in model_list:
        model_dict[model] = pickle.load(open(saved_model_path.format(model,model),'rb'))
        logger.info('{} has been load!'.format(model))
        try:
            model_dict['WillingToPay'].re_time._set_timeZone(ENV.TIMEZONE.value)
            logger.info('{} time zone is set to {}'.format(model,ENV.TIMEZONE.value))
        except:
            logger.info('{} does not require time zone!'.format(model))
    return model_dict