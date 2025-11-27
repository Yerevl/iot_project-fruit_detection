import asyncio
from aiocoap import Context, Message, resource
import mysql.connector

class InferenceResource(resource.Resource):
    async def render_post(self, request):
        data = request.payload.decode()
        print("Received inference data:", data)
        # Connect to MySQL
        conn = mysql.connector.connect(
            user='root',               # Default XAMPP user
            password='yeriftw23',               # Default XAMPP password (change if needed)
            host='127.0.0.1',
            database='fruit_detection'         # Your DB name
        )
        cursor.execute(
            "INSERT INTO inference (Label, Value, x, y, width, height) VALUES (%s, %s, %s, %s, %s, %s)",
            (label, value, x, y, width, height)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return Message(payload=b"ok")  # Reply to ESP32

def main():
    root = resource.Site()
    root.add_resource(['inference'], InferenceResource())
    asyncio.Task(Context.create_server_context(root, bind=('0.0.0.0', 5683)))  # Listen on UDP/5683
    print("CoAP server running on port 5683, resource: /inference")
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
