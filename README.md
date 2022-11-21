# Remote-ID

## Projeto de graduação 2022

### Autor: Pedro Henrique Freitas Silva

Nesse reposítório estão os códigos desenvolvidos para a execução de um simulador de comunicação de drones para identificação e localização por parte de um controlador de espaço aéreo.

## Instalação e Preparação

Para reprodução do trabalho, é preciso primeiro ter instalado e configurado o ROS, criar e configurar uma workspace. Instruções de como fazer isso podem ser encontradas em: http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment.

O programa foi feito com a distribuição Kinetic, então recomenda-se usar essa versão ou uma mais recente.

Com o workspace configurado, é necessário substituir a pasta src pela pasta presente nesse repositório. Por fim, executar o comando `catkin_make` para compilar os arquivos.

## Execução
Para a execução de qualquer cenário, é necessário rodar o comando `roscore` em um terminal.

Para cada cenário é preciso rodar cada um dos nós correspondentes executando `rosrun remoteid <nome do nó que deve ser executado>.py` em um terminal diferente. O mínimo para o funcionamneto de qualquer cenário é um nó piloto, o nó drone correspondente, um nó observador (ground) e o nó USS.

Para vizualização gráfica é preciso rodar também `rosrun remoteid plotter.py` em um terminal separado.

Qualquer novo nó que for criado precisa ser compilado pelo comando `chmod +x <nome do nó>.py` dentro da pasta `remoteid/scripts`.

### Espaços reservados
Para adicionar ou modificar um espaço reservado, é necessário possuir o SQLite instalado (mais informações em https://www.sqlite.org/index.html). Para acessar o SQLite, basta executar `sqlite3 .../src/remoteid/db/volumes.db` com o diretório onde se encontra o arquivo volumes.db. A partir desse ponto, se opera com comandos de SQL.
