from flask_restplus import Resource, Namespace, reqparse, fields
from init_optmizer import optimizer
import pathlib
import pandas as pd

from model.recommend_market_fund import get_recom_marker_fund
from model.portfolio import get_portfolio_data

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = DATA_PATH.joinpath('instruments.csv')

api = Namespace('wx', description='小程序分配页的信息')

_info_parser = reqparse.RequestParser()
_info_parser.add_argument('risk_value',
                          required=True,
                          type=float,
                          help='风险承受能力',
                          choices=(0.01, 0.02, 0.03, 0.04, 0.05))


ration_model = api.model(
    'ratio_model',
    {
        'Bond': fields.Float(default=0),
        'Hybrid': fields.Float(default=0),
        'QDII': fields.Float(default=0),
        'Stock': fields.Float(default=0),
        'Other': fields.Float(default=0),
        'Money': fields.Float(default=0),
        'Related': fields.Float(default=0),
    }
)

ans_model = api.model(
    'ans_model',
    {
        'Return': fields.Float,
        'Volatility': fields.Float,
        'SharpRatio': fields.Float
    }
)

info_model = api.model(
    'info_model',
    {
        'ans': fields.Nested(ans_model),
        'ratio': fields.Nested(ration_model)
    }
)


@api.route('')
class Allocator(Resource):

    @api.expect(_info_parser)
    def get(self):
        """
        获得小程序所需的信息
        :param
        :return:
        """
        args = _info_parser.parse_args()
        ret, vol, sr, w = optimizer.get_fixed_ans(fixed='volatility', value=args['risk_index'])
        market_dict, recom_dict, ratio = get_recom_marker_fund(w)
        # allocation_id = mongo.db.allocation.insert_one({'allocation': market_dict, 'recommend': recom_dict, 'ratio': ratio}).inserted_id
        top_7 = sorted(market_dict.items(), key=lambda x: x[1], reverse=True)[:7]
        top_7 = {
            k: v
            for k, v in top_7
        }
        return {
                   # 'allocation_id': allocation_id,
                   'allocation': top_7,
                   'ratio': ratio,
                   'return': ret,
                   'volatility': vol,
                   'sharp_ratio': sr
               }, 200

