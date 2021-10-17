# BestArbitrage
Intuitive cryptocurrency arbitrage software

example:

```python
from BestArbitrage.intra_exchange.trading_bot import Robot
from BestArbitrage import core
import ccxt

okex = ccxt.okex({
    'apiKey': 'xx0xx0x0-0y00-0000-0x0x-x00xx0xxxxx0x',
    'secret': 'X0XXXX0XXXXXX00XXXXX00XX00XX0X0X',
    'password': 'PaSsWoRd'
})
robot = Robot(client=core.Client(client=okex))
robot.start_arbitrage(min_profit=0.5, sleep_in_chains=1, sleep_in_deals=0.7)
```
