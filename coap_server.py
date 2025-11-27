import asyncio
import json
from aiocoap import Context, Message, resource
import mysql.connector

class InferenceResource(resource.Resource):
    async def render_post(self, request):
        # Parse the incoming JSON payload
        try:
            data = json.loads(request.payload.decode())
            label = data['Label']
            value = data['Value']
            x = data['x']
            y = data['y']
            width = data['width']
            height = data['height']
        except Exception as e:
            print("Error parsing payload or missing fields:", e)
            return Message(payload=b"parse_error")

        print(f"Received inference: label={label}, value={value}, x={x}, y={y}, width={width}, height={height}")
        
        # Connect to MySQL and insert the values
        try:
            conn = mysql.connector.connect(
                user='root',
                password='yeriftw23',
                host='127.0.0.1',
                database='fruit_detection'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO inference (Label, Value, x, y, width, height) VALUES (%s, %s, %s, %s, %s, %s)",
                (label, value, x, y, width, height)
            )
            conn.commit()
        except Exception as e:
            print("Database error:", e)
            return Message(payload=b"db_error")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
        return Message(payload=b"ok")  # Reply to ESP32

def main():
    root = resource.Site()
    root.add_resource(['inference'], InferenceResource())
    asyncio.Task(Context.create_server_context(root, bind=('0.0.0.0', 5683)))
    print("CoAP server running on port 5683, resource: /inference")
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()