import asyncio
import websockets

connected_clients = {}  # Bağlı kullanıcılar ve nickleri
message_history = []  # Sohbet geçmişi

async def handle_client(websocket, path):
    # İlk mesajda kullanıcıdan nick alıyoruz
    nickname = await websocket.recv()
    connected_clients[websocket] = nickname

    # Yeni kullanıcıya önceki mesajları gönder
    for message in message_history:
        await websocket.send(message)

    await broadcast(f"{nickname} sohbete katıldı!")

    try:
        while True:
            message = await websocket.recv()
            formatted_message = f"{nickname}: {message}"
            message_history.append(formatted_message)  # Mesajı kaydet
            await broadcast(formatted_message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        del connected_clients[websocket]
        await broadcast(f"{nickname} sohbete ayrıldı!")

async def broadcast(message):
    for client in connected_clients:
        await client.send(message)

async def main():
    # IP ve portu belirliyoruz (telefonun IP'si ve seçilen port)
    async with websockets.serve(handle_client, "192.168.1.30", 65235):
        await asyncio.Future()  # Sunucunun sonsuza kadar çalışmasını sağlar

asyncio.run(main())
