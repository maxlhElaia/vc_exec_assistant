
from abc import ABC

from domain.models import Action, Signal, PressMentionSignal, EmailAction, CommentAction, ShareOrRepostAction
import datetime
from typing import Dict, List, Literal

from openai import OpenAI
client = OpenAI()

class Agent(ABC):
    def process_signals(self, signals: list[Signal]) -> list[Action]:
        raise NotImplemented()

class PressMentionAgent(Agent):
    RESPONSE_CONFIGS: Dict[str, Dict[str, str]] = {
        'email': {
            'system_prompt': """You are a professional communications manager responsible for monitoring and responding to press mentions. 
            Your goal is to create engaging, professional email notifications that highlight the importance of press mentions and suggest 
            clear next steps for the team.""",
            'user_prompt': """Create a concise, action-oriented email notification about a press mention that:
            1. Highlights the key points of the mention
            2. Explains why it's important
            3. Suggests specific next steps
            4. Maintains a professional, positive tone

            Press Mention Details:
            - Title: {title}
            - Description: {description}
            - Platform: {platform}
            - Source: {source_name}
            - Engagement: {engagement_count} interactions
            - URL: {url_link}

            Format the response as a clear email message without any prefixes or labels."""
        },
        'comment': {
            'system_prompt': """You are a professional social media manager who crafts thoughtful, engaging responses to press mentions. 
            Your comments should be authentic, add value to the conversation, and maintain the company's professional image.""",
            'user_prompt': """Create a genuine, engaging comment that:
            1. Shows appreciation for the mention
            2. Adds value to the discussion
            3. Maintains professionalism while being conversational
            4. Stays under 280 characters
            5. Includes relevant emoji where appropriate

            Press Mention Details:
            - Title: {title}
            - Description: {description}
            - Platform: {platform}
            - Source: {source_name}
            - Engagement: {engagement_count} interactions
            - URL: {url_link}

            Format the response as a ready-to-post comment without any prefixes or labels."""
        },
        'repost': {
            'system_prompt': """You are a professional social media manager who creates engaging content for resharing press mentions. 
            Your goal is to amplify the original message while adding your own valuable perspective.""",
            'user_prompt': """Create an engaging repost message that:
            1. Highlights why this mention is worth sharing
            2. Adds your unique perspective
            3. Encourages further engagement
            4. Uses appropriate hashtags
            5. Keeps the message under 240 characters (to leave room for the URL)

            Press Mention Details:
            - Title: {title}
            - Description: {description}
            - Platform: {platform}
            - Source: {source_name}
            - Engagement: {engagement_count} interactions
            - URL: {url_link}

            Format the response as a ready-to-share message without any prefixes or labels."""
        },
        'context': {
            'system_prompt': """You are an analytical press monitoring specialist who provides detailed context and insights about press mentions. 
            Your goal is to help the team understand the full significance and implications of each mention.""",
            'user_prompt': """Provide a comprehensive context analysis that:
            1. Summarizes the key points and tone of the mention
            2. Analyzes the source's credibility and reach
            3. Evaluates the potential impact on our brand/reputation
            4. Identifies any trends or patterns with previous coverage
            5. Suggests strategic implications and opportunities

            Press Mention Details:
            - Title: {title}
            - Description: {description}
            - Platform: {platform}
            - Source: {source_name}
            - Engagement: {engagement_count} interactions
            - URL: {url_link}

            Format the response as a detailed analysis without any prefixes or labels."""
        }
    }

    def get_response(self, signal: PressMentionSignal, response_type: Literal['email', 'comment', 'repost', 'context']) -> str:
        """
        Generic response generator that handles all types of responses
        """
        if response_type not in self.RESPONSE_CONFIGS:
            raise ValueError(f"Invalid response type: {response_type}")
        
        config = self.RESPONSE_CONFIGS[response_type]
        
        messages = [
            {"role": "system", "content": config['system_prompt']},
            {
                "role": "user",
                "content": config['user_prompt'].format(
                    title=signal.title,
                    description=signal.description,
                    platform=signal.plateform,
                    source_name=signal.source_name,
                    engagement_count=signal.engagement_count,
                    url_link=signal.url_link
                )
            }
        ]
        
        try:
            completion = client.chat.completions.create(
                model="gpt-4-turbo",  # Using a more current model name
                messages=messages,
                temperature=0.7,
            )
            
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating {response_type} response: {str(e)}")
            return f"Unable to generate {response_type} response due to an error."

    def get_email_response(self, signal: PressMentionSignal) -> str:
        return self.get_response(signal, 'email')
    
    def get_comment_response(self, signal: PressMentionSignal) -> str:
        return self.get_response(signal, 'comment')
    
    def get_repost_response(self, signal: PressMentionSignal) -> str:
        return self.get_response(signal, 'repost')
    
    def get_context_response(self, signal: PressMentionSignal) -> str:
        return self.get_response(signal, 'context')
    
    def get_relevance_score(self, signal: PressMentionSignal) -> float:
        print("Computing relevance score for signal:", signal.title)
        normalized_engagement = min(signal.engagement_count / 500, 1.0)
        
        platform_scores = {
            "linkedin": 1.0,
            "twitter": 0.8,
            "facebook": 0.6,
            "other": 0.4
        }
        platform_score = platform_scores.get(signal.plateform, 0.4)
        
        days_since_post = (datetime.datetime.now() - signal.post_date).days
        if days_since_post <= 15:
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
            signal_score = self.get_relevance_score(signal)
            print("Relevance score for signal:", signal.title, signal_score)

            if signal_score < 0.5:
                print("Signal is not relevant enough, skipping")
                continue

            output = self.get_completion(signal)
            
            try:
                output = output.replace("- Message:", "").strip()
            except ValueError:
                output = "An important mention was detected, but the message couldn't be generated."

            email_content = self.get_email_response(signal)
            comment_content = self.get_comment_response(signal)
            repost_content = self.get_repost_response(signal)
            context_content = self.get_context_response(signal)

            # Generate 3 types of actions (email, comment, repost)
            # 1. Email the company with the message
            action1 = EmailAction(
                signal=signal,
                title=f"Press Mention: {signal.title}",
                description=output,
                url=signal.url_link,
                score=signal_score,
                email_message=email_content,
                context_message=context_content
            )
            # 2. Comment on the post with the message
            action2 = CommentAction(
                signal=signal,
                title=f"Press Mention: {signal.title}",
                description=output,
                url=signal.url_link,
                score=signal_score,
                email_content=email_content,
                comment_message=comment_content
            )
            # 3. Repost the post with the message
            action3 = ShareOrRepostAction(
                signal=signal,
                title=f"Press Mention: {signal.title}",
                description=output,
                url=signal.url_link,
                score=signal_score,
                email_content=email_content,
                repost_message=repost_content
            )

            actions.append(action1, action2, action3)            
        return actions
