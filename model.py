from openai_function_call import MultiTask, OpenAISchema
from pydantic import Field


class AdequateQuestions(OpenAISchema):
    "Correctly extracted user information"
    isSufficient: bool = Field(
        description="A boolean that determines whether or not a user has asked at least one question about each of the points to be discussed."  # noqa: E501
    )


class QuestionResponse(OpenAISchema):
    "Correctly extracted user information"
    question: str = Field("A question posed by a user")
    response: str = Field(description="A response to the user's question")


MultiQuestionResponse = MultiTask(QuestionResponse)


class QuestionSummary(OpenAISchema):
    "Correctly extracted user information"
    summary: str = Field(
        description="A summary of the questions that the user has asked so far and what areas the user has for improvement."
    )
