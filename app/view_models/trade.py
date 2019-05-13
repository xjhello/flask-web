# 从原始数据到视图数据在view_model转化
class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = [] #view_model实际数据
        self._parse(goods)

    def _parse(self, goods):
        self.total = len(goods)
        self.trades = [self._map_to_trade(gift) for gift in goods]

    def _map_to_trade(self, single): #向他请求此书。赠书者数据
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )