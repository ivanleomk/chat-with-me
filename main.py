from typing import List
import openai
import pydantic
import openai_function_call
import json
from Components import ClarifyingQuestionBank, Summarize
from Prompts import INSIGHT_PROMPT, SUMMARIZE_PROMPT

from model import AdequateQuestions

# Try to evaluate candidate suggestions

openai.api_key = # Fill this in

QUESTION_CONTEXT = """
You are an expert consultant here to guide a junior consultant on his first case. 

You have determined the revenue issues for the new client and are now guiding\
    the junior consultant to come up with the right questions to ask the client.

Here are the all the points you need him to arrive at in order to be considered\
    as having asked sufficient questions

- Train the sales staff better to sell- No, they’re pretty well trained
- Lower prices- No, it wouldn’t solve our margin issue
- Online store- We are not ready to make that investment at this time
- Turns out that American customers don’t love the styles and have some
trouble with Asian sizes (the styles tend to be too conservative, the colors are
too muted, our clothing tends to run small for the US market)
- Adjusting design and sizes and continuing to manufacture separately for the
American market will cost us $12M annually, but it will provide $23M
additional revenue per year
"""


def main():
    revenue_areas = [
        "Train the Sales Staff",
        # "Experiment with lowering Prices",
        # "Explore the use of an online store to sell merchandise",
        # "Differences between style and size preferences of American and Asian customers",
        "Adjusting design and sizes and continuing to manufacture separately for the American and Asian market",
    ]
    user_prompt = (
        "Generate some questions to ask a customer in order to increase revenue. "
    )

    RevenueQuestions = ClarifyingQuestionBank(revenue_areas, user_prompt, rounds=2)
    questions = RevenueQuestions.run()

    revenue_response = """
    - Train the sales staff better to sell- No, they're pretty well trained
    - Lower prices- No, it wouldn't solve our margin issue
    - Online store- We are not ready to make that investment at this time
    - Turns out that American customers don't love the styles and have some
    trouble with Asian sizes (the styles tend to be too conservative, the colors are too muted, our clothing tends to run small for the US market)
    -Adjusting design and sizes and continuing to manufacture separately for the American market will cost us $12M annually, but it will provide $23M additional revenue per year.
    """  # noqa: E501

    revenue_prompt = SUMMARIZE_PROMPT.format(
        context=revenue_response, questions=questions
    )
    revenue_summary = Summarize(
        existing_questions=questions,
        prompt=revenue_prompt,
        context=revenue_response,
    )
    revenue_summary.run()

    cost_areas = ["Manufacturing", "Shipping", "Labor", "Rent"]
    user_prompt = "Generate some questions to ask a customer in order to decrease costs."  # noqa: E501

    CostQuestions = ClarifyingQuestionBank(cost_areas, user_prompt, rounds=2)

    cost_questions = CostQuestions.run()

    cost_response = """
     - Manufacturing : We are already producing our clothing in the cheapest manner possible.
     - Shipping : We could cut 5% of our COGS by shipping the clothing by boat instead of air. This would save us an estimated $4.5 Million annually.
     - Labor : We have what we need, cannot reduce
     - Rent : There are a few different options avaliable to us for reducing rent. 
        a : We could move the location of our flagship store - No, we need it for marketing
        b : We could close our mall stores -  We are not ready to make that move
        c : We could share the rent with another business - YES! Opening a coffee shop within the store would cut 25% of our debt burden at the flagship store., saving an estimated 1.75M annually.
    """  # noqa: E501

    cost_prompt = SUMMARIZE_PROMPT.format(
        context=cost_response, questions=cost_questions
    )
    revenue_summary = Summarize(
        existing_questions=cost_questions,
        prompt=cost_prompt,
        context=cost_response,
    )
    revenue_summary.run()


if __name__ == "__main__":
    main()
