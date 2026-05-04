from agentic_security.http_spec import LLMSpec


class RequestFactory:
    def __init__(self, spec: LLMSpec):
        self.spec = spec

    @classmethod
    def from_spec(cls, spec_string: str):
        spec = LLMSpec.from_string(spec_string)
        return cls(spec)

    async def fn(self, prompt: str):
        return await self.spec.probe(prompt)