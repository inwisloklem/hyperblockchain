# Hyperblockchain


## Install

```
poetry install
```

## Run app

```
poetry run python3 -m backend.app
```

## In PEER mode

```
export PEER=True && poetry run python3 -m backend.app
```

## Run blockchain

```
poetry run python3 -m backend.blockchain.blockchain
```

## Scripts

```
poetry run python3 -m backend.scripts.average_block_rate
```

## Test

```
poetry run python3 -m pytest backend
```
