document.querySelector("#Room-Name-Input").onkeyup = e =>{
    if (e.keyCode === 13){
      document.querySelector("#Room-Name-Submit").click()
      }
  }

document.querySelector("#room-Submit").onclick = e => {
    var roomname = document.querySelector('#Room-Name-Input').value
                      
  if ( roomname === '') {
    e.preventDefault()
    alert('Please Enter a username to continue');
    }
  }