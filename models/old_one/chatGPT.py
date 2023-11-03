# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:58:19 2023

@author: SybilleDarbin
"""
# pip install --upgrade openai

# export OPENAI_API_KEY="<OPENAI_API_KEY>"


import openai
import os
# import pynecone as pc

# Load your API key from an environment variable or secret management service
openai.api_key = "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"
# openai.api_key = os.getenv("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")
openai.Moderation.create(
  input="I want to kill them.",
)
def chatbot():
  # Create a list to store all the messages for context
  messages = [
    {"role": "system", "content": "You are a helpful assistant. You are a French assistant who know about Tennis. You only speak and respond in French."},
    {"role": "user", "content": "What happen if I don't come for the reservation?"},
    {"role": "assistant", "content": "If you don't show up for a reservation, it is likely that the establishment or service provider will consider you a no-show. This could result in various consequences depending on the individual business's policies. Here are some possible outcomes:\n\n1. Loss of future reservations: If you frequently fail to show up for reservations without canceling, some establishments might choose to refuse future booking requests from you. They may consider you unreliable and prefer to allocate their resources to customers who are more dependable.\n\n2. Limited availability for other customers: By not showing up for a reservation, you may be taking up a space that could have been utilized by another customer. This can inconvenience the establishment and impact the experience of other. \n\n3. Blacklisting: In certain cases, establishments may choose to blacklist individuals who repeatedly fail to show up for reservations or exhibit a pattern of unreliable behavior. This means that you may be banned from making reservations or accessing certain services in the future.\n\nIt is always courteous to cancel reservations in advance if you decide not to use them. This allows the establishment to reallocate the resources or accommodate other customers. Remember to check the specific cancellation policy of the establishment beforehand, as there may be specific guidelines or deadlines for cancellations."}
  ]

  # Keep repeating the following
  while True:
    # Prompt user for input
    message = input("User: ")

    # Exit program if user inputs "quit"
    if message.lower() == "quit":
      break

    # Add each new message to the list
    messages.append({"role": "user", "content": message})

    # Request gpt-3.5-turbo for chat completion
    response = openai.ChatCompletion.create(
      # model = "gpt-3.5-turbo",
      model = "gpt-3.5-turbo",
      messages = messages
    )

    # Print the response and add it to the messages list
    chat_message = response['choices'][0]['message']['content']
    print(f"Bot: {chat_message}")
    messages.append({"role": "assistant", "content": chat_message})

if __name__ == "__main__":
  print("Start chatting with the bot (type 'quit' to stop)!")
  chatbot()
    
    