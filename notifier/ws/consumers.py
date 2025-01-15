from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TaskStatusConsumer(AsyncJsonWebsocketConsumer):
    """
    Async consumer for sending task status updates to users by user_id.
    """

    async def connect(self) -> None:
        """
        Called on client websocket connect.
        Subscribes the user to their personal channel.
        """
        # user must be authenticated
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user_id = self.scope["user"].id  # Get user_id from the scope
            self.group_name = (
                f"room_{self.user_id}"  # Create a unique group name for the user
            )
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send_json(
                {"message": f"Successfully connected to your room: {self.group_name}"}
            )

    async def disconnect(self, close_code: int) -> None:
        """
        Called when websocket disconnects.
        Unsubscribes the user from their personal channel.
        """
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict) -> None:
        """
        When we get a message from the client, we can subscribe to specific actions.
        """
        action = content.get("action")
        if action == "ping":
            await self.send_json({"message": "pong"})

    async def task_status_update(self, event: dict) -> None:
        """
        Handler method for receiving a 'task_status_update' event from channel layer.
        Sends task status updates to the user.
        """
        await self.send_json(
            {"task_id": event.get("task_id"), "status": event.get("status")}
        )
