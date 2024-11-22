from loguru import logger
import bittensor
import redis

redis_client = redis.Redis.from_url('redis://redis:6379')

def metagraph_refresh():
    pipe = redis_client.pipeline()
    subtensor = bittensor.Subtensor(network="finney")
    metagraph = subtensor.metagraph(netuid=19)

    for uid in metagraph.uids.tolist():
        try:
            pipe.set(f"node:{uid}:uid", uid)
            pipe.set(f"node:{uid}:stake", float(metagraph.stake[uid]))
            pipe.set(f"node:{uid}:rank", float(metagraph.ranks[uid]))
            pipe.set(f"node:{uid}:trust", float(metagraph.trust[uid]))
            pipe.set(f"node:{uid}:consensus", float(metagraph.consensus[uid]))
            pipe.set(f"node:{uid}:incentive", float(metagraph.incentive[uid]))
            pipe.set(f"node:{uid}:dividends", float(metagraph.dividends[uid]))
            pipe.set(f"node:{uid}:emission", float(metagraph.emission[uid]))
            pipe.set(f"node:{uid}:validator_trust", float(metagraph.validator_trust[uid]))
            pipe.set(f"node:{uid}:validator_permit", int(metagraph.validator_permit[uid]))
            pipe.set(f"node:{uid}:last_update", int(metagraph.last_update[uid]))
            pipe.set(f"node:{uid}:active", int(metagraph.active[uid]))
            pipe.set(f"node:{uid}:axon:ip_type", int(metagraph.axons[uid].ip_type))
            pipe.set(f"node:{uid}:axon:ip", str(metagraph.axons[uid].ip))
            pipe.set(f"node:{uid}:axon:port", int(metagraph.axons[uid].port))
            pipe.set(f"node:{uid}:hotkey", str(metagraph.hotkeys[uid]))
            pipe.set(f"node:{uid}:coldkey", str(metagraph.coldkeys[uid]))

            for key in [
                "uid", "stake", "rank", "trust", "consensus", "incentive",
                "dividends", "emission", "validator_trust", "validator_permit",
                "last_update", "active", "axon:ip_type", "axon:ip", "axon:port",
                "hotkey", "coldkey"
            ]:
                pipe.expire(f"node:{uid}:{key}", 300)

        except Exception as e:
            logger.error(f"Error processing uid {uid}: {e}")
    try:
        pipe.execute()
    except Exception as e:
        logger.error(f"Pipeline execution error: {e}")