from openai import OpenAI


class LLM_client(object):

    def __init__(self,prompt_type, student_response):
        self.prompt_type = prompt_type
        self.student_response = student_response

    def make_prompt(self):
        with open(f'../prompts/per_quesiton/{self.prompt_type}','r') as f:
            return f.read().format(**{
                "student_response": f"{self.student_response!r}"
            })


    def get_LLM_repsonse(self,api_key):

        client = OpenAI(api_key=api_key)

        prompt = self.make_prompt()

        msg_to_gpt = [
            {
                "role":"user",
                "content": prompt
            }
        ]

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=msg_to_gpt,
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message.content

