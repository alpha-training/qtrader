# Order management in qtrader

The following processes are involved in qtrader:

* `eng.q` - strategy engine
* `net.q` - netting & aggregation
* `om.q` - order management

# Timeline of example flow

The table below illustrates the event-by-event evolution of strategy intents, netting decisions, and order manager actions across `eng`, `net`, and `om`.

| time | proc | event             | strat  | sym  | strat_intent              | agg_intent        | actual_pos | delta_to_trade | om_action                     | notes                                                   |
|--------:|---------|-------------------|--------|------|---------------------------|-------------------|-----------:|----------------|-------------------------------|---------------------------------------------------------|
|       0 | eng     | strat1_update     | strat1 | IBM | +100                      |                   |          0 |                |                               | strat1 wants +100                                       |
|       1 | net     | net_recalc        |        | IBM | +100                      | +100              |          0 | +100           | send_buy_100                  | net computes agg = +100, delta = +100                   |
|       2 | om      | order_sent        |        | IBM |                           |                   |          0 | +100           | buy_100_sent                  | order goes to market                                    |
|       5 | om      | partial_fill      |        | IBM |                           |                   |         20 | +80            |                               | only 20 shares filled so far                            |
|      10 | eng     | strat2_update     | strat2 | IBM | -50                       |                   |         20 |                |                               | strat2 wants -50                                        |
|      11 | net     | net_recalc        |        | IBM | +100 + (-50) = +50        | +50               |         20 | +30            | reduce_buy_from_80_to_30      | agg target now +50; actual pos = 20; need only +30 more |
|      12 | om      | modification_sent |        | IBM |                           |                   |         20 | +30            | cancel_buy_80_and_buy_30      | cancel remaining 80, submit buy for 30                  |
|      18 | eng     | strat3_update     | strat3 | IBM | +40                       |                   |         20 |                |                               | strat3 wants +40                                        |
|      19 | net     | net_recalc        |        | IBM | +100 - 50 + 40 = +90      | +90               |         20 | +70            | send_buy_70                   | agg target rises to +90; need +70 more                  |
|      20 | om      | order_sent        |        | IBM |                           |                   |         20 | +70            | buy_70_sent                   | new buy order goes to market                            |
|      25 | om      | partial_fill      |        | IBM |                           |                   |         50 | +40            |                               | another 30 shares filled; pos = 50                      |
|      30 | eng     | strat1_update     | strat1 | IBM | +10                       |                   |         50 |                |                               | strat1 changes mind; wants only +10 now                 |
|      31 | net     | net_recalc        |        | IBM | +10 - 50 + 40 = 0         | 0                 |         50 | -50            | send_sell_50                  | agg target now 0; actual 50; must SELL 50               |
|      32 | om      | modification_sent |        | IBM |                           |                   |         50 | -50            | cancel_buy_70_and_sell_50     | cancel remaining buy 70 and sell 50                     |
|      40 | om      | fill              |        | IBM |                           |                   |          0 | 0              |                               | position returns to zero                                |

