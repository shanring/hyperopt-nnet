import hyperopt
from hyperopt import pyll
from hyperopt.fmin import fmin_pass_expr_memo_ctrl
from nips2011 import nnet1_space
from nips2011 import PyllLearningAlgo
# TODO: make this a Protocol
from skdata.larochelle_etal_2007 import Rectangles

@fmin_pass_expr_memo_ctrl
def eval_fn(expr, memo, ctrl):
    from skdata.iris.view import SimpleCrossValidation
    protocol = SimpleCrossValidation()
    algo = PyllLearningAlgo(expr, memo, ctrl)
    protocol.protocol(algo)
    results = algo.results
    loss = np.mean([
            d['err_rate'] for d in results['loss']
            #if d['task_name'] == 'valid' # XXX TODO
            ])
    return {
            'loss': loss,
            'status': 'ok',
            'algo_results': results,
            }

def test_nnet_iris():

    trials = hyperopt.Trials()

    hyperopt.fmin(
        eval_fn,
        space=nnet1_space(),
        max_evals=10,
        algo=hyperopt.rand.suggest,
        trials=trials,
        )

