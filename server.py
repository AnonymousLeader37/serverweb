import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)

connected_clients = {}
message_history = []

async def handle_client(websocket, path):
    try:
        # İlk mesajda kullanıcıdan nick alıyoruz
        nickname = await websocket.recv()
        connected_clients[websocket] = nickname

        logging.info(f"{nickname} bağlandı.")

        # Yeni kullanıcıya önceki mesajları gönder
        for message in message_history:
            await websocket.send(message)

        await broadcast(f"{nickname} sohbete katıldı!")

        while True:
            message = await websocket.recv()
            formatted_message = f"{nickname}: {message}"
            message_history.append(formatted_message)  # Mesajı kaydet
            await broadcast(formatted_message)
    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"{nickname} bağlantıyı kapattı: {e}")
    except Exception as e:
        logging.error(f"Bir hata oluştu: {e}")
    finally:
        del connected_clients[websocket]
        await broadcast(f"{nickname} sohbete ayrıldı!")

async def broadcast(message):
    for client in connected_clients:
        try:
            await client.send(message)
        except Exception as e:
            logging.error(f"Mesaj gönderirken hata oluştu: {e}")

async def main():
    try:
        async with websockets.serve(handle_client, "192.168.1.30", 65235):
            logging.info("Sunucu başlatıldı, bağlantılar bekleniyor...")
            await asyncio.Future()  # Sunucunun sonsuza kadar çalışmasını sağlar
    except Exception as e:
        logging.error(f"Sunucu başlatılamadı: {e}")

asyncio.run(main())
