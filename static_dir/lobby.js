document.querySelector("#lobby-Submit").onclick = e => {
    var username = document.querySelector('#User-Name-Input').value
                      
  if ( username === '') {
    e.preventDefault()
    alert('Please Enter a username to continue');
    }
  }