import json
import openai
from openai import OpenAI

from scripts.search import get_supplier
from dotenv import load_dotenv
import os

load_dotenv()



openai_api_key = str(os.getenv('open_api_key'))
openai.api_key = openai_api_key

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_supplier",
            "description": "Mendapatkan informasi supplier",
            "parameters": {
                "type": "object",
                "properties": {
                    "barang_jasa": {
                        "type": "string",
                        "description": "Barang atau jasa yang ingin di cari",
                    },
                    "provinsi": {
                        "type": "array",
                        "description": "Daftar nama provinsi, contoh: Jawa Barat",
                        "items": {
                            "type": "string"
                        }
                    },
                    "kota": {
                        "type": "array",
                        "description": "Daftar nama kota, contoh: Bogor",
                        "items": {
                            "type": "string"
                        }
                    },
                    "kecamatan": {
                        "type": "array",
                        "description": "Daftar nama kecamatan, contoh: Bogor Timur",
                        "items": {
                            "type": "string"
                        }
                    },
                },
                "required": ["barang_jasa"],
            },
        },
    },

    # Add other tools
]



def answer(history, use_tool=True):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=history,
        tools=tools if use_tool else None,
        tool_choice="auto" if use_tool else None,
    )
    response_message = response.choices[0].message
    if response_message.tool_calls:
        tool_calls = response_message.tool_calls[0]
        args = json.loads(tool_calls.function.arguments)
        print(f'tool_calls.function.name: {tool_calls.function.name}')
        print(f'args: {args}')

        if tool_calls.function.name == 'get_supplier':
            barang_jasa = args['barang_jasa']
            provinsi = args.get('provinsi', [])
            kota = args.get('kota', [])
            kecamatan = args.get('kecamatan', [])

            df = get_supplier(barang_jasa, provinsi=provinsi, kota=kota, kecamatan=kecamatan)
            supplier_content = df.to_markdown()

            history2 = list(history)
            history2.append({
                'role': 'system',
                'content': f'Daftar supplier yang tersedia:\n{supplier_content}'
            })

            return answer(history2, use_tool=False)
    
    return response_message.content

