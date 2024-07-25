# chatbot_ollama

# Modelos

Diversión con LLR y Ollama

1.- Instalarlo

curl -fsSL https://ollama.com/install.sh | sh

2.- Ejecutar el servidor

ollama serve

3.- Descargar el modelo Tinyllama

ollama pull tinyllama
ollama pull llama2

------- ollama list (muestra todos los modelos descargados)

4.- Realizar una pregunta

ollama run tinyllama ¿Porque el cielo es azul?

-------- ollama run tinyllama (modo chat (ctrl + d para finalizar chat))

5.- Llamadas a la API REST

curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt":"",
  "system": "",
  "stream": false
}'
