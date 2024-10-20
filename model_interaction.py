from http import HTTPStatus
from dashscope import Generation
import dashscope
#加入模型API
#目前使用通义千问API，可自行调节为其他API，并完整实现generate_response函数即可
def generate_response(prompt):
    print(prompt)
    messages = [
        {'role': 'system', 'content': 'you are a helpful assistant'},
        {'role': 'user', 'content': prompt}
    ]
    responses = Generation.call(
        model="qwen-turbo",
        messages=messages,
        result_format='message',
        stream=True,
        incremental_output=True
    )
    output = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            output += response.output.choices[0].message.content
        else:
            output += f"Error: {response.code}, {response.message}"
    return output
