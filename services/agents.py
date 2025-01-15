
from abc import ABC

from domain.models import Action, Signal, PressMentionSignal

from openai import OpenAI
client = OpenAI()


class Agent(ABC):
    def process_signals(self, signals: list[Signal]) -> list[Action]:
        raise NotImplemented()

class PressMentionAgent(Agent):
    def get_messages(self, signal: PressMentionSignal) -> str:
        messages = [
                {"role": "system", "content": "You are a professional assistant that evaluates press mention signals for their importance and urgency."},
                {
                    "role": "user",
                    "content": f"""
                    Based on the details provided below, generate:
                    1. A personalized, engaging notification message to prompt the user to take action.
                    2. A priority score between 0 and 1 (where 1 means extremely high priority and 0 means very low priority).

                    Signal Details:
                    - Title: {signal.title}
                    - Description: {signal.description}
                    - Platform: {signal.plateform}
                    - Source: {signal.source_name}
                    - Engagement Count: {signal.engagement_count}
                    - URL: {signal.url_link}

                    Response format:
                    - Message: "Your personalized message here"
                    - Score: [a number between 0 and 1]
                    """
                },
            ]
        
        return messages
    
    def process_signals(self, signals: list[PressMentionSignal]) -> list[Action]:
        actions = []
        for signal in signals:
            messages = self.get_messages(signal)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
            )

            output = completion.choices[0].message.content.strip()
            try:
                message, score = output.split("- Score:")
                message = message.replace("- Message:", "").strip()
                score = float(score.strip())
            except ValueError:
                message = "An important mention was detected, but the message couldn't be generated."
                score = 0.5

            action = Action(
                signal=signal,
                title=f"Press Mention: {signal.title}",
                description=message,
                url=signal.url_link,
                score=score,
            )
            actions.append(action)            
        return actions
