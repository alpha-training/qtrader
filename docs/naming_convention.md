# qtrader Naming Convention Guide

## Overview
This document defines **standard naming conventions** for all tables, columns, messages, and processes in the qtrader system. It follows modern institutional kdb+ practices and avoids collisions with q built-ins.

The goal is to ensure:

- clarity  
- consistency  
- zero ambiguity  
- readability across processes (eng → net → om)  
- future-proofing (interfacing with Python/Rust/C++)

# 1. Global Rules

## 1.1. Table Names
- Use **UpperCamelCase** for all table names.
- Rationale: avoids conflicts with column names, improves readability, distinguishes state tables in logs.

### Examples
```
Intent
Agg
Pos
Req
Order
Pending
Trade
EngState
```

## 1.2. Column Names
- Use **lowercase** (optional snake_case but only where absolutely necessary).
- Short, precise, industry-standard abbreviations are preferred.

### Examples
```
strat
sym
tgtpos
aggtgt
pos
reqqty
qty
pendqty
fillid
fillqty
px
ts
```

- **Never** use CamelCase in columns.
- **Never** use names of q keywords (e.g. delta, fill, exec, each, select).


## 1.3. Processes
Use short, lowercase nouns for process names:

```
eng   — strategy engine  
net   — netting engine  
om    — order manager  
tp    — tickerplant  
gate  — broker/FIX gateway  
```

## 1.4. Message Names
Use *Verb + Noun* in lowerCamelCase:

```
intentUpdate
reqUpdate
fillReport
posUpdate
orderAck
```

# 2. Tables Per Process

## 2.1. eng.q (Strategy Engine)

### Intent
Represents each strategy’s desired target position.

- time
- sym
- strat  
- sym  
- tgtpos (target position)
- conf  (confidence score - default to 1.0 for now)
- note  empty string for now

### EngState
Internal per-strategy diagnostic state.

- time
- sym
- strat  
- sig  
- lastupdate  
- ttl  

## 2.2. net.q (Netting Engine)

### Intent
Copy of eng Intent.

### Agg
Aggregated target per symbol.

- time
- sym  
- aggtgt  

### Pos
Mirror of actual filled positions (fed from om).

- time
- sym  
- pos  
- avgpx  
- pnl  

### Req
Required trade to reach target.

Columns:

- time
- sym  
- aggtgt  
- pos  
- reqqty  
- note  

## 2.3. om.q (Order Manager)

### Order
All outstanding orders.

Columns:

- time
- sym  
- orderid  
- side  
- qty  
- pendqty  
- filledqty  
- limitpx  
- algo  
- status  
- tsnew  
- tsupdate  

### Pending
Summaries of active outstanding orders.

Columns:

- time
- sym  
- buyqty  
- sellqty  
- netqty  

### Trade
Raw fills from broker.

Columns:

- time
- sym 
- fillid  
- orderid   
- fillqty  
- px 

### Pos
Book-of-record positions maintained by OM.

Columns:

- time
- sym  
- pos  
- avgpx  
- realpnl  
- unrlpnl  

# 3. Reserved & Forbidden Names

Avoid all q keywords and built-in function names as tables OR columns:

```
select, exec, delta, deltas, fill, fills, each, by, where, asc, desc,
fby, value, update, delete, from, show, type, key, til, raze, enlist
```

# 4. Column Naming Quick Reference

| Concept | Name | Notes |
|--------|------|-------|
| symbol | sym | standard |
| strategy | strat | short and clear |
| target position | tgtpos | strategies |
| aggregate target | aggtgt | net |
| actual position | pos | net/om |
| required qty | reqqty | replaces delta |
| order qty | qty | |
| unfilled qty | pendqty | |
| filled qty | fillqty | |
| price | px | |
| timestamp | time | universal |

# 5. Rationale

This naming system:

- prevents q keyword collisions  
- ensures clarity across processes  
- aligns with multi-language systems  
- matches institutional OMS/EMS naming  
- helps debugging at 3am  
- scales to many strategies & symbols  

# 6. Example Pipeline

### eng.Intent
```
strat | sym  | tgtpos | conf | ts
-----------------------------------
mean  | AAPL |  100   | 0.8  | ...
rev   | AAPL |  -50   | 0.5  | ...
```

### net.Agg
```
sym  | aggtgt
---------------
AAPL | 50
```

### net.Pos
```
sym  | pos
-----------
AAPL | 20
```

### net.Req
```
sym  | aggtgt | pos | reqqty
-------------------------------
AAPL | 50     | 20  | 30
```

```
om.Order, om.Trade, om.Pos follow the same naming logic.
```

