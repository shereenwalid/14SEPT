async for _event in _runner.run_async(
    user_id="ui", session_id=session.id, new_message=msg
):

try:
    um = getattr(_event, "usage_metadata", None)
    if um is not None:
        _metrics_add_tokens(
            opp_id,
            getattr(um, "prompt_token_count", 0) or 0,
            getattr(um, "candidates_token_count", 0) or 0,
            getattr(um, "total_token_count", 0) or 0,
        )
except Exception:  # noqa: BLE001 - metrics never break a run
    pass
