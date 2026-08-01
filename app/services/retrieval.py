import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def retrieve_top_sections(
    jd_embedding: list[float], resume_sections: dict, top_k: int = 3
) -> list[dict]:
    scored = [
        {
            "section": name,
            "text": data["text"],
            "score": cosine_similarity(jd_embedding, data["embedding"]),
        }
        for name, data in resume_sections.items()
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
