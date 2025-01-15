
from abc import ABC

from domain.models import Action, Signal, PressMentionSignal
import datetime

from openai import OpenAI
client = OpenAI()

class Agent(ABC):
    def process_signals(self, signals: list[Signal]) -> list[Action]:
        raise NotImplemented()

class PressMentionAgent(Agent):
    def get_completion(self, signal: PressMentionSignal) -> str:
        messages = [
                {"role": "system", "content": "You are a professional assistant that evaluates press mention signals for their importance and urgency."},
                {
                    "role": "user",
                    "content": f"""
                    Based on the details provided below, generate:
                    - A personalized, engaging notification message to prompt the user to take action.

                    Signal Details:
                    - Title: {signal.title}
                    - Description: {signal.description}
                    - Platform: {signal.plateform}
                    - Source: {signal.source_name}
                    - Engagement Count: {signal.engagement_count}
                    - URL: {signal.url_link}

                    Response format:
                    - Message: "Your personalized message here"
                    """
                },
            ]
        
        completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
            )
        
        return completion.choices[0].message.content.strip()
    
    def get_score(self, signal: PressMentionSignal) -> float:
        normalized_engagement = min(signal.engagement_count / 1000, 1.0)
        
        platform_scores = {
            "LinkedIn": 1.0,
            "Twitter": 0.8,
            "Facebook": 0.6,
            "Other": 0.4
        }
        platform_score = platform_scores.get(signal.plateform, 0.4)
        
        days_since_post = (datetime.datetime.now() - signal.post_date).days
        if days_since_post <= 7:
            recency_score = 1.0
        elif days_since_post <= 30:
            recency_score = 0.5
        else:
            recency_score = 0.2
        
        score = (
            (0.4 * normalized_engagement) +
            (0.2 * platform_score) +
            (0.15 * recency_score)
        )
        
        return round(min(max(score, 0), 1), 2)
    
    
    def process_signals(self, signals: list[PressMentionSignal]) -> list[Action]:
        actions = []
        for signal in signals:
            signal_score = self.get_score(signal)

            if signal_score < 0.5:
                continue

            output = self.get_completion(signal)
            
            try:
                # message, score = output.split("- Score:")
                output = output.replace("- Message:", "").strip()
                score = float(score.strip())
            except ValueError:
                output = "An important mention was detected, but the message couldn't be generated."
                score = 0.5

            action = Action(
                signal=signal,
                title=f"Press Mention: {signal.title}",
                description=output,
                url=signal.url_link,
                score=score,
            )
            actions.append(action)            
        return actions
