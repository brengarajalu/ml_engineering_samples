from typing import Dict

from langchain_community.vectorstores import Pinecone, Redis


class ContentMemoryModule:
    def __init__(self, config: Dict):
        # Short-term memory: Recent campaigns, current content series
        self.short_term = Pinecone(**config['redis'])

        # Long-term memory: Brand guidelines, historical performance
        self.long_term = Pinecone(**config['redis'])

        # Vector memory: Similar content, semantic relationships
        self.vector_store = Pinecone(**config['pinecone'])

    async def retrieve_marketing_context(
            self,
            topic: str,
            brand_id: str,
            campaign_id: str
    ) -> Dict:
        # Get campaign-specific recent context
        recent_context = await self.short_term.get(
            f"campaign:{campaign_id}:context"
        )

        # Get brand history and guidelines
        brand_context = await self.long_term.find_one(
            {"brand_id": brand_id}
        )

        # Find similar successful content
        content_embedding = self._embed_topic(topic)
        similar_content = await self.vector_store.query(
            vector=content_embedding,
            filter={"brand_id": brand_id},
            top_k=5
        )

        return {
            "campaign_context": recent_context,
            "brand_context": brand_context,
            "similar_content": similar_content
        }