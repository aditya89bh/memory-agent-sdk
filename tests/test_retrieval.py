from memory_agent_sdk import Memory, EventType, SQLiteStore

def test_retrieval_ranks_keyword_overlap_and_filters_tags():
    m=Memory(); m.remember("User prefers concise answers",tags=["preference"],importance=.9); m.remember("Use pytest for tests",tags=["project"],importance=.9)
    res=m.retrieve("concise answers",tags=["preference"])
    assert [r.text for r in res]==["User prefers concise answers"]
    assert m.events()[-1].type==EventType.MEMORY_RETRIEVED

def test_sqlite_store_persists_memory(tmp_path):
    path=tmp_path/"memory.db"; m=Memory(SQLiteStore(path)); r=m.remember("SQLite persists records",tags=["storage"])
    reopened=Memory(SQLiteStore(path))
    assert reopened.store.get(r.id).text=="SQLite persists records"
