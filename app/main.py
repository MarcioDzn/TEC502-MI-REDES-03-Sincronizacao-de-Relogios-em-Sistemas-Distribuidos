from flask import Flask, request, jsonify
from flask_cors import CORS
from Token import Token, Status, State
from Leader import Leader
import requests
import time
from time import sleep
import threading
import logging
from colorlog import ColoredFormatter
from utils import *

# Configuração do colorlog
formatter = ColoredFormatter(
    "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger('example')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app)

token = Token(Status.ACTIVE)

global leader, drift
leader = Leader()

currentTime = 0

alreadyApplied = False

SEND_TOKEN_TIMEOUT = 0.5
VERIFY_LEADER_TIMEOUT = 0.5
SET_LEADER_TIMEOUT = 0.5
WAIT_SEND_TOKEN_TIME = 0.2
WAIT_SYNC = 3
SYNC_TIMEOUT = 0.5
ASK_FOR_TOKEN_TIMEOUT = 0.5
CHANGE_TOKEN_ID_TIMEOUT = 0.5
drift = 0.9

CURRENT_NODE = 0
NODE_LIST = ["172.16.103.9:8088", "172.16.103.8:8088", "172.16.103.7:8088"]


def inactiveTokenTimer(checkIntervalMs=1, timeoutSeconds=((WAIT_SEND_TOKEN_TIME + SEND_TOKEN_TIMEOUT)*len(NODE_LIST))*3):
    start_time = time.time()

    # se o token não chegar em determinado tempo invalida gera um novo
    while (time.time() - start_time) < timeoutSeconds:
        if token.status == Status.ACTIVE:
            return
        sleep(checkIntervalMs / 1000.0)  

        response = verify_online(NODE_LIST[CURRENT_NODE].split(":")[0])

        if (not response):
            logger.warning("COMPUTADOR DESCONECTADO DA REDE")
            return 

    # manda uma mensagem pra todos perguntando se alguém tem o token
    logger.error("TOKEN INEXISTENTE")
    is_token_active = askForToken()

    # se ninguém tiver o token, gera um novo
    if (not is_token_active):
        token.status = Status.ACTIVE
        token.state = State.WALKING
        token.clearNodeClocks()

        token.id = token.id+1

        # muda o id do token atual para todos os bancos conectados
        changeTokenId()


def askForToken():
    for node in NODE_LIST:
        try:
            if (node != NODE_LIST[CURRENT_NODE]):
                response = requests.get(f"http://{node}/v1/api/token", timeout=ASK_FOR_TOKEN_TIMEOUT)

                if (response.status_code == 200):
                    return True

        except Exception as e:
            pass

    return False


def changeTokenId():
    for node in NODE_LIST:
        try:
            if (node != NODE_LIST[CURRENT_NODE]):
                response = requests.patch(f"http://{node}/v1/api/token", json={"id": token.id}, timeout=CHANGE_TOKEN_ID_TIMEOUT)

        except Exception as e:
            pass


def wait4Election():
    while (token.status != Status.ACTIVE):
        pass

    token.state = State.ELECTING

    global currentTime
    toElectNode(CURRENT_NODE, currentTime, currentTime, [])

    # flag pra indicar que já se candidatou
    global alreadyApplied
    alreadyApplied = True


def sync():
    while True:
        if (leader.id != CURRENT_NODE):
            continue

        sleep(WAIT_SYNC)
        for node in NODE_LIST:
            try:
                if (node != NODE_LIST[CURRENT_NODE]):
                    response = requests.post(f"http://{node}/v1/api/synchronization", json={"time": currentTime}, timeout=SYNC_TIMEOUT)

                    if (response.status_code == 406):
                        break

            except Exception as e:
                pass


def incrementTime():
    while True:
        global drift
        sleep(drift)

        global currentTime
        logger.info("TEMPO ATUAL: {}s | LIDER: {}".format(currentTime, leader.id))
        currentTime += 1


def sendToken():
    global token
    global leader

    next_node = CURRENT_NODE + 1

    offlineNodes = 0
    while token.status == Status.ACTIVE:
        if (next_node >= len(NODE_LIST)):
            next_node = 0

        if (next_node == CURRENT_NODE):
            next_node += 1

        try:
            sleep(WAIT_SEND_TOKEN_TIME)

            response = requests.post(f"http://{NODE_LIST[next_node]}/v1/api/token", json=({"token_status": str(token.status.value), "node_clocks": token.nodeClocks, "leader_id": token.leader, "state": str(token.state.value), "token_id": token.id}), timeout=SEND_TOKEN_TIMEOUT)

            if (response.status_code == 200):
                logger.info(f'TOKEN ENVIADO | ID: {token.id}')
                token.status = Status.INACTIVE
                threading.Thread(target=inactiveTokenTimer).start()
                return

        except Exception as e:
            next_node += 1

            if (offlineNodes == (len(NODE_LIST)-1)):
                return

            offlineNodes += 1


def toElectNode(nodeId, currentTimeNode, tokenTime, currentClocksList):
    global token
    global leader

    if (token.state != State.ELECTING):
        return 

    # verifica se já deu uma volta
    for node in currentClocksList:
        if (node["nodeId"] == CURRENT_NODE):
            currentClocksList = sorted(currentClocksList, key=lambda x: x['time'], reverse=True)

            logger.info('ELEIÇÃO SENDO REALIZADA')

            token.state = State.WALKING
            token.leader = currentClocksList[0]["nodeId"]
            leader.id = currentClocksList[0]["nodeId"]
            token.clearNodeClocks()

            # mandar broadcast pra todos informando o novo lider
            for node in NODE_LIST:
                try:
                    if (node != NODE_LIST[CURRENT_NODE]):
                        response = requests.post(f"http://{node}/v1/api/leader", json={"leader_id": leader.id}, timeout=SET_LEADER_TIMEOUT)
                except Exception as e:
                    pass

            return

    electionInfo = {"nodeId": nodeId, "time": currentTimeNode}
    if (currentTimeNode >= tokenTime):
        token.nodeClocks = ("first", electionInfo, currentClocksList)

    else:
        token.nodeClocks = ("end", electionInfo, currentClocksList)


def verifyLeaderOnline():
    global token
    global leader

    while True:
        if (token.status != Status.ACTIVE or token.state != State.WALKING):
            global alreadyApplied
            if (alreadyApplied):
                sendToken()
                alreadyApplied = False

            continue

        try:
            if (NODE_LIST[leader.id] != NODE_LIST[CURRENT_NODE]):
                requests.get(f"http://{NODE_LIST[leader.id]}/v1/api/leader", timeout=VERIFY_LEADER_TIMEOUT)

        # lider está inativo | começa a eleição
        except:
            logger.info('ELEIÇÃO INICIADA')
            token.state = State.ELECTING

            global currentTime
            toElectNode(CURRENT_NODE, currentTime, currentTime, [])
        finally:
            sendToken()



@app.route("/v1/api/token", methods=["POST"])
def receiveToken():
    global token
    global leader

    data = request.get_json()

    tokenId = data["token_id"]
    tokenStatus = data["token_status"]
    nodeClocks = data["node_clocks"]
    leaderId = data["leader_id"]
    tokenState = data["state"]

    if (tokenId < token.id):
        logger.warning("CHEGOU TOKEN INVALIDO")
        return jsonify({"message": "Token recebido, mas não mantido."}), 200

    token.id = tokenId
    logger.info(f"TOKEN RECEBIDO | ID: {token.id}")
    if (tokenStatus == "active"):
        if (tokenState == "walking"):
            token.state = State.WALKING
            leader.id = leaderId # atualiza o lider do nó que caiu e voltou
            token.leader = leaderId
            token.clearNodeClocks() # limpa a lista de clocks
        else:
            token.state = State.ELECTING

        token.status = Status.ACTIVE

    global currentTime

    if (nodeClocks):
        toElectNode(CURRENT_NODE, currentTime, nodeClocks[0]["time"], nodeClocks)

    # flag pra indicar que já se candidatou
    global alreadyApplied
    alreadyApplied = True

    return jsonify({"message": "Token recebido com sucesso"}), 200


@app.route("/v1/api/token", methods=["GET"])
def getToken():
    if (token.status == Status.ACTIVE):
        return jsonify({"message": "Token está neste nó"}), 200
    return jsonify({"message": "Token não está neste nó"}), 404


@app.route("/v1/api/token", methods=["PATCH"])
def modifyTokenId():
    data = request.get_json()

    updatedId = data["id"]

    token.id = updatedId

    return jsonify({"message": "Id atualizado com sucesso"}), 200


@app.route("/v1/api/leader", methods=["POST"])
def setLeader():
    global leader

    data = request.get_json()

    leader_id = data["leader_id"]

    leader.id = leader_id
    return jsonify({"message": "Lider definido!"}), 200


@app.route("/v1/api/leader", methods=["GET"])
def isLeader():
    return jsonify({"message": "Lider está aqui!"}), 200


@app.route("/v1/api/synchronization", methods=["POST"])
def syncTime():
    data = request.get_json()

    time = data["time"]

    global currentTime


    if (time < currentTime):
        threading.Thread(target=wait4Election).start()
        return jsonify({"message": "Não é possível voltar no tempo!"}), 406

    currentTime = time
    logger.info('SINCRONIZADO')

    return jsonify({"message": "Tempo sincronizado!"}), 200


@app.route("/v1/api", methods=["GET"])
def getInfos():
    global currentTime, drift

    isLeader = False
    if (leader.id == CURRENT_NODE):
        isLeader = True

    return jsonify({"node": NODE_LIST[CURRENT_NODE], "time": currentTime, "leader": isLeader, "drift": drift})


@app.route("/v1/api", methods=["PATCH"])
def getNodeInfos():
    data = request.get_json()

    global drift 
    drift = float(data["drift"])

    return jsonify({"message": "Drift alterado com sucesso"})


def main():
    app.run(host='0.0.0.0', port=8088, debug=False, threaded=True)


if __name__ == "__main__":
    threading.Thread(target=verifyLeaderOnline).start()
    threading.Thread(target=incrementTime).start()
    threading.Thread(target=sync).start()
    main()