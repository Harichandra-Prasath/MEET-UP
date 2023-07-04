
                document.querySelector("#Room-Name-Input").onkeyup = e =>{
                    if (e.keyCode === 13){
                        document.querySelector("#Room-Name-Submit").click()
                    }
                }

                document.querySelector("#Room-Name-Submit").onclick = e => {
                    var roomname = document.querySelector("#Room-Name-Input").value
                    var username = document.querySelector('#User-Name-Input').value
                    
                    if (roomname === '' || username === '') {
                        e.preventDefault()
                        alert('Please enter both the room name and username.');
                      } else {
                        sessionStorage.setItem('username', username);

                      } 
                }