# Introducing ProtoGamerNet
## What is ProtoGamerNet?

ProtoGamerNet is a tailored Python TCP protocol creator designed explicitly with game developers in mind. It streamlines the intricate process of message serialization and reserialization, enabling developers to define the specifications of various protocol messages in a simple JSON format. With just one click, these specifications are transformed into data classes, offering auto-completion features and ensuring an intuitive development process.

## Key Features:

** Protocol Specification with JSON: Define the essence of your game messages seamlessly.
** Automatic Data Class Generation: Equip your game with self-generated data classes for each protocol message.
** Server Module Integration: Once messages are sent using the generated protocol, they are efficiently deserialized and transformed ** into their respective Python classes, ready for processing.
** Worker Module: Register and run 'Frames' on your messages, organizing your game code with priority, push and pull methods.
** KernelEvents Manager: A state-of-the-art event management system. Register events, dispatch them, and effortlessly attach callbacks.