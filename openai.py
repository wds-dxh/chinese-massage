from openai import OpenAI
import pyttsx3

class HealthAdviceAssistant:
    def __init__(self, api_key, base_url="https://api.nextapi.fun/v1", model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.speech_engine = pyttsx3.init()

    def get_health_advice(self, fruit_type):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "病例建议：1.用根据用户描述的症状，推荐按摩的穴位。2.给出相应的注意事项。3.内容简洁明了，内容不要太多了，少于100字！！！。4.注意给出注意事项，内容要温暖，不要太机械了，给使用者家的感觉"},
                {"role": "user", "content": fruit_type}
            ],
            stream=True,
            model="gpt-3.5-turbo",
        )

        advice_text = ''
        for chunk in chat_completion:
            content_part = chunk.choices[0].delta.content
            if content_part is not None:
                advice_text = advice_text + content_part
                print(content_part, end="")

        self.speech_engine.say(advice_text)
        self.speech_engine.runAndWait()

if __name__ == "__main__":
    api_key = "ak-COVDNhZt8spc38GSRCPbi6IPbvH9EghL6pEfibt3uz8i87tE"  # Replace with your actual API key
    assistant = HealthAdviceAssistant(api_key)

    # Example usage
    fruit_type = "苹果"
    assistant.get_health_advice(fruit_type)
