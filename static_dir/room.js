let RoomName = JSON.parse(document.getElementById("room-name").textContent)
let users = JSON.parse(document.getElementById("users").textContent)
let LocalVideo = document.getElementById("local-stream")
let Username = JSON.parse(document.getElementById("username").textContent)
let Body = document.getElementById('body')
let ToggleCamera = document.getElementById('Toggle-Camera')
let ToggleMic = document.getElementById('Toggle-Mic')
let LeaveBtn = document.getElementById('Leave-Room')



let localstream;
let peerconnections = {};
let remotevideos = {};


const DEBUG = (...args) => console.log('[HCP-DEBUG]', ...args)

// const socket = new WebSocket('ws://'+ window.location.host + '/ws/'+ RoomName + '/');
const socket = new WebSocket(`wss://${window.location.host}/ws/${RoomName}/`);  // elegant

(async () => {
    const result = await fetch('/api/getServer')
    const resultJson = await result.json()
    const Servers = resultJson.ice_servers
    const servers = {
        iceServers: Servers
    }

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })  // await here
        localstream = stream
        LocalVideo.srcObject = stream
        LocalVideo.volume = 0
        LocalVideo.style.transform = 'scaleX(-1)';
        if (users.length > 1) {
            Initiateoffer(servers)
        }

    } catch (e) {
        console.log(e)
    }

    socket.onmessage = event => {
        const event_data = JSON.parse(event.data)
        if (event_data["type"] == "offer") {
            handleOffer(event_data,servers)
        }
        else if (event_data["type"] == "answer") {
            handleAnswer(event_data)
        }
        else if (event_data["type"] == "ice-candidate") {
            handleCandidates(event_data)
        }
        else if (event_data["type"] == "Message") {
            document.querySelector("#Chat-Log").value += (event_data["sender"] + ' ----> ' + event_data["message"] + '\n')
        }
        else if (event_data["type"] == "leave") {
            if (event_data["leaver"] != Username) {
                peerconnections[event_data["leaver"]].close()
                delete peerconnections[event_data["leaver"]]
                document.getElementById(event_data["leaver"] + "video").remove()
                let ind = users.indexOf(event_data["leaver"])
                users.splice(ind, 1)
            }
        }
    }

})()



function leaveroom() {
    socket.send(JSON.stringify({
        "type": "leave",
        "leaver": Username
    }))
    socket.close()
    fetch(`/room/remove/${RoomName}`, {
        method: "DELETE",
        body: JSON.stringify({
            user: Username,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
        }).then((response) => {
            if (response.ok){
                window.location.pathname = '/'
            }else{
                throw new Error('Api request failed')
            }
        })}

    

function Initiateoffer(servers) {
    for (let i = 0; i < users.length; i++) {
        if (users[i] != Username) {
            console.log("sending offer to " + users[i])
            const PeerConnection = new RTCPeerConnection(servers)

            localstream.getTracks().forEach(track => {
                PeerConnection.addTrack(track, localstream)
            });


            const RemoteVideo = document.createElement('video')
            RemoteVideo.autoplay = true
            RemoteVideo.height = 480
            RemoteVideo.width = 640
            RemoteVideo.id = users[i] + "video"
            remotevideos[users[i]] = RemoteVideo

            Body.appendChild(RemoteVideo)


            PeerConnection.createOffer().then(offer => {
                PeerConnection.setLocalDescription(offer)
                socket.send(JSON.stringify({
                    "type": "offer",
                    "sender": Username,
                    "reciever": users[i],
                    "offer": offer
                }))
            })

            PeerConnection.onicecandidate = event => {
                if (event.candidate) {
                    socket.send(JSON.stringify({
                        "type": "ice-candidate",
                        "sender": Username,
                        "reciever": users[i],
                        "icecandidates": event.candidate
                    }))
                }
            }

            PeerConnection.ontrack = event => {

                remotevideos[users[i]].srcObject = event.streams[0]

            }

            peerconnections[users[i]] = PeerConnection
        }
    }





}

function handleOffer(event_data,servers) {
    if (event_data['reciever'] == Username) {
        if (!peerconnections.hasOwnProperty(event_data['sender'])) {
            const PeerConnection = new RTCPeerConnection(servers)

            localstream.getTracks().forEach(track => {
                PeerConnection.addTrack(track, localstream)
            })

            const RemoteVideo = document.createElement('video')
            RemoteVideo.autoplay = true;
            RemoteVideo.height = 480
            RemoteVideo.width = 640
            RemoteVideo.id = event_data["sender"] + "video"
            remotevideos[event_data["sender"]] = RemoteVideo

            Body.appendChild(RemoteVideo)


            PeerConnection.setRemoteDescription(new RTCSessionDescription(event_data["offer"]))

            console.log(event_data["sender"])
            PeerConnection.createAnswer().then(answer => {
                PeerConnection.setLocalDescription(answer)
                socket.send(JSON.stringify({
                    "type": "answer",
                    "sender": Username,
                    "reciever": event_data["sender"],
                    "answer": answer
                }))
            })

            PeerConnection.onicecandidate = event => {
                if (event.candidate) {
                    socket.send(JSON.stringify({
                        "type": "ice-candidate",
                        "sender": Username,
                        "reciever": event_data["sender"],
                        "icecandidates": event.candidate
                    }))
                }
            }

            PeerConnection.ontrack = event => {

                remotevideos[event_data["sender"]].srcObject = event.streams[0]
            }

            peerconnections[event_data["sender"]] = PeerConnection
        }
    }
    else { return }

}

function handleAnswer(event_data) {
    if (event_data["reciever"] == Username) {
        const PeerConnection = peerconnections[event_data['sender']]
        PeerConnection.setRemoteDescription(new RTCSessionDescription(event_data["answer"]))
    }
    else {
        return
    }
}

function handleCandidates(event_data) {
    if (event_data["reciever"] == Username) {
        const Newcandidate = new RTCIceCandidate({
            candidate: event_data["icecandidates"].candidate,
            sdpMid: event_data["icecandidates"].sdpMid,
            sdpMLineIndex: event_data["icecandidates"].sdpMLineIndex
        }
        );

        const PeerConnection = peerconnections[event_data["sender"]]

        PeerConnection.addIceCandidate(Newcandidate).then(() => {
            console.log("success adding the candidates")
        }).catch(e => {
            console.log(e)
        })
    }
    else {
        return
    }
}

document.querySelector("#Message-Input").onkeyup = e => {
    if (e.keyCode === 13) {
        document.querySelector('#Message-Submit').click()
    }
}

document.querySelector('#Message-Submit').onclick = e => {
    const message = document.querySelector('#Message-Input').value
    socket.send(JSON.stringify({
        "sender": Username,
        "type": "Message",
        "message": message
    }))
    document.querySelector('#Message-Input').value = ''

}

ToggleCamera.addEventListener("click", togglecamera)
ToggleMic.addEventListener("click", togglemic)
LeaveBtn.addEventListener("click", leaveroom)


window.addEventListener("beforeunload", leaveroom);

function togglecamera() {
    let videotrack = localstream.getTracks().find(track => track.kind === "video")

    if (videotrack.enabled) {
        videotrack.enabled = false
        ToggleCamera.value = "Show Camera"
    }
    else {
        videotrack.enabled = true
        ToggleCamera.value = "Hide Camera"
    }
}

function togglemic() {
    let audiotrack = localstream.getTracks().find(track => track.kind === "audio")

    if (audiotrack.enabled) {
        audiotrack.enabled = false
        ToggleMic.value = "UnMute Audio"
    }
    else {
        audiotrack.enabled = true
        ToggleMic.value = "Mute Audio"
    }
}
