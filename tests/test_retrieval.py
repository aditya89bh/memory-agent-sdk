from memory_agent_sdk import EventType, Memory, RetrievalTrace, SQLiteStore


def test_retrieval_ranks_keyword_overlap_and_filters_tags():
    m=Memory(); m.remember("User prefers concise answers",tags=["preference"],importance=.9); m.remember("Use pytest for tests",tags=["project"],importance=.9)
    res=m.retrieve("concise answers",tags=["preference"])
    assert [r.text for r in res]==["User prefers concise answers"]
    assert m.events()[-1].type==EventType.MEMORY_RETRIEVED


def test_retrieval_trace_exposes_scoring_and_rejections():
    m=Memory()
    kept=m.remember("User prefers concise answers",tags=["preference"],importance=.9)
    skipped=m.remember("Use pytest for tests",tags=["project"],importance=.9)

    trace=m.retrieve_trace("concise answers",tags=["preference"])

    assert isinstance(trace, RetrievalTrace)
    assert trace.query=="concise answers"
    assert trace.requested_tags==["preference"]
    assert trace.candidates_seen==2
    assert trace.candidates_scored==1
    assert [result.id for result in trace.results]==[kept.id]
    assert trace.results[0].keyword_score > 0
    assert trace.results[0].importance_score == .9
    assert trace.rejected==[{"id":skipped.id,"reason":"tag_mismatch"}]
    assert m.events()[-1].details["trace"] is True


def test_sqlite_store_persists_memory(tmp_path):
    path=tmp_path/"memory.db"; m=Memory(SQLiteStore(path)); r=m.remember("SQLite persists records",tags=["storage"])
    reopened=Memory(SQLiteStore(path))
    assert reopened.store.get(r.id).text=="SQLite persists records"
