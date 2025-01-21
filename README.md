# NutriBot

Programa pensado para automação de mensagens para pacientes após uma semana da primeira consulta. O programa automaticamente faz o input das credencias no site, busca os ultimos 50 pacientes atendidos e dependendo das tags (de acordo com HTML do site) de cada paciente, pode criar 2 tipos de mensagem.
A mensagem é pré programada e varia de acordo com a tag e o nome do paciente e o horário de inicialização. O programa cria um link pra cada paciente que automaticamente abre o site do whatsapp web já com a mensagem individualizada. O usuario precisa apenas clicar em "enviar". É necessário que o usuário esteja com o whatsapp web previamente logado.

## Tencologias utilizadas

- Python
- Selenium
